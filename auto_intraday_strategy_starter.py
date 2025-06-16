import argparse
import time

import schedule

from src.notification.util import send_task_email_report
from src.realtime_strategy.price_strategy import RealtimePriceChange, RealtimePriceChangeAggregate
from src.realtime_strategy.volume_strategy import RealtimeVolumeIncrease
from src.notification.email_notification import trend_realtime_alert, volume_realtime_alert, \
    price_change_realtime_alert
from src.config.logging_config import get_logger
from src.Task import StrategyTaskScheduler, StrategyTask
from src.util.dao_util import get_realtime_strategy_data_config
from src.updater.market_symbol import future_ticker_dict, nasdaq_top100_ticker_dict, sp500_ticker_dict, \
    crypto_ticker_dict, forex_ticker_dict, \
    sector_etf_ticker_dict, commodity_etf_ticker_dict, index_etf_ticker_dict, country_etf_ticker_dict, \
    volatility_etf_ticker_dict

from datetime import datetime, timedelta, timezone

from src.realtime_strategy.trend_strategy import RealtimeMa20PriceUpTrendLast5, RealtimeMa20PriceDownTrendLast5
from src.updater.market_symbol_cn import sse_180_ticker_dict

logger = get_logger(__name__)


def run_trend_strategy(datasource):
    scheduler = StrategyTaskScheduler()

    for ticker_name in sorted(datasource["data"]):
        task_data = get_realtime_strategy_data_config(ticker_name, "5d", "1h")
        logger.info(f"working on the realtime data from {ticker_name}")

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=RealtimeMa20PriceUpTrendLast5,
                task_result_handler=scheduler.collect_result,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=RealtimeMa20PriceDownTrendLast5,
                task_result_handler=scheduler.collect_result,
                task_data=task_data,
                task_result=None
            )
        )

    scheduler.wait_for_task_completed()

    res_list = []
    while not scheduler.queue.empty():
        event_list = scheduler.queue.get()
        for e in event_list:
            if (datetime.fromtimestamp(e.event_date / 1000) + timedelta(hours=2)).astimezone(
                    timezone.utc) >= datetime.now().astimezone(timezone.utc):
                res_list.append(e)

    if len(res_list) > 0:
        trend_realtime_alert(prefix=datasource["name"], title="Trend Alert", event_list=res_list)
    logger.info(f" run_trend_strategy Sent {len(res_list)} events by email")

def run_price_change_strategy(datasource):
    scheduler = StrategyTaskScheduler()
    for ticker_name in sorted(datasource["data"]):
        task_data = get_realtime_strategy_data_config(ticker_name, "5d", "1h")
        logger.info(f"working on the realtime data from {ticker_name}")

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=RealtimePriceChangeAggregate,
                task_result_handler=scheduler.collect_result,
                task_data=task_data,
                task_result=None
            )
        )

    scheduler.wait_for_task_completed()

    res_list = []
    while not scheduler.queue.empty():
        event_list = scheduler.queue.get()
        for e in event_list:
            if ((datetime.fromtimestamp(e.event_date / 1000) + timedelta(hours=2)).astimezone(
                    timezone.utc) >= datetime.now().astimezone(timezone.utc)):
                res_list.append(e)

    if len(res_list) > 0:
        price_change_realtime_alert(prefix=datasource["name"], title="Price Change Alert",
                                    event_list=res_list)
    logger.info(f" run_price_change_strategy Sent {len(res_list)} events by email")


@send_task_email_report("auto_intraday_strategy_starter us_short_task")
def us_short_task():
    run_price_change_strategy(future_ticker_dict)
    run_price_change_strategy(crypto_ticker_dict)
    run_price_change_strategy(forex_ticker_dict)

    run_trend_strategy(future_ticker_dict)
    run_trend_strategy(crypto_ticker_dict)
    run_trend_strategy(forex_ticker_dict)


@send_task_email_report("auto_intraday_strategy_starter us_long_task")
def us_long_task():
    run_price_change_strategy(nasdaq_top100_ticker_dict)
    run_price_change_strategy(sp500_ticker_dict)
    run_price_change_strategy(sector_etf_ticker_dict)
    run_price_change_strategy(index_etf_ticker_dict)
    run_price_change_strategy(commodity_etf_ticker_dict)
    run_price_change_strategy(country_etf_ticker_dict)
    run_price_change_strategy(volatility_etf_ticker_dict)


@send_task_email_report("auto_intraday_strategy_starter cn_long_task")
def cn_long_task():
    run_price_change_strategy(sse_180_ticker_dict)


def us_task():
    us_short_task()
    us_long_task()


def cn_task():
    cn_long_task()


def auto():
    schedule.every().hour.at(":05").do(us_task)
    schedule.every().hour.at(":05").do(cn_task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="realtime strategy generator")
    parser.add_argument("--mode", help="auto/manual ", required=True)
    args = parser.parse_args()
    if args.mode == "auto":
        auto()
    else:
        us_task()
        cn_task()
