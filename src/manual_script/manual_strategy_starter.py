import argparse

from src.Task import StrategyTaskScheduler, StrategyTask
from src.strategy.moving_average_strategy import Ma5Ma10Buy
from src.updater.event_updater import push_event
from src.util.dao_util import get_strategy_data_config


def run_ma_strategy(ticker):
    scheduler = StrategyTaskScheduler()
    scheduler.start_task(

        StrategyTask(
            task_strategy_handler=Ma5Ma10Buy,
            task_result_handler=push_event,
            task_data=get_strategy_data_config(ticker, "2000-01-01", "2100-01-01"),
            task_result=None
        )
    )
    scheduler.wait_for_task_completed()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="manual offline strategy starter")

    parser.add_argument("--ticker", help="ticker name")
    args = parser.parse_args()
    run_ma_strategy(args.ticker)
