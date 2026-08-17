import os
from datetime import datetime, timezone
from shared.Candle import Candle

from dotenv import load_dotenv

from src.API.bybit import BybitAPI


def main() -> None:
    load_dotenv()

    client = BybitAPI(
        api_key=os.getenv("BYBIT_API_KEY"),
        api_secret=os.getenv("BYBIT_API_SECRET"),
        testnet=os.getenv("TEST_ENV", "true").lower() == "true",
    )

    server_time_ms = client.get_server_time()
    server_time = datetime.fromtimestamp(
        server_time_ms / 1_000,
        tz=timezone.utc,
    )
    print(f"Bybit server time: {server_time.isoformat()}")

    candles = client.get_candles( category="linear", symbol="BTCUSDT", interval="15", limit=10)
    candles_obj = [];
    print(f"Received {len(candles)} candles")
    print(candles)
    for candle in candles: 
        candles_obj.append(Candle(candle[0], candle[1], candle[2], candle[3], candle[4], candle[5], candle[6]))

    for candle in candles_obj: 
        print(candle)

if __name__ == "__main__":
    main()
