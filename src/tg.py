import json

from telethon import TelegramClient, functions
from telethon.tl.types import StarGiftUnique


def get_client():
    with open('imp/config.json', 'r') as f:
        CONFIG = json.load(f)

    api_id, api_hash = CONFIG['api_id'], CONFIG['api_hash']
    client = TelegramClient('imp/ricloned', api_id, api_hash)
    return client

async def get_all_gifts(client, username='me'):
    result = await client(functions.payments.GetSavedStarGiftsRequest(
        peer=username,
        offset='0',
        limit=100
    ))
    unique_gifts = []
    for gift_ in result.gifts:
        gift = gift_.gift
        if isinstance(gift, StarGiftUnique):
            gift_id = gift.id
            unique_gifts.append(gift_id)
    return unique_gifts