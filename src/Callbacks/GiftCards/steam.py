from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from Database.GiftCards import save_service_name
from Callbacks import confirm

def handle_steam_callback(call, bot):
    chat_id = call.message.chat.id
    
    try:
        # Clear any existing handlers and acknowledge the request
        # bot.answer_callback_query(call.id, "Steam gift card information requested.")
        bot.clear_step_handler_by_chat_id(chat_id=chat_id)
        
        # Ask user for the gift card code
        bot.edit_message_text(
            "Please send me the Steam gift card code:\n\n"
            "Note: Make sure to enter the code carefully",
            chat_id,
            call.message.message_id
        )
        print(call.message.message_id)
        bot.register_next_step_handler(call.message, process_code, bot)
    
    except Exception as e:
        bot.send_message(chat_id, "An error occurred. Please try again.")
        print(f"Error in handle_steam_callback: {str(e)}")

def process_code(message, bot):
    chat_id = message.chat.id
    code = message.text.strip()
    
    # Validate code
    if not code or len(code) < 5:  # Adjust minimum length as needed
        bot.send_message(chat_id, "Invalid code format. Please try again.")
        return
    
    try:
        message1 = int(message.message_id) - 1
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(
            "Please send me the price of the gift card:\n\n"
            "Format: Enter number only (e.g., 50)",
            chat_id,
            message1
        )
        bot.register_next_step_handler(message, process_price, bot, code, message1)
    
    except Exception as e:
        bot.send_message(chat_id, "An error occurred. Please try again.")
        print(f"Error in process_code: {str(e)}")

def process_price(message, bot, code, message1):
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
        message2 = message1
        print(message2)
        
        # Create confirmation keyboard
        confirm_keyboard = InlineKeyboardMarkup()
        confirm_keyboard.row(
            InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
            InlineKeyboardButton("❌ Clear", callback_data='clear')
        )
        
        # Show confirmation message with details
        confirmation_text = (
            "Please confirm the following details:\n\n"
            f"Service: Steam Gift Card\n"
            f"Code: {code}\n"
            f"Price: {price_float:.2f}\n\n"
            "Is this information correct?"
        )
        
        # Save to database if confirmed
        # save_service_name("Steam", code, price_float)
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(
            confirmation_text,
            chat_id,
            message2,
            reply_markup=confirm_keyboard
        )
        
    except Exception as e:
        bot.send_message(chat_id, "An error occurred while saving. Please try again.")
        print(f"Error in process_price: {str(e)}")
    
    @bot.callback_query_handler(func=lambda call: call.data == 'confirm')
    def handle_confirm_callback(call):
        save_service_name("Steam", code, price_float)
        confirm.handle_confirm_callback(call, bot)