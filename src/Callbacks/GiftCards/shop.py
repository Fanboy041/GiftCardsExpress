# callback to show shop balance
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from Database.GiftCards import get_gift_cards_price, get_gift_card_code_by_price
from Database.Users import get_wallet, update_wallet


def handle_shop_callback(call, bot):
    service_name = call.data.split('_', 1)[0]
    gift_card_prices = get_gift_cards_price(service_name)
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    prices_button = []
    gift_card_price_keyboard = []
    back_button_keyboard = [types.InlineKeyboardButton("Back 🔙", callback_data='shop')]

    back_keyboard = types.InlineKeyboardMarkup([back_button_keyboard])

    if not gift_card_prices:
        bot.edit_message_text("No gift cards available\n\nIf you want to request a gift card please let me know",
                              chat_id, message_id, reply_markup=back_keyboard)
        return

    for gift_card_price in gift_card_prices:
        prices_button.append(f"{gift_card_price}_{service_name}")
        gift_card_price_keyboard.append(InlineKeyboardButton(gift_card_price,
                                                             callback_data=f"{gift_card_price}_{service_name}"))

    shop_keyboard = [
        gift_card_price_keyboard,
        back_button_keyboard
    ]

    keyboard = InlineKeyboardMarkup(shop_keyboard)
    bot.edit_message_text(f"Choose your Price:\n\n", chat_id,
                          message_id, reply_markup=keyboard, parse_mode='HTML')

    @bot.callback_query_handler(func=lambda call: call.data in prices_button)
    def handle_yes_callback(call):
        price = float(call.data.split('_')[0])
        try:
            if price <= get_wallet(chat_id):
                text = update_wallet(chat_id, price)
                gift_card_code = get_gift_card_code_by_price(call.data.split('_')[1], price)
                message_text = f"The {service_name} key is: {gift_card_code}\n\n {text}"
            else:
                message_text = "You must add Balance to your wallet"

            bot.edit_message_text(f"{message_text}", chat_id, message_id,
                                  reply_markup=back_keyboard, parse_mode='HTML')

        except Exception as e:
            # Handle any errors that occur during message deletion or sending
            print(f"Error handling confirm callback: {str(e)}")
            raise
