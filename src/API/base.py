from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Literal

from shared.CandleSeries import CandleSeries


class ExchangeConnector(ABC):
    """Common interface implemented by every exchange connector."""

    @abstractmethod
    def get_server_time(self) -> int:
        """Return the exchange server time in milliseconds."""

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        interval: str,
        *,
        category: str = "linear",
        limit: int = 200,
    ) -> list[list[str]]:
        """Return candles ordered from oldest to newest."""

    @abstractmethod
    def fetch_klines_paged(
        self,
        symbol: str,
        interval: str,
        *,
        total_bars: int = 100_000,
        category: str = "linear",
    ) -> CandleSeries:
        """Fetch candle history backwards using exchange pagination."""

    @abstractmethod
    def get_ticker(
        self,
        symbol: str,
        *,
        category: str = "linear",
    ) -> dict[str, Any]:
        """Return the latest ticker for a symbol."""

    @abstractmethod
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
        """Place an authenticated order."""
