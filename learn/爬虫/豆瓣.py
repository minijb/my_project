import imp
from operator import mod
import requests
import re
import csv

url = r'http://movie.douban.com/top250'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'
}
resp = requests.get(url,headers=header)
page_content = resp.text

obj = re.compile('<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?'
                r'<span class="rating_num" property="v:average">(?P<rate>.*?)</span>',re.S)


iter = obj.finditer(page_content)

#写入csv
f = open('data.csv',mode='w',encoding='utf-8')
csvwriter = csv.writer(f)

for it in iter:
    print(it.group('name'),it.group('year').strip()+'  --  '+it.group('rate'))
    dic = it.groupdict()
    dic['year'] = dic['year'].strip()
    csvwriter.writerow(dic.values())






resp.close()
