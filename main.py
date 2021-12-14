from telegram.ext import Updater

from handler import setup_dispatcher
from settings import HEROKU_APP_NAME, PORT, TELEGRAM_TOKEN

# Setup bot handlers
updater = Updater(TELEGRAM_TOKEN)

dp = updater.dispatcher
dp = setup_dispatcher(dp)

# Run bot
if HEROKU_APP_NAME is None:  # pooling mode
    print("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
    print("Note: this is not a great way to deploy the bot in Heroku.")

    updater.start_polling()
    updater.idle()

else:  # webhook mode
    print(
        f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/"
    )
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}",
    )

    updater.idle()
