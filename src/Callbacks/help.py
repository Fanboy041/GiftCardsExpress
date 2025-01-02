from telebot import types
from telebot.types import InlineKeyboardMarkup


def handle_help_callback(call, bot):

    chat_id=call.message.chat.id
    message_id=call.message.message_id

    back_button = types.InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main_menu")

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="This is the help text.",
        reply_markup=InlineKeyboardMarkup().add(back_button)
    )