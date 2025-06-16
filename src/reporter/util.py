import json
import tempfile
from datetime import datetime, timedelta, timezone
from queue import PriorityQueue

import pdfkit
from jinja2 import Environment, FileSystemLoader

from src.model.event_enum import EventCategory
from src.config.logging_config import get_logger
from src.core.data import TimeSeriesData
from src.util.dao_util import get_security_data_by_date, get_technical_data_by_date
from src.updater.market_symbol import nasdaq_top100_ticker_dict, sp500_ticker_dict, crypto_ticker_dict

import pandas as pd
import numpy as np

logger = get_logger(__name__)


def get_ticker_last_data_and_change(ticker: str, last: int):
    start_date_str = (datetime.now() - timedelta(days=last)).strftime("%Y-%m-%d")
    end_date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    price_data = get_security_data_by_date(ticker, start_date=start_date_str, end_date=end_date_str)
    t = TimeSeriesData.from_array([float(x["close"]) for x in price_data], [x["publish_date"] for x in price_data])
    price_diff = (t.dataframe.diff().shift(periods=-1) / t.dataframe).shift(periods=1)
    ratio_diff = price_diff * 100
    return price_data, price_diff, ratio_diff


def get_ticker_last_data(ticker: str, last: int):
    start_date_str = (datetime.now() - timedelta(days=last)).strftime("%Y-%m-%d")
    end_date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    price_data = get_security_data_by_date(ticker, start_date=start_date_str, end_date=end_date_str)
    t = TimeSeriesData.from_array([float(x["close"]) for x in price_data], [x["publish_date"] for x in price_data])
    return t.dataframe


def get_ticker_technical_signal_data(technical_category: EventCategory, ticker: str, last: int):
    start_date = (datetime.now().astimezone(timezone.utc) - timedelta(days=last))
    end_date = (datetime.now().astimezone(timezone.utc) + timedelta(days=5))
    technical_signal_data = get_technical_data_by_date(technical_category=technical_category, ticker_name=ticker,
                                                       start_date=start_date,
                                                       end_date=end_date)
    technical_signal_data_list = []
    for event in technical_signal_data:
        raw_json = json.loads(event["event_data"])
        technical_signal_data_list.append(raw_json)
    return technical_signal_data_list


def generate_tmp_html(html: str):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp_name = tmp.name
        tmp.write(html)
    return tmp_name


def generate_tmp_pdf(html: str):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        pdfkit.from_string(html, tmp.name)


class PqElement(object):
    def __init__(self, obj):
        self.ticker = obj[0]
        self.change_in_ratio = obj[1]

    # Custom Compare Function (less than or equsal)
    def __lt__(self, obj):
        """self < obj."""
        return float(self.change_in_ratio[-1:].values[0]) > float(obj.change_in_ratio[-1:].values[0])

    # Print each element function
    def __repr__(self):
        return f'PQE:{self.ticker} : {self.change_in_ratio}'


def get_performance_dataframe(datasource, last: int):
    price_dict = {}
    pq = PriorityQueue()

    for ticker in datasource:
        try:
            price_data, price_diff, change_in_ratio = get_ticker_last_data_and_change(ticker=ticker, last=last + 10)
            if len(price_data) > 0:
                price_dict[ticker] = (price_data, price_diff, change_in_ratio)
                pq.put(PqElement((ticker, change_in_ratio)))
        except Exception as e:
            logger.error(f"Failed to use the {ticker} to generate the report \n {e}")

    report_df = pd.DataFrame()
    while not pq.empty():
        obj = pq.get()
        t, cg = obj.ticker, obj.change_in_ratio
        cg = cg[-last:]
        cg = cg.transpose()
        cg = cg.rename(index={"value": t})

        report_df = pd.concat([report_df, cg])

    rdf = report_df[report_df.columns[::-1]]
    rdf = rdf.round(3)
    return rdf.sort_index()


def get_performance_dataframe_by_date(datasource, last_days: list):
    price_report_df = pd.DataFrame()
    column_idx = None
    for ticker in datasource:
        try:
            price_data = get_ticker_last_data(ticker=ticker, last=400)
            if len(price_data) < np.abs(last_days[-1] or price_data.isnull().values.any() > 0):
                continue
            if column_idx is None:
                column_idx = price_data.index[last_days]
            price_slice = price_data.loc[column_idx]
            price_slice = price_slice.transpose()
            price_slice = price_slice.rename(index={"value": ticker})
            price_report_df = pd.concat([price_report_df, price_slice])
        except Exception as e:
            logger.error(f"Failed to use the {ticker} to generate the report {e}")

    price_diff_ratio_df = pd.DataFrame(columns=price_report_df.columns)

    for i in range(1, len(last_days)):
        price_diff_ratio_df[price_diff_ratio_df.columns.values[i]] = (price_report_df.iloc[:, 0] - price_report_df.iloc[
                                                                                                   :,
                                                                                                   i]) / price_report_df.iloc[
                                                                                                         :, i] * 100
    return price_diff_ratio_df.sort_index()


def get_oscillator_technical_signal_dataframe_by_data(datasource, last_days: int):
    report_df = pd.DataFrame()

    event_in_all = []

    for ticker in datasource:
        try:
            event_list = get_ticker_technical_signal_data(technical_category=EventCategory.OSCILLATOR, ticker=ticker,
                                                          last=last_days)

            event_in_all.extend(event_list)
        except Exception as e:
            logger.error(f"Failed to use the {ticker} to generate the report {e}")

    for e in event_in_all:
        e["action_date"] = datetime.fromtimestamp(e["action_date"] / 1000).astimezone(timezone.utc)

    return pd.DataFrame.from_dict(event_in_all)


def get_moving_average_technical_signal_dataframe_by_data(datasource, last_days: int):
    report_df = pd.DataFrame()

    event_in_all = []

    for ticker in datasource:
        try:
            event_list = get_ticker_technical_signal_data(technical_category=EventCategory.MOVING_AVERAGE,
                                                          ticker=ticker,
                                                          last=last_days)

            event_in_all.extend(event_list)
        except Exception as e:
            logger.error(f"Failed to use the {ticker} to generate the report {e}")

    for e in event_in_all:
        e["action_date"] = datetime.fromtimestamp(e["action_date"] / 1000).astimezone(timezone.utc)

    return pd.DataFrame.from_dict(event_in_all)


def get_trend_technical_signal_dataframe_by_data(datasource, last_days: int):
    report_df = pd.DataFrame()

    event_in_all = []

    for ticker in datasource:
        try:
            event_list = get_ticker_technical_signal_data(technical_category=EventCategory.TREND,
                                                          ticker=ticker,
                                                          last=last_days)

            event_in_all.extend(event_list)
        except Exception as e:
            logger.error(f"Failed to use the {ticker} to generate the report {e}")

    for e in event_in_all:
        e["action_date"] = datetime.fromtimestamp(e["action_date"] / 1000).astimezone(timezone.utc)

    return pd.DataFrame.from_dict(event_in_all)


if __name__ == "__main__":
    # data = get_oscillator_technical_signal_dataframe_by_data(crypto_ticker_dict["data"], last_days=7)
    # data
    data = get_oscillator_technical_signal_dataframe_by_data(nasdaq_top100_ticker_dict["data"], 3)
    print()
