import functions
import os
import json
from bs4 import BeautifulSoup
from transliterate import translit
import time
from pathlib import Path
import re
import requests

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

# find the total amount of downloadLinks
amount = 0
for category in categories_dict:
    for subcategory in categories_dict[category]["subcategories"]:
        #print(subcategory["downloadLink"])
        amount += 1
print(f"Total amount of downloadLinks: {amount}")

import os
import threading
import requests

headers = {
    "DNT": "1",
    "Cookie": "StoreSID=57fa2df7-c0be-432a-89bb-81c04a06b484; AKA_A2=A",
}

def get_request(url, file_name):
    querystring = {
        "$component":"Atcom.Sites.Yoda.Components.ProductList.Index",
        "sortby":"ByPopularity",
        "pg":"1",
        "endless":"false"
    }
    response = requests.get(url, headers=headers, params=querystring)
    with open(file_name, 'wb') as f:
        f.write(response.content)

# Create the responses folder if it doesn't exist
if not os.path.exists("responses"):
    os.mkdir("responses")

# Delete the responses folder and its contents if it exists
if os.path.exists("responses"):
    for filename in os.listdir("responses"):
        os.remove(os.path.join("responses", filename))
    os.rmdir("responses")

# Recreate the responses folder
os.mkdir("responses")

# Loop over the links and download the responses
threads = []
for i, category in enumerate(categories_dict):
    for j, subcategory in enumerate(categories_dict[category]["subcategories"]):
        url = subcategory["downloadLink"]
        file_name = f"responses/response{i+1}-{j+1}.html"
        thread = threading.Thread(target=get_request, args=[url, file_name])
        threads.append(thread)
        thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Count the number of response files
response_count = len([filename for filename in os.listdir("responses") if filename.endswith(".html")])

# Print the number of response files
print(f"Downloaded {response_count} responses.")

print("Done!")
