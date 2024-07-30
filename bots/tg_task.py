import os

import requests
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']


def tg_send_photo(file_path, send_to, caption=''):
    with open(file_path, 'rb') as img_file:
        img = {'photo': ('_', img_file, 'image/jpeg')}
        url = f'https://api.telegram.org/bot{TG_TOKEN}/sendPhoto?chat_id={send_to}&caption={caption}'
        response = requests.post(url, files=img)
        return response.json()
