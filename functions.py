import os
import requests
import re
from unidecode import unidecode as ud


def getPage(url, filename, auto, accept):
    """
    Downloads the HTML content of a webpage and saves it to a file.

    Parameters:
    url (str): The URL of the webpage to download.
    filename (str): The name of the file to save the HTML content to.
    auto (bool): If True, automatically downloads the file if it does not exist.
    accept (bool): If True, prompts the user to download the file if it does not exist.

    Returns:
    None: The function does not return anything.

    Raises:
    HTTPError: If there is an error with the HTTP request.
    """

    # Check if filename and url are not None
    if filename is None:
        print("filename is None, exiting...")
        exit()

    if url is None:
        print("File does not exist, exiting...")
        exit()

    # If auto mode is enabled, download the file without prompting the user
    if auto and not accept and (auto or accept) is not None:
        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text

            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
        except requests.exceptions.HTTPError as e:
            print("Http Error:", e)
            exit()

    # If the file already exists, prompt the user to overwrite it or use the existing file
    elif os.path.exists(filename):
        match input("File already exists, do you want to overwrite it? (y/n): "):
            case "y":
                try:
                    try:
                        os.remove(filename)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                        exit()

                    response = requests.get(url)
                    response.raise_for_status()
                    html = response.text

                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(html)
                except requests.exceptions.HTTPError as e:
                    print("Http Error:", e)
                    exit()
            case "n":
                print("Using existing file...")
            case _:
                print("Invalid choice, exiting...")
                exit()

    # If accept mode is enabled, prompt the user to download the file
    elif accept and not auto and (auto or accept) is not None:
        match input("File does not exist, download? (y/n): "):
            case "y":
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    html = response.text

                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(html)
                except requests.exceptions.HTTPError as e:
                    print("Http Error:", e)
                    exit()
            case "n":
                print("Using existing file...")
            case _:
                print("Invalid choice, exiting...")
                exit()

    # If none of the above conditions are true, something went wrong
    else:
        print("--- DEBUG INFORMATION ---")
        print(f"url:  url")
        print(f"filename:  filename")
        print(f"auto:  auto")
        print(f"accept:  accept")
        print("--- DEBUG INFORMATION ---")
        raise ValueError("getPage() has crashed.")


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
