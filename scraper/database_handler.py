from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from server import logger
LOGGER = logger.Logger

class DatabaseHandler:

    def __init__(self, client:MongoClient):
        self.client:MongoClient = client
        self.db_name = self.client["HigherLower"]
        self.collection_name = self.db_name["Products"]

    def test_connection(self):
        try:
            self.client.admin.command('ping')
            LOGGER.success("Database", "Connected to MongoDB")
        except Exception as e:
            LOGGER.error("Database", "Error while connecting to MongoDB", e)

    def write_category(self, product_data:list):
        try:
            self.collection_name.insert_many(product_data)
            LOGGER.success("Writing data", f"Wrote {len(product_data)} products.")
        except:
            LOGGER.error("Writing data", "Failed to write data in MongoDB")

    def delete_category(self, category):
        try:
            self.collection_name.delete_many({"category": category})
            LOGGER.success("Deleting data", f"Deleted products from category: {category}")
        except:
            LOGGER.error("Deleting data", f"Failed to delete category: {category}")

    def get_category(self, category):
        try:
            entries = self.collection_name.find({"category": category})
            return entries
        except:
            LOGGER.error("Getting data", f"Failed to find category: {category}")
            return []

    def get_all_entries(self):
        try:
            entries = self.collection_name.find(projection={'_id': False})
            return entries
        except:
            LOGGER.error("Getting data", f"Failed to get entries")
            return []