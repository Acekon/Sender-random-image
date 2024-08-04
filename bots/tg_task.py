import os

import requests
from dotenv import load_dotenv


load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']
http_proxy = os.environ['USER_PROXY']
https_proxy = os.environ['USER_PROXY']
ftp_proxy = os.environ['USER_PROXY']
proxyDict = {"http": http_proxy, "https": https_proxy, "ftp": ftp_proxy}


def tg_send_photo(file_path, send_to, caption=''):
    with open(file_path, 'rb') as img_file:
        img = {'photo': ('_', img_file, 'image/jpeg')}
        url = f'https://api.telegram.org/bot{TG_TOKEN}/sendPhoto?chat_id={send_to}&caption={caption}'
        response = requests.post(url, files=img, proxies=proxyDict)
        return response.json()


def tg_send_text(chat_id: str, text: str):
    tg_url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
    response = requests.post(tg_url, json={"chat_id": chat_id, "parse_mode": "html", "text": text}, proxies=proxyDict)
    if response.json().get("ok"):
        print(response.json())
    else:
        print(response.json())
    return response.json().get("result").get("message_id")


if __name__ == '__main__':
    pass
