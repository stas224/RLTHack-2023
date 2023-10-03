"""
    Этот скрипт добавляет колонку с ИНН, для тех компаний у кого он нашелся
"""


import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth

resource = 'spark_interfax'


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


def get_inn(vendor, driver):
    URL = f'https://spark-interfax.ru/search?Query={vendor}'
    driver.get(URL)
    source_page = driver.page_source
    soup = BeautifulSoup(source_page, "html.parser")
    vendor_card = soup.find('div', attrs={'class': {"code"}})
    inn = ''
    if vendor_card:
        spans = vendor_card.find_all('span')
        inn = spans[1].text.strip() if spans else ''
    return inn


def get_data(filename):
    print(f'Start parsing on {resource}')

    driver = get_driver()

    df = pd.read_csv(filename, sep=';')
    df['inn'] = df['vendor'].apply(lambda x: str(get_inn(x, driver)))
    df.to_csv(filename, index=False, sep=';')

    print('Parsing completion')
