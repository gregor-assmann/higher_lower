from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from util import logger
LOGGER = logger.Logger

class DatabaseHandler:

    def __init__(self, client:MongoClient):
        self.client:MongoClient = client
        self.db_name = self.client["HigherLower"]
        self.collection_name = self.db_name["Products"]

    def test_connection(self):
        """
        Tests the connection to the Database
        """
        try:
            self.client.admin.command('ping')
            LOGGER.success("Database", "Connected to MongoDB")
        except Exception as e:
            LOGGER.error("Database", "Error while connecting to MongoDB", e)

    def write_category(self, product_data:list):
        """
        Writes a list of products to the Database <br>
        It does not use a seperate Table for each category
        """
        try:
            self.collection_name.insert_many(product_data)
            LOGGER.success("Writing data", f"Wrote {len(product_data)} products.")
        except:
            LOGGER.error("Writing data", "Failed to write data in MongoDB")

    def delete_category(self, category):
        """
        Deletes all Products with the corresponding category tag.
        """
        try:
            self.collection_name.delete_many({"category": category})
            LOGGER.success("Deleting data", f"Deleted products from category: {category}")
        except:
            LOGGER.error("Deleting data", f"Failed to delete category: {category}")

    def get_category(self, category):

        """
        Gets all Products with the corresponding category tag.
        """
        try:
            entries = self.collection_name.find({"category": category}, projection={'_id': False})
            return entries
        except:
            LOGGER.error("Getting data", f"Failed to find category: {category}")
            return []

    def get_all_entries(self):

        """
        Gets all Products and returns a cursor. <br>
        Can be converted using `list()` to get a list of all entries.
        """

        try:
            entries = self.collection_name.find(projection={'_id': False})
            return entries
        except:
            LOGGER.error("Getting data", f"Failed to get entries")
            return []