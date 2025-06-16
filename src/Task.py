import concurrent
import queue
import threading
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

from src.config.logging_config import get_logger
from src.notification.util import send_crash_event

logger = get_logger(__name__)


class StrategyTask:

    def __init__(self, task_strategy_handler, task_result_handler, task_data, task_result):
        self.task_strategy_handler = task_strategy_handler
        self.task_data = task_data
        self.task_result_handler = task_result_handler
        self.task_result = task_result

    def execute(self):
        try:
            self.task_result = self.task_strategy_handler(self.task_data).execute_strategy()
        except Exception as e:
            logger.error(e)
            logger.error(f"Task data was : {self.task_data}" )
            send_crash_event(e, self.task_data)
        if self.task_result_handler is not None:
            try :
                self.task_result_handler(self.task_result)
            except Exception as e1:
                logger.error(e1)
                logger.error(f"Task data was : {self.task_data}")
                send_crash_event(e1, self.task_data)



class StrategyTaskScheduler:

    def __init__(self):
        self.futures = []
        self.pool = ThreadPoolExecutor(6)
        self.queue = queue.Queue()

    def start_task(self, task: StrategyTask):
        self.futures.append(self.pool.submit(task.execute))

    def wait_for_task_completed(self):
        for future in concurrent.futures.as_completed(self.futures):
            future.result()

    def collect_result(self, result):
        self.queue.put(result)
