import asyncio
import os

from dotenv import load_dotenv

from src.API.bybit import BybitAPI


async def main() -> None:
    load_dotenv()

    client = BybitAPI(
        api_key=os.getenv("BYBIT_API_KEY", ""),
        api_secret=os.getenv("BYBIT_API_SECRET", ""),
    )

    try:
        server_time = await client.get_server_time()
        print(server_time)
        print(server_time["result"]["timeSecond"])
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())