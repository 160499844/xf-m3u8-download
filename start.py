# _*_coding:utf-8_*_
"""使用ffmpeg下载m3u8"""

import pika
import json
import os
import uuid
import requests
import time

"""消息生产者"""
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'xf-server'))
channel = connection.channel()

# 声明queue
queue = channel.queue_declare(queue='yy_download_url')

def sendDownloadMsg(msg):
    """下载队列"""
    channel.basic_publish(exchange='',
                          routing_key='yy_download_url',
                          body=bytes(msg, encoding="utf8"))

    print(" [下载队列] %s" %msg)

def download(url,name):
    # 判断队列中还有多少消息没处理
    messageCount = queue.method.message_count
    print("当前队列未处理下载消息数量:%s" % str(messageCount))
    while messageCount > 20:
        time.sleep(1)
        messageCount = queue.method.message_count


    dTemp = {
        "videoUrl": url,
        "fileName": name + ".mp4",
    }
    try:
        pass
        sendDownloadMsg(json.dumps(dTemp))
    except Exception as e:
        print(e)


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
        #urls.append(m3u8_url)
        download(m3u8_url,name)

    return urls

def getPageList():
    for i in range(10,100):
        getPageDetails(i)
        print("--------------------------当前页数 %s-------------------------" % str(i))
        time.sleep(20)


if __name__ == '__main__':
    getPageList()