import csv

import requests
from bs4 import BeautifulSoup

resource = 'B2B_trade'
description = ''
region = ''


def define_page(s):
    p_buttons = s.find_all('button', class_='MuiPaginationItem-page')
    p_number = 1
    if len(p_buttons):
        p_number = max([int(button.text.strip()) for button in p_buttons])
    return p_number


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html.parser")


def get_data(filename, categories):

    print(f'Start of parsing on {resource}')

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for category in categories:
            URL = f"https://b2b.trade/ru/search?search={category}&pageSize=120&productsPage=1"
            soup = get_soup(URL)
            page_number = define_page(soup)

            for num_page in range(1, page_number + 1):

                if num_page != 1:
                    URL = f"https://b2b.trade/ru/search?search={category}&pageSize=120&productsPage={num_page}"
                    soup = get_soup(URL)

                product_cards = soup.find_all('article')

                print(f'take page {num_page} for {categories[category]}')

                for card in product_cards:
                    name = card.find('span', itemprop='name')
                    name = name.text.strip() if name else ''

                    price = card.find('p', itemprop='price')
                    price = price.text.strip() if price else ''

                    vendor = card.find('a', itemprop='brand')
                    vendor = vendor.text.strip() if vendor else ''

                    writer.writerow([resource, category, vendor, name, price, description, region])

            print(f'{"-" * 20} {category} is complete {"-" * 20}')
