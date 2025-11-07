import json
from os import path
import random
import util.logger as logger
import yaml

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from util import database_handler



LOGGER = logger.Logger



class Difficulty:
    def __init__(self, threshold = 1.2, base = 0.05, absolute = 120, relative = 1.0, relation_base = 0.2):
        self.threshold = threshold
        self.base = base # base probability for a product
        self.absolute = absolute # larger -> favors larger absolute gaps
        self.relative = relative # larger -> favors larger relative gaps
        self.relation_base = relation_base # maximum difference in relation, higher -> higher max probability

Difficulty.normal = Difficulty(1.2, 0.05, 120, 1, 0.2)
Difficulty.hard = Difficulty(1.1, 0.03, 80, 1.5, 0.25)
Difficulty.extreme = Difficulty(1, 0, 60, 1.5, 0.25)

class Product:
    def __init__(self,brand, name, price, img, category, link = None, high_q_img = None, alt="product"):
        self.brand = brand
        self.name = name
        self.price = float(price)
        self.img = img
        self.high_q_img = high_q_img
        self.alt = alt
        self.link = link
        self.category = category


    def get_product_relation(self, other, difficulty: Difficulty = Difficulty.normal):
        """
        Calculates how similar in price products are based on the `difficulty`
        """
        if self.price * difficulty.threshold >= other.price >= self.price / difficulty.threshold: return 0
        return difficulty.base + self.__class__.absolute_relation(self.price - other.price, difficulty.absolute) + self.__class__.relative_relation(self.price/other.price, difficulty.relative)

    @staticmethod
    def absolute_relation(delta_price, modifier = Difficulty.normal.absolute, relation_base = Difficulty.normal.relation_base):
        """
        Calculates the absolute relation based on the absolute price difference and `difficulty`
        """
        # At most relation_base
        return max(0, relation_base - abs(delta_price)/modifier)

    @staticmethod
    def relative_relation(price_ratio, modifier = Difficulty.normal.relative, relation_base = Difficulty.normal.relation_base):
        """
        Calculates the relative relation based on the price ratio and `difficulty`
        """
        # At most relation_base
        return max(0, -0.5*((((price_ratio if price_ratio > 1 else 1/price_ratio) - 1) * modifier)**2) + relation_base)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.price}, {self.img}, {self.high_q_img})'

    def __str__(self):
        return f'{self.name}: {self.price}€'

class ProductCollection:
    def __init__(self, config_path, file_path = None, *, category = None, products = None):
        self.products = None
        self.category = category
        self.db_uri = load_config(config_path)
        if products is None:
            if not file_path is None: self.load_products(file_path)
        else:
            self.products = products

    def load_products(self, file_path):

        """
        Loads Products from JSON as one large list and converts them to Product objects
        """

        #with open(file_path, encoding='utf-8') as f:

        """categories = json.load(f)
        products = None
        if self.category is None:
            # Adds together all products of all categories
            products = [product for k, v in categories.items() for product in v]
        else:
            products = categories[self.category]
        # Unpacks the product dictionary into the Product class constructor"""
            
        
        client = MongoClient(self.db_uri, server_api=ServerApi('1'))
        db_handler = database_handler.DatabaseHandler(client)
        db_handler.test_connection()

        products = list(db_handler.get_all_entries())

        LOGGER.load("Products", "Products loaded")
        self.products = [Product(**product) for product in products]

    def next_product(self, last_product: Product | int | None = None, difficulty: Difficulty = Difficulty.normal) -> Product:

        """
        Loads the next product randomly, based on the previous product if provided.
        """

        if last_product is None:
            return random.choice(self.products)
        if isinstance(last_product, int):
            last_product = self[last_product]
        # Shuffles the product list
        products = random.sample(self.products, len(self.products)) # doesnt use shuffle to return a new list
        products.remove(last_product)
        for product in products[:-1]:
            # Uses the product price similarity to randomly get the next product, becoming more probable the more similar the products are
            if random.random() < last_product.get_product_relation(product, difficulty):
                return product
        return products[-1]

    def __getitem__(self, item):
        return self.products[item]

    def __len__(self):
        return self.products.__len__()

    def __str__(self):
        return f'{self.__class__.__name__}{'[]' if self.products is None else [product for product in self.products]}'

def load_config(yaml_file:str):
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        db_link = data.get('db')["link"]
        db_password = data.get('db')["password"]

        db_uri = db_link.replace("<Password>", db_password)

        if db_uri:
            return db_uri
        else:
            print("Config", "No 'categories' in config-file")

    except FileNotFoundError:
        print("File", f"File '{yaml_file}' not found.")
    except yaml.YAMLError as e:
        print("Yaml", f"Failed parsing Yaml File", e)

def main():
    prodcoll = ProductCollection(config_path="game_config.yaml")
    prodcoll.load_products("some path")
    for prod in prodcoll.products:
        print(prod.name)

if __name__ == '__main__':
    main()