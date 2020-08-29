""""直接下载m3u8视频文件，再合成mp4"""
import requests

sesion = requests.session()
def download(url,file_name):
    """下载文件"""
    reponse = sesion.get(url,headers=headers)
    with open("temp/" + file_name,"wb") as code:
        code.write(reponse.content)


if __name__ == '__main__':

    headers = {
        "Referer": "https://www.yy.com/x/15012_1101280606_54880976_1598700607769",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    url = 'https://record.vod.huanjuyun.com/xcrs/15012_1101280606_54880976_1598700607769.m3u8'

    content = sesion.get(url, headers=headers).text
    lines = str(content).split("\n")
    count = 0
    for item in lines:
        print(item)
        if 'http' not in item:
            continue
        file_name = str(count) + '.ts'
        download(item,file_name)
        count += 1