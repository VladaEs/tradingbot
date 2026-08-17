import pandas as pd
import numpy as np
import time
import datetime
from collections import deque
from scipy.stats import zscore
from pybit.unified_trading import HTTP
import telebot
# === НАСТРОЙКИ ===

symbol = "BTCUSDT"
interval = "5m"

bb_period = 40
bb_std = 1

STOP_LOSS_PCT = 0.004

client = BinanceClient()

config = {
    'min_cluster': 3,
    'bull_quant': 0.75,
    'bear_quant': 0.25,
    'rsi': 60
}
