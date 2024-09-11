import json
import logging
import requests

logger = logging.getLogger("TonStateQuerier")


class TonStateQuerier:
    def __init__(self, provider_uri):
        self.provider_uri = provider_uri
        if provider_uri[-1] != '/':
            self.provider_uri +='/'

    def query_jetton_coin_balances(self, address: str, limit: int = 256, offset: int = 0, pages: int = None):
        responses = []
        while True:
            endpoint = f"{self.provider_uri}v3/jetton/wallets?owner_address={address}&limit={limit}&offset={offset}"
            response = requests.get(endpoint).content
            results = json.loads(response)
            if results.get('jetton_wallets'):
                responses += results.get('jetton_wallets')
                offset += 1
                if pages and offset == pages:
                    break
            else:
                break

        return responses

    def query_ton_coin_balances(self, address: str):
        endpoint = f"{self.provider_uri}v2/getAddressBalance?address={address}"
        response = requests.get(endpoint).content
        result = json.loads(response)
        return result