
# coding: utf-8

# In[18]:

import pymongo
from string import punctuation
import charts


# In[12]:

client = pymongo.MongoClient('localhost',27017)
ceshi = client['ganjin']
item_info = ceshi['item_infoY']


# In[6]:

for i in item_info.find().limit(200):
    print(i['area'])


# In[27]:

for i in item_info.find().limit(200):
    if i['area']:
        area = [i for i in i['area'] if i not in punctuation]
        area = [i for i in i['area'] if i is not '']
    else:
        area = ['不明']
#print(area)
    item_info.update({'_id':i['_id']},{'$set':{'area':area}})
    


# In[28]:

for i in item_info.find().limit(300):
    print(i['area'])


# In[35]:

area_list = []
for i in item_info.find():
    try:
        area_list.append(i['area'][1])
    except:
        area_list.append('不明')
area_index = list(set(area_list))
print(area_index)


# In[38]:

post_times = []
for index in area_index:
    post_times.append(area_list.count(index))
print(post_times)


# In[41]:

def data_gen(types):
    length = 0
    if length <= len(area_index):
        for area,times in zip(area_index,post_times):
            data = {
                'name':area,
                'data':[times],
                'type':types
            }
            yield data
            length += 1


# In[42]:

data_gen('column')


# In[44]:

for i in data_gen('column'):
    print(i)


# In[45]:

series = [data for data in data_gen('column')]
charts.plot(series, show='inline',options=dict(title=dict(text='北京城区二手物品发帖量')))


# In[ ]:



