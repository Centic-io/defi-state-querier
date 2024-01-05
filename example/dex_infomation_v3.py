import json
import os

from dotenv import load_dotenv

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor
from src.defi_services.databases.mongodb_klg import MongoDB

load_dotenv()

provider_url = {
    '0x1': os.environ.get("ETHEREUM_PROVIDER"),
    '0x38': os.environ.get("BSC_PROVIDER"),
    '0x89': os.environ.get("POLYGON_PROVIDER"),
    '0xfa': os.environ.get("FANTOM_PROVIDER"),
    '0xa4b1': os.environ.get("ARBITRUM_PROVIDER"),
    '0xa': os.environ.get("OPTIMISM_PROVIDER"),
    '0xa86a': os.environ.get("AVALANCHE_PROVIDER"),
    '0x2b6653dc': os.environ.get("TRON_PROVIDER")
}


def get_lp_token_list(job, wallet, dex_protocol):
    token_info = get_token_info()

    queries = [
        {
            'query_id': f'{dex_protocol}_lptokenlist',
            "entity_id": dex_protocol,
            'query_type': Query.farming_lp_token_list,
            'number_lp': 10,
            'supplied_data': {"token_info": list(token_info.keys())}
        }]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/lp_token_list.json', 'w') as f:
        json.dump(res, f)


def get_lp_token_info(job, wallet, dex_protocol):
    with open('test/lp_token_list.json', 'r') as f:
        data = json.loads(f.read())

    # data = {"0x3416cf6c708da44db2624d63ea0aaef7113527c6": {
    #     "token0": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    #     "token1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    #     "fee": "100"
    #   },
    #   "0x7858e59e0c01ea06df3af3d20ac7b0003275d4bf": {
    #     "token0": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    #     "token1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    #     "fee": "500"
    #   },
    #   "0xee4cf3b78a74affa38c6a926282bcd8b5952818d": {
    #     "token0": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    #     "token1": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    #     "fee": "3000"
    #   }
    # }
    queries = [
        {
            'query_id': f'{dex_protocol}_lptokeninfo',
            "entity_id": dex_protocol,
            'query_type': Query.lp_token_info,
            'supplied_data': {
                'lp_token_info': data[0][Query.farming_lp_token_list]}
        },
        {
            'query_id': f'{dex_protocol}_lptokenbalance',
            "entity_id": dex_protocol,
            'query_type': Query.token_pair_balance,
            'supplied_data': {
                'lp_token_info': data[0][Query.farming_lp_token_list]}
        }
    ]
    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/lp_token_info.json', 'w') as f:
        json.dump(res, f)


###USER
def get_user_nft(job, wallet, dex_protocol):
    queries = [
        {
            'query_id': f'{dex_protocol}_usernft',
            "entity_id": dex_protocol,
            'query_type': Query.dex_user_nft
        }
    ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/user_nft.json', 'w') as f:
        json.dump(res, f)


def get_user_info(job, wallet, dex_protocol):
    with open('test/user_nft.json', 'r') as f:
        data = json.loads(f.read())
    with open('test/lp_token_info.json', 'r') as f:
        token_pair_balance = json.loads((f.read()))[1].get('token_pair_balance')

    queries = [
        {
            'query_id': f'{dex_protocol}_userinfo',
            "entity_id": dex_protocol,
            'query_type': Query.dex_user_info,
            'supplied_data': {
                'user_data': data[0][Query.dex_user_nft],
                'lp_token_info': token_pair_balance
            }
        }
    ]

    res = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/user_info.json', 'w') as f:
        json.dump(res, f)


def get_token_info():
    mongo_klg = MongoDB()
    res = {}
    tokens = mongo_klg.get_top_1000_token(chain_id)
    for token in tokens:
        token_addr = token.get("address")
        decimals = token.get("decimals")
        price = token.get("price")
        res[token_addr] = {
            'decimals': decimals,
            'price': price
        }
    return res


if __name__ == "__main__":
    w = "0x1deb69730edc38e1989032f686a1e1b70f3c380f"
    dex_ids = [Dex.pancake_v3]

    for chain_id in [Chain.bsc, Chain.ethereum, Chain.fantom, Chain.polygon, Chain.arbitrum, Chain.avalanche]:
        for dex_id in dex_ids:

            try:
                job_ = StateProcessor(provider_url[chain_id], chain_id)
                if dex_id in job_.services:
                    # get_lp_token_list(job=job_, wallet=w, dex_protocol=dex_id)
                    # get_lp_token_info(job=job_, wallet=w, dex_protocol=dex_id)
                    # get_user_nft(job=job_, wallet=w, dex_protocol=dex_id)
                    get_user_info(job=job_, wallet=w, dex_protocol=dex_id)
                    # get_user_reward(job=job_, wallet=w, dex_protocol=dex_id)
                    # export_to_mongodb(chain_id, dex_id)
                    print(f'export {dex_id}  in {chain_id}')
            except Exception as ex:
                print(f'Error with chain {chain_id}')
                raise ex
