import aiohttp
import asyncio



urls = [
    'https://kr.zutuanla.com/file/2021/0512/447c93953eb3676bd3a3ce0d7a85785c.jpg',
    'https://i1.shaodiyejin.com/uploads/tu/201608/15/08082497.jpg',
    'https://i1.shaodiyejin.com/uploads/tu/201608/15/08082603.jpg'
]

async def download(url):
    name = url.rsplit("/")[-1]
    #aiohttp.ClientSession()#和request模块差不多
    async with aiohttp.ClientSession() as session :
        async with session.get(url) as resp:
            with open(name,'wb') as f:#自学aiofile
                f.write(await resp.content.read()) # ==resp.content
    print(name,'ok')
async def main():
    tasks = []
    for url in urls:
        tasks.append(download(url))
    await asyncio.wait(tasks)
    
if __name__ =='__main__':
    asyncio.run(main())