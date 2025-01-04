# callback to show shop balance
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from Callbacks import servicesNameAsButtons
from Database.GiftCards import get_gift_cards_price

#TODO: get prices to all services as String

def handle_shop_callback(call, bot):

    service_name = call.data.split('_', 1)[0]
    print(service_name)
    gift_card_prices = get_gift_cards_price(service_name)
    print(gift_card_prices)
    chat_id=call.message.chat.id
    message_id=call.message.message_id
    prices_button = []
    gift_card_price_keyboard = []
    back_button_keyboard = []

    back_button_keyboard.append(types.InlineKeyboardButton("Back 🔙", callback_data='back_to_shop_menu'))
    back_keybaord = types.InlineKeyboardMarkup([back_button_keyboard])

    if gift_card_prices == []:
        print("No gift cards available")
        bot.edit_message_text("No gift cards available\n\nIf you want to request a gift card please let me know", chat_id, message_id, reply_markup=back_keybaord)
        return

    for gift_card_price in gift_card_prices:
        prices_button.append(f"{gift_card_price}_{call.data}")
        gift_card_price_keyboard.append(InlineKeyboardButton(gift_card_price, callback_data=f"{gift_card_price}_{call.data}"))

    shop_keyboard = [
        gift_card_price_keyboard,
        back_button_keyboard
    ]

    keyboard = InlineKeyboardMarkup(shop_keyboard)
    bot.edit_message_text(f"Choose your Price:\n\n", chat_id,
                          message_id, reply_markup=keyboard, parse_mode='HTML')
