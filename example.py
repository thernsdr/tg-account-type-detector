import asyncio
from dotenv import load_dotenv
from os import getenv
from type_detector import get_username_info

load_dotenv()


async def main():
    for handle in ["durov", "onetimeusername", "tgbetachat", "abobabot", "somestupidshitnotusername*atall", "l0l"]:
        account_type = await get_username_info(username=handle,
                                               api_id=int(getenv('USERBOT_API_ID')),
                                               api_hash=getenv('USERBOT_API_HASH'))
        print(f"{handle}'s type: {account_type}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
