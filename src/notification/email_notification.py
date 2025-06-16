import time
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

from src.reporter.report_factory import TrendEventReport, VolumeAbnormalIncreaseReport, PriceChangeReport
from src.config.logging_config import get_logger
from src.model.event import Event

logger = get_logger(__name__)


class AmazonSESClient:
    def __init__(self):
        self.client = boto3.client("ses", region_name="us-west-2")
        self.recipient = ""

    def _send_html_email(self, sender, recipient, subject, body):

        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except Exception as e:
            logger.error(e)

    def _send_text_email(self, sender, recipient, subject, body):

        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': "UTF-8",
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        except Exception as e:
            logger.error(e)

    def send_event(self, sender, subject, html_body):
        self._send_html_email(sender, self.recipient, subject, html_body)

    def send_text_event(self, sender, subject, text_body):
        self._send_text_email(sender, self.recipient, subject, text_body)


def print_event(event_list: list):
    for e in event_list:
        print(e)


def trend_realtime_alert(prefix: str, title: str, event_list: list):
    ses_client = AmazonSESClient()
    current_date = datetime.now().astimezone(timezone.utc)
    current_hour = current_date.strftime("%Y-%m-%d-%H")
    email_subject = f"{prefix} {title}"
    subject = f"[{current_hour}] {prefix} {title}"
    reporter = TrendEventReport(subject=subject, event_list=event_list)
    html_body = reporter.render()
    ses_client.send_event(sender=f"{prefix}-Price-Trend-Alert@yunhantang.com", subject=email_subject, html_body=html_body)


def volume_realtime_alert(prefix: str, title: str, event_list: list):
    ses_client = AmazonSESClient()
    current_date = datetime.now().astimezone(timezone.utc)
    current_hour = current_date.strftime("%Y-%m-%d-%H")
    email_subject = f"{prefix} {title}"
    subject = f"[{current_hour}] {prefix} {title}"
    reporter = VolumeAbnormalIncreaseReport(subject=subject, event_list=event_list)
    html_body = reporter.render()
    ses_client.send_event(sender=f"{prefix}-Volume-Alert@yunhantang.com", subject=email_subject, html_body=html_body)


def price_change_realtime_alert(prefix: str, title: str, event_list: list):
    ses_client = AmazonSESClient()
    current_date = datetime.now().astimezone(timezone.utc)
    current_hour = current_date.strftime("%Y-%m-%d-%H")
    email_subject = f"{prefix} {title}"
    subject = f"[{current_hour}] {prefix} {title}"
    reporter = PriceChangeReport(subject=subject, event_list=event_list)
    html_body = reporter.render()
    ses_client.send_event(sender=f"{prefix}-Price-Change-Alert@yunhantang.com", subject=email_subject, html_body=html_body)
