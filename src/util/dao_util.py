from src.model.event_enum import EventCategory
from src.dao.dynamodb_dao import SecurityDataDynamodbClient, EventDynamodbClient
from src.updater.security_data_updater import get_yfinance_data_by_period_with_interval
from datetime import datetime

dynamo_security_data = SecurityDataDynamodbClient()
dynamo_event_data = EventDynamodbClient()


def get_security_data_by_date(ticker_name, start_date, end_date):
    return dynamo_security_data.query_by_date(ticker_name=ticker_name, start_date=start_date, end_date=end_date)


def get_technical_data_by_date(technical_category:EventCategory, ticker_name, start_date, end_date):
    return dynamo_event_data.query_by_category_item_and_date(event_category=technical_category.value, event_item=ticker_name, start_date=(int)(start_date.timestamp()) * 1000, end_date=(int)(end_date.timestamp()) * 1000)


def get_realtime_security_data_by_period(ticker_name, period, interval):
    return get_yfinance_data_by_period_with_interval(ticker_name=ticker_name, period=period, interval=interval)


def get_realtime_strategy_data_config(ticker_name, period, interval):
    data = get_realtime_security_data_by_period(ticker_name, period, interval)
    return {
        "name": ticker_name.upper(),
        "data": data
    }


def get_strategy_data_config(ticker_name, start_date, end_date):
    data = get_security_data_by_date(ticker_name, start_date, end_date)
    return {
        "name": ticker_name.upper(),
        "data": data
    }
