import os
from telegram.ext import ApplicationBuilder

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

async def start_webhook(application):
    await application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        webhook_url=f"{APP_URL}/{TOKEN}"
    )

if __name__ == '__main__':
    main()
