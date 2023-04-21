import os
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
#
# # Loop through each category and create a folder for it
# for category in categories_dict:
#     category_folder = os.path.join("categories", category)
#     os.mkdir(category_folder)
#
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

browser = webdriver.Chrome( executable_path=r"chromedriver.exe")
browser.get('https://www.sklavenitis.gr/trofes-eidi-gia-katoikidia/trofes-eidi-gia-skyloys/')

products = browser.find_elements_by_class_name("product")

for product in products:
    name = product.find_element_by_xpath('//*[@id="productList"]/div/section/div[1]/div[2]/article/h4/a')



browser.quit()