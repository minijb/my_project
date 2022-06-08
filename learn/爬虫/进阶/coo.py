from attr import attrs
import requests

#在session过程中，cookie不会丢失
session = requests.session()

#登录
url = "https://passport.17k.com/ck/user/login"
data = {
    'loginName': '15651976185',
    'password': 'zh3210981005'
}
resp = session.post(url,data=data)

# print(resp.text)
# print(resp.cookies)

#拿到书架上的数据
book_url = 'https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919'
book_resp = session.get(book_url)
print(book_resp.json())



book_resp.close()
resp.close()
