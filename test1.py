import requests
from bs4 import BeautifulSoup
url = url = f'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&_extra=&context=&page=1&page_size=36&order=&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=官方&category_id=&search_type=bili_user&order_sort=0&user_type=0&dynamic_offset=0&preload=true&com2co=true'
str = str('官方'.encode)
# print(requests.get(url+str).json()['data']['result'])

for obj in requests.get(url+str).json()['data']['result']:
    print(Columns(obj['mid']))
    
