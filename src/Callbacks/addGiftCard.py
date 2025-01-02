# callback to show addGiftCard balance
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Database.GiftCards import get_services_name
from Callbacks.GiftCards import steam


def handle_add_gift_card_callback(call, bot):
    chat_message_id = call.message.chat.id

   # Make inline keyboard
    service_name_keyboard = []
    for service_name in get_services_name():
        service_name_keyboard.append(InlineKeyboardButton(service_name, callback_data=service_name))
    start_keyboard = [
        service_name_keyboard,
        [
            types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu')
        ]
    ]

    keyboard = InlineKeyboardMarkup(start_keyboard)
    bot.edit_message_text(f"Choose your Service:\n\n", chat_message_id,
                          call.message.message_id, reply_markup=keyboard, parse_mode='HTML')

    # Steam Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'Steam')
    def handle_steam_callback(call):
        steam.handle_steam_callback(call, bot)
