import logging
import time

from pymongo import MongoClient, UpdateOne

from config import MongoDBConfig
logger = logging.getLogger("MongodbStreamingExporter")


class MongoExporter(object):
    def __init__(self,

                collector_id,
                db_prefix,
                 chain_id,
                 connection_url=None,
                database = MongoDBConfig.DATABASE,
                # collector = MongoDBConfig.COLLECTORS,
                event_collection = None):
        self._conn = None
        if not connection_url:
            connection_url = MongoDBConfig.CONNECTION_URL
        self.mongo = MongoClient(connection_url)
        if db_prefix:
            mongo_db_str = db_prefix + "_" + database
        else:
            mongo_db_str = database
        self.mongo_db = self.mongo[mongo_db_str]
        # self.mongo_collectors = self.mongo_db[collector]
        # self.collector_id = collector_id
        if event_collection:
            self.event = self.mongo_db[event_collection]
        else:
            self.event = self.mongo_db[collector_id]
        self.chain_id = chain_id

    def open(self):
        pass
    def export_items(self, items):
        self.export_events(items)

    def export_events(self, operations_data):
        if not operations_data:
            logger.debug(f"Error: Don't have any data to write")
            return
        start = time.time()
        bulk_operations = [UpdateOne({'_id': f"{self.chain_id}_{data['lp_token']}_{data['master_chef_address']}"}, {"$set": data}, upsert=True) for data in operations_data]
        logger.info("Updating into events ........")
        try:
            self.event.bulk_write(bulk_operations)
        except Exception as bwe:
            logger.error(f"Error: {bwe}")
        end = time.time()
        logger.info(f"Success write events to database take {end - start}s")

    def close(self):
        pass
