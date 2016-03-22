#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

client = pymongo.MongoClient('localhost',27017) #连接mongodb
zufang = client['ganjin'] #创建数据库
sheet_tab = zufang['item_info'] #创建一个sheet
for item in sheet_tab.find():
    if item['title'] is None:
        sheet_tab.remove(item)
print('Done')
