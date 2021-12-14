from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from handlers.states import ConversationStates, InitialSelectors
from settings import (REPLY_TO_THIS_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID,
                      WELCOME_MESSAGE, WRONG_REPLY)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [[InitialSelectors.FORWARDING, InitialSelectors.REQUEST_RIDE]]

    update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )
    user_info = update.message.from_user.to_dict()
    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f" 📞 Connected {user_info}.",
    )

    return ConversationStates.SELECTOR


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
