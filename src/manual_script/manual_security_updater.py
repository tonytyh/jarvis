from src.config.logging_config import get_logger
from src.updater.market_symbol import *
from src.updater.security_data_updater import update_all_data_by_period, update_all_date_by_date
from src.updater.market_symbol_cn import sse_180_ticker_dict

logger = get_logger(__name__)


def task():
    logger.info("+++++++++++++++++++++++++Start ingest data ++++++++++++++++++++++++")
    # update_all_data_by_period(future_ticker, "1y")
    update_all_date_by_date(dateset=sse_180_ticker_dict, start_date="2021-01-01", end_date="2022-03-06")
    logger.info("+++++++++++++++++++++++++End ingest data ++++++++++++++++++++++++++")


if __name__ == "__main__":
    task()