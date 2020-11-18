# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv

import pandas as pd
import xlwt
import re
import cssutils
import json


df = pd.DataFrame

def save_table_to_excel(list_catalog_number = [], list_feauture = [], list_pruduct = [], list_price_discount = []):

    path = 'DKS.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    # Write your DataFrame to a file
    df.to_excel(writer, 'DKS')

    # Save the result
    writer.save()



def save_to_excel(ws, wb, list_catalog_number = [], list_feauture = [], list_price_discount = [], catalog_item_price =[], list_img =[], icur = 1):
    i = 0  # параметр, позволяющий перемещаться в ячейках по столбцам
    j = icur  # параметр, позволяющий перемещаться в ячейках по строкам


    for x in range(1,len(list_catalog_number)-1):
        st = str(list_catalog_number[x])
        ws.write(j, 0, st.split(':')[1])
        ws.write(j, 1, list_feauture[x])
        ws.write(j, 2, list_price_discount[x])
        st = str(catalog_item_price[x]).split('.')[0]
        st1 = str(st).split(' ')[0]
        # print("price = {}".format(st))
        st = str(int(st1)*1.2).split('.')[0]
        ws.write(j, 3, st)
        st = list_img[x]
        b = str(st)
        ws.write(j, 5, b[b.find('(') + 1: b.find(')')])
        b = str(st)
        # print("list img = {}".format(b))
        st = 'https://adventa.su' + b[b.find('(') + 1: b.find(')')]
        print(st)
        #Чтобы в тексте скобки не воспринимались как регулярные выражения нужно перед скобакми и слешами ставить \
        ws.write(j, 4, st)

        # ws.write(j, 5, re.findall(r'Серия(.*?)Номинальное выходное напряжение', st))
        # ws.write(j, 6, re.findall(r'Напряжение \(В\)(.*?)Ном. ток в фазе \(A\)', st))
        # ws.write(j, 7, re.findall(r'Ном. ток в фазе \(A\)(.*?)Производительность', st))
        # ws.write(j, 8, re.findall(r'Производительность \(не менее, м3\/ч\)(.*?)Габариты \(ш/в/г, мм\)', st))
        # ws.write(j, 9, re.findall(r'Номинальное выходное напряжение, В(.*$)', st))
#        ws.write(j, 7, list_feauture[x])

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
    # Создается объект BeautifulSoup.Данные передаются конструктору.Вторая опция
    # уточняет объект  парсинга.
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)


    #Каталожный номер получаем
    list_catalog_number = get_data(soup, 'div', "artikul1")
    print(list_catalog_number)

    #Общее описание
    list_feauture = get_data(soup, 'div', "name2")
    print(list_feauture)

    #Общие данные по продукту UL
    # list_pruduct = get_data(soup, 'ul', "catalog-item__feature")
    # print(list_pruduct)

    #Берем цену со скидкой - пробуем, похоже без авторизации не будет брать
    list_price_discount = get_data(soup, 'div', "price_title")
    print(list_price_discount)

    # list_ul= get_data(soup, 'div', "wrap-pagination")
    # print(list_ul)

    #Стоимость получаем
    catalog_item_price= get_data(soup, 'div', "price_value")
    print(catalog_item_price)

    # soup_img = BeautifulSoup(html, 'html.parser')
    # data_img = soup_img.find_all('div', {"class": "img-container__content"})
    # # data_img = get_data(soup_img, 'div', "catalog-item-top")
    # # print(data_img)
    # list_img = []
    # # div = soup_img.find('div', {"class": "catalog-item-top"})
    # for article in data_img:
    #     list_img.append(article.find('img').attrs['src'])

    # html = """<div class="image" style="background-image: url('/uploads/images/players/16113-1399107741.jpeg');" />"""
    # soup_img = BeautifulSoup(html, 'html.parser')
    div_style = soup.find_all('div', {'class':'img-container__content'})
    print(div_style)
    list_img = div_style

    # print("style=".format(div_style))
    # # div_style = soup_img.find_all('div', {"class": "img-container__content"})#['style']
    # style = cssutils.parseStyle(div_style)
    # print("style=".format(style))
    # url = style['background']
    # print("url=".format(url))
    #
    # # >> > url
    # # u'url(/uploads/images/players/16113-1399107741.jpeg)'
    # url = url.replace('url(', '').replace(')', '')  # or regex/split/find/slice etc.
    # print('url='.format(url));

    save_to_excel(ws, wb, list_catalog_number, list_feauture, list_price_discount, catalog_item_price, list_img,  icur)
    return len(list_catalog_number)


#dks data = get_link(get_html('https://www.tesli.com/catalog/ibp/istochniki-bespereboynogo-pitaniya/?display_type=tile&set_filter=Показать&arrFilter_P1_MIN=1970&arrFilter_P1_MAX=8292697&arrFilter_208_1955232490=DKC&1458992227='))
#data = get_link(get_html('https://www.tesli.com/catalog/ibp/istochniki-bespereboynogo-pitaniya/?sort=price&display_type=tile&0=&1=&set_filter=Показать&arrFilter_P1_MIN=1970&arrFilter_P1_MAX=8292697&arrFilter_208_1955232490=DKC&arrFilter_208_4171867725=EATON&arrFilter_208_1597891823=Schneider+Electric&1458992227='))
wb = xlwt.Workbook()
ws = wb.add_sheet('ПУШКИ', cell_overwrite_ok=True)
path = 'Adventa s7_1200.xlsx'
ws.write(0, 0, "Каталожный номер")
ws.write(0, 1, "Описание")
ws.write(0, 2, "Стоимость за")
ws.write(0, 3, "Цена c НДС, Евро")
ws.write(0, 4, "Адрес картинки")
ws.write(0, 5, "Адрес картинки относительный")
ws.write(0, 6, "Напряжение (В)")
ws.write(0, 7, "Ном. ток в фазе (A)")
ws.write(0, 8, "Производительность (не менее, м3/ч)")
ws.write(0, 9, "Номинальное выходное напряжение, В")

adr = 1
icuri = 1
# Тут прописываем нужный файл для парсинга с Адвенты. Приходится в firefox полностью
# открывать нужную страницу путем нажатия "Показать еще" и сохранять потом в файл и его парсить
##########################################################
f_o =open('Контроллеры SIMATIC S7-1500 ADVENTA.html', encoding="utf8")
# f_o =open('Микроконтроллеры SIMATIC S7-1200 ADVENTA.html', encoding="utf8")
# f_o = open('Логические модули LOGO! ADVENTA.html', encoding="utf8")
f_read= f_o.read()
# print(f_read)

get_link(ws, wb, f_read, icuri)
# get_link(ws, wb, get_html('https://www.tesli.com/catalog/nvo/promyshlennaya-avtomatizatsiya/bloki-pitaniya/?PAGEN_1='+str(adr)), icuri)
# while adr <= 6:
#     leni = get_link(ws, wb, get_html('https://www.tesli.com/catalog/nvo/promyshlennaya-avtomatizatsiya/bloki-pitaniya/?PAGEN_1='+str(adr)), icuri)
#     adr = adr + 1
#     icuri = icuri + leni
#     print('https://www.elcomspb.ru/retail/thermotechnics/heaters/?page='+str(adr))
