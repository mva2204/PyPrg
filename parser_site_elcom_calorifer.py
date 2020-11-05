# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from lxml import etree

import pandas as pd
import xlwt
import re

df = pd.DataFrame

def save_table_to_excel(list_catalog_number = [], list_feauture = [], list_pruduct = [], list_price_discount = []):

    path = 'DKS.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    # Write your DataFrame to a file
    df.to_excel(writer, 'DKS')

    # Save the result
    writer.save()



def save_to_excel(ws, wb, list_catalog_number = [], list_feauture = [], list_pruduct = [], list_price_discount = [], catalog_item_price =[], list_img =[], icur = 1):
    i = 0  # параметр, позволяющий перемещаться в ячейках по столбцам
    j = icur  # параметр, позволяющий перемещаться в ячейках по строкам


    for x in range(1,len(list_catalog_number)):
        ws.write(j, 0, list_catalog_number[x])
        ws.write(j, 1, list_feauture[x])
        st = list_feauture[x]
        #Чтобы в тексте скобки не воспринимались как регулярные выражения нужно перед скобакми и слешами ставить \
        ws.write(j, 4, re.findall(r'Источник тепла(.*?)Тепл. мощность \(кВт\)', st))
        ws.write(j, 5, re.findall(r'Тепл. мощность \(кВт\)(.*?)Напряжение \(В\)', st))
        ws.write(j, 6, re.findall(r'Напряжение \(В\)(.*?)Ном. ток в фазе \(A\)', st))
        ws.write(j, 7, re.findall(r'Ном. ток в фазе \(A\)(.*?)Производительность', st))
        ws.write(j, 8, re.findall(r'Производительность \(не менее, м3\/ч\)(.*?)Габариты \(ш/в/г, мм\)', st))
        ws.write(j, 9, re.findall(r'Габариты \(ш/в/г, мм\)(.*$)', st))
#        ws.write(j, 7, list_feauture[x])
        ws.write(j, 2, catalog_item_price[x])
        ws.write(j, 3, list_img[x])
        j += 1
    # ws.write(0, 0, "Каталожный номер")
    # ws.write(0, 1, "Описание")
    # ws.write(0, 2, "Цена каталог руб")
    # ws.write(0, 3, "Картинка")
    # ws.write(0, 4, "Источник тепла")
    # ws.write(0, 5, "Тепл. мощность (кВт)")
    # ws.write(0, 6, "Напряжение (В)")
    # ws.write(0, 7, "Ном. ток в фазе (A)")
    # ws.write(0, 8, "Производительность (не менее, м3/ч)")
    # ws.write(0, 9, "Габариты (ш/в/г, мм)")

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

def get_link(ws, wb, html, icur = 1):
    soup = BeautifulSoup(html, 'lxml')

    list_catalog_number = get_data(soup, 'div', "caption")
    print(list_catalog_number)

    list_feauture = get_data(soup, 'div', "attrs-block")
    print(list_feauture)

    list_pruduct = get_data(soup, 'div', "catalog-item__title")
    print(list_pruduct)


    list_price_discount = get_data(soup, 'span', "catalog-item-price catalog-item-price_personal")
    print(list_price_discount)

    list_ul= get_data(soup, 'div', "wrap-pagination")
    print(list_ul)

    catalog_item_price= get_data(soup, 'div', "price")
    print(catalog_item_price)

    soup_img = BeautifulSoup(html, 'html.parser')
    data_img = soup_img.find_all('div', {"class": "image"})
    # data_img = get_data(soup_img, 'div', "catalog-item-top")
    # print(data_img)
    list_img = []
    # div = soup_img.find('div', {"class": "catalog-item-top"})
    for article in data_img:
        list_img.append(article.find('img').attrs['src'])

    # for article in articles:
    #     img_src = article.find('div', class_='o-rating_thumb c-white').img['data-original']
    #     headline = article.h2.text.strip()
    #     summary = article.find('p', class_='mt-15@m+ t-d5@m- t-d5@tp+ c-gray-3').text

    # images = soup.findAll('img')
    # print(images)

    # for i in range(0,len(list_catalog_number)):
    #     data_all = {'Каталожный номер': list_catalog_number[i],
    #             'Свойства': list_feauture[i],
    #             'Описание': list_pruduct[i],
    #             'Скидка': list_price_discount[i]
    #             }
    #     csv_read(data_all)
#    save_table_to_excel(list_catalog_number, list_feauture, list_pruduct, list_price_discount)
    save_to_excel(ws, wb, list_catalog_number, list_feauture, list_pruduct, list_price_discount,catalog_item_price, list_img,  icur)
    return len(list_catalog_number)


#dks data = get_link(get_html('https://www.tesli.com/catalog/ibp/istochniki-bespereboynogo-pitaniya/?display_type=tile&set_filter=Показать&arrFilter_P1_MIN=1970&arrFilter_P1_MAX=8292697&arrFilter_208_1955232490=DKC&1458992227='))
#data = get_link(get_html('https://www.tesli.com/catalog/ibp/istochniki-bespereboynogo-pitaniya/?sort=price&display_type=tile&0=&1=&set_filter=Показать&arrFilter_P1_MIN=1970&arrFilter_P1_MAX=8292697&arrFilter_208_1955232490=DKC&arrFilter_208_4171867725=EATON&arrFilter_208_1597891823=Schneider+Electric&1458992227='))
wb = xlwt.Workbook()
ws = wb.add_sheet('ПУШКИ', cell_overwrite_ok=True)
path = 'Elcom pushki.xlsx'
ws.write(0, 0, "Каталожный номер")
ws.write(0, 1, "Описание")
ws.write(0, 2, "Цена каталог руб")
ws.write(0, 3, "Картинка")
ws.write(0, 4, "Источник тепла")
ws.write(0, 5, "Тепл. мощность (кВт)")
ws.write(0, 6, "Напряжение (В)")
ws.write(0, 7, "Ном. ток в фазе (A)")
ws.write(0, 8, "Производительность (не менее, м3/ч)")
ws.write(0, 9, "Габариты (ш/в/г, мм)")

adr = 1
icuri = 1
while adr <= 14:
    leni = get_link(ws, wb, get_html('https://www.elcomspb.ru/retail/thermotechnics/heaters/?page='+str(adr)), icuri)
    adr = adr + 1
    icuri = icuri + leni
    print('https://www.elcomspb.ru/retail/thermotechnics/heaters/?page='+str(adr))
