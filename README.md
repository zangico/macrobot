# Macrobot: a Telegram bot for Macrodroid.
First prototype to bridge Telegram commands with MacroDroid automations.

## Features
- Receives Telegram updates and triggers MacroDroid via webhook
- Docker-first deployment
- Nginx + Let's Encrypt example

## Prerequisites
- Telegram Bot token (create via BotFather).
- Public address (needed for Telegram webhooks).
- MacroDroid on Android with a Webhook/HTTP Trigger configured. (Read section above)
- Docker and Docker Compose (or bash to run `main.sh`).
- Nginx and Certbot on the server (for TLS).

## Macrodroid Configuration
For this prototype there's only battery percentage handling.
You must create a macro as follows:

### Trigger
**Webhook URL**\
Append `/battery` to the url and save body to a local variable

### Action
**HTTP Request**\
1. Create a `POST`request. Put the url with https://MACROBOT_HOST/send_battery
2. Set `{"webhook_req": {lv=variable_name}, "battery" : {battery}}` where `variable_name` is the name of the local variable you saved in the webhook trigger

## .env
- `TELEGRAM__BOT_TOKEN`: the Telegram token provided by BotFather.
- `TELEGRAM__WEBHOOK_SECRET`: a random secret string; longer values are more secure. Just avoid special characters and consider that too long might not work (have to check)
 - `TELEGRAM__MACROBOT_HOST`: Only domain of your bot. Will be used in macrodroid as well as Telegram Webhook

## Configuration & Start
1. Copy `.env.dist` to `.env` and fill with your data
2. Run the bot with `docker compose up` or `./main.sh` (both needs MACRODROID_WEBHOOK env var).

## Nginx configuration
Add entry in NGINX changing MACROBOT_HOST to your domain. You can find example in the repo
```bash
sudo nano /etc/nginx/sites-available/macrobot
```

Enable server and reload nginx
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

## Changelog
### 14/10/2025:
 - First Release

## Roadamp
 - Implement Welcome messagge
 - Implement webhook saving
 - Implement generic macrodroid automation
 - Implement multi-language

## Extra
Code is linted with [Ruff](https://github.com/astral-sh/ruff) and formatted with [Black](https://github.com/psf/black).

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Copyright

&copy; 2025 zangico. All rights reserved.

## Contributing

Contributions are welcome! Please open issues or submit pull requests via GitHub. Before contributing, review the code of conduct and ensure your changes follow project guidelines. (TBD).
