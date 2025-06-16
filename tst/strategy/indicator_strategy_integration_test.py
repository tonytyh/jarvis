from src.strategy.oscillator_strategy import MacdSell, MacdBuy,Rsi6OverSold,Rsi6OverBought
from src.util.dao_util import get_strategy_data_config

from datetime import datetime,timedelta


def test_macd_buy():
    b = MacdBuy(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    b_res = b.execute_strategy()
    [print(e) for e in b_res]


def test_macd_sell():
    b = MacdSell(get_strategy_data_config("MSFT", "2021-05-01", "2022-02-05"))
    b_res = b.execute_strategy()
    [print(e.event_name) for e in b_res]



def test_rsi6_oversell():
    b = Rsi6OverSold(get_strategy_data_config("AAPL", "2021-05-01", "2022-02-09"))
    b_res = b.execute_strategy()
    [print(e) for e in b_res]

def test_rsi6_overbought():
    b = Rsi6OverBought(get_strategy_data_config("AAPL", "2021-05-01", "2022-02-09"))
    b_res = b.execute_strategy()
    [print(e.event_name) for e in b_res]

def test():
    d = datetime.now() - timedelta(days=30)

