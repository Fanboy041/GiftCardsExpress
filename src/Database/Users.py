from Database.MongoDB import client

# Create a schema for users
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


def get_wallet(chat_id):
    return get_user(chat_id)["wallet"]


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
        if get_user(user_info.get("chat_id"))['username'] != username:
            users.update_one({"chat_id": user_info.get("chat_id")},
                            {"$set": {"username": user_info.get("username")}})

        if get_user(user_info.get("chat_id"))['full_name'] != full_name:
            users.update_one({"chat_id": user_info.get("chat_id")},
                            {"$set": {"full_name": user_info.get("full_name")}})
    else:
        users.insert_one(user_info)


def __user_existed(info):
    existed = get_user(info.get("chat_id")) is not None

    if existed:
        return True

    else:
        return False
