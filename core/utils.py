from datetime import datetime, timezone

import requests
from cryptography.fernet import Fernet
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from celery.utils.log import get_logger


logger = get_logger(__name__)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def timestamp_utc_now():
    dt = datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = int(utc_time.timestamp())

    return utc_timestamp


def get_utc_datetime():
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return utc_time


def encrypt(text, key=b"AayCd4+++N7Y9vzrjAz+/xViD/rf3hC29HFt28LaIYQ="):
    text = text.encode()
    fernet = Fernet(key)
    return fernet.encrypt(text).decode()


def decrypt(text, key=b"AayCd4+++N7Y9vzrjAz+/xViD/rf3hC29HFt28LaIYQ="):
    text = text.encode()
    fernet = Fernet(key)
    return fernet.decrypt(text).decode()
