import functions
import os
import json
from bs4 import BeautifulSoup
from transliterate import translit
import requests
import concurrent.futures
from tqdm import tqdm
from playwright.sync_api import sync_playwright


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

headers = {
    "DNT": "1",
    "Cookie": "to-be-determined",
}

def get_request(url, file_name, headers):
    querystring = {
        "$component":"Atcom.Sites.Yoda.Components.ProductList.Index",
        "sortby":"ByPopularity",
        "pg":"1",
        "endless":"false"
    }
    response = requests.get(url, headers=headers, params=querystring)
    with open(os.path.join('responses', file_name), 'wb') as f:
        f.write(response.content)

def send_and_save_requests():
    urls = [subcategory["downloadLink"] for category in categories_dict.values() for subcategory in category["subcategories"]]
    file_names = [f"response{i}.html" for i in range(1, len(urls) + 1)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_request, url, file_name, headers) for url, file_name in zip(urls, file_names)]
        with tqdm(total=len(futures)) as pbar:
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)

    num_files = len(os.listdir('responses'))
    if num_files == len(urls):
        print(f"All {num_files} responses have been successfully saved in the 'responses' folder.")
    else:
        print("Error: Number of files in 'responses' folder does not match the number of links.")
        exit()

def get_cookie_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.sklavenitis.gr/")
        page.click("button.nvcookies__button.nvcookies__button--primary.consent-give")
        print(context.cookies())
        cookie_for_requests = ''
        for cookie in context.cookies():
            cookie_for_requests += cookie['name'] + '=' + cookie['value'] + ';'

        browser.close()
        print(f"Cookie for requests: {cookie_for_requests}")
        headers["Cookie"] = cookie_for_requests

if __name__ == '__main__':
    get_cookie_playwright()
    print(f"Cookie for requests 2 : {headers['Cookie']}")
    send_and_save_requests()

print("Done!")