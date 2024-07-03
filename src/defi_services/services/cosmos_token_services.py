import json
from urllib.parse import quote
import requests
import base64

from cosmpy.cosmwasm.rest_client import RestClient
from cosmpy.cosmwasm.rest_client import CosmWasmRestClient
from cosmpy.protos.cosmwasm.wasm.v1.query_pb2 import QuerySmartContractStateRequest

from defi_services.constants.cosmos_decimals_constant import Denoms, MulticallContract


class CosmosTokenServices:
    def __init__(self, lcd: str, rest_uri: str, chain_id: str):
        self.chain_id = chain_id
        self.lcd = lcd

        self.rest_uri = rest_uri
        self.client = CosmWasmRestClient(RestClient(rest_address=rest_uri))

        self.decimals = Denoms.cosmos
        self.decimals.update(Denoms.orai)

    # queries the balance of all coins for a single account.
    def query_coin_balances(self, address: str):
        responses = []
        endpoint = '/cosmos/bank/v1beta1/balances/'

        response = requests.get(self.lcd + endpoint + address, timeout=60).content
        results = json.loads(response)

        responses += results['balances']
        pagination = results['pagination']['next_key']

        while pagination is not None:
            response = requests.get(self.lcd + endpoint + '?pagination.key=' + quote(str(pagination)), timeout=60)
            results = json.loads(response.content)

            responses += results['balances']
            pagination = results['pagination']['next_key']

        return responses

    # queries the balance of a given denom for a single account.
    def query_balances_by_denom(self, address, denom):
        endpoint = '/cosmos/bank/v1beta1/balances/'

        response = requests.get(self.lcd + endpoint + address + '/by_denom?denom=' + denom, timeout=60)
        return json.loads(response.content)

    def query_token_decimal(self):
        endpoint = '/cosmos/bank/v1beta1/denoms_metadata'

        response = requests.get(self.lcd + endpoint, timeout=60)
        return json.loads(response.content)

    def query_balances(self, address: str, tokens: list):
        balance_query, cw20_tokens = self.get_balance_function_info(address, tokens)
        queries = []
        for token in cw20_tokens:
            queries.append({
                "address": token,
                "data": self.encode_data({"token_info": {}})
            })
        queries.append({
            "address": MulticallContract.mapping.get(self.chain_id).get("multicall_balance"),
            "data": self.encode_data(balance_query)
        })
        query = {
            "aggregate": {
                "queries": queries
            }
        }
        query = json.dumps(query).encode('utf-8')
        request_ = QuerySmartContractStateRequest(
            address=MulticallContract.mapping.get(self.chain_id).get("multicall"), query_data=query)
        response_ = self.client.SmartContractState(request_)
        decoded_data = self.decode_response_data(response_, cw20_tokens, tokens)
        return decoded_data

    def decode_response_data(self, response_data, cw20_tokens, tokens):
        response_data = json.loads(response_data.data)
        return_data = response_data.get("return_data", [])
        if not len(return_data):
            return None
        decimals = {}
        for idx in range(0, len(cw20_tokens)):
            encoded_data = return_data[idx]
            decoded_data = self.decode_data(encoded_data['data'])
            decimals[cw20_tokens[idx]] = decoded_data.get("decimals")

        balance_data = self.decode_data(return_data[-1]['data'])
        balances = {}
        for idx in range(0, len(tokens)):
            balances[tokens[idx]] = int(balance_data[idx])

        for token in tokens:
            if decimals.get(token) is not None:
                balances[token] /= 10**decimals[token]
            else:
                balances[token] /= 10**self.decimals.get(token, {}).get("decimal", 0)

        return balances

    @staticmethod
    def encode_data(params: dict):
        data = json.dumps(params).encode('utf-8')
        encode_data = base64.b64encode(data).decode()
        return encode_data

    @staticmethod
    def decode_data(encode_data: str):
        decoded_data = base64.b64decode(encode_data)
        decoded_data = json.loads(decoded_data)
        return decoded_data

    @staticmethod
    def get_balance_function_info(address: str, tokens: list):
        data = {
            "balance": {
                "address": address,
                "assets": []
            }
        }
        cw20_tokens = []
        for token in tokens:
            head = token[:4]
            if len(token) < 10 or head == 'ibc/':
                data["balance"]["assets"].append({
                    "native_token": {
                        "denom": token
                    }
                })
            else:
                data["balance"]["assets"].append(
                    {
                        "token": {
                            "contract_addr": token
                        }
                    }
                )
                cw20_tokens.append(token)
        return data, cw20_tokens
