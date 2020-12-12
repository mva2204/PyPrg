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
from requests_html import HTMLSession


df = pd.DataFrame


class Tesli_parser(object):


    def __init__(self):
        # self.stuct_parser = stuct_parser #Планирую сюда все исходные данные списком
        self.df = pd.DataFrame#Для работы и сохранения в xlsx
        self.df_app = pd.DataFrame#Для работы и сохранения в xlsx
        self.mainsite = ''
        self.name_save_file = ''

    def get_list_pagination(self, html_src, mainsite, name_save_file = 'default', count_pagination_all=1):
        self.mainsite = mainsite
        # Создается объект BeautifulSoup.Данные передаются конструктору.Вторая опция
        # уточняет объект  парсинга.
        list_href = []
        for x in range(1, count_pagination_all):
            list_href.append(html_src + str(x))
            print('Page={}'.format(html_src + str(x)))

        print(list_href)

        catalog_number = []
        feauture = []
        item_price = []
        img =[]
        img_relation = []
        #Каталожный номер получаем
        self.df = pd.DataFrame({'Каталожный номер': catalog_number,
                           'Описание': feauture,
                           'Цена, Руб': item_price,
                           'Адрес картинки': img,
                           'Адрес картинки относительный': img_relation},
                          )
        for x in range(0, len(list_href)):
            self.parse_html(name_save_file, list_href[x])
            print("self.df={}".format(self.df))

        # Create a workbook and add a worksheet.
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        self.name_save_file = name_save_file
        name_xlsx = './pareser/' + self.name_save_file + '.xlsx'
        writer = pd.ExcelWriter(name_xlsx, engine='xlsxwriter')

        self.df.to_excel(writer, self.name_save_file)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def parse_html(self, namefile, html):

        # Create a workbook and add a worksheet.
        # if len(namefile) > 30:#xlsxwriter.exceptions.InvalidWorksheetName: Excel worksheet name 'Модули дискретных входов ADVENTA' must be <= 31 chars.
        #     name_xlsx = namefile[0:29]
        # else:
        name_xlsx = namefile.split('.')[0] + '.xlsx'
        wb = xlsxwriter.Workbook(name_xlsx)

        path = namefile

        self.get_link(namefile, wb, self.get_html(html))


    def get_data(self, soup, tag, atrtag):
        convert = soup.find_all(tag, {"class": atrtag})
        list_tag_val = []
    #    data = []
        for entry in convert:
            list_tag_val.append(entry.get_text(strip=True))
    #        data = {'Описание': entry.get_text()}
        return list_tag_val#, data

    def get_link(self, namefile, wb, html):
        # Создается объект BeautifulSoup.Данные передаются конструктору.Вторая опция
        # уточняет объект  парсинга.
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)

        #Каталожный номер получаем
        list_catalog_number = self.get_data(soup, 'div', "catalog-item__code")
        print(list_catalog_number)

        #Общее описание
        list_feauture = self.get_data(soup, 'div', "catalog-item__title")
        print(list_feauture)

        #Общие данные по продукту UL
        list_pruduct = self.get_data(soup, 'ul', "catalog-item__feature")
        print(list_pruduct)

        #Стоимость получаем
        catalog_item_price= self.get_data(soup, 'span', "catalog-item-price__val")
        print(catalog_item_price)
        print("catalog_item_price type = {}".format(catalog_item_price))

        soup_img = BeautifulSoup(html, 'html.parser')
        data_img = soup_img.find_all('a', {"class": "catalog-item__img js-product-link"})
        list_img = []
        for article in data_img:
            list_img.append(article.find('img').attrs['src'])

        self.save_to_excel(namefile, wb, list_catalog_number, list_feauture, list_pruduct,  catalog_item_price, list_img)

    def save_to_excel(self, namefile, ws, list_catalog_number = [], list_feauture = [], list_pruduct= [], catalog_item_price =[], list_img =[]):

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
        item_price = []
        img =[]
        img_relation = []
        for x in range(0,len(list_catalog_number)):

            st = str(list_catalog_number[x]).split('KEAZ')[-1]
            catalog_number.append(st)

            feauture.append(list_feauture[x])

            st = str(catalog_item_price[x]).split(',')[0]
            # st1 = str(st).split(' ')[0]
            # # print("price = {}".format(st))
            # st = str(int(st1)*1.2).split('.')[0]
            item_price.append(st)

            st = list_img[x]
            img_relation.append(st)

            b = str(st)
            # print("list img = {}".format(b))
            st = self.mainsite + st
            print(st)
            #Чтобы в тексте скобки не воспринимались как регулярные выражения нужно перед скобакми и слешами ставить \
            img.append(st)


        self.df_app = pd.DataFrame({'Каталожный номер':catalog_number,
                          'Описание':feauture,
                          'Цена, Руб':item_price,
                          'Адрес картинки': img,
                          'Адрес картинки относительный': img_relation},
                          )
        res = self.df.append(self.df_app)
        self.df = res
        print("df____ = {}".format(self.df))
        print("df_app___ = {}".format(self.df_app))


    def get_html(self, url):
        r = requests.get(url)    # Получим метод Response
        r.encoding = 'utf8'
        return r.text   # Вернем данные объекта text

namefile = 'Модули инверторов, SafeMC (двухосевые модули) ADVENTA.html'#Если парсим скачанный HTML файл в корне программы
name_get_html = 'https://www.tesli.com/search/?q=КЭАЗ&PAGEN_1='

# ВНИМАНИЕ!!!!
# 0 - скачанный htmlfile, Если  namefile = 'Аналоговые входы ADVENTA.html' должен лежать в корне программы
# 1 - ссылка на сайт, то namefile = 'Аналоговые входы ADVENTA' присваивается название для excel
# и ниже прописывается путь к парсируемому сайту     get_link(namefile, wb, get_html('https://adventa.su/ru/stocklist/70274'), icuri)
flag_site_or_htmlfile = 1
if flag_site_or_htmlfile:
    #Получаем весь список ссылок со страницы по div с class
    # get_list_href(flag_site_or_htmlfile, get_html(name_get_html), 'https://adventa.su', div_class='cablink')
    tesli_parser = Tesli_parser()
    tesli_parser.get_list_pagination(name_get_html, 'https://www.tesli.com', 'КЭАЗ', 1112)
else:
    #Если работаем только с одной страницей - не проверял
    tesli_parser = Tesli_parser()
    tesli_parser.parse_html(namefile, name_get_html, flag_site_or_htmlfile)



