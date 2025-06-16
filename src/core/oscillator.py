from src.core.data import TimeSeriesData
from src.core.compute import exponential_moving_average, relative_index
import pandas as pd


def moving_average_convergence_divergence(t: TimeSeriesData):
    ema12 = exponential_moving_average(t, 12)
    ema26 = exponential_moving_average(t, 26)
    fast_macd = TimeSeriesData.from_dataframe((ema12 - ema26).dataframe)
    slow_macd = exponential_moving_average(fast_macd, 9)
    return fast_macd, slow_macd, fast_macd - slow_macd


def relative_strength_index(t: TimeSeriesData, window_size: int):
    rs = relative_index(t, window_size)
    rsi = 100 - (100 / (1 + rs))

    return TimeSeriesData.from_dataframe(pd.DataFrame(rsi.values.squeeze(), index=t.dataframe.index[1:])[window_size:])
