from decimal import Decimal
from typing import Any, Literal

from pybit.unified_trading import HTTP

from src.API.base import ExchangeConnector


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
