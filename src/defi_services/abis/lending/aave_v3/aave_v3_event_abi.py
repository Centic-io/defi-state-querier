AAVE_V3_LENDING_EVENT_ABI = [
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "reserve",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "on_behalf_of",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": False,
        "internalType": "enum DataTypes.InterestRateMode",
        "name": "interest_rate_mode",
        "type": "uint8"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "borrow_rate",
        "type": "uint256"
      },
      {
        "indexed": True,
        "internalType": "uint16",
        "name": "referral",
        "type": "uint16"
      }
    ],
    "name": "Borrow",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "collateral_asset",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "debt_asset",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "debt_to_cover",
        "type": "uint256"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "liquidated_collateral_amount",
        "type": "uint256"
      },
      {
        "indexed": False,
        "internalType": "address",
        "name": "liquidator",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "bool",
        "name": "receive_atoken",
        "type": "bool"
      }
    ],
    "name": "LiquidationCall",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "reserve",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "on_behalf_of",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": True,
        "internalType": "uint16",
        "name": "referral",
        "type": "uint16"
      }
    ],
    "name": "MintUnbacked",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "reserve",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "repayer",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": False,
        "internalType": "bool",
        "name": "use_atokens",
        "type": "bool"
      }
    ],
    "name": "Repay",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "reserve",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "on_behalf_of",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": True,
        "internalType": "uint16",
        "name": "referral",
        "type": "uint16"
      }
    ],
    "name": "Supply",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "reserve",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "Withdraw",
    "type": "event"
  }
]