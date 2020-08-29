"""使用ffmpeg下载m3u8"""

import os
import uuid


application_path = 'D:/web_application/ffmpeg-20200824-3477feb-win64-static/bin/'#ffmpeg.exe位置

if __name__ == '__main__':
    url = "https://record.vod.huanjuyun.com/xcrs/15012_1101280606_54880976_1598702407173.m3u8" #m3u8的地址
    save_path = 'temp/' + str(uuid.uuid1()).replace("-","")+'.mp4'
    cmd = '%sffmpeg.exe  -i "%s" -vcodec copy -acodec copy -absf aac_adtstoasc  "%s"' %(application_path,url,save_path)
    print(cmd)
    os.system(
        cmd
    )