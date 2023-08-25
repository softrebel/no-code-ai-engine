from db import connect_to_mongo, close_mongo_connection
from celery.signals import worker_shutdown, worker_init, worker_init, setup_logging
from core.utils import get_utc_datetime, timestamp_utc_now
from celery import Celery
from core import settings
from core import redis_conn
from celery.utils.log import get_task_logger
from redbeat.schedulers import (
    RedBeatSchedulerEntry,
    get_redis,
    RedBeatConfig,
    get_logger,
    ensure_conf,
)

from logging.config import dictConfig
import celery
from core.logging import celery_log_config


@setup_logging.connect
def setup_logging(**_kwargs):
    dictConfig(celery_log_config)


@worker_init.connect
def setup_worker_init(**kwargs):
    connect_to_mongo()


@worker_shutdown.connect
def setup_worker_shutdown(**kwargs):
    print("bye")
    close_mongo_connection()


app = Celery("tasks", broker=settings.REDIS_BROKER, backend=settings.REDIS_BACKEND)
# add redbeat
app.conf.update(redbeat_redis_url=settings.REDBEAT_REDIS_URL)

logger = get_task_logger(__name__)


class CustomSchedulerEntry(RedBeatSchedulerEntry):
    @classmethod
    def get_all_entries(cls) -> list[RedBeatSchedulerEntry]:
        ensure_conf(app)
        conf = RedBeatConfig(app)
        redis = get_redis(app)
        schedule_keys = redis.zrange(conf.schedule_key, 0, -1)
        entries = [cls.from_key(key, app=app) for key in schedule_keys]
        return entries

    @classmethod
    def get_entry_by_key(cls, key: str) -> RedBeatSchedulerEntry:
        conf = RedBeatConfig(app)
        schedule_key = f"{conf.key_prefix}{key}"
        entry = cls.from_key(schedule_key, app=app)
        return entry

    @classmethod
    def get_entry_by_task_name_and_id(
        cls, task_name: str, id: str
    ) -> RedBeatSchedulerEntry:
        key = cls.encode_key(task_name, id)
        entry = cls.get_entry_by_key(key)
        return entry

    @classmethod
    def remove_by_schedule_key(cls, schedule_key: str) -> None:
        conf = RedBeatConfig(app)
        redis = get_redis(app)
        redis.zrem(conf.schedule_key, schedule_key)
        logger.info(f"removed {schedule_key}")

    @classmethod
    def remove_by_key(cls, key: str) -> None:
        conf = RedBeatConfig(app)
        schedule_key = f"{conf.key_prefix}{key}"
        cls.remove_by_schedule_key(schedule_key)

    @classmethod
    def remove_by_task_name_and_id(cls, task_name: str, id: str) -> None:
        key = cls.encode_key(task_name, id)
        cls.remove_by_key(key)

    @classmethod
    def delete_entry(cls, entry: RedBeatSchedulerEntry) -> None:
        key = entry.key
        entry.delete()
        logger.info(f"deleted {key}")

    @classmethod
    def encode_key(cls, task_name: str, id: str) -> str:
        return f"{task_name:s}::{id:s}"

    @classmethod
    def decode_key(cls, key) -> tuple[str, str]:
        task_name, id = key.split("::")
        return task_name, id

    @classmethod
    def create_entry(
        cls, task_name: str, id: str, args=(), interval=None
    ) -> RedBeatSchedulerEntry:
        interval = (
            interval if interval else celery.schedules.schedule(run_every=60)
        )  # seconds
        name = cls.encode_key(task_name, id)
        entry = cls(name, task_name, interval, args=args, app=app)
        entry.save()
        logger.info(f"started {name}")
        return entry

    @classmethod
    def update_entry(
        cls,
        entry: RedBeatSchedulerEntry,
        interval: celery.schedules.schedule = None,
        args: tuple = None,
    ) -> None:
        if interval:
            entry.schedule = interval
        if args:
            entry.args = args
        entry.save()
        logger.info(f"updated {entry.name}")
