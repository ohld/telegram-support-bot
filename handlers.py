from telegram import Update
from telegram.ext import ContextTypes
from settings import (
    TELEGRAM_SUPPORT_CHAT_ID,
    FORWARD_MODE,
    PERSONAL_ACCOUNT_CHAT_ID,
    WELCOME_MESSAGE,
)
import logging


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text(
        f"{WELCOME_MESSAGE} {update.effective_user.first_name}"
    )


async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward user messages to the support group or personal account."""
    if FORWARD_MODE == "support_chat":
        forwarded_msg = await update.message.forward(TELEGRAM_SUPPORT_CHAT_ID)
    elif FORWARD_MODE == "personal_account":
        forwarded_msg = await update.message.forward(PERSONAL_ACCOUNT_CHAT_ID)
    else:
        await update.message.reply_text("Invalid forwarding mode.")
        return

    if forwarded_msg:
        # Store the user_id in the conversation context
        context.bot_data[str(forwarded_msg.message_id)] = update.effective_user.id
        await update.message.reply_text(
            "Your message has been forwarded. We'll get back to you soon!"
        )
        logging.info(
            f"Forwarded message ID: {forwarded_msg.message_id} from user ID: {update.effective_user.id}"
        )
    else:
        await update.message.reply_text(
            "Sorry, there was an error forwarding your message. Please try again later."
        )


async def forward_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward messages from the group or personal account back to the user."""
    logging.info("forward_to_user called")
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        logging.info("Message is a reply to another message")
        # Retrieve the user_id from the bot_data using the original message_id
        original_message_id = str(update.message.reply_to_message.message_id)
        user_id = context.bot_data.get(original_message_id)
        logging.info(f"Original message ID: {original_message_id}, User ID: {user_id}")
        if user_id:
            try:
                await context.bot.send_message(
                    chat_id=user_id, text=update.message.text
                )
                await update.message.reply_text(
                    "Message sent to the user successfully."
                )
                # Clean up the stored user_id
                del context.bot_data[original_message_id]
            except Exception as e:
                logging.error(f"Error sending message to user: {str(e)}")
                await update.message.reply_text(
                    f"Error sending message to user: {str(e)}"
                )
        else:
            logging.warning("Could not find the user to reply to.")
            await update.message.reply_text("Could not find the user to reply to.")
    else:
        logging.warning("This message is not a reply to a forwarded message.")
        await update.message.reply_text(
            "This message is not a reply to a forwarded message."
        )
