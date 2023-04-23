import functions
import os
import json
from bs4 import BeautifulSoup
from transliterate import translit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
import re

BASE_URL = "https://www.sklavenitis.gr"
KATIGORIES_URL = "https://www.sklavenitis.gr/katigories"
FOLDER_NAME = "sklavenitis"

# Since we are doing the shop sklavenitis.gr, we need to put everything in a folder called sklavenitis
if not os.path.exists(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)
    print("Folder created")
    os.chdir(FOLDER_NAME)
else:
    os.chdir(FOLDER_NAME)
print("Folder already exists, using existing folder...")

# This file is essential for the scraper to work, it contains all the categories and subcategories of the shop
functions.getPage(KATIGORIES_URL, "sklavenitis-katigories.html", False, True)

# Once the file is downloaded, we can start scraping the data
# We need to find the categories and subcategories
doc = open('sklavenitis-katigories.html', encoding="utf-8")
soup = BeautifulSoup(doc, "html.parser")
categories = soup.find_all("div", class_="categories_item")

# Loop through each category and print the category name, image and subcategories.
categories_dict = {}
categories_list = []

for category in categories:
    # Use the url BASE_URL/eidi-artozacharoplasteioy/psomi-typopoiimeno/
    # to get the subcategories and the total products
    # the first part after the domain is the category name
    # the second part is the subcategory name

    category_name = category.find("h3", class_="categories_title").text.strip()
    category_name = translit(category_name, "el", 'en')
    category_name = functions.removeNonAlphaNumeric(
        category_name, True, False, True, False)

    category_image = category.find(
        "img")["src"].strip().replace("\n", "").replace("\t", "")
    subcategories = category.find("div", class_="categories_subs")
    subcategories_list = []

    for subcategory in subcategories.find_all("a"):
        subcategory_name = subcategory.text.strip()
        subcategory_name = translit(subcategory_name, "el", 'en')
        subcategory_name = functions.removeNonAlphaNumeric(
            subcategory_name, True, False, True, False)
        subcategory_link = subcategory["href"].strip()
        original_subcategory_link = subcategory_link
        subcategory_link = functions.removeNonAlphaNumeric(
            subcategory_link, True, True, False, True)

        subcategories_list.append({
            "name": subcategory_name,
            "link": subcategory_link,
            "downloadLink": BASE_URL + original_subcategory_link,
            "productsAmount": "Unknown"
        })

    categories_dict[category_name] = {
        "image": category_image,
        "subcategoryAmount": len(subcategories_list),
        "subcategories": subcategories_list
    }

    categories_list.append(categories_dict)


# json dump
with open("sklavenitis.json", "w", encoding="utf-8") as f:
    json.dump(categories_dict, f, ensure_ascii=False, indent=4)

# Now we download the html files for each subcategory
print("'FOLDERING' TIME")
for category in categories_dict:
    category_folder = category
    if not os.path.exists(category_folder):
        os.mkdir(category_folder)
        print("Folder created")

        for subcategory in categories_dict[category]["subcategories"]:
            filename = subcategory["name"] + ".html"
            functions.getPage(
                subcategory["downloadLink"], filename, True, False)
            os.rename(filename, os.path.join(category_folder, filename))
            print("File downloaded and moved")
    else:
        print("Folder already exists, using existing folder...")

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--blink-settings=imagesEnabled=false')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
# #extra options
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# driver = webdriver.Chrome(chrome_options=chrome_options )

# file_path = "allantika/loykanika.html"
# html_file = os.path.abspath(file_path)
# driver.get("file:///" + html_file)

# SCROLL_PAUSE_TIME = 1
# time.sleep(SCROLL_PAUSE_TIME)

# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")

# for x in range(0, 10):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     price_search = driver.find_elements(By.CLASS_NAME, "price")
#     name_search = driver.find_elements(By.CLASS_NAME, "product__title")

#     name_prices = {}
#     price_list = []
#     name_list = []

#     for i in price_search:
#         product_price = i.get_attribute("data-price")
#         price_list.append(product_price)

#     for i in name_search:
#         product_name = i.text
#         name_list.append(product_name)

#     # add to dictionary
#     for i in range(0, len(price_list)):
#         name_prices[name_list[i]] = price_list[i]


#     time.sleep(SCROLL_PAUSE_TIME)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

# driver.close()

def extract_max_product(soup):
    # Find the span element with class "current-page" and extract its text
    current_page_span = soup.find('span', {'class': 'current-page'})
    current_page_text = current_page_span.text.strip()

    # Extract the second number from the text using regex
    matches = re.findall(r"\d+", current_page_text)
    max_product = matches[1] if len(matches) > 1 else None

    return max_product


def process_html_file(file_path):
    # This function should process the HTML file and return the relevant data as a dictionary

    # Parse the HTML using BeautifulSoup
    doc = open(file_path, encoding="utf-8")
    soup = BeautifulSoup(doc, "html.parser")

    # Find the span element with class "current-page" and extract its text
    current_page_span = soup.find('span', {'class': 'current-page'})
    current_page_text = current_page_span.text.strip()

    # Extract the second number from the text using regex
    matches = re.findall(r"\d+", current_page_text)
    max_product = matches[1] if len(matches) > 1 else None

    # Determine if max_product is less than or equal to 24
    under24 = False
    if max_product is not None:
        max_product = int(max_product)
        under24 = max_product <= 24

    # Return a dictionary with the max_product and under24 values
    return {"max_product": max_product, "under24": under24}



def process_directory(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".html"):
            # If this is an HTML file, process it and write the JSON file
            try:
                data = process_html_file(file_path)
                print("Processing file: " + file_path)
                print("Filename: " + filename)

                json_path = os.path.splitext(file_path)[0] + ".json"
                with open(json_path, "w") as json_file:
                    json.dump(data, json_file)

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        elif os.path.isdir(file_path):
            # If this is a directory, recursively process it
            process_directory(file_path)


# Start processing the root directory
root_dir = "."
process_directory(root_dir)

print("Done!")

