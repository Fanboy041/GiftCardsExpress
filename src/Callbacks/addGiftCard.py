# callback to show addGiftCard balance
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Database.GiftCards import save_service_name, get_services_name


def handle_add_gift_card_callback(call, bot):
    chat_message_id = call.message.chat.id
    # Make inline keyboard
    start_keyboard = [
        [
            InlineKeyboardButton("💳 Steam", callback_data="steam"),
        ],
        [
            types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
        ]
    ]

    keyboard = InlineKeyboardMarkup(start_keyboard)

    message = save_service_name("Steam", "12345", "10€")
    bot.send_message(call.message.chat.id,
                     message,
                     parse_mode='HTML')

    message1 = save_service_name("Google Play", "1236765765", "1000€")
    bot.send_message(call.message.chat.id,
                     message1,
                     parse_mode='HTML')

    bot.edit_message_text(f"Choose your Service:\n\n", chat_message_id,
                          call.message.message_id, reply_markup=keyboard, parse_mode='HTML')
