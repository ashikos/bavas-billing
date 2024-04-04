from datetime import datetime


def convert_str_to_datetime(date_str, format):
    """Convert str date to datetime object"""

    date_obj = datetime.strptime(date_str, format)
    return date_obj
