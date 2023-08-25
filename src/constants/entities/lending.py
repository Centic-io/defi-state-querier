from constants.chain_constant import Chain
from services.lending.aave_v2_services import AaveV2StateService


class Lending:
    aave_v2 = "aave-v2"
    all = [aave_v2]
    ethereum = {
        aave_v2: AaveV2StateService
    }
    mapping = {
        Chain.ethereum: ethereum
    }

