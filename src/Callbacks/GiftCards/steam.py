# callback to show addGiftCard balance
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def handle_add_steam_card_callback(call, bot):
    chat_message_id = call.message.chat.id
    # Make inline keyboard
    start_keyboard = [
        [
            types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
        ]
    ]

    keyboard = InlineKeyboardMarkup(start_keyboard)

    bot.edit_message_text(f"Choose your Service:\n\n", chat_message_id,
                          call.message.message_id, reply_markup=keyboard, parse_mode='HTML')
