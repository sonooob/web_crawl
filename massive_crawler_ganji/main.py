from multiprocessing import Pool
from channel_extact import channel_list
from pages_parsing import get_links_from,url_list,get_item_info,item_info


db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y


def get_all_links(channel):
    for page in range(1,150):
        get_links_from(channel,page)

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_links(),channel_list.spilt())

