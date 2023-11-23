import os
from web3 import Web3

from defi_services.abis.dex.pancakeswap.masterchef_v0_abi import PANCAKESWAP_MASTERCHEF_V0_ABI
from defi_services.abis.dex.pancakeswap.pancakeswap_masterchef_v2_abi import PANCAKESWAP_MASTERCHEF_V2_ABI
from defi_services.constants.token_constant import ContractAddresses
from defi_services.jobs.processors.dex_state_processor import DexStateProcessor

def test_pancake_v2_processor_job():
    provider_uri = os.environ.get("BSC_PROVIDER", "https://bsc-dataseed4.binance.org/")
    user ="0x17c29152f2f4183528b14267bb6a3eec026e8125"

    job=DexStateProcessor(provider_uri,PANCAKESWAP_MASTERCHEF_V2_ABI, ContractAddresses.PANCAKE_FARM_V2)
    web3 = Web3(Web3.HTTPProvider(provider_uri))
    master_chef_contract= web3.eth.contract(abi=PANCAKESWAP_MASTERCHEF_V2_ABI, address=ContractAddresses.PANCAKE_FARM_V2)
    pool_length = master_chef_contract.functions.poolLength().call()
    lp_token_list = []
    for pid in range(0, int(pool_length/5)):
        lp_token = master_chef_contract.functions.lpToken(pid).call()
        lp_token_list.append(lp_token)

    job.run(lp_token_list,user, batch_size = 100, max_workers = 8,ignore_error= True)

def test_pancake_v0_processor_job():
    provider_uri = os.environ.get("BSC_PROVIDER", "https://bsc-dataseed4.binance.org/")
    user = "0x17c29152f2f4183528b14267bb6a3eec026e8125"
    job = DexStateProcessor(provider_uri, PANCAKESWAP_MASTERCHEF_V0_ABI, ContractAddresses.PANCAKE_FARM)
    web3 = Web3(Web3.HTTPProvider(provider_uri))
    master_chef_addr = ContractAddresses.PANCAKE_FARM
    if web3.isAddress(master_chef_addr):
        master_chef_addr = web3.toChecksumAddress(master_chef_addr)
    master_chef_contract = web3.eth.contract(abi=PANCAKESWAP_MASTERCHEF_V0_ABI, address=master_chef_addr)
    pool_length = master_chef_contract.functions.poolLength().call()
    lp_token_list = []
    for pid in range(0, int(pool_length / 10)):
        pool_info = master_chef_contract.functions.poolInfo(pid).call()
        lp_token_list.append(pool_info[0])
    job.run(lp_token_list, user, batch_size=100, max_workers=8, ignore_error=True)

if __name__ == "__main__":
    test_pancake_v2_processor_job()