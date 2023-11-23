
from pymongo import MongoClient

import logging

from config import MongoDbKLGConfig
logger = logging.getLogger("MongoDB")


class MongoDB:
    def __init__(self, graph=None):
        if not graph:
            graph = MongoDbKLGConfig.HOST

        self.connection_url = graph.split("@")[-1]
        self.connection = MongoClient(graph)
        self.mongo_db = self.connection[MongoDbKLGConfig.KLG_DATABASE]

        self._wallets_col = self.mongo_db["wallets"]
        self._multichain_wallets_col = self.mongo_db["multichain_wallets"]
        self._multichain_wallets_credit_scores_col = self.mongo_db[
            "multichain_wallets_credit_scores_v3"

        ]
        self._smart_contracts_col = self.mongo_db["smart_contracts"]

        self._profiles_col = self.mongo_db["profiles"]

        self._configs_col = self.mongo_db["configs"]

        # self._create_index()

    #######################
    #       Index         #
    #######################

    # def _create_index(self):
    #     ...

    def get_smart_contract(self, chain_id, address):
        address = address.lower()
        key = f"{chain_id}_{address}"
        filter_ = {"_id": key}
        return self.mongo_db["smart_contracts"].find_one(filter_)

    #######################
    #       Token         #
    #######################
    def get_tokens_by_keys(self, keys, projection):
        filter_statement = {
            "idCoingecko": {"$exists": True},
            "_id": {"$in": keys}
        }
        cursor = self._smart_contracts_col.find(filter_statement, projection)
        return cursor

    #######################
    #      Wallets        #
    #######################

    # @sync_log_time_exe(tag=TimeExeTag.databases)
    # def get_wallet(self, address, chain_id=None):
    #     if chain_id is None:
    #         filter_statement = {'_id': address}
    #         doc = self._multichain_wallets_col.find_one(filter_statement)
    #     else:
    #         filter_statement = {'_id': f'{chain_id}_{address}'}
    #         doc = self._wallets_col.find_one(filter_statement)
    #     return doc

    # @sync_log_time_exe(tag=TimeExeTag.databases)
    # def get_wallets_with_batch_idx(self, batch_idx=1, batch_size=10000, chain_id=None, projection=None):
    #     projection_statement = self.get_projection_statement(projection)
    #     if chain_id is None:
    #         filter_statement = {'flagged': batch_idx}
    #         cursor = self._multichain_wallets_col.find(filter=filter_statement, projection=projection_statement, batch_size=batch_size)
    #     else:
    #         filter_statement = {'flagged': batch_idx, 'chainId': chain_id}
    #         cursor = self._wallets_col.find(filter=filter_statement, projection=projection_statement, batch_size=batch_size)
    #     return cursor

    # @sync_log_time_exe(tag=TimeExeTag.databases)
    # def get_selective_wallet_addresses(self, batch_size=10000):
    #     filter_statement = {'selective': True}
    #     projection_statement = self.get_projection_statement(['address'])
    #     cursor = self._wallets_col.find(filter=filter_statement, projection=projection_statement, batch_size=batch_size)
    #     data = [doc['address'] for doc in cursor]
    #     return data

    # def check_exists_wallets(self, addresses, batch_size):
    #     keys = []
    #     for address in addresses:
    #         keys.extend([f'{chain_id}_{address}' for chain_id in ChainConstant.all])

    #     filter_statement = {'_id': {'$in': keys}}
    #     cursor = self._multichain_wallets_col.find(filter=filter_statement, projection=['chainId', 'address', 'createdAt'], batch_size=batch_size)
    #     wallets = []
    #     for doc in cursor:
    #         wallets.append({
    #             'chain_id': doc['chainId'],
    #             'address': doc['address'],
    #             'created_at': doc.get('createdAt')
    #         })
    #     return wallets

    def get_wallet_addresses(
        self, chain_id=None, batch_size=100000, update_created_at=False
    ):
        try:
            if chain_id:
                filter_statement = {"chainId": chain_id}
                cursor = self._wallets_col.find(
                    filter=filter_statement,
                    projection=["address"],
                    batch_size=batch_size,
                )
            else:
                filter_statement = {}
                if update_created_at:
                    filter_statement = {"updatedCreatedAt": {"$exists": False}}
                cursor = self._multichain_wallets_col.find(
                    filter=filter_statement,
                    projection=["address"],
                    batch_size=batch_size,
                )

            addresses = [doc["address"] for doc in cursor]
            return addresses
        except Exception as ex:
            logger.exception(ex)
            return []



    # @sync_log_time_exe(tag=TimeExeTag.database)
    def get_multichain_wallets_with_flags(self, flag_idx, projection=None, batch_size=10000):
        try:
            filter_statement = {
                "flagged": flag_idx
            }
            projection_statement = self.get_projection_statement(projection)
            cursor = self._multichain_wallets_col.find(filter_statement, projection=projection_statement,
                                                       batch_size=batch_size)
            return cursor
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_multichain_wallets_scores_by_keys(self, keys, projection=None):
        filter_statement = {'_id': {'$in': keys}}
        cursor = self._multichain_wallets_credit_scores_col.find(filter_statement, projection=projection)
        return cursor


    def get_multichain_wallets_scores_by_flag(self, flag_idx, projection=None):
        filter_statement = {'flagged': flag_idx}
        cursor = self._multichain_wallets_credit_scores_col.find(filter_statement, projection=projection)
        return cursor



    def get_wallet_flagged_state(self, chain_id=None):
        if chain_id is None:
            key = 'multichain_wallets_flagged_state'
        else:
            key = f'wallets_flagged_state_{chain_id}'
        filter_statement = {
            "_id": key
        }
        config = self._configs_col.find_one(filter_statement)
        if not config:
            return None
        return config



    @staticmethod
    def get_projection_statement(projection: list = None):
        if projection is None:
            return None

        projection_statements = {}
        for field in projection:
            projection_statements[field] = True

        return projection_statements
