#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
from channel_extact import channel_list
from pages_parsing import get_links_from

def get_all_links(channel):
    for page in range(1,150):
        get_links_from(channel,page)

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_links,channel_list.split())

