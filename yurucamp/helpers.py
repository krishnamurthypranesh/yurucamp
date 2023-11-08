from datetime import datetime

import ksuid


def get_current_datetime():
    return datetime.utcnow()


def get_current_date():
    return datetime.utcnow().date()


def generate_id():
    return str(ksuid.Ksuid())
