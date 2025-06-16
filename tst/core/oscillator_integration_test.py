from src.core.compute import intersection
from src.core.data import TimeSeriesData
from src.core.oscillator import moving_average_convergence_divergence, relative_strength_index
from src.strategy.oscillator_strategy import MacdBuy, MacdSell
from src.util.dao_util import get_security_data_by_date, get_strategy_data_config
import matplotlib.pyplot as plt
from datetime import datetime


def test_macd():
    data = get_security_data_by_date("MSFT", "2021-08-01", "2022-02-02")
    data.sort(key=lambda x: datetime.strptime(x["publish_date"], "%Y-%m-%d"))
    t = TimeSeriesData.from_array([x["close"] for x in data], [x["publish_date"] for x in data])
    macd, macd_ema9,macd_diff = moving_average_convergence_divergence(t)

    res = intersection(macd, macd_ema9, "up")
    print(res)

    plt.plot(macd.dataframe)
    plt.plot(macd_ema9.dataframe)
    plt.show()


def test_rsi():
    data = get_security_data_by_date("AAPL", "2021-07-01", "2022-02-09")
    t = TimeSeriesData.from_array([x["close"] for x in data], [x["publish_date"] for x in data])

    rsi_6 = relative_strength_index(t,6)
    # rsi_12 = relative_strength_index(t, 12)
    rsi_14 = relative_strength_index(t, 14)
    # print(rsi_14.dataframe)
    rsi_24 = relative_strength_index(t, 24)


    plt.plot(t.dataframe)
    plt.plot(rsi_6.dataframe)
    # plt.plot(rsi_12.dataframe)
    plt.plot(rsi_14.dataframe)
    plt.plot(rsi_24.dataframe)
    plt.show()


