# callback to show shop balance
from telebot import types


def handle_shop_callback(call, bot):
    chat_message_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back_button = types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
    keyboard.add(back_button)
    bot.edit_message_text(f"Choose your Service:\n\n", chat_message_id,
                          call.message.message_id, reply_markup=keyboard, parse_mode='HTML')
