from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import database_handler as db_handler

db_uri = "mongodb+srv://gregorassmann:Gregor.2007@higherlower.ojazzfb.mongodb.net/?appName=HigherLower"

client = MongoClient(db_uri, server_api=ServerApi('1'))
database_handler = db_handler.DatabaseHandler(client)
database_handler.test_connection()
