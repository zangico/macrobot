# Macrobot: a Telegram bot for MacroDroid
A bot to bridge Telegram commands with MacroDroid automations.

## Features
- Receives Telegram updates and triggers MacroDroid via webhook
- Forwards SMS and generic events from the device to Telegram
- Docker-first deployment (Gunicorn + Uvicorn)
- Nginx reverse proxy + optional Basic Auth + Let's Encrypt example

## Prerequisites
- Telegram Bot token (create via BotFather).
- Public address (needed for Telegram webhooks).
- MacroDroid on Android with a Webhook/HTTP Trigger configured.
- Docker and Docker Compose (or local run with `./main.sh`).
- Nginx and Certbot on the server (for TLS).
- Optional for local dev: Python 3.12 and Poetry.

## MacroDroid Configuration
In `macrodroid_examples/` folder you can find 3 macro examples on how macrodroid can integrate with the bot.
Import the macros, adjust you host and authorizations. Take note of the webhook url if you want to use macrodroid webhook feature

## Configuration & Start
1. Copy `.env.dist` to `.env` and fill it with your data.
2. Start with Docker Compose
   - The service is bound only to `127.0.0.1` on the configured port: `127.0.0.1:${API__PORT}` (default 8000)
   - Run: `docker compose up -d`
3. Local start (without Docker)
   - Activate your virtualenv (e.g. with Poetry) and run `./main.sh --dev` for development or `./main.sh --prod` for production.

## Nginx configuration
Add a site entry in NGINX replacing MACROBOT_HOST with your domain. You can find an example in the repository:

```bash
sudo nano /etc/nginx/sites-available/macrobot
```

Add your credentials to htpasswd

```bash
sudo apt install apache2-utils
sudo htpasswd -b /etc/nginx/.htpasswd choose_username choose_password
```

Enable the site and reload nginx

```bash
sudo ln -s /etc/nginx/sites-available/macrobot /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl reload nginx
```

Request a certificate with Certbot (Let's Encrypt)

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d MACROBOT_HOST
```

## Endpoints
- `POST /telegram_webhook?secret=...`
  - Endpoint called by Telegram. The `secret` query parameter must match `TELEGRAM__WEBHOOK_SECRET`.
- `POST /reply_from_macrodroid`
  - Sends a message to a Telegram user (JSON payload: `{ "chat_id": int, "text": str }`). Useful to forward events from MacroDroid, e.g. missed calls.
- `POST /sms?number=+123456...` body: text/plain
  - Forwards a received SMS to the `ADMIN_CHAT_ID` on Telegram.

For ready-to-use examples, see `test/test.http.dist` (compatible with the VS Code REST Client extension). Copy it to `test.http`, set the variables at the top, and try the requests.

## Changelog
### 20/10/2025:
- Main refactor with architectural improvments, poetry implementation, setup tutorial for development, macro examples
- Added `/sms` endpoint and improved handling of `/telegram_webhook`

### 14/10/2025:
- First Release

## Roadmap
- Persist webhook setup/status and health checks

## Extra
Code is linted with [Ruff](https://github.com/astral-sh/ruff) and formatted with [Black](https://github.com/psf/black).

For local development details (Poetry, Python 3.12, Docker flow), see `REAMDE_DEV.md`.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Copyright

© 2025 zangico. All rights reserved.

## Contributing

Contributions are welcome! Please open issues or submit pull requests via GitHub. Before contributing, review the code of conduct and ensure your changes follow project guidelines. (TBD).
