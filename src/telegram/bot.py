import requests

from nucleo import logger

from . import commands


class TelegramBot:

    def __init__(self, token, secret, host):
        self.token = token
        self.secret = secret
        self.host = host

    def set_webhook(self):
        url = f"https://{self.host}/telegram_webhook?secret={self.secret}"
        api_url = f"https://api.telegram.org/bot{self.token}/setWebhook"
        try:
            response = requests.post(api_url, data={"url": url}, timeout=10)
            logger.info(f"Webhook set: {response.json()}")
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")

    def is_secret_valid(self, secret):
        return secret == self.secret

    def sort_message(self, chat_id, text: str):
        if text.startswith("/"):
            command = text[1:].split(" ")[0]
            return commands.sort_commands(chat_id, command)

    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send telegram message: {e}")
