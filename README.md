# Food Price Tracker

This is a web scraper written in Python that scrapes multiple grocery sites such as Sklavenitis to gather information about categories, subcategories, and their products. The scraper saves the responses in HTML files and puts them in a folder named `sklavenitis/responses`.

**It's still a work in progress.
It currently only scrapes the Sklavenitis site.**

## Installation

1. Clone the repository
```
git clone https://github.com/PegosStelios/food-price-tracker.git
```
2. Install the required packages
```
pip install -r requirements.txt
```
3. Run the scraper
```
python main.py
```

## Usage

When you run the scraper, it will create a folder named `sklavenitis` if it does not already exist. It will download an HTML file named `sklavenitis-katigories.html` that contains all the categories and subcategories of the shop. It will then scrape the data and save each response in an HTML file named `response{i}.html` in a folder named `responses`.

## Contact

If you have any questions or suggestions, feel free to contact me.