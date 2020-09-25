from datetime import datetime


def get_timestamp(date=datetime.now()):
    return date.strftime('%Y-%m-%dT%H:%M:%S')
