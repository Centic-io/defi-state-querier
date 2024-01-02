import json

from defi_services.constants.chain_constant import Chain
from defi_services.constants.entities.dex_constant import Dex
from defi_services.constants.query_constant import Query
from defi_services.jobs.processors.state_processor import StateProcessor

provider_url = {
    "0x38": 'https://bsc-dataseed3.binance.org/',
    '0x1': "https://rpc.ankr.com/eth",
    '0xfa': "https://rpc.ankr.com/fantom",
    '0xa': "https://optimism.llamarpc.com",
    '0xa4b1': "https://rpc.ankr.com/arbitrum",
    '0xa86a': "https://rpc.ankr.com/avalanche",
    '0x89': "https://rpc.ankr.com/polygon"
}


def get_lp_token_list(_dex_protocol):
    """Get all LP"""
    queries = [
        {
            'query_id': f'{_dex_protocol}_{Query.lp_token_list}',
            "entity_id": _dex_protocol,
            'query_type': Query.lp_token_list,
            'number_lp': 200
        },
        {
            'query_id': f'{_dex_protocol}_{Query.farming_lp_token_list}',
            "entity_id": _dex_protocol,
            'query_type': Query.farming_lp_token_list,
            'number_lp': 200
        }
    ]

    lp_token_list = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('../test/lp_token_list.json', 'w') as f:
        json.dump(lp_token_list, f, indent=2)

    return lp_token_list


def get_lp_token_info(_dex_protocol):
    with open('../test/lp_token_list.json') as f:
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
    lp_token_info.update(dict(list(lp_token_list[0][Query.lp_token_list].items())[-2:]))
    lp_token_info.update(dict(list(lp_token_list[1][Query.farming_lp_token_list].items())[-2:]))

    queries = [
        {
            'query_id': f'{_dex_protocol}_{Query.lp_token_info}',
            "entity_id": _dex_protocol,
            'query_type': Query.lp_token_info,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]
    lp_token_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('../test/lp_token_info.json', 'w') as f:
        json.dump(lp_token_info, f, indent=2)

    return lp_token_info


def get_lp_token_liquidity(_dex_protocol):
    with open('../test/lp_token_info.json') as f:
        lp_token_info = json.load(f)

    # Input format
    # lp_token_info = {
    #     "0x168b273278f3a8d302de5e879aa30690b7e6c28f": {
    #         "pid": 4,
    #         "token0": "0xad6caeb32cd2c308980a548bd0bc5aa4306c6c18",
    #         "token1": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    #     },
    #     "0xdd5bad8f8b360d76d12fda230f8baf42fe0022cf": {
    #         "farming_pid": 5,
    #         "token0": "0x7083609fce4d1d8dc0c979aab8c869ea2c873402",
    #         "token1": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    #     },
    #     "0x3dcb1787a95d2ea0eb7d00887704eebf0d79bb13": {
    #         "farming_pid": 8,
    #         "token0": "0x4b0f1812e5df2a09796481ff14017e6005508003",
    #         "token1": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    #     }
    # }
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    queries = [
        {
            'query_id': f'{_dex_protocol}_{Query.token_pair_balance}',
            "entity_id": _dex_protocol,
            'query_type': Query.token_pair_balance,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]
    lp_token_token_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)

    with open('../test/token_pair_balance.json', 'w') as f:
        json.dump(lp_token_token_info, f, indent=2)

    return lp_token_token_info


# TEST USER INFO ##
def get_user_info(_dex_protocol):
    with open('../test/lp_token_info.json') as f:
        lp_token_info = json.load(f)
    lp_token_info = lp_token_info[0][Query.lp_token_info]

    with open('../test/token_pair_balance.json') as f:
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
            'query_id': f'{_dex_protocol}_{Query.dex_user_info}',
            "entity_id": _dex_protocol,
            'query_type': Query.dex_user_info,
            'supplied_data': {
                'lp_token_info': lp_token_info
            },
            'stake': True
        }
    ]

    user_info = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('../test/dex_user_info.json', 'w') as f:
        json.dump(user_info, f, indent=2)

    return user_info


def get_user_reward(_dex_protocol):
    with open('../test/lp_token_info.json') as f:
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
            'query_id': f'{_dex_protocol}_{Query.protocol_reward}',
            "entity_id": _dex_protocol,
            'query_type': Query.protocol_reward,
            'supplied_data': {
                'lp_token_info': lp_token_info
            }
        }
    ]

    user_reward = job.run(wallet, queries, batch_size=100, max_workers=8, ignore_error=True)
    with open('../test/dex_user_reward.json', 'w') as f:
        json.dump(user_reward, f, indent=2)

    return user_reward


if __name__ == "__main__":
    wallet = "0x89089fd89dfEdC7350861C99b71DABF4fdEA2fc0"
    dex_protocol = Dex.sushi

    for chain_id in [Chain.ethereum]:
        try:
            job = StateProcessor(provider_url[chain_id], chain_id)
            get_lp_token_list(dex_protocol)
            get_lp_token_info(dex_protocol)
            get_lp_token_liquidity(dex_protocol)
            get_user_info(dex_protocol)
            get_user_reward(dex_protocol)
        except Exception as ex:
            print(f'Error with chain {chain_id}')
            raise ex
