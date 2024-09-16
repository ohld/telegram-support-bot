from telegram import Update
from telegram.ext import ContextTypes
from settings import TELEGRAM_SUPPORT_CHAT_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text("Welcome to the support bot!")


async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward user messages to the support group."""
    forwarded_msg = await update.message.forward(TELEGRAM_SUPPORT_CHAT_ID)
    if forwarded_msg:
        # Store the user_id in the conversation context
        context.bot_data[str(forwarded_msg.message_id)] = update.effective_user.id
        await update.message.reply_text(
            "Your message has been forwarded to our support team. We'll get back to you soon!"
        )
    else:
        await update.message.reply_text(
            "Sorry, there was an error forwarding your message. Please try again later."
        )


async def forward_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward messages from the group back to the user."""
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        # Retrieve the user_id from the bot_data using the original message_id
        original_message_id = str(update.message.reply_to_message.message_id)
        user_id = context.bot_data.get(original_message_id)

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
                await update.message.reply_text(
                    f"Error sending message to user: {str(e)}"
                )
        else:
            await update.message.reply_text("Could not find the user to reply to.")
    else:
        await update.message.reply_text(
            "This message is not a reply to a forwarded message."
        )
