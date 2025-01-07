from Database.GiftCards import save_gift_card_name
from telebot import types
from telebot.types import InlineKeyboardMarkup


def handle_add_gift_card_code_callback(call, bot):
    chat_id = call.message.chat.id
    service_name = call.data.split('_', 1)[0]
    message_id = call.message.message_id

    try:
        # Clear any existing handlers and acknowledge the request
        # bot.clear_step_handler_by_chat_id(chat_id=chat_id)

        # Ask user for the gift card code
        bot.edit_message_text(
            f"Please send me the {service_name} gift card code:\n\n"
            "Note: Make sure to enter the code carefully",
            chat_id,
            message_id
        )
        bot.register_next_step_handler(call.message, process_code, bot, service_name, message_id)

    except Exception as e:
        bot.send_message(chat_id, "An error occurred. Please try again.")
        print(f"Error in handle_steam_callback: {str(e)}")


def process_code(message, bot, service_name, message_id):
    chat_id = message.chat.id
    code = message.text.strip()

    # Validate code
    if not code or len(code) < 5:  # Adjust minimum length as needed
        bot.send_message(chat_id, "Invalid code format. Please try again.")
        return

    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(
            "Please send me the price of the gift card:\n\n"
            "Format: Enter number only (e.g., 50)",
            chat_id,
            message_id
        )
        bot.register_next_step_handler(message, process_price, bot, code, service_name, message_id)

    except Exception as e:
        bot.send_message(chat_id, "An error occurred. Please try again.")
        print(f"Error in process_code: {str(e)}")


def process_price(message, bot, code, service_name, message_id):
    chat_id = message.chat.id
    price = message.text.strip()

    # Validate price
    try:
        price_float = float(price)
        if price_float <= 0:
            bot.send_message(chat_id, "Price must be greater than 0. Please try again.")
            return
    except ValueError:
        bot.send_message(chat_id, "Invalid price format. Please enter a number.")
        return

    try:

        # Create confirmation keyboard
        start_keyboard = [
            [
                types.InlineKeyboardButton("✅ Yes", callback_data=f'yes_add_gift_card_{service_name}'),
                types.InlineKeyboardButton("❌ Clear", callback_data='back_to_main_menu')
            ]
        ]

        confirm_keyboard = InlineKeyboardMarkup(start_keyboard)

        # Show confirmation message with details
        confirmation_text = (
            "Please confirm the following details:\n\n"
            f"Service: {service_name} Gift Card\n"
            f"Code: {code}\n"
            f"Price: {price_float:.2f}\n\n"
            "Is this information correct?"
        )

        # Save to database if confirmed
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(
            confirmation_text,
            chat_id,
            message_id,
            reply_markup=confirm_keyboard
        )

    except Exception as e:
        bot.send_message(chat_id, "An error occurred while saving. Please try again.")
        print(f"Error in process_price: {str(e)}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f"yes_add_gift_card_{service_name}"))
    def handle_yes_callback(call):
        text = save_gift_card_name(service_name, code, price_float)
        try:
            # Delete the previous message
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            # Send a new message confirming the action
            bot.send_message(chat_id=call.message.chat.id, text=f"{text}")

        except Exception as e:
            # Handle any errors that occur during message deletion or sending
            print(f"Error handling confirm callback: {str(e)}")
            raise
