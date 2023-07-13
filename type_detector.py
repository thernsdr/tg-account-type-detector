from typing import Union

import aiohttp
from bs4 import BeautifulSoup
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import UsernameNotOccupied, UsernameInvalid
from pyrogram.raw.functions.contacts import ResolveUsername
import pyrogram.raw.types as pyrogram_types


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


async def get_type_via_userbot(username: str, api_id: int, api_hash: str) -> str:
    """
    Returns the type of account with the given username, using TG userbot (Pyrogram)
    :param username: Telegram username
    :param api_id: my.telegram.org/apps API ID
    :param api_hash: my.telegram.org/apps API Hash
    :return: Account type (user/bot)
    :rtype: str
    """

    async with Client("my_own_app", api_id=api_id, api_hash=api_hash) as app:
        try:
            peer_data = await app.invoke(ResolveUsername(username=username))
            peer_type = type(peer_data.peer)

            if peer_type == pyrogram_types.peer_user.PeerUser:  # User or bot
                if peer_data.users[0].bot:
                    return "bot"
                else:
                    return "user"
            elif peer_type == pyrogram_types.peer_channel.PeerChannel:  # Group chat or channel
                return "channel"

        except UsernameNotOccupied:  # The username is not occupied
            return "invalid"

        except UsernameInvalid:  # The username is invalid
            return "invalid"

        return "unknown"


async def get_username_info(username: str, api_id: int, api_hash: str) -> str:
    """
    Returns the type of account with the given username
    :param username: Telegram username
    :param api_id: my.telegram.org/apps API ID
    :param api_hash: my.telegram.org/apps API Hash
    :return: Account type (user/bot/channel/group)
    :rtype: str
    """

    if not (all(char.isalnum() or char == "_" for char in username) and 4 <= len(username) <= 32):
        return "invalid"

    html_response = await get(f"https://t.me/{username}")
    soup = BeautifulSoup(html_response, features="html.parser")
    div_extra = soup.find("div", {"class": "tgme_page_extra"})

    if div_extra:
        specific_str = div_extra.text.strip()

        if "subscribers" in specific_str:
            return "channel"
        elif "members" in specific_str:
            return "group"

    # The program comes here if it is a user / bot / could not be determined by HTML parsing

    return await get_type_via_userbot(username, api_id, api_hash)
