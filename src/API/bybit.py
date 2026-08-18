from decimal import Decimal
import time
from typing import Any, Literal

from pybit.unified_trading import HTTP

from src.API.base import ExchangeConnector
from shared.CandleSeries import CandleSeries, Candle

class BybitAPI(ExchangeConnector):
    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        *,
        testnet: bool = True,
    ) -> None:
        session_options: dict[str, Any] = {"testnet": testnet}

        if api_key and api_secret:
            session_options.update(
                api_key=api_key,
                api_secret=api_secret,
            )

        self._session = HTTP(**session_options)

    @staticmethod
    def _result(response: dict[str, Any]) -> dict[str, Any]:
        if response.get("retCode") != 0:
            raise RuntimeError(
                f"Bybit error {response.get('retCode')}: "
                f"{response.get('retMsg', 'Unknown error')}"
            )

        return response["result"]

    def get_server_time(self) -> int:
        response = self._session.get_server_time()
        result = self._result(response)
        return int(result["timeSecond"]) * 1_000

    def get_candles(
        self,
        symbol: str,
        interval: str,
        *,
        category: str = "linear",
        limit: int = 200,
    ) -> list[list[str]]:
        if not 1 <= limit <= 1_000:
            raise ValueError("limit must be between 1 and 1000")

        response = self._session.get_kline(
            category=category,
            symbol=symbol.upper(),
            interval=interval,
            limit=limit,
        )
        candles = self._result(response)["list"]

        # Bybit returns the newest candle first.
        return list(reversed(candles))

    @staticmethod
    def _to_candle(raw_candle: list[str]) -> Candle:
        return Candle(
            int(raw_candle[0]),
            float(raw_candle[1]),
            float(raw_candle[2]),
            float(raw_candle[3]),
            float(raw_candle[4]),
            float(raw_candle[5]),
            float(raw_candle[6]),
        )

    def fetch_klines_paged(
        self,
        symbol: str,
        interval: str,
        *,
        total_bars: int = 100_000,
        category: str = "linear",
    ) -> CandleSeries:
        if total_bars <= 0:
            raise ValueError("total_bars must be positive")

        page_limit = 1_000
        end_time = self.get_server_time()
        candles_by_start_time: dict[int, Candle] = {}

        while len(candles_by_start_time) < total_bars:
            bars_left = total_bars - len(candles_by_start_time)
            response = self._session.get_kline(
                category=category,
                symbol=symbol.upper(),
                interval=interval,
                limit=min(page_limit, bars_left),
                end=end_time,
            )
            raw_candles = self._result(response)["list"]

            if not raw_candles:
                break

            for raw_candle in raw_candles:
                candle = self._to_candle(raw_candle)
                candles_by_start_time[candle.get_start_time()] = candle

            # Bybit returns each page from newest to oldest.
            oldest_start_time = int(raw_candles[-1][0])
            next_end_time = oldest_start_time - 1
            if next_end_time >= end_time:
                break

            end_time = next_end_time

            if len(raw_candles) < min(page_limit, bars_left):
                break

            time.sleep(0.2)

        ordered_candles = [
            candles_by_start_time[start_time]
            for start_time in sorted(candles_by_start_time)
        ]
        return CandleSeries(ordered_candles[-total_bars:])

    def get_ticker(
        self,
        symbol: str,
        *,
        category: str = "linear",
    ) -> dict[str, Any]:
        response = self._session.get_tickers(
            category=category,
            symbol=symbol.upper(),
        )
        tickers = self._result(response)["list"]

        if not tickers:
            raise LookupError(f"No ticker returned for {symbol}")

        return tickers[0]

    def place_order(
        self,
        symbol: str,
        side: Literal["Buy", "Sell"],
        quantity: Decimal,
        *,
        category: str = "linear",
        order_type: Literal["Market", "Limit"] = "Market",
        price: Decimal | None = None,
    ) -> dict[str, Any]:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if order_type == "Limit" and price is None:
            raise ValueError("price is required for a limit order")

        order: dict[str, Any] = {
            "category": category,
            "symbol": symbol.upper(),
            "side": side,
            "orderType": order_type,
            "qty": str(quantity),
        }

        if price is not None:
            order["price"] = str(price)

        response = self._session.place_order(**order)
        return self._result(response)
