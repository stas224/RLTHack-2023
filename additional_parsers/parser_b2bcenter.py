"""
    Этот скрипт собирает поставщиков с сайта b2bcenter

    На вход подается:
        категория,
        количество компаний в данной категории,
        код категории в ссылке на нее,
        файл, куда нужно записать данные

    Данные записываются в csv-file в таком виде:
        категория,
        поставщик,
        регион
"""

import csv
import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    options.add_argument("--headless")

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


def get_data():
    with open(filename, 'a', newline='', encoding='UTF-8') as new:
        writer = csv.writer(new, delimiter=';')
        driver = get_driver()
        print('driver start')
        writer.writerow(['category', 'company', 'region'])
        for page in range(0, item_count, 20):
            URL = f'https://www.b2b-center.ru/firms/?target=2&okpd2%5B0%5D={ind}&from={0}'
            driver.get(URL)
            source_page = driver.page_source
            soup = BeautifulSoup(source_page, "html.parser")
            vendor_card = soup.find('tbody').find_all('tr')

            for card in vendor_card:
                card = card.find_all('td')
                name = card[0].text.strip()
                region = card[1].text.strip()
                writer.writerow([category, name, region])

            time.sleep(random.randint(5, 15))
            print('nice')


if __name__ == '__main__':

    category = input()
    item_count = int(input())
    ind = int(input())
    filename = input()

    get_data()
