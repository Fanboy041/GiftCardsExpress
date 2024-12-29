import logging
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

# MongoDB database connection uri
uri = os.getenv("MONGO_URI")

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a new client and connect to the server
client = MongoClient(uri)

# Create "Permissions" database
db = client.permissions  # Permissions is the name of the database

# Create the collections
if "users" not in db.list_collection_names():
    db.create_collection("users")

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
    "wallet": int
}

# Define the collections for users
users = client.permissions.users


# Create a function to get the owner information from the database
def get_owner():
    return users.find_one({"rule": "Owner"})


# Create a function to get the user information from the database
def get_user(chat_id):
    return users.find_one({"chat_id": chat_id})


# Create a function to get all users information from the database
def get_users():
    return users.find_one({"rule": "User"})


def delete_user(chat_id):
    return users.delete_one({'chat_id': chat_id})


# Create a function to save the owner information to the database
def save_owner(full_name, username, chat_id):
    owner_info = {
        "rule": "Owner",
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id,
        "wallet": 0
    }
    if __user_existed(owner_info) is True:
        # TODO: check username and fullname before updating
        users.update_one({"chat_id": owner_info.get("chat_id")},
                         {"$set": {"full_name": owner_info.get("full_name"), "username": owner_info.get("username")}})
    else:
        users.insert_one(owner_info)


# Create a function to save the user information to the database
def save_user(full_name, username, chat_id):
    user_info = {
        "rule": "User",
        "full_name": full_name,
        "username": username,
        "chat_id": chat_id,
        "wallet": 0
    }
    if __user_existed(user_info) is True:
        # TODO: check username and fullname before updating
        users.update_one({"chat_id": user_info.get("chat_id")},
                         {"$set": {"full_name": user_info.get("full_name"), "username": user_info.get("username")}})
    else:
        users.insert_one(user_info)


def __user_existed(info):
    existed = get_user(info.get("chat_id")) is not None

    if existed:
        return True

    else:
        return False
