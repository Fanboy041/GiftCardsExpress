def handle_confirm_callback(call, bot):
    
    try:
        # Delete the previous message
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        # Send a new message confirming the action
        bot.send_message(chat_id=call.message.chat.id, text="Action confirmed!")
        
    except Exception as e:
        # Handle any errors that occur during message deletion or sending
        print(f"Error handling confirm callback: {str(e)}")
        raise