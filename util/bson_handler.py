import bson

import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from util import database_handler

class BsonHandler:

    def __init__(self, db_handler:database_handler.DatabaseHandler):
        self.db_handler = db_handler

    
    def create_local_dump(self):
        
        """
        Dumps the product Data into ./DB/products.bson for later access
        """

        data = list(self.db_handler.get_all_entries())
        formatted_data = {"entries": data} # format data into a dict

        with open("./DB/products.bson", "wb") as local_db:
            local_db.write(bson.encode(formatted_data))
    
    def load_from_bson(self):

        """
        Reads data from the local dump<br>
        Returns a list of all products
        """

        products = []
        with open("./DB/products.bson", "rb") as local_db:
            data = local_db.read()
            products = bson.decode(data)["entries"]
        return products


