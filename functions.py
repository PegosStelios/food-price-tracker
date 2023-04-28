import os
import requests
import re
from unidecode import unidecode as ud

def get_categories_page(url, filename):
    try:
        if os.path.exists(filename):
            answer = input(f"The file '{filename}' already exists. Do you want to overwrite it? [y/n]: ")
            if answer.lower() != 'y':
                print("Using the existing file.")
                return
        response = requests.get(url)
        response.raise_for_status()  # raises an exception if the response is not OK
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the categories page: {e}")
        print("--- DEBUG INFORMATION ---")
        print(f"url:  {url}")
        print(f"filename:  {filename}")
        print("--- DEBUG INFORMATION ---")
        raise ValueError("get_categories_page() has crashed.")
    except Exception as e:
        print(f"An error occurred while checking the existence of file or overwriting it: {e}")
        print("--- DEBUG INFORMATION ---")
        print(f"filename: {filename}")
        print("--- DEBUG INFORMATION ---")
        raise ValueError("get_categories_page() has crashed.")



def removeNonAlphaNumeric(string, unidecode, replaceWithDash, replaceWithUnderscore, removeSlashes):
    """
    Removes all non-alphanumeric characters from a string, and replaces spaces with either a dash or underscore.
    Also, can optionally convert accented characters to their ASCII equivalent using unidecode.
    Returns the modified string.

    Args:
    string (str): The string to modify.
    unidecode (bool): Whether to convert accented characters to their ASCII equivalent using unidecode. Default is False.
    replaceWithDash (bool): Whether to replace spaces with a dash. If both replaceWithDash and replaceWithUnderscore are False, no replacement will be done. Default is False.
    replaceWithUnderscore (bool): Whether to replace spaces with an underscore. If both replaceWithDash and replaceWithUnderscore are False, no replacement will be done. Default is False.

    Returns:
    str: The modified string.

    Raises:
    ValueError: If string is None, empty, replaceWithDash and replaceWithUnderscore are both True, or if any of the arguments are None.
    """

    if string is None:
        print("String is None, exiting...")
        exit()

    if string == "":
        print("String is empty, exiting...")
        exit()

    if replaceWithDash is None:
        print("ReplaceWithDash is None, exiting...")
        exit()

    if replaceWithUnderscore is None:
        print("ReplaceWithUnderscore is None, exiting...")
        exit()

    if replaceWithDash and replaceWithUnderscore:
        print("ReplaceWithDash and replaceWithUnderscore are both True, exiting...")
        exit()

    if removeSlashes is None:
        print("RemoveSlashes is None, exiting...")
        exit()

    if removeSlashes:
        string = string.replace("/", "")

    if unidecode is None:
        print("Unidecode is None, exiting...")
        exit()

    if unidecode:
        string = ud(string)

    if replaceWithDash and not replaceWithUnderscore:
        string = re.sub(r'[^a-zA-Z0-9]+', '-', string)
        string = re.sub(r'\s+', '-', string)
        string = string.lower()

        return string

    if replaceWithUnderscore and not replaceWithDash:
        string = re.sub(r'[^a-zA-Z0-9]+', '_', string)
        string = re.sub(r'\s+', '_', string)
        string = string.lower()

        return string

    print("--- DEBUG INFORMATION ---")
    print(f"string:  string")
    print(f"unidecode:  unidecode")
    print(f"replaceWithDash:  replaceWithDash")
    print(f"replaceWithUnderscore:  replaceWithUnderscore")
    print("--- DEBUG INFORMATION ---")
    raise ValueError("removeNonAlphaNumeric() has crashed.")


if __name__ == "__main__":
    print("This is a module, not a script!")
