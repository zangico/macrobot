import os

import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from nucleo import logger, settings
from telegram import TelegramBot

app = FastAPI()

bot = TelegramBot(
    settings.TELEGRAM.BOT_TOKEN,
    settings.TELEGRAM.WEBHOOK_SECRET,
    settings.TELEGRAM.MACROBOT_HOST,
)


@app.post("/reply_from_macrodroid")
async def send_battery(request: Request):
    data = await request.json()

    chat_id = data.get("chat_id")
    text = data.get("text")

    bot.send_message(chat_id, text)
    logger.info(f"Sent {text=} to {chat_id=}")
    return JSONResponse({"ok": True})


def forward_command(chat_id, command):
    webhook_url = os.getenv("MACRODROID_WEBHOOK")
    try:
        logger.info(f"Calling {webhook_url=}")
        macrodroid_request = {"chat_id": chat_id, "request": command}
        requests.post(webhook_url, json=macrodroid_request, timeout=5)
    except Exception as e:
        logger.error(f"Failed to call macrodroid webhook: {e}")
        bot.send_message(chat_id, "Errore chiamando il dispositivo (webhook).")
        return JSONResponse({"ok": False})
    bot.send_message(
        chat_id, "Richiesta inviata al dispositivo. Attendi la risposta..."
    )


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

    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()

    if not text:
        return JSONResponse({"ok": True})

    try:
        command_to_forward = bot.sort_message(chat_id, text)

        if command_to_forward:
            forward_command(chat_id, command_to_forward)

    except Exception as e:
        logger.exception(e)

    return JSONResponse({"ok": True})


@app.get("/")
async def index():
    logger.info("Home")
    return PlainTextResponse("Hello from MacroBot")


if __name__ == "__main__":
    bot.set_webhook()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=60010)
