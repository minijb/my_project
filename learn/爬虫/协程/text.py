import asyncio
import time

async def download(url):
    await asyncio.sleep(2)#requests.get()
    
async def main():
    urls = [
        'www.baidu.com',
        'www.bilibili.com'
    ]
    tasks = []
    for i in urls:
        tasks.append(download(i))
        
    await asyncio.wait(tasks)