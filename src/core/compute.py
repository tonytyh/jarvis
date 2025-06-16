import pandas as pd
import numpy as np

from src.core.data import TimeSeriesData


def moving_average(time_series_data: TimeSeriesData, window_size: int):
    return TimeSeriesData.from_dataframe(time_series_data.dataframe.rolling(window_size).sum() / window_size)


def exponential_moving_average(time_series_data: TimeSeriesData, window_size: int):
    return TimeSeriesData.from_dataframe(time_series_data.dataframe.ewm(span=window_size, adjust=False).mean())


def highest_row(time_series_data: TimeSeriesData):
    df = time_series_data.dataframe
    idx = df.idxmax()
    return TimeSeriesData.from_dataframe(df.loc[idx])


def lowest_row(time_series_data: TimeSeriesData):
    df = time_series_data.dataframe
    idx = df.idxmin()
    return TimeSeriesData.from_dataframe(df.loc[idx])


def intersection(a_time_series_data: TimeSeriesData, b_time_series_data: TimeSeriesData, direction: str):
    if direction.lower() != "up" and direction != "down":
        raise Exception("Direction needs to be either up or down")

    res = pd.DataFrame()
    c_time_series_data = a_time_series_data - b_time_series_data
    c_df = c_time_series_data.dataframe

    l = len(c_df)
    for r in range(0, l):
        if c_df.iloc[r]["value"] != np.NaN and r + 1 < l and c_df.iloc[r + 1]["value"] != np.NaN:
            curr_value = c_df.iloc[r]["value"]
            next_value = c_df.iloc[r + 1]["value"]
            time_label = c_df.iloc[r + 1].name

            if direction.lower() == "up":
                if curr_value < 0 and 0 < next_value:
                    res = pd.concat(
                        [res, pd.DataFrame(data={"value": [a_time_series_data.dataframe.loc[time_label]["value"]]},
                                           index=[time_label])])

            if direction.lower() == "down":
                if curr_value > 0 and 0 > next_value:
                    res = pd.concat(
                        [res, pd.DataFrame(data={"value": [a_time_series_data.dataframe.loc[time_label]["value"]]},
                                           index=[time_label])])

        if c_df.iloc[r]["value"] == 0:
            curr_value = c_df.iloc[r]["value"]

            if direction.lower() == "up" and r + 1 < l and c_df.iloc[r + 1]["value"] > 0:
                time_label = c_df.iloc[r + 1].name
                res = pd.concat(
                    [res, pd.DataFrame(data={"value": [a_time_series_data.dataframe.loc[time_label]["value"]]},
                                       index=[time_label])])
            if direction.lower() == "down" and r + 1 < l and c_df.iloc[r + 1]["value"] < 0:
                time_label = c_df.iloc[r + 1].name
                res = pd.concat(
                    [res, pd.DataFrame(data={"value": [a_time_series_data.dataframe.loc[time_label]["value"]]},
                                       index=[time_label])])

    return TimeSeriesData.from_dataframe(res)


def is_uptrend(time_series_data: TimeSeriesData):
    ma = time_series_data
    for i in range(1, len(ma)):
        if ma[i - 1].dataframe.iloc[0] >= ma[i].dataframe.iloc[0]:
            return False

    return True


def is_downtrend(time_series_data: TimeSeriesData):
    ma = time_series_data
    for i in range(1, len(ma)):
        if ma[i - 1].dataframe.iloc[0] < ma[i].dataframe.iloc[0]:
            return False

    return True


def relative_index(time_series_data: TimeSeriesData, window_size: int):
    df = time_series_data.dataframe
    np_array = df.values.squeeze()
    U = []
    D = []
    n = window_size

    for i in range(1, len(np_array)):
        diff = np_array[i - 1] - np_array[i]
        if diff < 0:
            U.append(-diff)
            D.append(0)
        if diff > 0:
            U.append(0)
            D.append(diff)

        if diff == 0:
            U.append(0)
            D.append(0)

    pd_U = pd.DataFrame(U)
    pd_D = pd.DataFrame(D)

    avg_U = pd_U.ewm(com=n - 1, adjust=True, min_periods=n).mean()
    avg_D = pd_D.ewm(com=n - 1, adjust=True, min_periods=n).mean()

    rs = avg_U / avg_D

    return rs

# def rsi(df, periods=14, ema=True):
#     """
#     Returns a pd.Series with the relative strength index.
#     """
#     close_delta = df['close'].diff()
#
#     # Make two series: one for lower closes and one for higher closes
#     up = close_delta.clip(lower=0)
#     down = -1 * close_delta.clip(upper=0)
#
#     if ema == True:
#         # Use exponential moving average
#         ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
#         ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
#     else:
#         # Use simple moving average
#         ma_up = up.rolling(window=periods, adjust=False).mean()
#         ma_down = down.rolling(window=periods, adjust=False).mean()
#
#     rsi = ma_up / ma_down
#     rsi = 100 - (100 / (1 + rsi))
#     return rsi
