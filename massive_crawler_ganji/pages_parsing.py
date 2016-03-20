#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganjin']
url_list = ganji['url_list']
item_info = ganji['item_info']

header = {
    'Cookie' :'statistics_clientid=me; citydomain=bj; ganji_uuid=9257642197179156333250; ganji_xuuid=2ed4f604-c2da-478e-d2e5-996fe26960f9.1458365636931; GANJISESSID=a9f7c34780cd8db481c8b40ee280f558; sscode=HgEWH11vguOqFw2QHgb1BZaD; GanjiUserName=%23sina_652044638; GanjiUserInfo=%7B%22user_id%22%3A652044638%2C%22email%22%3A%22%22%2C%22username%22%3A%22%23sina_652044638%22%2C%22user_name%22%3A%22%23sina_652044638%22%2C%22nickname%22%3A%22%5Cu9ed1%5Cu4eba%5Cu4e30hello%22%7D; bizs=%5B%5D; supercookie=AwHlZQD0AwZ4WTR3BGLmAmuwMJIxA2ZjAJRjAGL0LGtlBQqxATMxLmxkMJEvLJD1AGL%3D; t3=3; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22api.t.sina.com.cn%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22other_api.t.sina.com.cn%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A48836813392%7D; __utma=32156897.1370301295.1458365637.1458365637.1458365637.1; __utmb=32156897.46.10.1458365637; __utmc=32156897; __utmz=32156897.1458365637.1.1.utmcsr=study.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/course/courseLearn.htm',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'

}
# 在最左边是在python 中对象的名称，后面的是在数据库中的名称
# spider 1
def get_links_from(channel, pages):
    #ul.pagelink clearfix没有这个就终止
    list_view = '{}o{}/'.format(channel,str(pages))
    wb_data = requests.get(list_view,headers=header)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('ul', 'pageLink clearfix'):
        for link in soup.select('li.js-item > a'):
            item_link = link.get('href')
            if 'bj.ganji.com' in item_link.split('/'):
                url_list.insert_one({'url': item_link})
                print(item_link)
                #return urls
    else:
        # It's the last page !
        pass

#get_links_from('http://bj.ganji.com/jiaju/', 200)
#spider 2
def get_item_info(url):
    wb_data = requests.get(url, headers=header)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title = soup.select('h1.title-name')[0].get_text() if soup.select('h1.title-name') else None
    price = soup.select('.f22.fc-orange.f-type')[0].text if  soup.select('.f22.fc-orange.f-type') else None
    date = soup.select('i.pr-5')[0].text.strip().split(u'\xa0')[0] if soup.select('i.pr-5') else None
    cate = soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a')[0].text if soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a') else None
    areas = soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a ')
    area_t = []
    if soup.select('#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a '):
        for area in areas:
            area_t.append(area.text)#将多个区域标签放入一个List里
    quality = soup.select('ul.second-det-infor.clearfix > li')[0].get_text()[16:].strip() if soup.select('ul.second-det-infor.clearfix > li') else None

    item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area_t, 'cate': cate, 'quality': quality, 'url': url})
    print({'title': title, 'price': price, 'date': date, 'cate': cate, 'area': area_t, 'quality': quality})

#get_item_info('http://bj.ganji.com/jiaju/1890423960x.htm')

