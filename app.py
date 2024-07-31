import asyncio
import fnmatch
import os
import random
import time
import logging
import shutil

from dotenv import load_dotenv
import schedule

from bots.discord_task import discord_send_photo
from bots.tg_task import tg_send_photo

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
source_path = os.path.dirname(os.path.abspath(__file__))

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
SOURCE_DIR = os.path.join(source_path, 'in')
DESTINATION_DIR = os.path.join(source_path, 'out')


def get_random_image_path():
    img_files = []
    pattern = '*.*'
    for path, dirs, files in os.walk(SOURCE_DIR):
        matched_strings = fnmatch.filter(files, pattern)
        for filename in matched_strings:
            full_path = os.path.join(path, filename)
            img_files.append(full_path)
        else:
            break
    if len(img_files) != 0:
        tmp_random_image = []
        for _ in range(10):
            tmp_random_image.append(random.randrange(0, len(img_files)))
        img_path = img_files[tmp_random_image[random.randrange(0, 8)]]
        return img_path
    else:
        return False


def move_image(image_path):
    logger.info(f"Moving image {image_path}")
    shutil.move(image_path, DESTINATION_DIR)


def task_tg_send_photo(image_path):
    logger.info(f'Task TG start sending random message')
    tg_img = tg_send_photo(file_path=image_path, send_to=TG_CHAT_ID)
    if tg_img.get('ok'):
        logger.info(f'Send TG successfully: {tg_img}')
    else:
        logger.error(f'Send TG not successfully: {tg_img}')
        return False
    logger.info(f'Task TG end sending random message')
    return True


def task_discord_send_photo(image_path):
    logger.info(f'Task Discord start sending random message')
    discord_result = asyncio.run(discord_send_photo(img_path=image_path))
    if discord_result:
        logger.info(f'Send Discord successfully: {image_path}')
    else:
        logger.error(f'Send Discord not successfully: {image_path}')
        return False
    logger.info(f'Task Discord end sending random message')
    return True


def task_send_random_message():
    image_path = get_random_image_path()
    logger.info(f'Image open {image_path}')
    task_tg_send_photo(image_path)
    task_discord_send_photo(image_path)
    move_image(image_path)


def main_run():
    start_times = ['11:40', '11:41']*2
    print(f'Task will sending : {start_times}')
    for times in start_times:
        schedule.every().day.at(times).do(task_send_random_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main_run()
