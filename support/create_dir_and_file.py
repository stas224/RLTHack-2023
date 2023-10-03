import csv
import datetime
import os


def get_date():
    today = datetime.date.today()
    format_date = today.strftime('%Y-%m-%d')
    return format_date


def create_data_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def create_data_file():
    folder_path = './data'
    create_data_folder(folder_path)

    date = get_date()
    file_path = f'{folder_path}/{date}.csv'

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['resource', 'category', 'vendor', 'name', 'price', 'description', 'region'])

    return file_path
