# callback to show addGiftCard balance
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Database.GiftCards import get_services_name
from Callbacks.GiftCards import serviceName
from Callbacks import addService


def handle_services_name_as_buttons_callback(call, bot):
    chat_message_id = call.message.chat.id
    services_name = get_services_name()

    # Make inline keyboard
    service_name_keyboard = []
    add_service_name_keyboard = []

    for service_name in services_name:
        service_name_keyboard.append(InlineKeyboardButton(service_name, callback_data=service_name))

    if call.data == 'add_gift_card':
        add_service_name_keyboard.append(InlineKeyboardButton("Add Service ➕", callback_data='add_service'))

    add_service_name_keyboard.append(types.InlineKeyboardButton("Back 🔙", callback_data='back_to_main_menu'))

    start_keyboard = [
        service_name_keyboard,
        add_service_name_keyboard
    ]

    keyboard = InlineKeyboardMarkup(start_keyboard)
    bot.edit_message_text(f"Choose your Service:\n\n", chat_message_id,
                          call.message.message_id, reply_markup=keyboard, parse_mode='HTML')

    # Services Callback
    @bot.callback_query_handler(func=lambda call: call.data in services_name)
    def handle_service_callback(call):
        serviceName.handle_service_callback(call, bot)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_service"))
    def handle_add_service_callback(call):
        addService.handle_add_service_callback(call, bot)
