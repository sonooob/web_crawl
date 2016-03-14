#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017) #连接mongodb
zufang = client['zufang'] #创建数据库
sheet_tab = zufang['sheet_tab2'] #创建一个sheet

urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,4)]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Cookie':'abtest_ABTest4SearchDate=b; OZ_1U_2282=vid=v6e6c2af4e4ed8.0&ctime=1457964225&ltime=1457964222; OZ_1Y_2282=erefer=-&eurl=http%3A//bj.xiaozhu.com/search-duanzufang-p1-0&etime=1457963695&ctime=1457964225&ltime=1457964222&compid=2282; __utma=29082403.655236123.1457963696.1457963696.1457963696.1; __utmb=29082403.6.10.1457963696; __utmc=29082403; __utmz=29082403.1457963696.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
}

def get_info(url):
    wb_data = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('div.result_intro > a')
    prices =  soup.select('span.result_price > i')
    for title,price in zip(titles,prices):
        data = {
            'title':title.get_text(),
            'price':int(price.get_text())
        }
        sheet_tab.insert_one(data)

for url in urls:
   get_info(url)

# $lt/$lte/$gt/$gte/$ne，依次等价于</<=/>/>=/!=。（l表示less g表示greater e表示equal n表示not  ）
for item in sheet_tab.find({'price':{'$gt':500}}):
    print(item)




