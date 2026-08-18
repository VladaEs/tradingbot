from shared.Candle import Candle

def simple_moving_average(data: list[Candle], period: int) -> list[float | None]:
    """
    Calculate the Simple Moving Average (SMA) of a given data series.

    Parameters:
    data (list or array-like): The input data series (e.g., stock prices).
    period (int): The number of periods over which to calculate the SMA.
    period must be a positive integer and it decides how many data points are used to calculate the average.
    e.g., if period=5, the SMA is calculated using the last 5 data points.
    Returns:
    list: A list containing the SMA values.
    """
    if period <= 0:
        raise ValueError("Period must be a positive integer.")
    if len(data) == 0:
        raise ValueError("Data series cannot be empty.")
    if len(data) < period:
        raise ValueError("Data length must be greater than or equal to the period.")
    sma_values = []
    # example : 1-100
    for i in range(len(data)):
        if i < period - 1:
            sma_values.append(None) # Not enough data to calculate SMA
        else:
            sum = 0.0
            for k in range(period): 
                sum += data[i - k].get_close_price()
            sma_values.append(sum / period)
    return sma_values



# period = 4
# [1,2,3,3,4,5,6,7,8,9,0, 10]
# [n,n,n,3+3+2+1/4, ...]
