import json
import os

from dotenv import load_dotenv

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.constants.entities.dex_info_constant import DexInfo
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor

from defi_services.databases.mongodb_exporter import MongoExporter

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
    """Get all LP"""
    queries = [
        # {
        #     'query_id': f'{dex_protocol}_{Query.lp_token_list}',
        #     "entity_id": dex_protocol,
        #     'query_type': Query.lp_token_list,
        #     'number_lp': 20
        # },
        {
            'query_id': f'{dex_protocol}_{Query.farming_lp_token_list}',
            "entity_id": dex_protocol,
            'query_type': Query.farming_lp_token_list,
            # 'number_lp': 20
        }
    ]

    lp_token_list = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('test/lp_token_list.json', 'w') as f:
        json.dump(lp_token_list, f, indent=2)

    return lp_token_list


def get_lp_token_info(job, wallet, dex_protocol):
    with open('test/lp_token_list.json') as f:
        lp_token_list = json.load(f)

    # Input Format
    # lp_token_info = {
    #     "0x168b273278f3a8d302de5e879aa30690b7e6c28f": {
    #         "pid": 4
    #     },
    #     "0xdd5bad8f8b360d76d12fda230f8baf42fe0022cf": {
    #         "farming_pid": 5
    #     },
    #     "0x3dcb1787a95d2ea0eb7d00887704eebf0d79bb13": {
    #         "farming_pid": 8
    #     }
    # }
    lp_token_info = {}
    # lp_token_info.update(dict(list(lp_token_list[0][Query.lp_token_list].items())))
    lp_token_info.update(dict(list(lp_token_list[0][Query.farming_lp_token_list].items())))

    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.lp_token_info}',
            "entity_id": dex_protocol,
            'query_type': Query.lp_token_info,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]
    lp_token_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('test/lp_token_info.json', 'w') as f:
        json.dump(lp_token_info, f, indent=2)

    return lp_token_info


def get_lp_token_liquidity(job, wallet, dex_protocol):
    with open('test/lp_token_info.json') as f:
        lp_token_info = json.load(f)
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    # Input format
    # lp_token_info = {
    #       "0x06da0fd433c1a5d7a4faa01111c044910a184553": {
    #         "total_supply": 0.08599627202057003,
    #         "token0": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    #         "token1": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    #         "name": "SushiSwap LP Token",
    #         "decimals": 18,
    #         "stake_balance": 0.08245173084735195,
    #         "acc_reward_per_share": 13.87566465730498,
    #         "alloc_point": 1100,
    #         "farming_pid": 0
    #       },
    #       "0x397ff1542f962076d0bfe58ea045ffa2d347aca0": {
    #         "total_supply": 0.0739607160789963,
    #         "token0": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    #         "token1": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    #         "name": "SushiSwap LP Token",
    #         "decimals": 18,
    #         "stake_balance": 0.05191755786871983,
    #         "acc_reward_per_share": 15.913618906828649,
    #         "alloc_point": 3000,
    #         "farming_pid": 1
    #       },
    #     "0xe7e656893030187f1073e5b2d768e3c1e8861f26": {
    #         "total_supply": 1.0,
    #         "token0": None,
    #         "token1": None,
    #         "name": "Bsc Dummy Token",
    #         "decimals": 0,
    #         "stake_balance": 1.0,
    #         "acc_reward_per_share": 4571214724711396.0,
    #         "alloc_point": 0,
    #         "farming_pid": 359
    #     },
    #     "0xcb277e48526f30f625e24850cf293d89301ea470": {
    #         "total_supply": 1.0,
    #         "token0": None,
    #         "token1": None,
    #         "name": "Bttc Dummy Token",
    #         "decimals": 0,
    #         "stake_balance": 1.0,
    #         "acc_reward_per_share": 2.0635693678518308e+16,
    #         "alloc_point": 450,
    #         "farming_pid": 360
    #     },
    #     "0x11b66abb675b955bd6f066fde849442865c60e29": {
    #         "total_supply": 1.0,
    #         "token0": None,
    #         "token1": None,
    #         "name": "OP Dummy Token",
    #         "decimals": 0,
    #         "stake_balance": 1.0,
    #         "acc_reward_per_share": 4.407230162602343e+16,
    #         "alloc_point": 0,
    #         "farming_pid": 361
    #     }
    # }

    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.token_pair_balance}',
            "entity_id": dex_protocol,
            'query_type': Query.token_pair_balance,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]
    lp_token_token_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('test/token_pair_balance.json', 'w') as f:
        json.dump(lp_token_token_info, f, indent=2)

    return lp_token_token_info


# TEST USER INFO ##
def get_user_info(job, wallet, dex_protocol):
    with open('test/lp_token_info.json') as f:
        lp_token_info = json.load(f)
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    with open('test/token_pair_balance.json') as f:
        lp_token_liquidity_info = json.load(f)
    lp_token_liquidity_info = lp_token_liquidity_info[0][Query.token_pair_balance]

    for lp_token, info in lp_token_info.items():
        info.update(lp_token_liquidity_info[lp_token])

    # Input format
    # lp_token_info = {
    #     "0x168b273278f3a8d302de5e879aa30690b7e6c28f": {
    #         "pid": 4,
    #         "token0": "0xad6caeb32cd2c308980a548bd0bc5aa4306c6c18",
    #         "token1": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
    #         "total_supply": 1200.2464779364304,
    #         "decimals": 18,
    #         "token0_amount": 18448.04236946028,
    #         "token1_amount": 121.70884726666941,
    #         "stake_balance": 0.0,
    #         "token0_stake_amount": 0.0,
    #         "token1_stake_amount": 0.0
    #     },
    #     "0xdd5bad8f8b360d76d12fda230f8baf42fe0022cf": {
    #         "farming_pid": 5,
    #         "token0": "0x7083609fce4d1d8dc0c979aab8c869ea2c873402",
    #         "token1": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
    #         "total_supply": 7255.38761224426,
    #         "decimals": 18,
    #         "token0_amount": 50582.682462821846,
    #         "token1_amount": 1362.10369903655,
    #         "stake_balance": 3862.313577411147,
    #         "token0_stake_amount": 26927.049483659805,
    #         "token1_stake_amount": 725.0986290177685
    #     },
    #     "0x3dcb1787a95d2ea0eb7d00887704eebf0d79bb13": {
    #         "farming_pid": 8,
    #         "token0": "0x4b0f1812e5df2a09796481ff14017e6005508003",
    #         "token1": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
    #         "total_supply": 16407.43254875897,
    #         "decimals": 18,
    #         "token0_amount": 352605.673046255,
    #         "token1_amount": 1561.1056042802186,
    #         "stake_balance": 10681.897524257238,
    #         "token0_stake_amount": 229560.4540660897,
    #         "token1_stake_amount": 1016.3424435791009
    #     }
    # }

    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.dex_user_info}',
            "entity_id": dex_protocol,
            'query_type': Query.dex_user_info,
            'supplied_data': {
                'lp_token_info': lp_token_info
            },
            'stake': True
        }
    ]

    user_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/dex_user_info.json', 'w') as f:
        json.dump(user_info, f, indent=2)

    return user_info


def get_user_reward(job, wallet, dex_protocol):
    with open('test/lp_token_info.json') as f:
        lp_token_info = json.load(f)
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    # Input Format
    # lp_token_info = {
    #     "0x168b273278f3a8d302de5e879aa30690b7e6c28f": {
    #         "pid": 4
    #     },
    #     "0xdd5bad8f8b360d76d12fda230f8baf42fe0022cf": {
    #         "farming_pid": 5
    #     },
    #     "0x3dcb1787a95d2ea0eb7d00887704eebf0d79bb13": {
    #         "farming_pid": 8
    #     }
    # }

    queries = [
        {
            'query_id': f'{dex_protocol}_{Query.protocol_reward}',
            "entity_id": dex_protocol,
            'query_type': Query.protocol_reward,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]

    user_reward = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('test/dex_user_reward.json', 'w') as f:
        json.dump(user_reward, f, indent=2)

    return user_reward


def export_to_mongodb(chain_id, dex_protocol):
    with open('test/lp_token_info.json', 'r') as f:
        data = json.loads(f.read())
        lp_token_info = data[0].get('lp_token_info')
    with open('test/token_pair_balance.json', 'r') as f:
        data = json.loads(f.read())
        token_pair_balance = data[0].get('token_pair_balance')

    lastest_info = []
    for lp_token, value in lp_token_info.items():
        lptoken_dict = {}
        lptoken_dict['lp_token'] = lp_token
        lptoken_dict['master_chef_address'] = DexInfo.mapping.get(chain_id).get(dex_protocol).get('master_chef_address')
        lptoken_dict['service'] = dex_protocol
        lptoken_dict.update(value)

        if lp_token in token_pair_balance:
            value2 = token_pair_balance[lp_token]
            lptoken_dict.update(value2)

        lastest_info.append(lptoken_dict)

    item_exporter = MongoExporter(collector_id='lptoken', db_prefix='', chain_id=chain_id)
    item_exporter.export_items(lastest_info)


if __name__ == "__main__":
    w = "0x89089fd89dfEdC7350861C99b71DABF4fdEA2fc0"
    dex_ids = [Dex.sushi_v2, Dex.spooky_v2, Dex.quickswap_v2]

    for chain_id in [Chain.bsc, Chain.ethereum, Chain.fantom, Chain.polygon, Chain.arbitrum, Chain.avalanche]:
        for dex_id in dex_ids:
            try:
                job_ = StateProcessor(provider_url[chain_id], chain_id)
                if dex_id in job_.services:
                    # get_lp_token_list(job=job_, wallet=w, dex_protocol=dex_id)
                    # get_lp_token_info(job=job_, wallet=w, dex_protocol=dex_id)
                    get_lp_token_liquidity(job=job_, wallet=w, dex_protocol=dex_id)
                    get_user_info(job=job_, wallet=w, dex_protocol=dex_id)
                    # get_user_reward(job=job_, wallet=w, dex_protocol=dex_id)
                    export_to_mongodb(chain_id, dex_id)
                    print(f'export {dex_id}  in {chain_id}')
            except Exception as ex:
                print(f'Error with chain {chain_id}')
                raise ex
