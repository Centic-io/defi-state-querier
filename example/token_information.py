from defi_services.abis.token.erc20_abi import ERC20_ABI
from defi_services.jobs.state_querier import StateQuerier

queries = {
    "symbol": {
        "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "abi": ERC20_ABI,
        "function": "symbol",
        "params": [],
        "block_number": "latest"
    },
    "total_supply": {
        "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "abi": ERC20_ABI,
        "function": "totalSupply",
        "params": [],
        "block_number": "latest"
    },
    "decimals": {
        "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "abi": ERC20_ABI,
        "function": "decimals",
        "params": [],
        "block_number": "latest"
    },
    "balance_of": {
        "address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "abi": ERC20_ABI,
        "function": "balanceOf",
        "params": ["0x36696169C63e42cd08ce11f5deeBbCeBae652050"],
        "block_number": 30984033
    }
}

job = StateQuerier("https://rpc.ankr.com/bsc")
response_data = job.query_state_data(queries=queries)
print(response_data)