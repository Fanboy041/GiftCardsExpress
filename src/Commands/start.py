from Database.Users import users, save_owner, save_user, get_owner, get_user
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from Callbacks import wallet, shop, servicesNameAsButtons, help
from Database.GiftCards import get_gift_cards, get_service_info


def send_welcome(message, bot):
    if message.chat.type == "private":

        # User's information
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if last_name:
            full_name = first_name + " " + last_name
        else:
            full_name = first_name

        username = message.from_user.username
        chat_id = message.chat.id

        # Make inline keyboard
        start_keyboard = [
            [
                InlineKeyboardButton("💳 My Wallet", callback_data="wallet"),
                InlineKeyboardButton("🛒 Shop", callback_data="shop")
            ],
            [
                InlineKeyboardButton("💰 Add Balance", callback_data="add_balance"),
                InlineKeyboardButton("ℹ️ Help", callback_data="help")
            ]
        ]

        user_start_keyboard = InlineKeyboardMarkup(start_keyboard)

        owner_start_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Gift Card", callback_data="add_gift_card"),
                InlineKeyboardButton("🔎 Show Gift Card", callback_data="show_gift_card")
                # InlineKeyboardButton("➖ Remove Gift Card", callback_data="remove_gift_card")
            ],
            *start_keyboard
        ])

        # Set owner if it's the first user and there is one owner only
        if users.count_documents({}) == 0:
            save_owner(full_name, username, chat_id)
            bot.send_message(message.chat.id, f"Welcome <b>{full_name}</b>\nYou are my owner from now on",
                             parse_mode='HTML', reply_markup=owner_start_keyboard)

        else:
            unsavedUser = get_user(chat_id)
            # Save the user info in the database
            save_user(full_name, username, chat_id)

            # Send message to owner when a new member joined
            user = get_user(chat_id)

            # Counting the number of the users
            total_users = users.count_documents({})
            # Get chat ID from owner document
            owner_chat_id = get_owner()['chat_id']

            if owner_chat_id != user['chat_id'] and unsavedUser is None:
                bot.send_message(owner_chat_id,
                                 f"🔥 New member:\n\n👤 <a href=\"tg://user?id={user.get('chat_id')}\">{user.get('full_name')}</a>\n\nTotal users: {total_users}",
                                 parse_mode='HTML')

            if message.chat.id == get_owner()['chat_id']:
                bot.send_message(message.chat.id,
                                 f"Hey owner, <b>{full_name}</b>!\n\nThank you for interacting with me. I'm excited "
                                 f"to have you on board. 🌹",
                                 parse_mode='HTML', reply_markup=owner_start_keyboard)
            else:
                bot.send_message(message.chat.id,
                                 f"Welcome, <b>{full_name}</b>!\n\nThank you for interacting with our Telegram bot. "
                                 f"We're excited to have you on board. 🌹",
                                 parse_mode='HTML', reply_markup=user_start_keyboard)

    else:
        bot_username = bot.get_me().username
        if f"@{bot_username}" in message.text:
            bot.reply_to(message, "Please run the command in private")

    # Wallet Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'wallet')
    def handle_wallet_callback(call):
        wallet.handle_wallet_callback(call, bot)

    # Shop Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'shop')
    def handle_shop_callback(call):
        shop.handle_shop_callback(call, bot)

    # AddGiftCard Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'add_gift_card')
    def handle_services_name_as_buttons_callback(call):
        servicesNameAsButtons.handle_services_name_as_buttons_callback(call, bot)

    # Help Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'help')
    def handle_help_callback(call):
        help.handle_help_callback(call, bot)

    # Back Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_main_menu')
    def back_to_main_menu_callback(call):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_welcome(call.message, bot)
