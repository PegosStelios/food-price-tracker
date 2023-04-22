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

BASE_URL = "https://www.sklavenitis.gr"
KATIGORIES_URL = "https://www.sklavenitis.gr/katigories"
FOLDER_NAME = "sklavenitis"

# Since we are doing the shop sklavenitis.gr, we need to put everything in a folder called sklavenitis
if not os.path.exists(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)
    print("Folder created")
    os.chdir(FOLDER_NAME)
else:
    print("Folder already exists, using existing folder...")
    os.chdir(FOLDER_NAME)

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
            functions.getPage(subcategory["downloadLink"], filename, True, False)
            os.rename(filename, os.path.join(category_folder, filename))
            print("File downloaded and moved")
    else:
        print("Folder already exists, using existing folder...")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(chrome_options=chrome_options )

file_path = "trofes_eidi_gia_katoikidia/trofes_eidi_gia_skyloys.html"
html_file = os.path.abspath(file_path)
driver.get("file:///" + html_file)

SCROLL_PAUSE_TIME = 5
time.sleep(SCROLL_PAUSE_TIME)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

for x in range(0, 10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    search = driver.find_elements(By.CLASS_NAME, "product")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print(len(search))
driver.close()