"""
    Этот скрипт собирает данные о компаниях с сайта rusprofile
    На вход подается два названия файла
    первый - csv-file, в котором записаны компании, которые нужно проверить
    второй - сsv-file, куда нужно записать данные

    Данные в таком формате:
        изначалньное название,
        полное название,
        ИНН,
        регион регистрации,
        надежность,
        кол-во хороших отзывов,
        кол-во плохих отзывов

    *Если proxy устрели, то их можно заменить в папке support
"""

import csv
import random
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium_stealth import stealth

BASE_URL = 'https://www.rusprofile.ru'
URL = 'https://www.rusprofile.ru/'


def click_link(driver, inn_):
    try:
        click_input = driver.find_element("class name", "input-holder")
        click_input.click()
    except Exception as e:
        print(e)
    else:
        try:
            text_input = driver.find_element("class name", "index-search-input")
            text_input.click()
            text_input.send_keys(inn_)
        except Exception as e:
            print(e)
        else:
            try:
                search = driver.find_element("class name", "search-btn")
                search.click()
            except Exception as e:
                print(e)
            else:
                return 0
    return 1


def choose_company(driver, soup):
    try:
        company_card = soup.find('div', attrs={'class': {"company-item__title"}})
        company_ = company_card.find('a').get('href')
        temp_url = f'{BASE_URL}{company_}'
        print(temp_url)
        driver.get(temp_url)

    except Exception as e:
        return 0
    else:
        return 1


def get_proxy():
    with open('../support/proxy_list.txt', 'r', encoding='UTF-8') as proxy_file:
        proxy_list = proxy_file.read().splitlines()

    return proxy_list


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    proxy_list = get_proxy()
    options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
    stealth(driver,
            languages=["en-US", "en"],
            useraget=UserAgent().random,
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


def get_data(vendors, file):
    driver = get_driver()
    print('ok')
    driver.get(URL)

    with open(vendors, 'r') as old, open(file, 'a', newline='') as new:
        reader = csv.reader(old, delimiter=';')
        writer = csv.writer(new, delimiter='@')
        writer.writerow(['company', 'company_full', 'inn', 'region', 'reliability', 'good', 'bad'])
        print(f"{'-' * 20}Start session{'-' * 20}")
        for ind, (trash, company, inn) in enumerate(reader, 1):

            if ind % 7 == 0:
                driver.close()
                driver.quit()
                driver = get_driver()
                driver.get(BASE_URL)

            if click_link(driver, inn):
                print('URL Error')
                continue
            source_page = driver.page_source
            soup = BeautifulSoup(source_page, "html.parser")

            if choose_company(driver, soup):
                source_page = driver.page_source
                soup = BeautifulSoup(source_page, "html.parser")
            try:
                region = soup.find('span', attrs={'itemprop': {"addressRegion"}}).text.strip()
                reliability = soup.find('a', attrs={'data-goal': {"reliability_button_ul"}}).text.strip()
                feedback = soup.find_all('div', attrs={'class': {"connexion-col__num"}})
                company_full = soup.find('h2',
                                         attrs={"class": {"company-name"}, "itemprop": {"legalName"}}).text.strip()
                good, bad = feedback[0].text, feedback[1].text
            except Exception as e:
                print("Data Error")
            else:
                writer.writerow([company, company_full, inn, region, reliability, good, bad])

            try:
                button = driver.find_element("class name", "head__logo")
                button.click()
            except Exception as e:
                print("Start page Error")

            time.sleep(5)
            company_full = region = reliability = good = bad = ''
            print(f"{'-' * 20}Company {ind} complete {'-' * 20}")


if __name__ == '__main__':
    file_vendors = input()
    new_file = input()
    get_data(file_vendors, new_file)
