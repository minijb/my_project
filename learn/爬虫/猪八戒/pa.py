import requests
from lxml import etree

#获取基础内容
url = "https://www.zbj.com/search/f/?kw=saas"
resp = requests.get(url)

#获取部件
html = etree.HTML(resp.text)
#所有服务商的div
list_divs = html.xpath('/html/body/div[6]/div/div/div[2]/div[5]/div[1]/div')


for div in list_divs[:-1]:
    price = div.xpath("./div/div/a[2]/div[2]/div[1]/span[1]/text()")[0]
    name = div.xpath("./div/div/a[2]/div[2]/div[2]/p/text()")[0]
    com_name = div.xpath("./div/div/a[1]/div[1]/p/text()")[1][3:]
    print('*'*10)
    print(f"title: {name}")
    print(f'from : {com_name} ---- price : {price}')
    



resp.close()