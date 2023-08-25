from datetime import datetime, timezone


def timestamp_utc_now():
    dt = datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = int(utc_time.timestamp())

    return utc_timestamp
