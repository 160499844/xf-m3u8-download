# _*_coding:utf-8_*_
"""下载文件队列"""
import uuid
import pika, time
import json
import os

application_path = 'D:/web_application/ffmpeg-20200824-3477feb-win64-static/bin/'#ffmpeg.exe位置

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'xf-server',heartbeat = 1000,socket_timeout=1000))
channel = connection.channel()

channel.queue_declare(queue='yy_download_url')

def callback(ch, method, properties, body):
    """消息消费者"""
    msg = str(body, encoding="utf-8")
    print(" [x] 收到: %r" % msg)
    data = json.loads(msg)
    try:
        fileName = data['fileName']
        videoUrl = data['videoUrl']
        downloadUrl(videoUrl,fileName)
    except Exception as e:
        print(e)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉发送端我已经处理完了
    time.sleep(1)

def downloadUrl(url,fileName):
    #url = "http://198.255.82.92//mp43/389713.mp4?st=S3jjErxckn44i32ZeBqi7g&e=1597565454"
    start = time.time()
    """下载文件"""
    save_path = 'Z:/data/其他视频/yy直播/' + fileName

    #判断文件是否存在
    if os.path.exists(save_path) == False:

        cmd = '%sffmpeg.exe  -i "%s" -vcodec copy -acodec copy -absf aac_adtstoasc  "%s"' % (
            application_path, url, save_path)
        print(cmd)
        os.system(
            cmd
        )
        end = time.time()
        print('下载耗时:', end - start)
    else:
        print("文件已存在,跳过")


if __name__ == "__main__":
    #download("http://198.255.82.92//mp43/389713.mp4?st=S3jjErxckn44i32ZeBqi7g&e=1597565454")
    channel.basic_consume(on_message_callback=callback, queue='yy_download_url')

    print(' [*] 关闭请按 CTRL+C')
    channel.start_consuming()
