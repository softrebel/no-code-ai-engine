from .config import *
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(name="tasks.manage_order")
def manage_order(order_id: str) -> bool:
    logger.info(order_id)
    return True
