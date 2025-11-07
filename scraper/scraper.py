import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import yaml

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import high_quality_img as hqi
import helper_functions as helper

import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # project root: higher_lower
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from util import database_handler as db_handler


def scraper(x_paths:dict, category:str, driver:webdriver.Chrome):
    """
    Scraped die gerade geladene Seite <br>
    Kann nicht eine komplette Seite scannen, da diese automatisch generiert wird und nicht preloaded ist. <br>
    """
    scraped_data = []
    successful_products = 0

    try:
        articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )

        for article in articles:
            try:
                product_brand = article.find_element(By.XPATH, x_paths["brand"])
                product_name = article.find_element(By.XPATH, x_paths["name"])
                product_link = article.find_element(By.XPATH, x_paths["link"])

                try: #get the price by the right tag
                    product_price = article.find_element(By.XPATH, x_paths["original_price"])
                except NoSuchElementException:
                    product_price = article.find_element(By.XPATH, x_paths["price"])
                product_image = article.find_element(By.XPATH, x_paths["img"])

                #get the right image url and generate the high quality link
                image_url = product_image.get_attribute("src")
                if not image_url:
                    image_url = product_image.get_attribute("data-src")
                alt_image = product_image.get_attribute("alt")
                
                # ... 💀
                high_quality_img_url = hqi.even_better_and_stupidly_simple_img_link(image_url)

                data = {
                    "brand": product_brand.text.strip(),
                    "name": product_name.text.strip(),
                    "price": helper.clean_price(product_price.text),
                    "img": image_url,
                    "high_q_img": high_quality_img_url,
                    "alt": alt_image,
                    "link": product_link.get_attribute("href"),
                    "category": category,
                }
                scraped_data.append(data)
                
                successful_products += 1
                print(f"\033[FSuccesfully collected: {successful_products} products!" )

            except NoSuchElementException as e:
                pass

    except TimeoutException:
        print("Timed out whilst trying to load articles.")
        pass

    return scraped_data

def scrape_category(url:str, x_paths:dict, db_uri:str, category:str, driver:webdriver.Chrome):
    """
    Scraped eine komplette Seite indem sie sie durchscrollt <br>

    Gibt eine liste an Produkten zurück
    """

    print(f"Scraping {url}\n")

    #Setup parameters
    driver.get(url)
    max_height = driver.execute_script("return document.body.scrollHeight")
    current_height = 0
    product_data = []


    #scroll through the page and scrape loaded products
    step_size_px = 500
    while current_height < max_height:  
        current_height += step_size_px
        percentage = min(100, int((current_height / max_height) * 100))
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(.05) # give page some time to load on each step, could prob be optimized
        print(f"\033[FLoaded: {percentage}% of page!" )

    print("Collecting Data...\n")
    product_data.extend(scraper(x_paths=x_paths, driver=driver, category = category))
    product_data = helper.remove_duplicates(product_data) # might be unnecessary

    #Debugging    
    #for item in product_data:
    #    print(item)
    #print(len(product_data))

    return product_data

def scrape_main(search_terms:list, x_paths:dict, db_uri:str, export_path:str='articles.json', await_debug:bool=False):
    """
    Scraped die gegebenen Suchterme und speichert die Produkte auf MongoDB mit folgenden Werten: 
    - Name ("name")
    - Preis ("price")
    - original Bild ("img")
    - high-res Bild ("high_q_img")    
    - Link (zu Produkt) ("link")
    - Kategorie ("category")
    """

    client = MongoClient(db_uri, server_api=ServerApi('1'))
    database_handler = db_handler.DatabaseHandler(client)
    database_handler.test_connection()
    category_dict = {}

    #Setup WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    print("Initializing WebDriver...")
    if await_debug:
        time.sleep(13) # Await all debug prints from selenium to finish

    #Search and scrape each category
    for search_term in search_terms:
        products = scrape_category(f"https://www.otto.de/suche/{search_term}/?verkaeufer=otto", x_paths=x_paths, driver=driver, db_uri=db_uri, category = search_term)
        print(f"Collected {len(products)} unique products!")        
        # Handle Data storage
        database_handler.delete_category(category=search_term)
        database_handler.write_category(products)
        category_dict[search_term] = products
        print("---------------------------------------------------------")

    # Export data to JSON
    # Left in in case its needed later
    #helper.export_to_json(category_dict, export_path)

    #Print summary
    for category in category_dict:
        print(f"Category: {category}, Articles: {len(category_dict[category])}")
    total_count = sum(len(category) for category in category_dict.values())
    print(f"Total articles scraped: {total_count}")

    driver.quit()
    
def load_config(yaml_file:str):
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        # get config data by paramater
        categories = data.get('categories')
        x_paths = data.get('paths')

        db_link = data.get('db')["link"]
        db_password = data.get('db')["password"]

        db_uri = db_link.replace("<Password>", db_password)

        if categories:
            return categories, x_paths, db_uri
        else:
            print("Config", "No 'categories' in config-file")

    except FileNotFoundError:
        print("File", f"File '{yaml_file}' not found.")
    except yaml.YAMLError as e:
        print("Yaml", f"Failed parsing Yaml File", e)

if __name__ == "__main__":
    
    yaml_file = "scraper_config.yaml"

    categories, x_paths, db_uri = load_config(yaml_file)
    
    scrape_main(search_terms = categories, x_paths=x_paths, db_uri=db_uri, export_path='articles.json', await_debug=False)