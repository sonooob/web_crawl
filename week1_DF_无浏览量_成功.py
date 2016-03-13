#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time

url = 'http://bj.58.com/pbdn/0/'

def get_urls(url):
    wb_data= requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('#infolist > table > tr > td.img > a')
    urls = []
    for title in titles:
        link = title.get('href')
        name = title.img.get('alt')
        if name != u'转转':
            urls.append(link)
    return urls

def get_detail():
    urls = get_urls(url)
    for link in urls:
        wb_data= requests.get(link)
        time.sleep(3)
        soup = BeautifulSoup(wb_data.text,'lxml')
        content = {
            'category':soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a')[0].get_text(),
            'title':soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1')[0].get_text(),
            'time':soup.select('#index_show > ul.mtit_con_left.fl > li.time')[0].get_text(),
            'price':soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span')[0].get_text(),
            'quality':soup.select('#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(2) > div.su_tit')[0].get_text()
        }
        print(content)

get_detail()







#jingzhun > tbody > tr:nth-child(1) > td.img > a > img
#infolist > table:nth-child(5) > tbody > tr:nth-child(1) > td.img > a > img
#infolist > table:nth-child(26) > tbody > tr:nth-child(1) > td.img > a > img
