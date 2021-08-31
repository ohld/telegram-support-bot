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

# If user don't allow forward his messages Bot adds his comment with thue user_id to reply
# Support team must reply to "bot reply", not to original user forwarded message
# Customize message for support team here:
REPLY_TO_THIS_MESSAGE=User above don't allow forward his messages. Reply to this message.
# If support reply to forwarded messages with hidded sender, bor warns with next error:
WRONG_REPLY=User above don't allow forward his messages. You must reply to bot reply under user forwarded message.

```

## Run bot locally

First, you need to install all dependencies:

```bash
pip install -r requirements.txt
```

Then you can run the bot. Don't forget to create `.env` file in the root folder with all required params (read above).

``` bash
python main.py
```
