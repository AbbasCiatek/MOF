import sys
from typing import Optional

from beanie import init_beanie
from motor.core import (
    AgnosticClient,
    AgnosticCollection,
    AgnosticDatabase,
)
from motor.motor_asyncio import AsyncIOMotorClient

from mof.apienv import apienv
from mof.auth.models.session_doc import SessionDocument
from mof.firm.models.firm_doc import FirmDocument
from mof.logger import logger
from mof.user.models.user_doc import UserDocument

async_mongodb_client = None


def get_mongodb_config():
    config = {
        "username": apienv.DB_USER,
        "password": apienv.DB_PASS,
        "host": apienv.DB_HOST,
        "db": apienv.DB_NAME,
        "url": apienv.DB_URL,
    }
    return config


def get_async_mongodb_client() -> AgnosticClient:
    global async_mongodb_client
    if async_mongodb_client is None:
        config = get_mongodb_config()
        url = config.get("url")
        print(f"Connecting to mongodb at {url}")
        async_mongodb_client = AsyncIOMotorClient(url)
    return async_mongodb_client


def get_async_mongodb_database(db_name: Optional[str] = None) -> AgnosticDatabase:
    if db_name is None:
        db_name = get_mongodb_config().get("db")
    client = get_async_mongodb_client()
    return client[db_name]


def get_async_mongodb_collection(col_name: str) -> AgnosticCollection:
    db = get_async_mongodb_database()
    return db[col_name]


async def start_async_mongodb() -> AgnosticDatabase:
    try:
        logger.log(0, "Starting Mongodb Connection")
        async_mongodb_database = get_async_mongodb_database()
        await init_beanie(
            database=async_mongodb_database,
            document_models=[UserDocument, SessionDocument, FirmDocument],
        )
        logger.log(0, "started mongodb connection")
        return async_mongodb_database
    except Exception as e:
        logger.exception(f"Failed to start mongodb. error={e}")
        sys.exit(1)
