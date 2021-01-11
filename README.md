# telegram-support-bot
Easy way to use Telegram bot to hide your identity. Useful for support, anonymous channel management. Free clone of Livegram Bot. 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## How bot works:

1. Your client write a message to your bot
2. Bot forwards the message to your secret chat
3. Any chat participant can reply on a forwarded message
4. Bot will copy the message and send it to your client

## .env variables

You need to specify these env variables to run this bot. If you run it locally, you can also write them in `.env` text file.

``` bash
TELEGRAM_TOKEN=  # your bot's token
TELEGRAM_SUPPORT_CHAT_ID=  # chat_id where the bot will forward all incoming messages

# optional params
HEROKU_APP_NAME=  # name of your Heroku app for webhook setup
WELCOME_MESSAGE=  # text of a message that bot will write on /start command
```