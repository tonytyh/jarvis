import boto3
import time

NAME_SPACE = "Jarvis"


class CloudWatchClient:

    def __init__(self):
        self.client = boto3.client("cloudwatch")

    def put_metric(self, name, value, unit, dimensions):
        self.client.put_metric_data(
            Namespace=NAME_SPACE,
            MetricData=[
                {
                    "MetricName": name,
                    "Dimensions": dimensions,
                    "Value": value,
                    "Unit": unit
                }
            ]
        )