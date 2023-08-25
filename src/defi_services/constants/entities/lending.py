from defi_services.constants.chain_constant import Chain
from defi_services.services.lending.aave_v2_services import AaveV2StateService


class Lending:
    # service
    aave_v2 = "aave-v2"
    all = [aave_v2]

    # chain
    ethereum = {
        aave_v2: AaveV2StateService
    }

    # mapping
    mapping = {
        Chain.ethereum: ethereum
    }

