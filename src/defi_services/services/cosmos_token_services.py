import json
from urllib.parse import quote
import requests


class CosmosTokenServices:
    def __init__(self, lcd: str, denom: str):
        self.lcd = lcd
        self.denom = denom

    # queries the balance of all coins for a single account.
    def query_balances(self, address: str):
        responses = []
        endpoint = '/cosmos/bank/v1beta1/balances/'
        try:
            results = json.loads(requests.get(self.lcd + endpoint + address, timeout=60).content)
            responses += results['balances']
            pagination = results['pagination']['next_key']
            while pagination is not None:
                results = json.loads(
                    requests.get(self.lcd + endpoint + '?pagination.key=' + quote(str(pagination)), timeout=60).content)
                responses += results['balances']
                pagination = results['pagination']['next_key']
            return responses
        except Exception:
            raise Exception

    # queries the balance of a given denom for a single account.
    def query_balances_by_denom(self, address, denom):
        endpoint = '/cosmos/bank/v1beta1/balances/'
        try:
            return json.loads(
                requests.get(self.lcd + endpoint + address + '/by_denom?denom=' + denom, timeout=60).content)
        except Exception:
            raise Exception

    def query_token_decimal(self):
        endpoint = '/cosmos/bank/v1beta1/denoms_metadata'
        try:
            return json.loads(requests.get(self.lcd + endpoint, timeout=60).content)
        except Exception:
            raise Exception
