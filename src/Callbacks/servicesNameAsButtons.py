# callback to show addGiftCard balance
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Database.GiftCards import get_services_name, get_gift_cards_price
from Callbacks.GiftCards import addGiftCardCode, shop
from Callbacks import addService


def handle_services_name_as_buttons_callback(call, bot):
    chat_message_id = call.message.chat.id
    services_name = get_services_name()
    services_button = []

    # Make inline keyboard
    service_name_keyboard = []
    add_service_name_keyboard = []
    types.InlineKeyboardMarkup(row_width=2)
    for service_name in services_name:
        services_button.append(f"{service_name}_{call.data}")
        service_name_keyboard.append(InlineKeyboardButton(service_name, callback_data=f"{service_name}_{call.data}"))

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
    @bot.callback_query_handler(func=lambda call: call.data in services_button)
    def handle_add_gift_card_code_callback(call):
        service_name_button = call.data.split('_', 1)
        match service_name_button[1]:
            case 'add_gift_card':
                # if 'add_gift_card' == service_name_button[1]:
                addGiftCardCode.handle_add_gift_card_code_callback(call, bot)
            case 'shop':
                shop.handle_shop_callback(call, bot)
            case 'back_to_shop_menu':
                shop.handle_shop_callback(call, bot)
            case 'show_gift_card':
                print(get_services_name())
            case _:
                return "Something's wrong with the internet"

    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_service"))
    def handle_add_service_callback(call):
        addService.handle_add_service_callback(call, bot)
