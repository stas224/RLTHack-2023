"""
    Этот скрипт собирает данные о поставщиках и их товарах с сайтов b2btrade.ru, pulscen.ru и
    sypl.biz в csv-file по категориям из файла ./support/categories.json и записывает их в папку
    ./data
"""

import json

from main_parsers.parser_b2btrade import get_data as b2btrade_data
from main_parsers.parser_pulscen import get_data as pulscen_data
from main_parsers.parser_spark_interfax import get_data as add_inn
from main_parsers.parser_syplbiz import get_data as syplbiz_data
from support.create_dir_and_file import create_data_file as create_csv


def prepare():
    filename = create_csv()
    with open('support/categories.json', 'r', encoding='UTF-8') as f:
        categories = json.load(f)

    return filename, categories


def main():
    filename, categories = prepare()

    pulscen_data(filename, categories)
    b2btrade_data(filename, categories)
    syplbiz_data(filename, categories)
    add_inn(filename)


if __name__ == '__main__':
    main()
