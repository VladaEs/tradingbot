from shared.Candle import Candle


class CandleSeries:
    candles: list[Candle]

    def __init__(self, candles: list[Candle] | None = None) -> None:
        self.candles = list(candles) if candles is not None else []

    def get_candles(self) -> list[Candle]:
        return self.candles

    def get_candle(self, index: int) -> Candle:
        if index < 0 or index >= len(self.candles):
            raise IndexError("Candle index out of range")
        return self.candles[index]

    def push_candle(self, candle: Candle) -> None:
        self.candles.append(candle)

    def push_candles(self, candles: list[Candle]) -> None:
        self.candles.extend(candles)

    def __len__(self) -> int:
        return len(self.candles)
