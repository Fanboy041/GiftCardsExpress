import telebot, logging
import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# MongoDB database connection uri
uri = os.getenv("MONGO_URI")



# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a new client and connect to the server
client = MongoClient(uri)

# Create "Permissions" database
db = client.permissions # Permissions is the name of the database

""" # Create the collections
db.create_collection("user_collection") 
"""

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

    

# Create a schema for users that contains a full name and username and chat id of the user
user_schema = {
    "rule": str,
    "full_name": str,
    "username": str,
    "chat_id": int,
    # "wallet": 0
    "wallet": int
}

# # Define the collections for owner, users
collection = client.permissions.collection

# Create a function to get the owner information from the database
def get_owner(rule):
    return collection.find_one({"rule": rule})

# Create a function to get the user information from the database
def get_user(chat_id):
    return collection.find_one({"chat_id": chat_id})

# Create a function to get all users information from the database
def get_users(rule):
    return collection.find_one({"rule": rule})

def delete_user(chat_id):
    return collection.delete_one({'chat_id': chat_id})

# Create a function to save the owner information to the database
def save_owner(full_name, username, chat_id):
    owner_info = {
        "rule": "Owner",
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id,
        "wallet": 0
    }
    user_existed(owner_info)

    # owner_existed = collection.find_one({"chat_id": chat_id}) is not None

    # if owner_existed:
    #     collection.update_one({"chat_id": chat_id}, {"$set": owner_info})

    # else:
    #     collection.insert_one(owner_info)

# Create a function to save the user information to the database
def save_user(full_name, username, chat_id):
    user_info = {
        "rule": "User",
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id,
        "wallet": 0
    }
    user_existed(user_info)
    
    # user_existed = collection.find_one({"chat_id": chat_id}) is not None

    # if user_existed:
    #     collection.update_one({"chat_id": chat_id}, {"$set": {"full_name": full_name, "username": username}})

    # else:
    #     if (collection.find_one({"chat_id": chat_id}) is None):
    #         collection.insert_one(user_info)
    #         # Send message to owner when a new member joined

    #         user = get_user(chat_id)

    #         # Counting the number of the users
    #         total_users = collection.count_documents({})
    #         # Get chat ID from owner document
    #         owner_chat_id = collection.find_one()['chat_id']
    #         if owner_chat_id != user['chat_id']:
    #             bot.send_message(owner_chat_id, f"🔥 New member:\n\n👤 <b>{full_name}</b>\n\nTotal users: {total_users}", parse_mode='HTML' )

def user_existed(info):
    existed = collection.find_one({"chat_id": info.get("chat_id")}) is not None

    if existed:
        if info.get("rule") == "Owner":
            collection.update_one({"chat_id": info.get("chat_id")}, {"$set": info})

        elif info.get("rule") == "User":
            collection.update_one({"chat_id": info.get("chat_id")}, {"$set": {"full_name": info.get("full_name"), "username": info.get("username")}})

    else:
        if info.get("rule") == "Owner":
            collection.insert_one(info)

        elif info.get("rule") == "User":
            if (collection.find_one({"chat_id": info.get("chat_id")}) is None):
                collection.insert_one(info)
                # Send message to owner when a new member joined

                user = get_user(info.get("chat_id"))

                # Counting the number of the users
                total_users = collection.count_documents({})
                # Get chat ID from owner document
                owner_chat_id = collection.find_one()['chat_id']
                if owner_chat_id != user['chat_id']:
                    bot.send_message(owner_chat_id, f"🔥 New member:\n\n👤 <b>{info.get("full_name")}</b>\n\nTotal users: {total_users}", parse_mode='HTML')