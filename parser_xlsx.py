# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv

import pandas as pd
import xlwt
import re
import cssutils
import json
import xlsxwriter



df = pd.DataFrame

def save_table_to_excel(list_catalog_number = [], list_feauture = [], list_pruduct = [], list_price_discount = []):

    path = 'DKS.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    # Write your DataFrame to a file
    df.to_excel(writer, 'DKS')

    # Save the result
    writer.save()



def save_to_excel(namefile, ws, list_catalog_number = [], list_feauture = [], list_price_discount = [], catalog_item_price =[], list_img =[], icur = 1):
    i = 0  # параметр, позволяющий перемещаться в ячейках по столбцам
    j = icur  # параметр, позволяющий перемещаться в ячейках по строкам

    # ws.write(0, 0, "Каталожный номер")
    # ws.write(0, 1, "Описание")
    # ws.write(0, 2, "Стоимость за")
    # ws.write(0, 3, "Цена c НДС, Евро")
    # ws.write(0, 4, "Адрес картинки")
    # ws.write(0, 5, "Адрес картинки относительный")
    # ws.write(0, 6, "Напряжение (В)")
    # ws.write(0, 7, "Ном. ток в фазе (A)")
    # ws.write(0, 8, "Производительность (не менее, м3/ч)")
    # ws.write(0, 9, "Номинальное выходное напряжение, В")

    catalog_number = []
    feauture = []
    price_discount = []
    item_price = []
    img =[]
    img_relation = []
    for x in range(0,len(list_catalog_number)):

        st = str(list_catalog_number[x])
        catalog_number.append(st.split(':')[1])

        feauture.append(list_feauture[x])

        price_discount.append(list_price_discount[x])

        st = str(catalog_item_price[x]).split('.')[0]
        st1 = str(st).split(' ')[0]
        # print("price = {}".format(st))
        st = str(int(st1)*1.2).split('.')[0]
        item_price.append(st)

        st = list_img[x]
        b = str(st)
        img_relation.append(b[b.find('(') + 1: b.find(')')])

        b = str(st)
        # print("list img = {}".format(b))
        st = 'https://adventa.su' + b[b.find('(') + 1: b.find(')')]
        print(st)
        #Чтобы в тексте скобки не воспринимались как регулярные выражения нужно перед скобакми и слешами ставить \
        img.append(st)
        j += 1

    df = pd.DataFrame({'Каталожный номер':catalog_number,
                      'Описание':feauture,
                      'Стоимость за':price_discount,
                      'Цена c НДС, Евро':item_price,
                      'Адрес картинки': img,
                      'Адрес картинки относительный': img_relation},
                      )

    # Create a workbook and add a worksheet.
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    name_xlsx = namefile.split('.')[0] + '.xlsx'
    writer = pd.ExcelWriter(name_xlsx, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    st1 = namefile.split('.')[0]
    if len(st1) > 31:  # xlsxwriter.exceptions.InvalidWorksheetName: Excel worksheet name 'Модули дискретных входов ADVENTA' must be <= 31 chars.
        st = namefile[0:30]
    else:
        st = namefile.split('.')[0]
    df.to_excel(writer, sheet_name=st)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

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

def get_link(namefile, wb, html, icur = 1):
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

    #Берем поле цена за какое количество. Два значение (Цена: по запросу , Цена без НДС за 1 шт.:)
    list_price_discount = get_data(soup, 'div', "price_title")
    print(list_price_discount)

    # list_ul= get_data(soup, 'div', "wrap-pagination")
    # print(list_ul)

    #Стоимость получаем
    catalog_item_price= get_data(soup, 'div', "price_value")
    print(catalog_item_price)
    print("catalog_item_price type = {}".format(catalog_item_price))

    # if(len(catalog_item_price) == 0)
    # catalog_item_price.insert(0,'0')
    for x in range(0, len(list_catalog_number)):
        print("list_price_discount[{}] = {}".format(x, list_price_discount[x]))
        print("list_catalog_number[{}] = {}".format(x, list_catalog_number[x]))
        st_list = str(list_price_discount[x])
        if st_list.find("по запросу") != -1:
            catalog_item_price.insert(x, '0')

        print("catalog_item_price[{}] = {}".format(x, catalog_item_price[x]))

    div_style = soup.find_all('div', {'class':'img-container__content'})
    print(div_style)
    list_img = div_style

    save_to_excel(namefile, wb, list_catalog_number, list_feauture, list_price_discount, catalog_item_price, list_img,  icur)
    return len(list_catalog_number)



namefile = 'Измерение температуры'
name_get_html = 'https://adventa.su/ru/stocklist/70334'

#0 - скачанный htmlfile, Если  namefile = 'Аналоговые входы ADVENTA.html' должен лежать в корне программы
# 1 - ссылка на сайт, то namefile = 'Аналоговые входы ADVENTA' присваивается название для excel
#и ниже прописывается путь к парсируемому сайту     get_link(namefile, wb, get_html('https://adventa.su/ru/stocklist/70274'), icuri)
flag_site_or_htmlfile = 1


# Create a workbook and add a worksheet.
# if len(namefile) > 30:#xlsxwriter.exceptions.InvalidWorksheetName: Excel worksheet name 'Модули дискретных входов ADVENTA' must be <= 31 chars.
#     name_xlsx = namefile[0:29]
# else:
name_xlsx = namefile.split('.')[0]+'.xlsx'
wb = xlsxwriter.Workbook(name_xlsx)

path = namefile

adr = 1
icuri = 1
# Тут прописываем нужный файл для парсинга с Адвенты. Приходится в firefox полностью
# открывать нужную страницу путем нажатия "Показать еще" и сохранять потом в файл и его парсить
##########################################################

#0 - скачанный htmlfile, Если  namefile = 'Аналоговые входы ADVENTA.html' должен лежать в корне программы
if not flag_site_or_htmlfile:
    # Чтение из сохраненного файла
    f_o =open(namefile, encoding="utf8")
    f_read= f_o.read()
    # print(f_read)
    get_link(namefile, wb, f_read, icuri)

# 1 - ссылка на сайт, то namefile = 'Аналоговые входы ADVENTA' присваивается название для excel
#и ниже прописывается путь к парсируемому сайту     get_link(namefile, wb, get_html('https://adventa.su/ru/stocklist/70274'), icuri)
else:
    get_link(namefile, wb, get_html(name_get_html), icuri)

# while adr <= 6:
#     leni = get_link(ws, wb, get_html('https://www.tesli.com/catalog/nvo/promyshlennaya-avtomatizatsiya/bloki-pitaniya/?PAGEN_1='+str(adr)), icuri)
#     adr = adr + 1
#     icuri = icuri + leni
#     print('https://www.elcomspb.ru/retail/thermotechnics/heaters/?page='+str(adr))
