from Database.MongoDB import users, save_owner, save_user, get_owner, get_user


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

        # Set owner if it's the first user and there is one owner only
        if users.count_documents({}) == 0:
            save_owner(full_name, username, chat_id)
            bot.send_message(message.chat.id, f"Welcome <b>{full_name}</b>\nYou are my owner from now on",
                             parse_mode='HTML')
            # logging.info(message.text)

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
                # TODO make new member as telegram member not like this shit
                bot.send_message(owner_chat_id,
                                 f"🔥 New member:\n\n👤 <b>{user.get("full_name")}</b>\n\nTotal users: {total_users}",
                                 parse_mode='HTML')

            if message.chat.id == get_owner()['chat_id']:
                bot.send_message(message.chat.id,
                                 f"Hey owner, <b>{full_name}</b>!\n\nThank you for interacting with me. I'm excited "
                                 f"to have you on board. 🌹",
                                 parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                                 f"Welcome, <b>{full_name}</b>!\n\nThank you for interacting with our Telegram bot. "
                                 f"We're excited to have you on board. 🌹",
                                 parse_mode='HTML')

    else:
        bot_username = bot.get_me().username
        if f"@{bot_username}" in message.text:
            bot.reply_to(message, "Please run the command in private")
