import httpx
from fastapi import Body, FastAPI, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from nucleo import logger, settings
from telegram import TelegramBot

app = FastAPI()

bot = TelegramBot(
    settings.TELEGRAM.BOT_TOKEN,
    settings.TELEGRAM.WEBHOOK_SECRET,
    settings.TELEGRAM.MACROBOT_HOST,
)


async def send_error(error):
    if not settings.APP.SEND_ERROR:
        return
    message = f"Error in bot:\n\n{error}"
    await bot.send_message(settings.TELEGRAM.ADMIN_CHAT_ID, message)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Query params: {dict(request.query_params)}")
    body = await request.body()
    logger.debug(f"Body: {body.decode('utf-8') if body else '<empty>'}")

    response = await call_next(request)
    logger.debug(f"Response status: {response.status_code}")

    return response


@app.post("/reply_from_macrodroid")
async def send_battery(request: Request):
    data = await request.json()

    chat_id = data.get("chat_id")
    text = data.get("text")

    await bot.send_message(chat_id, text)
    logger.info(f"Sent {text=} to {chat_id=}")
    return JSONResponse({"ok": True})


async def forward_command(chat_id, command):
    webhook_url = settings.MACRODROID_WEBHOOK
    try:
        logger.debug(f"Forwarding {command=} to {chat_id=}")
        logger.debug(f"Calling {webhook_url=}")
        macrodroid_request = {"chat_id": chat_id, "request": command}
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(webhook_url, json=macrodroid_request)
    except Exception as e:
        logger.error(f"Failed to call macrodroid webhook: {e}")
        await bot.send_message(chat_id, "Errore chiamando il dispositivo (webhook).")
        return JSONResponse({"ok": False})
    await bot.send_message(
        chat_id, "Richiesta inviata al dispositivo. Attendi la risposta..."
    )


async def forward_sms(chat_id, number: str, text: str):
    message = f"SMS from {number}:\n\n{text}"
    await bot.send_message(chat_id, message)


@app.post("/sms")
async def sms(
    chat_id: int = Query(...),
    number: str | None = Query(None),
    body: str = Body(..., media_type="text/plain"),
):
    logger.info("New SMS to forward")
    logger.debug(f"chat_id={chat_id}, number={number}, body={body}")

    try:
        await forward_sms(chat_id, number, body)
    except Exception as e:
        logger.exception(e)
        await send_error(e)
        return JSONResponse(
            status_code=500, content={"detail": "Failed to forward SMS"}
        )
    return JSONResponse(status_code=200, content={"detail": "SMS forwarded"})


@app.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    secret = request.query_params.get("secret")

    if not bot.is_secret_valid(secret):
        logger.warning(f"Access denied: wrong secret ({secret})")
        return JSONResponse({"ok": False, "error": "invalid secret"})

    data = await request.json()
    logger.info(f"parsing wehbook {data}")

    message = data.get("message") or data.get("edited_message")
    if not message:
        return JSONResponse({"ok": False, "error": "no message"})

    text = (message.get("text") or "").strip()

    if not text:
        return JSONResponse({"ok": True})

    try:
        command_to_forward = await bot.sort_message(text)

        if command_to_forward:
            await forward_command(command_to_forward)

    except Exception as e:
        logger.exception(e)

    return JSONResponse({"ok": True})


@app.get("/")
async def index():
    logger.info("Home")
    return PlainTextResponse("Hello from MacroBot")


if __name__ == "__main__":

    async def startup():
        await bot.set_webhook()

    import asyncio

    asyncio.run(startup())

    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=settings.API.PORT, reload=True)
