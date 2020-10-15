# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from lxml import etree

import pandas as pd
import xlwt


def save_table_to_excel(list_catalog_number = [], list_feauture = [], list_pruduct = [], list_price_discount = []):
    # Specify a writer
    df = pd.DataFrame
#    df['list_catalog_number'] = False
#    df['list_feauture'] = False
#    df['list_pruduct'] = False
#    df['list_price_discount'] = False
    for i in range(0, len(list_catalog_number)):
        df.iat[i, 'list_catalog_number'] = list_catalog_number[i]
        df.iat[i, 1] = list_feauture[i]
        df.iat[i, 2] = list_pruduct[i]
        df.iat[i, 3] = list_price_discount[i]
#    model = PandasModel(df)
    path = 'DKS.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    # Write your DataFrame to a file
    df.to_excel(writer, 'DKS')

    # Save the result
    writer.save()



def save_to_excel(list_catalog_number = [], list_feauture = [], list_pruduct = [], list_price_discount = []):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('ДКС')
    path = 'DKS.xlsx'
    i = 0  # параметр, позволяющий перемещаться в ячейках по столбцам
    j = 0  # параметр, позволяющий перемещаться в ячейках по строкам

    for x in range(0,len(list_catalog_number)):
        ws.write(j, 0, list_catalog_number[x])
        ws.write(j, 1, list_feauture[x])
        ws.write(j, 2, list_pruduct[x])
        ws.write(j, 3, list_price_discount[x])
        j += 1

    wb.save(path)

def get_html(url):
    r = requests.get(url)    # Получим метод Response
    r.encoding = 'utf8'
    return r.text   # Вернем данные объекта text


def csv_read(data):
    with open("data.csv", 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((data['Каталожный номер'], data['Свойства'], data['Описание'], data['Скидка']))

def get_data(soup, tag, atrtag):
    convert = soup.find_all(tag, {"class": atrtag})
    list_tag_val = []
#    data = []
    for entry in convert:
        list_tag_val.append(entry.get_text(strip=True))
#        data = {'Описание': entry.get_text()}
    return list_tag_val#, data

def get_link(html):
    soup = BeautifulSoup(html, 'lxml')
#    print (soup)
    try:
#        head = soup.find('div', id='catalog-item__code').find_all('a', class_="js-product-link")
#        head = soup.find_all('a', class_="js-product-link")
        catalog_grid_item = soup.find_all('div', class_="catalog-grid-item")
#        print(catalog_grid_item)
    except AttributeError:
        pass

#    convert = soup.find_all('div', {"class":"catalog-item__code"})
    list_catalog_number = get_data(soup, 'div', "catalog-item__code")
    print(list_catalog_number)

    list_feauture = get_data(soup, 'ul', "catalog-item__feature")
    print(list_feauture)

    list_pruduct = get_data(soup, 'a', "js-product-link")
    print(list_pruduct)

    list_price_discount = get_data(soup, 'span', "catalog-item-price__val")
    print(list_price_discount)

    for i in range(0,len(list_catalog_number)):
        data_all = {'Каталожный номер': list_catalog_number[i],
                'Свойства': list_feauture[i],
                'Описание': list_pruduct[i],
                'Скидка': list_price_discount[i]
                }
        csv_read(data_all)
#    save_table_to_excel(list_catalog_number, list_feauture, list_pruduct, list_price_discount)
    save_to_excel(list_catalog_number, list_feauture, list_pruduct, list_price_discount)



data = get_link(get_html('https://www.tesli.com/catalog/ibp/istochniki-bespereboynogo-pitaniya/?display_type=tile&set_filter=Показать&arrFilter_P1_MIN=1970&arrFilter_P1_MAX=8292697&arrFilter_208_1955232490=DKC&1458992227='))
