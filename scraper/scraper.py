import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

import high_quality_img as hqi
import helper_functions as helper

def scraper(driver:webdriver.Chrome):
    """
    Scraped die gerade geladene Seite <br>
    Kann nicht eine komplette Seite scannen, da diese automatisch generiert wird und nicht preloaded ist. <br>
    """
    scraped_data = []

    try:
        articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )

        for article in articles:
            try:
                list_item = article.find_element(By.CSS_SELECTOR, "li.find_tile")

                product_brand = list_item.find_element(By.CLASS_NAME, "find_tile__brand")

                product_name = list_item.find_element(By.CLASS_NAME, "find_tile__name")

                product_link = list_item.find_element(By.CLASS_NAME, "find_tile__productLink")

                #get the price by the right tag
                try:
                    product_price = list_item.find_element(By.CSS_SELECTOR, ".find_tile__priceValue--strikethrough")
                except NoSuchElementException:
                    product_price = list_item.find_element(By.CSS_SELECTOR, ".find_tile__priceValue")

                product_image = list_item.find_element(By.CSS_SELECTOR, "div.find_tile__productImageContainer picture img.find_tile__productImage")

                #get the right image url and generate the high quality link
                image_url = product_image.get_attribute("src")
                if not image_url:
                    image_url = product_image.get_attribute("data-src")
                alt_image = product_image.get_attribute("alt")
                
                # ... 💀
                high_quality_img_url = hqi.even_better_and_stupidly_simple_img_link(image_url, alt_image)

                data = {
                    "brand": product_brand.text.strip(),
                    "name": product_name.text.strip(),
                    "price": helper.clean_price(product_price.text),
                    "img": image_url,
                    "high_q_img": high_quality_img_url,
                    "alt": alt_image,
                    "link": product_link.get_attribute("href"),
                }
                scraped_data.append(data)

            except NoSuchElementException:
                #print("Some elements not found in this article, skipping...")
                pass

    except TimeoutException:
        print("Timed out waiting for products to load.")

    return scraped_data


def scrape_full_page(url:str, driver:webdriver.Chrome):
    """
    Scraped eine komplette Seite indem sie sie durchscrollt
    """
    
    print(f"Scraping {url}\n")

    #Setup parameters
    driver.get(url)
    max_height = driver.execute_script("return document.body.scrollHeight")
    current_height = 0
    product_data = []

    #scroll through the page and scrape currently loaded products
    while current_height < max_height:  
        current_height += 4500
        percentage = min(100, int((current_height / max_height) * 100))
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        print(f"\033[FProgress: {percentage}% of category!" )

        product_data.extend(scraper(driver))


    product_data = helper.remove_duplicates(product_data)

    #Debugging    
    #for item in product_data:
    #    print(item)
    #print(len(product_data))

    return product_data


#---Main execute---#

def scrape_main(search_terms:list, export_path:str='articles.json', await_debug:bool=False):
    """
    Scraped die gegebenen Suchterme und gibt eine JSON mit folgenden Produktdaten aus:
    - Name ("name")
    - Preis ("price")
    - original Bild ("img")
    - high-res Bild ("high_q_img")    
    - Link (zu Produkt)
    """

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
        products = scrape_full_page(f"https://www.otto.de/suche/{search_term}/?verkaeufer=otto", driver)
        category_dict[search_term] = products

    #Export data to JSON
    helper.export_to_json(category_dict, export_path)

    #Print summary
    for category in category_dict:
        print(f"Category: {category}, Articles: {len(category_dict[category])}")
    total_count = sum(len(category) for category in category_dict.values())
    print(f"Total articles scraped: {total_count}")

    driver.quit()
    
if __name__ == "__main__":
    #categories = ["multimedia", "hello kitty", "moebel","haushalt", "bekleidung", "sport", "gartengeraete", "kostueme", "kleidung", "haustier kostueme", "haustier accessoires", "geraet", "bau", "beauty", "kind", "utensilien", "pc accessoires"]
    categories = ["kostueme"]
    scrape_main(search_terms = categories, export_path='articles.json', await_debug=False)