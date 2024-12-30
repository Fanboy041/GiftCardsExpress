import telebot
import logging
import os
import importlib
from Database.MongoDB import *
from dotenv import load_dotenv

# load the .env file
load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

try:
    # Logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    commands_dir = os.path.join(os.path.dirname(__file__), 'Commands')
    commands = {}

    for folderName in os.listdir(commands_dir):
        if folderName.endswith('.py') and folderName != '__init__.py':
            command_name = os.path.splitext(folderName)[0]
            command = importlib.import_module(f'Commands.{command_name}')
            commands[command_name] = command


    callbacks_dir = os.path.join(os.path.dirname(__file__), 'Callbacks')
    callbacks = {}

    for folderName in os.listdir(callbacks_dir):
        if folderName.endswith('.py') and folderName != '__init__.py':
            callback_name = os.path.splitext(folderName)[0]
            callback = importlib.import_module(f'Callbacks.{callback_name}')
            callbacks[callback_name] = callback


    logging.info("Main script runs successfully, Bot is working")

    # Start command
    @bot.message_handler(commands=['start'])
    def handle_start_command(message):
        if 'startCommand' in commands:
            commands['startCommand'].send_welcome(message, bot)

    # Wallet Callback
    @bot.callback_query_handler(func=lambda call: call.data == 'wallet')
    def handle_wallet_callback(call):
        if 'walletCallback' in callbacks:
            callbacks['walletCallback'].handle_wallet_callback(call)

    bot.infinity_polling()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")
