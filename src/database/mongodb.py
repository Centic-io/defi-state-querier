import sys

from pymongo import MongoClient

from config import MongoDBConfig
from constants.mongo_constant import MongoDBCollections
from utils.logger_utils import get_logger

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None, database=MongoDBConfig.DATABASE):
        if not connection_url:
            connection_url = MongoDBConfig.CONNECTION_URL

        self.connection_url = connection_url.split('@')[-1]
        try:
            self.connection = MongoClient(connection_url)
            self.mongo_db = self.connection[database]
        except Exception as e:
            logger.exception(f"Failed to connect to MongoDB: {connection_url}: {e}")
            sys.exit(1)
        self._smart_contracts_col = self.mongo_db[MongoDBCollections.smart_contracts]

    def get_token_prices(self, tokens: list, chain_id: str):
        keys = [f"{chain_id}_{token}" for token in tokens]
        data = self._smart_contracts_col.find({"_id": {"$in": keys}})
        result = {}
        for datum in data:
            result[datum.get('address')] = datum.get('price', 1)

        return result
