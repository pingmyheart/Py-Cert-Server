import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.database import Database

load_dotenv()


def mongo_client() -> Database:
    """
    Create a MongoDB client using environment variables for configuration.

    Returns:
        Database: A MongoDB Database client instance.
    """
    # Load environment variables
    mongo_username = os.getenv("MONGODB_USERNAME")
    mongo_password = os.getenv("MONGODB_PASSWORD")
    mongo_host = os.getenv("MONGODB_HOST")
    mongo_db = os.getenv("MONGODB_DB")

    # Create a MongoDB client
    client = MongoClient(host=mongo_host,
                         username=mongo_username,
                         password=mongo_password,
                         authSource='admin',
                         authMechanism='SCRAM-SHA-1')

    return client[mongo_db]
