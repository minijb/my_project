# https://video.pearvideo.com/mp4/short/20220531/1654013277307-15888537-hd.mp4
# https://www.pearvideo.com/video_1760962
# https://video.pearvideo.com/mp4/short/20220531/cont-1760962-15888537-hd.mp4

from turtle import pensize
import requests

url ='https://www.pearvideo.com/video_1760962'
count_ID = url.split('_')[1]
videoStatusUrl = 'https://www.pearvideo.com/videoStatus.jsp?contId=1760962&mrd=0.198104403550027'
headers = {
    "User_Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
    'Referer': 'https://www.pearvideo.com/video_1760962'#防盗链！！！！！从哪个页面进行请求的
}

video_status_resp = requests.get(videoStatusUrl,headers=headers)
# print(video_status_resp.json()['videoInfo']['videos']['srcUrl'])
src_url = video_status_resp.json()['videoInfo']['videos']['srcUrl']
#进行替换
systemTime = video_status_resp.json()['systemTime']
src_url = src_url.replace(systemTime,f"cont-{count_ID}")
headers = {
    "User_Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'
}
print(src_url)
video_resp = requests.get(src_url,headers=headers)
#下载视频
with open('a.mp4','wb') as f:
    f.write(video_resp.content)