from base64 import encode
import re
import requests

domain_url = r'https://dytt89.com'
resp = requests.get(domain_url,verify=False)
resp.encoding = 'gbk'#指定编码

obj = re.compile(r'2022必看热片.*?<ul>(?P<content>.*?)</ul>',re.S)
obj_child_url = re.compile(r"<li><a href='(?P<url>.*?)' title",re.S)
obj_title = re.compile(r"片　　名　(?P<title>.*?)<br />.*?"
                    r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<url>.*?)">',re.S)


iter = obj.finditer(resp.text)

page_content  = obj.search(resp.text).group()
target_url = obj_child_url.finditer(page_content)


chile_hrefs = []
for it in target_url:
    chile_href = domain_url+it.group('url')
    # print(chile_href)#获得了子页面的url
    chile_hrefs.append(chile_href)

# print(chile_hrefs)
for url in chile_hrefs:
    child_resp = requests.get(url,verify=False)
    child_resp.encoding = 'gbk'
    child_title = obj_title.search(child_resp.text).group('title')
    child_url = obj_title.search(child_resp.text).group('url')
    print(child_title,child_url)
    child_resp.close()
resp.close()