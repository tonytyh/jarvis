import time
import random

from src.metric.util import push_latency_metric


@push_latency_metric("just test")
def foo():
    time.sleep(0.0001)


if __name__ == "__main__":
    for i in range(1000):
        print(f"{i} ")
        foo()
