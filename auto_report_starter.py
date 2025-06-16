import argparse

import schedule
import time

from src.notification.util import send_task_email_report
from src.reporter.performance_reporter import \
    generate_long_term_performance_report, generate_performance_report_last_n_day, generate_technical_signal_report, \
    generate_trend_performance_report
from src.config.logging_config import get_logger
from src.updater.market_symbol import nasdaq_top100_ticker_dict, sp500_ticker_dict, future_ticker_dict, \
    crypto_ticker_dict, forex_ticker_dict, \
    sector_etf_ticker_dict, index_etf_ticker_dict, commodity_etf_ticker_dict, volatility_etf_ticker_dict, \
    country_etf_ticker_dict

from src.updater.market_symbol_cn import sse_180_ticker_dict

logger = get_logger(__name__)


@send_task_email_report("auto_report_starter us_task")
def us_task():
    logger.info("+++++++++++++++++++++++++ Generating Report ++++++++++++++++++++++++++++++++")
    generate_performance_report_last_n_day(title="Nasdaq Top 100 Performance Report", file_name="nasdaq-top-100", n=7,
                                           datasource=nasdaq_top100_ticker_dict)

    generate_performance_report_last_n_day(title="S&P 500 Performance Report", file_name="sp500", n=7,
                                           datasource=nasdaq_top100_ticker_dict)

    # long term report

    generate_long_term_performance_report(title="S&P 500 Performance Report", file_name="sp500",
                                          datasource=sp500_ticker_dict)

    generate_long_term_performance_report(title="Nasdaq Top 100 Performance Report", file_name="nasdaq-top-100",
                                          datasource=nasdaq_top100_ticker_dict)

    generate_long_term_performance_report(title="Sector ETF Performance Report", file_name="sector-etf",
                                          datasource=sector_etf_ticker_dict)

    generate_long_term_performance_report(title="Index ETF Performance Report", file_name="index-etf",
                                          datasource=index_etf_ticker_dict)

    generate_long_term_performance_report(title="Commodity ETF Performance Report", file_name="commodity-etf",
                                          datasource=commodity_etf_ticker_dict)

    generate_long_term_performance_report(title="Country ETF Performance Report", file_name="country-etf",
                                          datasource=country_etf_ticker_dict)

    generate_long_term_performance_report(title="Volatility ETF Performance Report", file_name="volatility-etf",
                                          datasource=volatility_etf_ticker_dict)

    generate_long_term_performance_report(title="Future Commodity Performance Report", file_name="future-commodity",
                                          datasource=future_ticker_dict)

    generate_long_term_performance_report(title="Crypto Currency Performance Report", file_name="crypto-currency",
                                          datasource=crypto_ticker_dict)
    # technical report
    generate_technical_signal_report(title="S&P 500 Technical Performance Report", file_name="sp500",
                                     datasource=sp500_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Nasdaq Top 100 Technical Performance", file_name="nasdaq-top-100",
                                     datasource=nasdaq_top100_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Sector ETF Technical Performance Report", file_name="sector-etf",
                                     datasource=sector_etf_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Index ETF Technical Performance Report", file_name="index-etf",
                                     datasource=index_etf_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Commodity ETF Technical Performance Report", file_name="commodity-etf",
                                     datasource=commodity_etf_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Country ETF Technical Performance Report", file_name="country-etf",
                                     datasource=country_etf_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Volatility ETF Technical Performance Report", file_name="volatility-etf",
                                     datasource=volatility_etf_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Future Commodity Technical Performance Report",
                                     file_name="future-commodity",
                                     datasource=future_ticker_dict, last_day=2)

    generate_technical_signal_report(title="Crypto Currency Technical Performance Report", file_name="crypto-currency",
                                     datasource=crypto_ticker_dict, last_day=2)

    ## trend report
    generate_trend_performance_report(title="S&P 500 Trend Performance Report", file_name="sp500",
                                      datasource=sp500_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Nasdaq Top 100 Trend Performance Report", file_name="nasdaq-top-100",
                                      datasource=nasdaq_top100_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Sector ETF Trend Performance Report", file_name="sector-etf",
                                      datasource=sector_etf_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Index ETF Trend Performance Report", file_name="index-etf",
                                      datasource=index_etf_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Commodity ETF Trend Performance Report", file_name="commodity-etf",
                                      datasource=commodity_etf_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Country ETF Trend Performance Report", file_name="country-etf",
                                      datasource=country_etf_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Volatility ETF Trend Performance Report", file_name="volatility-etf",
                                      datasource=volatility_etf_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Future Commodity Trend Performance Report", file_name="future-commodity",
                                      datasource=future_ticker_dict, last_day=2)

    generate_trend_performance_report(title="Crypto Currency Trend Performance Report", file_name="crypto-currency",
                                      datasource=crypto_ticker_dict, last_day=2)

    logger.info("+++++++++++++++++++++++++ Ended report generation ++++++++++++++++++++++++++")


@send_task_email_report("auto_report_starter us_task")
def cn_task():
    generate_long_term_performance_report(title="SSE 180 Performance Report", file_name="sse-180",
                                          datasource=sse_180_ticker_dict)
    generate_technical_signal_report(title="SSE 180 Technical Performance Report", file_name="sse-180",
                                     datasource=sse_180_ticker_dict,
                                     last_day=2)

    generate_trend_performance_report(title="SSE 180 Trend Performance Report", file_name="sse-180",
                                      datasource=sse_180_ticker_dict,
                                      last_day=2)


def auto():
    schedule.every().day.at("22:10").do(us_task)
    schedule.every().day.at("08:10").do(cn_task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="report generator")
    parser.add_argument("--mode", help="auto/manual ", required=True)
    args = parser.parse_args()

    if args.mode == "auto":
        auto()
    else:
        us_task()
        cn_task()
