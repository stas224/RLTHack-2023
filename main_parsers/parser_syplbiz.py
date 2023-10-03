import csv
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth

BASE_URL = 'https://supl.biz/'
resource = 'suplbiz'
region = ''

pattern_re = "[;\\n]"


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver_ = webdriver.Chrome(options=options)

    stealth(driver_,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver_


def get_data(filename, categories):
    print(f'Start of parsing on {resource}')

    driver = get_driver()
    driver.get(BASE_URL)
    time.sleep(5)

    with open(filename, 'a', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=';')

        for index, category in enumerate(categories, 1):
            url_category = '%20'.join(category.split())
            URL = f'https://supl.biz/proposals/search/?query={url_category}'
            driver.get(URL)

            try:
                button = driver.find_element("class name", "c_eiWTRONj")
                button.click()
            except Exception as e:
                print(f'No banner on {resource}')

            source_page = driver.page_source
            soup = BeautifulSoup(source_page, "html.parser")
            product_cards = soup.find_all('div', attrs={'class': {'a_0C-R-igw'}})

            print(f'take page for {categories[category]}')
            for card in product_cards:
                try:
                    name = card.find('h3', attrs={'itemprop': {'name'}}).text.strip()
                    name = re.sub(pattern_re, ' ', name)
                except Exception as e:
                    print('Name err')

                try:
                    description = card.find('span', attrs={'itemprop': {'description'}}).text.strip()
                    description = re.sub(pattern_re, ' ', description)
                except Exception as e:
                    print('Description err')

                try:
                    price = card.find('meta', attrs={'itemprop': {'price'}}).get('content')
                    price = re.sub(pattern_re, ' ', price)
                except Exception as e:
                    print('Price err')

                try:
                    vendor = card.find('a', attrs={'class': {'c_w08v1ylG a_1f5wjnCB'}}).text.strip()
                    vendor = re.sub(pattern_re, ' ', vendor)
                except:
                    print('Err vendor')

                writer.writerow([resource, category, vendor, name, price, description, region])
                name = description = price = vendor = ''

            print(f'{"-" * 20} {category} is complete {"-" * 20}')
            time.sleep(5)

    driver.close()
    driver.quit()
