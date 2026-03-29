import asyncio
import json
from random import randint

from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.types import InputEmojiStatusCollectible

from src.tg import get_client, get_all_gifts


async def start(timeout, every_time):
    while True:
        try:
            client = get_client()
            async with client:
                unique_gifts = await get_all_gifts(client)
                while True:
                    try:
                        gift_now = unique_gifts[randint(0, len(unique_gifts)-1)]
                        while True:
                            try:
                                await client(UpdateEmojiStatusRequest(
                                    emoji_status=InputEmojiStatusCollectible(
                                        collectible_id=gift_now,
                                    )
                                ))
                                print('success change prem status')
                                break
                            except Exception as e:
                                print(e)
                                gift_now = unique_gifts[randint(0, len(unique_gifts))]
                                await asyncio.sleep(30)
                        await asyncio.create_task(change_status(client, timeout, every_time))
                    except Exception as e:
                        print(e)
                        await asyncio.sleep(30)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)


async def change_status(client, timeout, every_time):
    while timeout - every_time >= 0:
        try:
            await client(UpdateProfileRequest(
                about=f'{timeout:.13f}'
            ))
            print(f'change status to {timeout:.13f}')
            timeout -= every_time

            await asyncio.sleep(every_time * 60)
        except Exception as e:
            time = int(str(e).split("A wait of ")[1].split(" seconds is required")[0])
            print(f'sleep {time}')
            await asyncio.sleep(time)


if __name__ == "__main__":
    with open('imp/config.json', 'r') as f:
        CONFIG = json.load(f)

    timeout, every_time = CONFIG['timeout'], CONFIG['every_time']

    asyncio.run(start(timeout, every_time))
