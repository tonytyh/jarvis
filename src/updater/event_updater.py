from src.config.logging_config import get_logger
from src.dao.dynamodb_dao import EventDynamodbClient


logger = get_logger(__name__)

eventDynamodbClient = EventDynamodbClient()


def push_event(event_list: list):
    for e in event_list:
        eventDynamodbClient.insert(e)
