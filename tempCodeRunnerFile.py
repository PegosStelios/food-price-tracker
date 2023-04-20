# Find all dropdown menus with class name 'categories_subs'
dropdown_menus = soup.find_all('div', {'class': 'categories_subs'})

# Loop through each dropdown menu and extract the data
for dropdown_menu in dropdown_menus:
    menu_items = dropdown_menu.find_all('a')
    for item in menu_items:
        print(item.text.strip())