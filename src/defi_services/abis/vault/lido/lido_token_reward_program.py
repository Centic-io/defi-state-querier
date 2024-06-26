import json

LIDO_TOKEN_REWARD_PROGRAM_ABI = json.loads('''
[
  {
    "name": "VestingEscrowCreated",
    "inputs": [
      {
        "name": "creator",
        "type": "address",
        "indexed": true
      },
      {
        "name": "recipient",
        "type": "address",
        "indexed": true
      },
      {
        "name": "escrow",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "ERC20Recovered",
    "inputs": [
      {
        "name": "token",
        "type": "address",
        "indexed": false
      },
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "ETHRecovered",
    "inputs": [
      {
        "name": "amount",
        "type": "uint256",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "VotingAdapterUpgraded",
    "inputs": [
      {
        "name": "voting_adapter",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "OwnerChanged",
    "inputs": [
      {
        "name": "owner",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "name": "ManagerChanged",
    "inputs": [
      {
        "name": "manager",
        "type": "address",
        "indexed": false
      }
    ],
    "anonymous": false,
    "type": "event"
  },
  {
    "stateMutability": "nonpayable",
    "type": "constructor",
    "inputs": [
      {
        "name": "target",
        "type": "address"
      },
      {
        "name": "token",
        "type": "address"
      },
      {
        "name": "owner",
        "type": "address"
      },
      {
        "name": "manager",
        "type": "address"
      },
      {
        "name": "voting_adapter",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "deploy_vesting_contract",
    "inputs": [
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "vesting_duration",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "deploy_vesting_contract",
    "inputs": [
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "vesting_duration",
        "type": "uint256"
      },
      {
        "name": "vesting_start",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "deploy_vesting_contract",
    "inputs": [
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "vesting_duration",
        "type": "uint256"
      },
      {
        "name": "vesting_start",
        "type": "uint256"
      },
      {
        "name": "cliff_length",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "deploy_vesting_contract",
    "inputs": [
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "vesting_duration",
        "type": "uint256"
      },
      {
        "name": "vesting_start",
        "type": "uint256"
      },
      {
        "name": "cliff_length",
        "type": "uint256"
      },
      {
        "name": "is_fully_revokable",
        "type": "bool"
      }
    ],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "recover_erc20",
    "inputs": [
      {
        "name": "token",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "recover_ether",
    "inputs": [],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "update_voting_adapter",
    "inputs": [
      {
        "name": "voting_adapter",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "change_owner",
    "inputs": [
      {
        "name": "owner",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "nonpayable",
    "type": "function",
    "name": "change_manager",
    "inputs": [
      {
        "name": "manager",
        "type": "address"
      }
    ],
    "outputs": []
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "token",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "target",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "voting_adapter",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "owner",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "stateMutability": "view",
    "type": "function",
    "name": "manager",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ]
  }
]
''')