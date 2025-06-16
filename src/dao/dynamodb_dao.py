import boto3
from boto3.dynamodb.conditions import Key, Attr
from matplotlib.backend_bases import Event

from src.metric.util import add_metric
from src.config.env import *
from src.model.security_data import SecurityData
from src.config.logging_config import get_logger
from decimal import Decimal
import json

from datetime import datetime

logger = get_logger(__name__)
REGION_NAME = None

if current_env == "prod":
    REGION_NAME = "us-west-2"
else:
    REGION_NAME = "us-west-1"

dynamo = boto3.resource('dynamodb', region_name=REGION_NAME)
client = boto3.client("dynamodb")

print(f"Current Region : {REGION_NAME} and current env is : {current_env}")
logger.info(f"Current Region : {REGION_NAME} and current env is : {current_env}")


class SecurityDataDynamodbClient:
    def __init__(self):
        self.dynamodb = dynamo
        self.table_name = "security_data"

    def query_by_date(self, ticker_name, start_date, end_date):

        table = self.dynamodb.Table(self.table_name)
        documents = []

        try:
            response = table.query(
                KeyConditionExpression=Key("publish_date").between(start_date, end_date) & Key("ticker").eq(ticker_name)
            )
            documents.extend(response["Items"])
            LastEvaluatedKey = response['LastEvaluatedKey'] if "LastEvaluatedKey" in response else None

            while LastEvaluatedKey is not None:
                response = table.query(
                    KeyConditionExpression=Key("publish_date").between(start_date, end_date) & Key("ticker").eq(
                        ticker_name),
                    ExclusiveStartKey=LastEvaluatedKey
                )
                LastEvaluatedKey = response['LastEvaluatedKey'] if "LastEvaluatedKey" in response else None
                documents.extend(response["Items"])

            documents.sort(key=lambda x: datetime.strptime(x["publish_date"], "%Y-%m-%d"))
            add_metric("dynamodb_query_security_data_successful")
            return documents

        except Exception as e:
            logger.error(e)
            add_metric("dynamodb_query_security_data_failed")

        return documents

    def insert(self, item: SecurityData):
        change_item = json.loads(item.to_json(), parse_float=Decimal)
        table = self.dynamodb.Table(self.table_name)

        try:
            response = table.put_item(
                Item=change_item,
                ConditionExpression='attribute_not_exists(id)'
            )
            logger.info(f"inserted {item.id}")
            add_metric("dynamodb_insert_security_data_successful")
        # except Exception as e:
        except client.exceptions.ConditionalCheckFailedException as e:
            logger.debug(f"{item.id} already exists")
        except Exception as e:
            logger.error(f"failed to insert {item.id} because {e}")
            add_metric("dynamodb_insert_security_data_failed")


class EventDynamodbClient:

    def __init__(self):
        self.dynamodb = dynamo
        self.table_name = "event"

    def insert(self, event: Event):
        table = self.dynamodb.Table(self.table_name)
        change_item = json.loads(event.to_json(), parse_float=Decimal)

        try:
            response = table.put_item(
                Item=change_item,
                ConditionExpression='attribute_not_exists(event_category) AND attribute_not_exists(event_type)'
            )
            logger.info(f"inserted {event.event_category}/{event.event_type}/{event.event_item}")
            add_metric("dynamodb_insert_event_successful")
        except client.exceptions.ConditionalCheckFailedException as e:
            logger.debug(f"{event.event_category}/{event.event_type}/{event.event_item} exists")
        except Exception as e:
            logger.error(
                f"failed to insert {event.event_category}/{event.event_type}/{event.event_item} because {e}")
            add_metric("dynamodb_insert_event_failed")

    def query_by_category_item_and_date(self, event_category, event_item, start_date, end_date):

        table = self.dynamodb.Table(self.table_name)
        documents = []

        LastEvaluatedKey = None
        try:
            response = table.query(
                KeyConditionExpression=Key("event_category").eq(event_category),
                FilterExpression=Attr("event_item").eq(event_item) & Attr("event_date").between(start_date, end_date)
            )

            documents.extend(response["Items"])
            LastEvaluatedKey = response['LastEvaluatedKey'] if "LastEvaluatedKey" in response else None
            while LastEvaluatedKey is not None:
                response = table.query(
                    KeyConditionExpression=Key("event_category").eq(event_category),
                    ExclusiveStartKey=LastEvaluatedKey,
                    FilterExpression=Attr("event_item").eq(event_item) & Attr("event_date").between(start_date, end_date)
                )
                LastEvaluatedKey = response['LastEvaluatedKey'] if "LastEvaluatedKey" in response else None

                documents.extend(response["Items"])
            add_metric("dynamodb_query_event_successful")
            return documents

        except Exception as e:
            logger.error(e)
            add_metric("dynamodb_query_event_failed")

        return documents
