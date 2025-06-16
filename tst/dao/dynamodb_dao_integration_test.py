from datetime import datetime
import time

from src.dao.dynamodb_dao import EventDynamodbClient
from src.model.event import TechnicalAnalysisOfflineEvent_BuyAndSell


def test_insert_event():
    e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
        "Ma5Ma2Buy",
        "TSLA",
        45,
        "buy",
        datetime.now()
    )
    event_dynamodb_client = EventDynamodbClient()
    event_dynamodb_client.insert(e)
