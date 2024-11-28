import json
import time

from defi_services.jobs.tcv import TCV
from defi_services.services.vault.vault_info.arbitrum.tcv_arb import TCV_VAULT_ARBITRUM

addresses = [
    # "0xebe714023617FF6D2e59FdBa33ADFd166F9668b6",
    # "0x805d0d2ae6D777Be7C126bf75330F0E471D9D584",
    # "0xa21957306BD617E489f2A4070975e5Abf4F6F1AF",
    # "0x1fDe5D126d3380A255b65929637AEe719fc5F895",
    # "0x357c71ccB434D1b2A4e0265b31F8b6c7e4265fd4",
    "0xc724c8cB5db8bb39Bca44D2Da43f8B2F97af2991",
    # "0x480751fE6145978564249916Ec4C217eC8df90cd",
    # "0xE4d50470a463370CD14852311f5491dE88609a01",
    # "0xD617E75f30a432E7ea158501f9E4fD6Ce92cD2dC",
    # "0x6325ae204778fa9DB0f873E09ae0c38A80f41381",
    # "0x6FE548250913Ecd37C77Da9ce0785afE4C4A3da1"
]

job = TCV(provider_uri="https://arbitrum-one-rpc.publicnode.com", chain_id="0xa4b1")

data = {}
for address in addresses:
    start_time = time.time()
    tvl_info = job.get_tvl_info(address, TCV_VAULT_ARBITRUM.get("reservesList"))
    data[address] = tvl_info
    print(f'[{round(time.time() - start_time, 3)}s] Executed {address} - info {tvl_info}')


with open('../test/tcv_wallets.json', 'w') as f:
    json.dump(data, f, indent=2)
