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
categories = soup.find_all("h3", class_="categories_title")

# Add all the categories to a list purging the the spaces.
categories_list = []
for category in categories:
    categories_list.append(category.text.strip())

# Make a dictionary with the categories as keys and empty lists as values.
categories_dict = {}
for category in categories_list:
    categories_dict[category] = []

# Find all dropdown menus with class name 'categories_subs'
dropdown_menus = soup.find_all('div', {'class': 'categories_subs'})

# Loop through each dropdown menu and extract the data
for dropdown_menu in dropdown_menus:
    menu_items = dropdown_menu.find_all('a')
    for item in menu_items:
        print(item.text.strip())


# The code above scrapes all the categories items from the website.
# Each time we move to a new category (we can tell we moved since each category has a unique image),
# save all it's items to a dictionary with the categories_list values as keys.