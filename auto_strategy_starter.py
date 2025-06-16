import argparse
import time

import schedule

from src.notification.util import send_task_email_report
from src.config.logging_config import get_logger
from src.Task import StrategyTaskScheduler, StrategyTask
from src.strategy.moving_average_strategy import Ma20Ma60Buy, Ma20Ma60Sell, Ma5Ma20Sell, Ma5Ma20Buy, Ma5Ma10Buy, \
    Ma5Ma10Sell, Ma10Ma20Sell, Ma10Ma20Buy
from src.util.dao_util import get_strategy_data_config
from src.updater.event_updater import push_event
from src.updater.market_symbol import sp500_ticker_dict, nasdaq_top100_ticker_dict, future_ticker_dict, \
    sector_etf_ticker_dict, \
    index_etf_ticker_dict, commodity_etf_ticker_dict, country_etf_ticker_dict, crypto_ticker_dict

from datetime import datetime, timedelta

from src.strategy.oscillator_strategy import Rsi6OverSold, Rsi6OverBought, MacdBuy, MacdSell
from src.strategy.trend_strategy import Ma20PriceUpTrendLast7, Ma20PriceDownTrendLast7, Ma5PriceUpTrendLast3, \
    Ma5PriceDownTrendLast3, MaPriceStrongUptrend, MaPriceStrongDownTrend, Ma10PriceUpTrendLast5, Ma10PriceDownTrendLast5
from src.updater.market_symbol_cn import sse_180_ticker_dict

logger = get_logger(__name__)


def run_moving_average_strategy(datasource):
    scheduler = StrategyTaskScheduler()

    for ticker_name in sorted(datasource["data"]):
        start_date_str = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date_str = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        task_data = get_strategy_data_config(ticker_name, start_date_str, end_date_str)
        logger.info(f"working on the data from {ticker_name} from {start_date_str} to {end_date_str}")

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma20Ma60Buy,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )
        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma20Ma60Sell,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma10Ma20Sell,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma10Ma20Buy,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma5Ma20Sell,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma5Ma20Buy,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma5Ma10Buy,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )
        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma5Ma10Sell,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

    scheduler.wait_for_task_completed()


def run_trend_strategy(datasource):
    scheduler = StrategyTaskScheduler()

    for ticker_name in sorted(datasource["data"]):
        start_date_str = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")
        end_date_str = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        task_data = get_strategy_data_config(ticker_name, start_date_str, end_date_str)
        logger.info(f"working on the data from {ticker_name} from {start_date_str} to {end_date_str}")

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma10PriceUpTrendLast5,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma10PriceDownTrendLast5,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )
        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma20PriceUpTrendLast7,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma20PriceDownTrendLast7,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma5PriceUpTrendLast3,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Ma5PriceDownTrendLast3,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

    scheduler.wait_for_task_completed()


def run_strong_trend_strategy(datasource):
    scheduler = StrategyTaskScheduler()

    for ticker_name in sorted(datasource["data"]):
        start_date_str = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")
        end_date_str = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        task_data = get_strategy_data_config(ticker_name, start_date_str, end_date_str)
        logger.info(f"working on the data from {ticker_name} from {start_date_str} to {end_date_str}")

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=MaPriceStrongUptrend,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=MaPriceStrongDownTrend,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.wait_for_task_completed()


def run_oscillator_strategy(datasource):
    scheduler = StrategyTaskScheduler()

    for ticker_name in sorted(datasource["data"]):
        start_date_str = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")
        end_date_str = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        task_data = get_strategy_data_config(ticker_name, start_date_str, end_date_str)
        logger.info(f"working on the data from {ticker_name} from {start_date_str} to {end_date_str}")

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=MacdBuy,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=MacdSell,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Rsi6OverBought,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

        scheduler.start_task(
            StrategyTask(
                task_strategy_handler=Rsi6OverSold,
                task_result_handler=push_event,
                task_data=task_data,
                task_result=None
            )
        )

    scheduler.wait_for_task_completed()


@send_task_email_report("auto_strategy_starter us_task")
def us_task():
    run_moving_average_strategy(sp500_ticker_dict)
    run_moving_average_strategy(nasdaq_top100_ticker_dict)
    run_moving_average_strategy(sector_etf_ticker_dict)
    run_moving_average_strategy(index_etf_ticker_dict)
    run_moving_average_strategy(commodity_etf_ticker_dict)
    run_moving_average_strategy(country_etf_ticker_dict)
    run_moving_average_strategy(future_ticker_dict)
    run_moving_average_strategy(crypto_ticker_dict)

    run_trend_strategy(sp500_ticker_dict)
    run_trend_strategy(nasdaq_top100_ticker_dict)
    run_trend_strategy(sector_etf_ticker_dict)
    run_trend_strategy(index_etf_ticker_dict)
    run_trend_strategy(commodity_etf_ticker_dict)
    run_trend_strategy(country_etf_ticker_dict)
    run_trend_strategy(future_ticker_dict)
    run_trend_strategy(crypto_ticker_dict)

    run_strong_trend_strategy(sp500_ticker_dict)
    run_strong_trend_strategy(nasdaq_top100_ticker_dict)
    run_strong_trend_strategy(sector_etf_ticker_dict)
    run_strong_trend_strategy(index_etf_ticker_dict)
    run_strong_trend_strategy(commodity_etf_ticker_dict)
    run_strong_trend_strategy(country_etf_ticker_dict)
    run_strong_trend_strategy(future_ticker_dict)
    run_strong_trend_strategy(crypto_ticker_dict)

    run_oscillator_strategy(sp500_ticker_dict)
    run_oscillator_strategy(nasdaq_top100_ticker_dict)
    run_oscillator_strategy(sector_etf_ticker_dict)
    run_oscillator_strategy(index_etf_ticker_dict)
    run_oscillator_strategy(commodity_etf_ticker_dict)
    run_oscillator_strategy(country_etf_ticker_dict)
    run_oscillator_strategy(future_ticker_dict)
    run_oscillator_strategy(crypto_ticker_dict)


@send_task_email_report("auto_strategy_starter cn_task")
def cn_task():
    run_moving_average_strategy(sse_180_ticker_dict)
    run_trend_strategy(sse_180_ticker_dict)
    run_strong_trend_strategy(sse_180_ticker_dict)
    run_oscillator_strategy(sse_180_ticker_dict)


def auto():
    schedule.every().day.at("22:10").do(us_task)
    schedule.every().day.at("10:10").do(cn_task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="strategy generator")
    parser.add_argument("--mode", help="auto/manual ", required=True)
    args = parser.parse_args()
    if args.mode == "auto":
        auto()
    else:
        us_task()
        cn_task()
