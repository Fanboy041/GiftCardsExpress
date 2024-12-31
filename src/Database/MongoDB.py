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
if "giftCards" not in db.list_collection_names():
    db.create_collection("giftCards")

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
