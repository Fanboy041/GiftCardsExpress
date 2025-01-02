from Database.GiftCards import save_service_name
from telebot import types
from telebot.types import InlineKeyboardMarkup


def handle_add_service_callback(call, bot):
    chat_id = call.message.chat.id

    try:
        # Ask user for the gift card code
        bot.edit_message_text(
            "please send me the correct service name you want to add:\n\n"
            "Note: Make sure to enter the code carefully",
            chat_id,
            call.message.message_id
        )
        bot.register_next_step_handler(call.message, process_Service, bot)

    except Exception as e:
        bot.send_message(chat_id, "An error occurred. Please try again.")
        print(f"Error in handle_add_service_callback: {str(e)}")


def process_Service(message, bot):
    chat_id = message.chat.id
    # service_name = message.text

    try:
        # Create confirmation keyboard
        start_keyboard = [
            [
                types.InlineKeyboardButton("✅ Yes", callback_data='yes_add_service'),
                types.InlineKeyboardButton("❌ Clear", callback_data='back_to_main_menu')
            ]
        ]

        confirm_keyboard = InlineKeyboardMarkup(start_keyboard)

        # Show confirmation message with details
        confirmation_text = (
            f"do you want to save the service name '{message.text}'?"
        )

        # Save to database if confirmed
        # Todo: فارط نعس مالي حيل اكتب انكليزي
        # TODO: المهم هون عم يحفظ المسج القديمة لاخر يوم بعمرو يعني بضل حافطها وعم يكررها وما بيهتم شو اليوزر بيعطيه
        oldMessage = int(message.message_id) - 1
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(
            confirmation_text,
            chat_id,
            oldMessage,
            reply_markup=confirm_keyboard
        )

    except Exception as e:
        bot.send_message(chat_id, "An error occurred while saving. Please try again.")
        print(f"Error in process_service: {str(e)}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("yes_add_service"))
    def handle_yes_callback(call):
        text = save_service_name(message.text)
        try:
            # Delete the previous message
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            # Send a new message confirming the action
            bot.send_message(chat_id=call.message.chat.id, text=f"{text}")

        except Exception as e:
            # Handle any errors that occur during message deletion or sending
            print(f"Error handling confirm callback: {str(e)}")
            raise
