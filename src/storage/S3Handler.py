import boto3
from botocore.exceptions import ClientError

from src.config.logging_config import get_logger

logger = get_logger(__name__)


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")
        self.bucket_name = "jarvis-report-us-west-2"

    def upload_file(self, file_name, object_name):
        try:
            logger.info(f"Uploading file to {object_name}")
            response = self.client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logger.error(f"Failed to upload {object_name}")
