from concurrent.futures import ThreadPoolExecutor

import yfinance as yf
from datetime import datetime
import time
import random

from src.metric.util import push_latency_metric
from src.model.security_data import SecurityData
from src.config.logging_config import get_logger
from src.dao.dynamodb_dao import SecurityDataDynamodbClient
import numpy as np
import math
logger = get_logger(__name__)


def parse_history(ticker_name, records):
    documents = []
    for publish_date in records:
        values = records[publish_date]
        datetime_string = publish_date.strftime("%Y-%m-%d")
        id_name = ticker_name + "-" + datetime_string
        if values["Open"] == np.nan or values["Open"] == np.NAN or math.isnan(values["Open"]):
            continue
        documents.append(
            SecurityData(
                id_name=id_name,
                ticker_name=ticker_name.upper(),
                publish_date=datetime_string,
                open_price=values["Open"],
                high_price=values["High"],
                low_price=values["Low"],
                close_price=values["Close"],
                volume=values["Volume"],
                dividends=values["Dividends"],
                stock_splits=values["Stock Splits"],
                update_date=datetime.timestamp(datetime.now())
            )
        )

    return documents


@push_latency_metric(operation_name="yfinance.history")
def get_yfinance_data_by_period(ticker_name: str, period: str):
    t = yf.Ticker(ticker_name)
    h = t.history(period)
    return h


@push_latency_metric(operation_name="yfinance.history")
def get_yfinance_data_by_period_with_interval(ticker_name: str, period: str, interval: str):
    t = yf.Ticker(ticker_name)
    h = t.history(period=period, interval=interval)
    return h


# get the history prices of a given ticker.
def update_one_ticker_price_by_period(ticker_name: str, period: str):
    wait_random_time()
    dynamo = SecurityDataDynamodbClient()
    h = get_yfinance_data_by_period(ticker_name=ticker_name, period=period)
    records = h.to_dict("index")
    documents = parse_history(ticker_name, records)
    for item in documents:
        dynamo.insert(item)


@push_latency_metric(operation_name="yfinance.history")
def get_yfinance_data_by_date(ticker_name: str, start_date: str, end_date: str):
    t = yf.Ticker(ticker_name)
    h = t.history(start=start_date, end=end_date)
    return h


def update_one_ticker_with_by_date(ticker_name: str, start_date: str, end_date: str):
    wait_random_time()
    dynamo = SecurityDataDynamodbClient()

    h = get_yfinance_data_by_date(ticker_name=ticker_name, start_date=start_date, end_date=end_date)

    records = h.to_dict("index")
    documents = parse_history(ticker_name, records)
    for item in documents:
        dynamo.insert(item)


def update_all_data_by_period(datasource, period: str):
    futures = []
    pool = ThreadPoolExecutor(4)
    for t in datasource["data"]:
        futures.append(pool.submit(update_one_ticker_price_by_period, t, period))
    for future in futures:
        future.result()


def update_all_date_by_date(dateset, start_date, end_date):
    futures = []
    pool = ThreadPoolExecutor(4)
    for t in dateset["data"]:
        futures.append(pool.submit(update_one_ticker_with_by_date, t, start_date, end_date))

    for future in futures:
        future.result()

def wait_random_time():
    sleep_time = random.random() / 2
    time.sleep(sleep_time)


if __name__ == "__main__":
    update_one_ticker_price_by_period("600028.SS","1mo")
