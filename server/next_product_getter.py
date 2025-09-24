import json
from os import path
import random



class Difficulty:
    def __init__(self, threshold = 1.2, base = 0.05, absolute = 120, relative = 1.0, relation_base = 0.2):
        self.threshold = threshold
        self.base = base
        self.absolute = absolute
        self.relative = relative
        self.relation_base = relation_base

Difficulty.normal = Difficulty(1.2, 0.05, 120, 1, 0.2)
Difficulty.hard = Difficulty(1.1, 0.03, 120, 1.5, 0.25)
Difficulty.extreme = Difficulty(1, 0, 120, 1.5, 0.25)

class Product:
    def __init__(self,brand, name, price, img, link = None, high_q_img = None, alt="product"):
        self.brand = brand
        self.name = name
        self.price = float(price)
        self.img = img
        self.high_q_img = high_q_img
        self.alt = alt
        self.link = link

    # Calculates how similar in price products are
    def get_product_relation(self, other, difficulty: Difficulty = Difficulty.normal):
        if self.price * difficulty.threshold >= other.price >= self.price / difficulty.threshold: return 0
        return difficulty.base + self.__class__.absolute_relation(self.price - other.price, difficulty.absolute) + self.__class__.relative_relation(self.price/other.price, difficulty.relative)

    # Based on the absolute price difference
    @staticmethod
    def absolute_relation(delta_price, modifier = Difficulty.normal.absolute, relation_base = Difficulty.normal.relation_base):
        # At most 0.2
        return max(0, relation_base - abs(delta_price)/modifier)

    # Based on the relative price ratio
    @staticmethod
    def relative_relation(price_ratio, modifier = Difficulty.normal.relative, relation_base = Difficulty.normal.relation_base):
        # At most 0.2
        return max(0, -0.5*((((price_ratio if price_ratio > 1 else 1/price_ratio) - 1) * modifier)**2) + relation_base)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.price}, {self.img}, {self.high_q_img})'

    def __str__(self):
        return f'{self.name}: {self.price}€'

class ProductCollection:
    def __init__(self, file_path = None, *, category = None, products = None):
        self.products = None
        self.category = category
        if products is None:
            if not file_path is None: self.load_products(file_path)
        else:
            self.products = products

    def load_products(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            categories = json.load(f)
            products = None
            if self.category is None:
                # Adds together all products of all categories
                products = [product for k, v in categories.items() for product in v]
            else:
                products = categories[self.category]
            # Unpacks the product dictionary into the Product class constructor
            self.products = [Product(**product) for product in products]

    def next_product(self, last_product: Product | int | None = None, difficulty: Difficulty = Difficulty.normal) -> Product:
        if last_product is None:
            return random.choice(self.products)
        if isinstance(last_product, int):
            last_product = self[last_product]
        # Shuffles the product list
        products = random.sample(self.products, len(self.products))
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

def main():
    catalog = ProductCollection(path.relpath('../scraper/articles.json'))
    print(len(catalog))
    categories = []
    with open(path.relpath('../scraper/articles.json')) as f:
        categories = json.load(f).keys()
    print(sum([len(ProductCollection(path.relpath('../scraper/articles.json'), category=category)) for category in categories]))

if __name__ == '__main__':
    main()