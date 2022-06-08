import requests
from bs4 import BeautifulSoup
import time

domain_url = 'https://www.umei.cc/katongdongman/katongrenwu/'
base_url = 'https://www.umei.cc'
content = requests.get(domain_url)
content.encoding='utf-8'

#找到pic所在的ul
bs_content = BeautifulSoup(content.text,'html.parser')
pic_ul = bs_content.find('ul',attrs={'class':"pic-list after"})

#找到a标签并获得链接
#链接地址为一个数据
href_list = []
pic_li = pic_ul.find_all('li')
for li in pic_li:
    pic_a = li.find('a')
    # print(base_url+pic_a.get('href'))#拿去href属性中的值
    href_list.append(base_url+pic_a.get('href'))
    

    
for index,href in enumerate(href_list):
    child_content = requests.get(href)
    child_content.encoding='utf-8'
    bs_child = BeautifulSoup(child_content.text,'html.parser')
    child_img_url = bs_child.find('div',attrs={'class':"content-box"}).find('img').get('src')
    # print(child_img_url)
    #下载文件
    img_resp = requests.get(child_img_url)
    with open('./learn/爬虫/img/'+str(index)+'.jpg','wb') as f:
        f.write(img_resp.content)#写入字节
    #防止被干掉
    print('over:'+str(index))
    child_content.close()
    time.sleep(1)
    
    
content.close()