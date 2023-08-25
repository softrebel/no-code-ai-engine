from pymongo import MongoClient
from bunnet import init_bunnet
from core.config import settings
from schemas import File, User, Model
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

class WorkActionDataBase:
    client: MongoClient = None


AI_DB = WorkActionDataBase()

def connect_to_mongo():
    AI_DB.client = MongoClient(settings.MONGODB_URL)
    init_bunnet(
        database=AI_DB.NoCodeAI,
        document_models=[File, User, Model],
    )
    logger.info("mongodb connected.")


def close_mongo_connection():
    AI_DB.client.close()
    logger.info("mongodb closed.")


def get_mongo_database(db_name=settings.MONGODB_NAME):
    return AI_DB.client[db_name]

