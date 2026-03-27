import asyncio
import json
from random import randint

from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.types import InputEmojiStatusCollectible

from src.tg import get_client, get_all_gifts


async def start(timeout, every_time):
    client = get_client()
    async with client:
        try:
            while True:
                unique_gifts = await get_all_gifts(client)
                gift_now = unique_gifts[randint(0, len(unique_gifts))]

                while True:
                    try:
                        await client(UpdateEmojiStatusRequest(
                            emoji_status=InputEmojiStatusCollectible(
                                collectible_id=gift_now,
                            )
                        ))
                        print('success change prem status')
                        break
                    except:
                        await asyncio.sleep(15)
                await asyncio.create_task(change_status(client, timeout, every_time))
        except:
            await asyncio.sleep(30)


async def change_status(client, timeout, every_time):
    while timeout - every_time >= 0:
        await client(UpdateProfileRequest(
            about=f'{timeout:.13f}'
        ))
        print(f'change status to {timeout:.13f}')
        timeout -= every_time

        await asyncio.sleep(every_time * 60)


if __name__ == "__main__":
    with open('imp/config.json', 'r') as f:
        CONFIG = json.load(f)

    timeout, every_time = CONFIG['timeout'], CONFIG['every_time']

    asyncio.run(start(timeout, every_time))
