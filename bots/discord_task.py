import asyncio
import logging
import os
import time

import discord
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
DISCORD_CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])
USER_PROXY = os.environ['USER_PROXY']


async def discord_send_photo(img_path):
    client = discord.Client(intents=discord.Intents.default(), proxy=USER_PROXY)
    result_future = asyncio.Future()

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            file = discord.File(img_path)
            await channel.send(file=file)
            result_future.set_result(True)
        except Exception as e:
            result_future.set_result(False)
        finally:
            await client.close()

    await client.start(DISCORD_TOKEN)
    await client.close()
    return await result_future

