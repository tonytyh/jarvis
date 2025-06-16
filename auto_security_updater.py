import argparse

import schedule
import time

from src.notification.util import send_task_email_report
from src.config.logging_config import get_logger
from src.updater.market_symbol import sp500_ticker_dict, nasdaq_top100_ticker_dict, future_ticker_dict, \
    crypto_ticker_dict, \
    volatility_etf_ticker_dict, country_etf_ticker_dict, commodity_etf_ticker_dict, index_etf_ticker_dict, \
    sector_etf_ticker_dict, forex_ticker_dict
from src.updater.security_data_updater import update_all_data_by_period
from src.updater.market_symbol_cn import sse_180_ticker_dict

logger = get_logger(__name__)


@send_task_email_report("auto_security_updater us_task")
def us_task():
    logger.info("+++++++++++++++++++++++++Start ingest data ++++++++++++++++++++++++")
    update_all_data_by_period(sp500_ticker_dict, "1mo")
    update_all_data_by_period(nasdaq_top100_ticker_dict, "1mo")
    update_all_data_by_period(sector_etf_ticker_dict, "1mo")
    update_all_data_by_period(index_etf_ticker_dict, "1mo")
    update_all_data_by_period(commodity_etf_ticker_dict, "1mo")
    update_all_data_by_period(country_etf_ticker_dict, "1mo")
    update_all_data_by_period(volatility_etf_ticker_dict, "1mo")
    update_all_data_by_period(forex_ticker_dict, "1mo")
    update_all_data_by_period(crypto_ticker_dict, "1mo")
    logger.info("+++++++++++++++++++++++++End ingest data ++++++++++++++++++++++++++")


@send_task_email_report("auto_security_updater cn_task")
def cn_task():
    logger.info("+++++++++++++++++++++++++Start ingest data ++++++++++++++++++++++++")
    update_all_data_by_period(sse_180_ticker_dict, "1mo")
    logger.info("+++++++++++++++++++++++++End ingest data ++++++++++++++++++++++++++")


def auto():
    schedule.every().day.at("21:10").do(us_task)
    schedule.every().day.at("21:20").do(us_task)
    schedule.every().day.at("21:30").do(us_task)
    schedule.every().day.at("21:40").do(us_task)
    schedule.every().day.at("21:50").do(us_task)

    schedule.every().day.at("09:10").do(cn_task)
    schedule.every().day.at("09:20").do(cn_task)
    schedule.every().day.at("09:30").do(cn_task)
    schedule.every().day.at("09:40").do(cn_task)
    schedule.every().day.at("09:50").do(cn_task)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="security data updator")
    parser.add_argument("--mode", help="auto/manual ", required=True)
    args = parser.parse_args()
    if args.mode == "auto":
        auto()
    else:
        us_task()
        cn_task()
