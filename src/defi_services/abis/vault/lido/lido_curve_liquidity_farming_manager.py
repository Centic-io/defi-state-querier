import json

LIDO_CURVE_LIIQUIDITY_FARMING_MANAGER_ABI = json.loads('''
[
  {
    "outputs": [],
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "name": "transfer_ownership",
    "outputs": [],
    "inputs": [
      {
        "type": "address",
        "name": "_to"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function",
    "gas": 36247
  },
  {
    "name": "set_rewards_contract",
    "outputs": [],
    "inputs": [
      {
        "type": "address",
        "name": "_rewards_contract"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function",
    "gas": 36277
  },
  {
    "name": "is_rewards_period_finished",
    "outputs": [
      {
        "type": "bool",
        "name": ""
      }
    ],
    "inputs": [],
    "stateMutability": "view",
    "type": "function",
    "gas": 2017
  },
  {
    "name": "start_next_rewards_period",
    "outputs": [],
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "function",
    "gas": 5262
  },
  {
    "name": "recover_erc20",
    "outputs": [],
    "inputs": [
      {
        "type": "address",
        "name": "_token"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "name": "recover_erc20",
    "outputs": [],
    "inputs": [
      {
        "type": "address",
        "name": "_token"
      },
      {
        "type": "address",
        "name": "_recipient"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "name": "owner",
    "outputs": [
      {
        "type": "address",
        "name": ""
      }
    ],
    "inputs": [],
    "stateMutability": "view",
    "type": "function",
    "gas": 1241
  },
  {
    "name": "rewards_contract",
    "outputs": [
      {
        "type": "address",
        "name": ""
      }
    ],
    "inputs": [],
    "stateMutability": "view",
    "type": "function",
    "gas": 1271
  }
]
''')