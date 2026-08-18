class Candle: 

    def __init__(self, startTime: int, openPrice: float, hightPrice: float, LowPrice: float, closePrice: float, volume: float, turnover: int) -> None:
        self.startTime = startTime
        self.openPrice = openPrice
        self.hightPrice = hightPrice
        self.LowPrice = LowPrice
        self.closePrice = closePrice
        self.volume = volume
        self.turnover = turnover

    def __str__(self) -> str:
        return f"Candle(startTime={self.startTime}, openPrice={self.openPrice}, hightPrice={self.hightPrice}, LowPrice={self.LowPrice}, closePrice={self.closePrice}, volume={self.volume}, turnover={self.turnover})"

    def get_start_time(self) -> int:
        return self.startTime
    def get_open_price(self) -> float:
        return self.openPrice
    def get_hight_price(self) -> float:
        return self.hightPrice
    def get_low_price(self) -> float:
        return self.LowPrice 
    def get_close_price(self) -> float:
        return self.closePrice
    def get_volume(self) -> float:
        return self.volume
    def get_turnover(self) -> int:
        return self.turnover
    

    