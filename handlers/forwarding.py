from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler)

from handlers.general import cancel
from handlers.states import ConversationStates, InitialSelectors
from settings import (REPLY_TO_THIS_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID,
                      WELCOME_MESSAGE)


def forward_to_chat(update: Update, context: CallbackContext) -> int:
    """{
        'message_id': 5,
        'date': 1605106546,
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'},
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f"{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}",
        )
    return ConversationStates.TALKING


def forward_to_user(update: Update, context: CallbackContext) -> int:
    """{
        'message_id': 10, 'date': 1605106662,
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True},
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659,
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True},
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'},
            'forward_date': 1605106658,
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [],
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        },
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False,
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = None
    if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
    elif REPLY_TO_THIS_MESSAGE in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split("\n")[0])
        except ValueError:
            user_id = None
    if user_id:
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id,
        )
    else:
        context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=WRONG_REPLY)

    return ConversationStates.TALKING


def start_talking(update: Update, context: CallbackContext) -> int:

    update.message.reply_text("Ahora puedes hablar con un humano")
    return ConversationStates.TALKING


### Define converation logic

entry_point_forwarding = MessageHandler(
    Filters.regex(f"^{InitialSelectors.FORWARDING_PREFIX}"), start_talking
)

states_dict_forwarding = {
    ConversationStates.TALKING: [
        CommandHandler("cancel", cancel),
        MessageHandler(Filters.chat_type.private, forward_to_chat),
    ],
}
