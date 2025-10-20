import httpx

from nucleo import logger

from . import commands


class TelegramBot:

    def __init__(self, token, secret, host):
        self.token = token
        self.secret = secret
        self.host = host

    async def set_webhook(self):
        url = f"https://{self.host}/telegram_webhook?secret={self.secret}"
        api_url = f"https://api.telegram.org/bot{self.token}/setWebhook"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(api_url, json={"url": url})
                data = response.json()
                if (
                    data.get("ok")
                    and data.get("description") == "Webhook is already set"
                ):
                    logger.debug(f"Webhook set: {data}")
                else:
                    logger.info(f"Webhook set: {data}")
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")

    def is_secret_valid(self, secret):
        return secret == self.secret

    async def sort_message(self, chat_id, text: str):
        if text.startswith("/"):
            command = text[1:].split(" ")[0]
            return await commands.sort_commands(self, chat_id, command)

    async def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send telegram message: {e}")
