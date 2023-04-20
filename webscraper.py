import os
import requests
from bs4 import BeautifulSoup

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

getPage()

# Find every categories_title in the file using BeautifulSoup.
doc = open('sklavenitis-katigories.html', encoding="utf-8")
soup = BeautifulSoup(doc, "html.parser")
categories = soup.find_all("div", class_="categories_item")


# Loop through each category and print the category name, image and subcategories.
# Each category should be its own dictionary with the following keys: name, image, subcategories. (Use the name of the category as the key.)
# The subcategories should be a list of dictionaries with the following keys: name, link.

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

#print(categories_dict)
print(categories_dict["Είδη Αρτοζαχαροπλαστείου"])