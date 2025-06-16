import yfinance as yf
import json

from src.updater.market_symbol import *


def update_ticker_info():
    info_dict = {}
    datasource = [
        sp500_ticker_dict,
        nasdaq_top100_ticker_dict,
        future_ticker_dict,
        crypto_ticker_dict,
        forex_ticker_dict,
        sector_etf_ticker_dict,
        index_etf_ticker_dict,
        commodity_etf_ticker_dict,
        country_etf_ticker_dict,
        volatility_etf_ticker_dict

    ]

    for d in datasource:
        for ticker in d["data"]:
            t = yf.Ticker(ticker)
            info = t.info
            info_dict[ticker] = {
                "name":info["shortName"] if "shortName" in info.keys() else None,
                "sector": info["sector"] if "sector" in info.keys() else None,
                "industry": info["industry"] if "industry" in info.keys() else None,
                "category": info["category"] if "category" in info.keys() else None
            }
            print(info_dict[ticker])

    with open("market_info.json", "w") as f:
        f.write(json.dumps(info_dict))


if __name__ == "__main__":
    update_ticker_info()
