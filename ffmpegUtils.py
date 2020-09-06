"""使用ffmpeg下载m3u8"""

import os
import uuid
import requests


application_path = 'D:/web_application/ffmpeg-20200824-3477feb-win64-static/bin/'#ffmpeg.exe位置
def download(url):
    """下载文件"""
    save_path = 'history/' + str(uuid.uuid1()).replace("-", "") + '.mp4'
    cmd = '%sffmpeg.exe  -i "%s" -vcodec copy -acodec copy -absf aac_adtstoasc  "%s"' % (
    application_path, url, save_path)
    print(cmd)
    os.system(
        cmd
    )
def getPageDetails(i):
    urls=[]
    url = "https://www.yy.com/u/videos/3/80801/%s/30" % i
    headers = {
        "referer":"https://www.yy.com/u/videos/80801",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    }
    js = requests.get(url,headers=headers).json()
    data = js['videoPage']['result']
    for item in data:
        #url = "https://record.vod.huanjuyun.com/xcrs/15012_1101280606_54880976_1598796911058.m3u8"  # m3u8的地址

        href = item['playUrl']#/x/15012_1101280606_54880976_1598684403197
        name = str(href).split("/")[-1]
        m3u8_url = "https://record.vod.huanjuyun.com/xcrs/%s.m3u8" % name
        urls.append(m3u8_url)


    return urls

def getPageList():
    for i in range(1,2):
        urls = getPageDetails(i)
        for url in urls:
            print(url)
            download(url)


if __name__ == '__main__':
    getPageList()