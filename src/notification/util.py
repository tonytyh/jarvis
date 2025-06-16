import time
from datetime import datetime, timezone

from src.notification.email_notification import AmazonSESClient

email_client = AmazonSESClient()


def send_task_email_report(operation_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            current_date = datetime.now().astimezone(timezone.utc)
            date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')

            email_client.send_text_event(
                sender="Task-Report@yunhantang.com",
                subject=f"{operation_name} Report ",
                text_body=f"The {operation_name} was finished at {date_str}. The total execution time is {round(end_time - start_time,2)} seconds"
            )

            return result

        return wrapper

    return decorator


def send_crash_event(e, data):
    current_date = datetime.now().astimezone(timezone.utc)
    date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')
    email_client.send_text_event(
        sender="Crash-Report@yunhantang.com",
        subject=f"Crash Report",
        text_body=f"The system was crashed at {date_str}. "
                  f"\n\n The error was : {str(e)} "
                  f"\n\n The data was {str(data)}"
    )


