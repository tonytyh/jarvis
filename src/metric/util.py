import time
from datetime import datetime

from src.metric.cloudwatch import CloudWatchClient

cloud_watch_client = CloudWatchClient()


def push_latency_metric(operation_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            cloud_watch_client.put_metric(
                name="Latency",
                value=int((end_time - start_time) * 1000),
                unit="Milliseconds",
                dimensions=[{
                    "Name": "Operation",
                    "Value": operation_name
                }]
            )

            cloud_watch_client.put_metric(
                name="Calls",
                value=1,
                unit="Count",
                dimensions=[{
                    "Name": "Operation",
                    "Value": operation_name
                }]
            )

            return result
        return wrapper
    return decorator


def add_metric(operation_name):
    cloud_watch_client.put_metric(
        name="Calls",
        value=1,
        unit="Count",
        dimensions=[{
            "Name": "Operation",
            "Value": operation_name
        }]
    )
