import os
from datetime import datetime, timezone, timedelta

import pandas as pd

from src.config.logging_config import get_logger
from src.notification.util import send_crash_event
from src.reporter.report_factory import GeneralPerformanceReport, LongTermPerformanceReport, TechnicalPerformanceReport, \
    TrendPerformanceReport
from src.reporter.util import get_ticker_last_data_and_change, generate_tmp_pdf, \
    get_performance_dataframe_by_date, get_performance_dataframe, get_oscillator_technical_signal_dataframe_by_data, \
    get_moving_average_technical_signal_dataframe_by_data, get_trend_technical_signal_dataframe_by_data
from src.updater.market_symbol import sp500_ticker_dict, sp500_top10_ticker_dict, nasdaq_top100_ticker_dict

import pdfkit
import time
import tempfile

from src.storage.S3Handler import S3Client

logger = get_logger(__name__)


def generate_performance_report_last_n_day(title, file_name: str, n: int, datasource: dict):
    try:
        last = n
        data = get_performance_dataframe(datasource["data"], last)
        report_date = data.columns[0].strftime("%Y-%m-%d")
        html_object_name = f"{report_date}/html/{report_date}-{file_name}-last-{last}-day-performance-{int(time.time())}.html"
        csv_object_name = f"{report_date}/csv/{report_date}-{file_name}-last-{last}-day-performance-{int(time.time())}.csv"
        report_agent = GeneralPerformanceReport(data, title)
        html_output = report_agent.render()
        csv_output = data.to_csv()
        tmp_name = os.path.join(os.getcwd(), "out.tmp")
        s3_client = S3Client()
        with open(tmp_name, "w") as f:
            f.write(html_output)
        s3_client.upload_file(tmp_name, html_object_name)
        os.remove(tmp_name)
        with open(tmp_name, "w") as f:
            f.write(csv_output)
        s3_client.upload_file(tmp_name, csv_object_name)
        os.remove(tmp_name)
    except Exception as e:
        logger.error(e)
        send_crash_event(e, datasource["name"])


def generate_long_term_performance_report(title: str, file_name: str, datasource: dict):
    try:
        title = title
        last_days = [-1, -2, -6, -11, -21, -61, -121, -251]
        data = get_performance_dataframe_by_date(datasource=datasource["data"], last_days=last_days)
        report_date = data.columns[0].strftime("%Y-%m-%d")
        data = data.iloc[:, 1:]
        html_object_name = f"{report_date}/html/{report_date}-{file_name}-long-term-performance-{int(time.time())}.html"
        csv_object_name = f"{report_date}/csv/{report_date}-{file_name}-long-term-performance-{int(time.time())}.csv"
        report_agent = LongTermPerformanceReport(data.sort_index(), title)
        html_output = report_agent.render()
        csv_output = data.to_csv()
        tmp_name = os.path.join(os.getcwd(), "out.tmp")
        s3_client = S3Client()
        with open(tmp_name, "w") as f:
            f.write(html_output)
        s3_client.upload_file(tmp_name, html_object_name)
        os.remove(tmp_name)
        with open(tmp_name, "w") as f:
            f.write(csv_output)
        s3_client.upload_file(tmp_name, csv_object_name)
        os.remove(tmp_name)

    except Exception as e:
        logger.error(e)
        send_crash_event(e, datasource["name"])


def generate_technical_signal_report(title: str, file_name: str, datasource: dict, last_day):
    try:
        oscillator_data = get_oscillator_technical_signal_dataframe_by_data(datasource=datasource["data"],
                                                                            last_days=last_day)
        moving_average_data = get_moving_average_technical_signal_dataframe_by_data(datasource=datasource["data"],
                                                                                    last_days=last_day)

        raw_data = pd.concat([oscillator_data, moving_average_data])

        if len(raw_data) == 0:
            logger.info(f"The {title} report for last {last_day} days is empty, no need to generate the report ")
            return
        data = raw_data.sort_values(by=["ticker", "indicator", "action_date"])
        data = data.reset_index(drop=True)

        report_agent = TechnicalPerformanceReport(data, title)
        html_output = report_agent.render()
        start_date = (datetime.now() - timedelta(days=last_day)).strftime("%Y-%m-%d")
        end_date = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d")

        csv_object_name = f"{end_date}/csv/{start_date}-to-{end_date}-{file_name}-technical-performance-{int(time.time())}.csv"
        html_object_name = f"{end_date}/html/{start_date}-to-{end_date}-{file_name}-technical-performance-{int(time.time())}.html"

        tmp_name = os.path.join(os.getcwd(), "out.tmp")
        data.to_csv(tmp_name)
        s3_client = S3Client()
        s3_client.upload_file(tmp_name, csv_object_name)
        os.remove(tmp_name)

        tmp_name = os.path.join(os.getcwd(), "out.tmp")
        with open(tmp_name, "w") as f:
            f.write(html_output)
        s3_client = S3Client()
        s3_client.upload_file(tmp_name, html_object_name)
        os.remove(tmp_name)

    except Exception as e:
        logger.error(e)
        send_crash_event(e, datasource["name"])


def generate_trend_performance_report(title: str, file_name: str, datasource: dict, last_day):
    try:
        trend_data = get_trend_technical_signal_dataframe_by_data(datasource=datasource["data"],
                                                                  last_days=last_day)

        if len(trend_data) == 0:
            logger.info(f"The {title} report for last {last_day} days is empty, no need to generate the report ")
            return
        data = trend_data.sort_values(by=["ticker", "trend_type", "action_date"])

        report_agent = TrendPerformanceReport(data, title)
        html_output = report_agent.render()
        start_date = (datetime.now() - timedelta(days=last_day)).strftime("%Y-%m-%d")
        end_date = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d")

        csv_object_name = f"{end_date}/csv/{start_date}-to-{end_date}-{file_name}-trend-performance-{int(time.time())}.csv"
        html_object_name = f"{end_date}/html/{start_date}-to-{end_date}-{file_name}-trend-performance-{int(time.time())}.html"

        tmp_name = os.path.join(os.getcwd(), "out.tmp")
        data.to_csv(tmp_name)
        s3_client = S3Client()
        s3_client.upload_file(tmp_name, csv_object_name)
        os.remove(tmp_name)

        tmp_name = os.path.join(os.getcwd(), "out.tmp")
        with open(tmp_name, "w") as f:
            f.write(html_output)
        s3_client = S3Client()
        s3_client.upload_file(tmp_name, html_object_name)
        os.remove(tmp_name)

    except Exception as e:
        logger.error(e)
        send_crash_event(e, datasource["name"])


if __name__ == "__main__":
    # df = get_performance_dataframe_last_n_day(nasdaq_top100_ticker, 14)
    # reporter = GeneralPerformanceReport(df, "Nasdaq Top 100 Performance")
    # with open("out.html", "w") as f:
    #     f.write(reporter.render())
    # generate_sp_500_top_10_report_last_n_day(14)
    # generate_sp_500_report_last_n_day(14)

    # generate_long_term_performance_report("Nasdaq Top 100 Performance", "nasdaq-top-100", nasdaq_top100_ticker_dict)
    generate_trend_performance_report("Nasdaq Top 100 Performance", "", nasdaq_top100_ticker_dict, 5)
