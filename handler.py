import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

from handlers.forwarding import (entry_point_forwarding, forward_to_user,
                                 states_dict_forwarding)
from handlers.general import cancel, start
from handlers.request_ride import (entry_point_request_ride,
                                   states_dict_request_ride)
from handlers.states import ConversationStates, InitialSelectors
from settings import (REPLY_TO_THIS_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID,
                      WELCOME_MESSAGE, WRONG_REPLY)

SELECTOR_HANDLES = [
    entry_point_request_ride,
    entry_point_forwarding,
]

STATES = {
    ConversationStates.SELECTOR: SELECTOR_HANDLES,
    **states_dict_request_ride,
    **states_dict_forwarding,
}

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states=STATES,
    fallbacks=[CommandHandler("cancel", cancel)],
)


def setup_dispatcher(dp):
    dp.add_handler(conversation_handler)
    dp.add_handler(
        MessageHandler(
            Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user
        )
    )
    return dp
