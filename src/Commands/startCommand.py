def send_welcome(message, bot):
    bot.send_message(message.chat.id, f"Welcome\nYou are my owner from now on", parse_mode='HTML')
