import csv
import random
import re
import time

import requests
from bs4 import BeautifulSoup

resource = 'pulscen'

pattern_re = "[;\\n]"


def extract(field):
    return field.text.strip() if field else ''


def get_cards(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    cards = soup.find_all('li', attrs={'class': {"product-listing__item", "js-product-listing-item"}})
    return cards


def get_data(filename, categories):
    print(f'Start of parsing on {resource}')

    with open(filename, 'a', newline='', encoding='utf-8') as file:

        writer = csv.writer(file, delimiter=';')
        count_page = 26

        for category in categories:
            for num_page in range(1, count_page):
                time.sleep(3)
                URL = f"https://msk.pulscen.ru/search/price?q={category}&page={num_page}"
                product_cards = get_cards(URL)

                while not len(product_cards):
                    sleep = random.randint(60, 100)
                    print(f'I am sleeping for {sleep} seconds')
                    time.sleep(sleep)
                    product_cards = get_cards(URL)

                print(f'take page {num_page} for {categories[category]}')

                for card in product_cards:
                    vendor = card.get('data-company-name')
                    vendor = re.sub(pattern_re, ' ', vendor)

                    region = extract(card.find('div', attrs={'class': {"product-listing__company-info-region"}}))
                    region = re.sub(pattern_re, ' ', region)

                    name = extract(card.find('span', attrs={"class": {"product-listing__product-name"}}))
                    name = re.sub(pattern_re, ' ', name)

                    price = card.get('data-price')
                    price = re.sub(pattern_re, ' ', price)

                    description = extract(card.find('div', attrs={'class': {'product-listing__product-description'}}))
                    description = re.sub(pattern_re, ' ', description)

                    writer.writerow([resource, category, vendor, name, price, description, region])

            print(f'{"-" * 20} {category} is complete {"-" * 20}')
            time.sleep(random.randint(30, 100))
