from src.updater.security_data_updater import update_one_ticker_price_by_period, get_yfinance_data_by_period_with_interval
from src.updater.market_symbol import future_ticker_dict


def test_get_future_date():
    get_yfinance_data_by_period_with_interval(ticker_name="ES=F", period="5d", interval="15m")


if __name__ == "__main__":
    update_one_ticker_price_by_period("KSU", "1y")
