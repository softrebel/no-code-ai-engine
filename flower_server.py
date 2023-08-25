from os import system
from core import settings

system(
    f'./venv/bin/celery --broker="{settings.REDIS_BROKER}" flower --address=0.0.0.0 --basic_auth={settings.USER_FLOWER}:{settings.PASS_FLOWER}'
)
