from telegram import (InlineQueryResult, InlineQueryResultArticle,
                      InputTextMessageContent, KeyboardButton, ParseMode,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

from handlers.states import ConversationStates, InitialSelectors


def origin(update: Update, context: CallbackContext) -> int:
    """
    Select Origin
    """
    reply_keyboard = [["Montevideo", "Punta del Este", "La Paloma"]]

    update.message.reply_text(
        "Elige de donde quieres partir" "Si la ubicación no aparece, puedes escribirla",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="De donde sales?",
        ),
    )

    return ConversationStates.DESTINATION


def destination(update: Update, context: CallbackContext) -> int:
    """
    Select Destination
    """
    reply_keyboard = [["Montevideo", "Punta del Este", "La Paloma"]]
    context.user_data["origin"] = update.message.text

    update.message.reply_text(
        "Elige a donde quieres llegar" "Si la ubicación no aparace, puedes escribirla",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="A donde quieres ir?",
        ),
    )

    return ConversationStates.PHONE


def get_phone(update: Update, context: CallbackContext) -> int:
    """
    Select Destination
    """
    context.user_data["destination"] = update.message.text

    con_keyboard = KeyboardButton(
        text="Comparte con nosotros tu contacto", request_contact=True
    )
    custom_keyboard = [[con_keyboard]]

    update.message.reply_text(
        "Dame tu número",
        reply_markup=ReplyKeyboardMarkup(
            custom_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Dame tu telefono",
        ),
    )

    return ConversationStates.SAVE_REQUEST


def save_request(update: Update, context: CallbackContext) -> int:

    context.user_data["phone_number"] = update.message.contact.phone_number
    update.message.reply_text(str(context.user_data))

    return ConversationHandler.END


## Define the relevant pieces of the conversation

entry_point_request_ride = MessageHandler(
    Filters.regex(f"^{InitialSelectors.REQUEST_RIDE_PREFIX}"), origin
)

states_dict_request_ride = {
    ConversationStates.DESTINATION: [
        MessageHandler(Filters.text, callback=destination)
    ],
    ConversationStates.PHONE: [MessageHandler(Filters.text, callback=get_phone)],
    ConversationStates.SAVE_REQUEST: [
        MessageHandler(Filters.contact, callback=save_request)
    ],
}
