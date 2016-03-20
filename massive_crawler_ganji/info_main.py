#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Pool
from pages_parsing import get_links_from,url_list,get_item_info,item_info

db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y

if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(get_item_info,rest_of_urls)