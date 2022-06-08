import requests
from bs4 import BeautifulSoup
import time
from rich import print

url = 'https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&_extra=&context=&page=1&page_size=42&order=&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=38%E5%A4%A7%E4%BD%90&preload=true&com2co=true'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}
resp = requests.get(url,headers=headers)

print(resp.json()['data']['result'][10]['data'])
# for obj in resp.json()['data']['result'][10]['data']:
#     # url = f'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&_extra=&context=&page=1&page_size=36&order=&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword={str}&category_id=&search_type=bili_user&order_sort=0&user_type=0&dynamic_offset=0&preload=true&com2co=true'
    
    # print(obj['mid'])
    