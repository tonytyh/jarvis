from src.strategy.moving_average_strategy import *
from src.util.dao_util import get_security_data_by_date, get_strategy_data_config
from src.strategy.trend_strategy import Ma20PriceUpTrendLast7, Ma20PriceDownTrendLast7, Ma5PriceUpTrendLast3, \
    Ma5PriceDownTrendLast3, MaPriceStrongDownTrend, MaPriceStrongUptrend


def test_ma5_ma20_buy():
    b = Ma5Ma20Buy(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    b_res = b.execute_strategy()
    s = Ma5Ma20Sell(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    s_res = s.execute_strategy()
    [print(e) for e in b_res]
    [print(e) for e in s_res]


def test_ma5_ma10_buy():
    b = Ma5Ma10Buy(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    b_res = b.execute_strategy()
    s = Ma5Ma10Sell(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    s_res = s.execute_strategy()
    [print(e) for e in b_res]
    [print(e) for e in s_res]


def test_Ma20PriceUpTrendLast7():
    b = Ma20PriceUpTrendLast7(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    b_res = b.execute_strategy()
    [print(e) for e in b_res]


def test_Ma20PriceDownTrendLast7():
    b = Ma20PriceDownTrendLast7(get_strategy_data_config("JPM", "2021-05-01", "2022-02-05"))
    b_res = b.execute_strategy()
    [print(e.event_name) for e in b_res]


def test_Ma20PriceUpTrendLast3():
    b = Ma5PriceUpTrendLast3(get_strategy_data_config("XOM", "2021-12-01", "2022-02-08"))
    b_res = b.execute_strategy()
    [print(e) for e in b_res]


def test_Ma20PriceDownTrendLast3():
    b = Ma5PriceDownTrendLast3(get_strategy_data_config("MSFT", "2021-12-01", "2022-02-08"))
    b_res = b.execute_strategy()
    [print(e.event_name) for e in b_res]


def test_MaStrongUptrend():
    b = MaPriceStrongUptrend((get_strategy_data_config("MSFT", "2021-05-01", "2022-02-08")))
    b_res = b.execute_strategy()
    [print(e) for e in b_res]


def test_MaStrongDowntrend():
    b = MaPriceStrongDownTrend((get_strategy_data_config("MSFT", "2021-05-01", "2022-02-08")))
    b_res = b.execute_strategy()
    [print(e) for e in b_res]
