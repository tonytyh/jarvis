import argparse
from src.updater.security_data_updater import *

parser = argparse.ArgumentParser(description="price_updater")

parser.add_argument("--ticker", help="ticker name")
args = parser.parse_args()

update_one_ticker_price_by_period(
    ticker_name=args.ticker,
    period="1y"
)






