import telebot, logging
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

    for foldername in os.listdir(commands_dir):
        if foldername.endswith('.py') and foldername != '__init__.py':

            command_name = os.path.splitext(foldername)[0]
            command = importlib.import_module(f'Commands.{command_name}')
            commands[command_name] = command


    logging.info("Main script runs successfully, Bot is working")

    # Start command
    @bot.message_handler(commands=['start'])
    def handle_start_command(message):
        if 'startCommand' in commands:
            commands['startCommand'].send_welcome(message, bot)


    bot.infinity_polling()
except KeyboardInterrupt:
    logging.info("Polling manually interrupted.")
