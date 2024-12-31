# callback to show wallet balance
from telebot import types
from Database.Users import get_wallet


def handle_wallet_callback(call, bot):
    chat_message_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
    keyboard.add(back_button)
    bot.edit_message_text(f"Your Wallet has: {get_wallet(chat_message_id)}\n\n", chat_message_id,
                          call.message.message_id, reply_markup=keyboard, parse_mode='HTML')
