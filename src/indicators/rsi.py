
from shared.Candle import Candle

# rsi
def relative_strength_index(data: list[Candle], period: int) -> list[float | None]:
    """
    Calculate the Relative Strength Index (RSI) of a given data series.

    Parameters:
    data (list or array-like): The input data series (e.g., stock prices).
    period (int): The number of periods over which to calculate the RSI.
    period must be a positive integer and it decides how many data points are used to calculate the average.
    e.g., if period=14, the RSI is calculated using the last 14 data points.

    Returns:
    list: A list containing the RSI values.
    """
    if period <= 0:
        raise ValueError("Period must be a positive integer.")
    if len(data) == 0:
        raise ValueError("Data series cannot be empty.")
    if len(data) < period:
        raise ValueError("Data length must be greater than or equal to the period.")

    rsi_values = []

    
    changes = []
    # start from the second data point to calculate changes
    for i in range(1, len(data)):
        changes.append(data[i].get_close_price() - data[i - 1].get_close_price())



    avarage_gain = None
    avarage_loss = None
    for i in range(len(data)):
        if i < period: 
            rsi_values.append(None)
        else: 
            gains = []
            losses = []
            for k in range(period):
                change = changes[i - k - 1]  # -1 because changes start from index 0
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(abs(change))
            if avarage_gain is None or avarage_loss is None:
                avarage_gain = sum(gains) / period if gains else 0
                avarage_loss = sum(losses) / period if losses else 0
            else:
                current_change = changes[i - 1]
                current_gain = max(current_change, 0)
                current_loss = max(-current_change, 0)
                avarage_gain = (avarage_gain * (period - 1) + current_gain ) / period
                avarage_loss = (avarage_loss * (period - 1) + current_loss) / period

            if avarage_gain == 0 and avarage_loss == 0:
                rsi = 50
            elif avarage_loss == 0:
                rsi = 100
            else:
                rs = avarage_gain / avarage_loss
                rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
    return rsi_values

