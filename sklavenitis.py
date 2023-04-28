import functions
import os
from bs4 import BeautifulSoup
from transliterate import translit
import requests
import concurrent.futures
from tqdm import tqdm
from playwright.sync_api import sync_playwright
import re

BASE_URL = "https://www.sklavenitis.gr"
KATIGORIES_URL = "https://www.sklavenitis.gr/katigories"
FOLDER_NAME = "sklavenitis"
CATEGORIES_DICT = {}
CATEGORIES_LIST = []

if __name__ == '__main__':
    print("This is a module, not a script. Please run main.py instead.")
    exit()

# Since we are doing the shop sklavenitis.gr, we need to put everything in a folder called sklavenitis.
def create_folder():
    if not os.path.exists(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)
        print("Folder created")
        os.chdir(FOLDER_NAME)
    else:
        os.chdir(FOLDER_NAME)
    print("Folder already exists, using existing folder...")

# This file is essential for the scraper to work, it contains all the categories and subcategories of the shop.
def create_categories():
    functions.get_categories_page(KATIGORIES_URL, "sklavenitis-katigories.html")

    # Once the file is downloaded, we can start scraping the data.
    # We need to find the categories and subcategories.
    doc = open('sklavenitis-katigories.html', encoding="utf-8")
    soup = BeautifulSoup(doc, "html.parser")
    categories = soup.find_all("div", class_="categories_item")

    for category in categories:
        # Use the url BASE_URL/eidi-artozacharoplasteioy/psomi-typopoiimeno/
        # to get the subcategories and the total products.
        # the first part after the domain is the category name.
        # the second part is the subcategory name.

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

        CATEGORIES_DICT[category_name] = {
            "image": category_image,
            "subcategoryAmount": len(subcategories_list),
            "subcategories": subcategories_list
        }

    CATEGORIES_LIST.extend(CATEGORIES_DICT.values())


    import json
    with open("sklavenitis.json", "w", encoding="utf-8") as f:
        json.dump(CATEGORIES_DICT, f, ensure_ascii=False, indent=4)


# To be used later for when we send the requests.
headers = {
    "DNT": "1",
    "Cookie": "to-be-determined",
}

def get_category_and_subcategory(url):
    # Extract the category and subcategory from the URL.
    parts = url.split("/")
    if len(parts) < 5:
        raise ValueError("Invalid URL format.")
    category = parts[3]
    subcategory = parts[4]
    return category, subcategory


def get_request(url, file_name, headers):
    querystring = {
        "$component":"Atcom.Sites.Yoda.Components.ProductList.Index",
        "sortby":"ByPopularity",
        "pg":"1",
        "endless":"false"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        with open(os.path.join('responses', file_name), 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - Could not save response for {url}")
        exit()


def send_and_save_requests():
    # Send the requests and save the responses using the links from the categories_dict.
    urls = [subcategory["downloadLink"] for category in CATEGORIES_DICT.values()
            for subcategory in category["subcategories"]]
    print(urls)
    file_names = [f"{get_category_and_subcategory(url)[0]}/{get_category_and_subcategory(url)[1]}.html" for url in urls]

    # Create directories for each category if they do not exist already.
    for category in CATEGORIES_DICT.keys():
        os.makedirs(f"responses/{category}", exist_ok=True)

    # We use multithreading to speed up the process, we can use up to 3 threads at a time without getting flagged.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_request, url, f"responses/{file_name}", headers)
                   for url, file_name in zip(urls, file_names)]
        with tqdm(total=len(futures)) as pbar:
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)

    # Check if all the responses have been saved.
    num_files = len(os.listdir('responses'))
    if num_files == len(urls):
        print(
            f"All {num_files} responses have been successfully saved in the 'responses' folder.")
    else:
        print("Error: Number of files in 'responses' folder does not match the number of links.")
        exit()

# We need to get the cookies from the website to be able to send requests.
def get_cookie_playwright():
    with sync_playwright() as p:
        # Launch the browser in headless mode and create a new page.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.sklavenitis.gr/")
        # Click the button to accept the cookies.
        page.click(
            "button.nvcookies__button.nvcookies__button--primary.consent-give")
        # Get the correct cookies and add them to the headers.
        cookie_for_requests = ''
        for cookie in context.cookies():
            cookie_for_requests += cookie['name'] + '=' + cookie['value'] + ';'
        headers["Cookie"] = cookie_for_requests
        browser.close()


# TODO: Save the responses using a proper name. (category-subcategory.html)
# TODO: Get the products from each subcategory.
# TODO: Find a way to get the total products for each subcategory. (multiple of 24 based on the total products listed on the website)
# TODO: Fix responses not getting saved in the correct folder, now they wont save at all.