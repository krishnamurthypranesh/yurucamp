from datetime import datetime


def get_current_datetime():
    return datetime.utcnow()


def get_current_date():
    return datetime.utcnow().date()
