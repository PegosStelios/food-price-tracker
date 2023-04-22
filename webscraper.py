import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


URL = 'https://www.sklavenitis.gr'

def getPage(url='https://www.sklavenitis.gr/katigories/', filename='sklavenitis-katigories.html'):
    if not os.path.exists(filename):
        if input("File does not exist, download? (y/n)") == "y":
            print("Downloading file...")
            response = requests.get(url)
            html = response.text

            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            print("File does not exist, exiting...")
            exit()

def getPageNoAccept(url='https://www.sklavenitis.gr/katigories/', filename='sklavenitis-katigories.html'):
    if not os.path.exists(filename):
        print("Downloading file...")
        response = requests.get(url)
        html = response.text

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

getPage()

# Find every categories_title in the file using BeautifulSoup.
doc = open('sklavenitis-katigories.html', encoding="utf-8")
soup = BeautifulSoup(doc, "html.parser")
categories = soup.find_all("div", class_="categories_item")


# Loop through each category and print the category name, image and subcategories.

categories_dict = {}
categories_list = []

for category in categories:
    category_name = category.find("h3", class_="categories_title").text.strip()
    category_image = category.find("img")["src"].strip().replace("\n", "").replace("\t", "")
    subcategories = category.find("div", class_="categories_subs")
    subcategories_list = []

    for subcategory in subcategories.find_all("a"):
        subcategory_name = subcategory.text.strip()
        subcategory_link = subcategory["href"].strip()

        subcategories_list.append({
            "name": subcategory_name,
            "link": subcategory_link
        })

    categories_dict[category_name] = {
        "image": category_image,
        "subcategories": subcategories_list
    }

    categories_list.append(categories_dict)

# It should look like this
# categories_dict = {
#     category_name = {
#         "image": image,
#         "subcategories": subcategories_list
#     }
# }

# Follow the link of each subcategory and save the html file.
# Save them in a folder named after the categories_dict.keys()
# Make sure each subcategory is saved inside its parent key folder.

# Create a folder for categories

# os.mkdir("sklavenitis")

# # Loop through each category and create a folder for it
# for category in categories_dict:
#     category_folder = os.path.join("sklavenitis", category)
#     os.mkdir(category_folder)

#     # Loop through each subcategory and save the HTML file in the category folder
#     for subcategory in categories_dict[category]["subcategories"]:
#         filename = subcategory["name"] + ".html"
#         getPageNoAccept(URL + subcategory["link"], os.path.join(category_folder, filename))

# Everything is neatly saved in the categories folder.
# Now we can scrape the data from each subcategory and save it in each own JSON file.

# Test run with a single file
# Open the file and parse it with BeautifulSoup

doc = open('sklavenitis/Τροφές & Είδη για Κατοικίδια/Τροφές & Είδη για Σκύλους.html', encoding="utf-8")
soup = BeautifulSoup(doc, "html.parser")

# Find the products container
# Get every class id in the container named productList

products = soup.find("div", id="productList").find_all("div", class_="product")

print(len(products))

driver = webdriver.Chrome( executable_path=r"chromedriver.exe")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
#extra options
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver.get('https://www.sklavenitis.gr/trofes-eidi-gia-katoikidia/trofes-eidi-gia-skyloys/')

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
driver.close()

print(len(search))

print(categories_dict["Τροφές & Είδη για Κατοικίδια"])

driver.quit()