import sklavenitis

if __name__ == '__main__':
    sklavenitis.create_folder()
    sklavenitis.create_categories()
    sklavenitis.get_cookie_playwright()
    sklavenitis.send_and_save_requests()

print("Done!")