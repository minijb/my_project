from cgi import print_arguments
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import requests
import csv
from threading import RLock

lock = RLock()

def download_one_page(url,num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'
    }
    data = {
        'limit': 20,
        'current': num
    }
    resp = requests.post(url,headers=headers,data=data)
    content = resp.json()['list']
    
    
    lock.acquire()
    #newline保证行之间没有空格
    with open('data.csv','a',encoding='utf-8',newline="") as f:
        writer = csv.writer(f)
        for i in range(20):
            writer.writerow([content[i]['prodName'],content[i]['lowPrice']])
    # for i in range(20):
    #     print(content[i]['prodName']+','+content[i]['lowPrice'])
    lock.release()
    print(f'{num}:over')
    
url = 'http://www.xinfadi.com.cn/getPriceData.html'

with ThreadPoolExecutor(50) as p :
    for i in range(1,1000):
        p.submit(download_one_page,url,i)
print('over')
