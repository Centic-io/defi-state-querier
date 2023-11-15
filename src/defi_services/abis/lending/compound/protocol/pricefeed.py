
import json

PRICEFEED = json.loads("""
[
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "anchorToleranceMantissa_",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "anchorPeriod_",
        "type": "uint256"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig[]",
        "name": "configs",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "anchorPrice",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oldTimestamp",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newTimestamp",
        "type": "uint256"
      }
    ],
    "name": "AnchorPriceUpdated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      }
    ],
    "name": "FailoverActivated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      }
    ],
    "name": "FailoverDeactivated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "to",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferRequested",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "to",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "reporter",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "anchor",
        "type": "uint256"
      }
    ],
    "name": "PriceGuarded",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "price",
        "type": "uint256"
      }
    ],
    "name": "PriceUpdated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oldTimestamp",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newTimestamp",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "oldPrice",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newPrice",
        "type": "uint256"
      }
    ],
    "name": "UniswapWindowUpdated",
    "type": "event"
  },
  {
    "inputs": [],
    "name": "acceptOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      }
    ],
    "name": "activateFailover",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "anchorPeriod",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      }
    ],
    "name": "deactivateFailover",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "ethBaseUnit",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "expScale",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "i",
        "type": "uint256"
      }
    ],
    "name": "getTokenConfig",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "cToken",
        "type": "address"
      }
    ],
    "name": "getTokenConfigByCToken",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "reporter",
        "type": "address"
      }
    ],
    "name": "getTokenConfigByReporter",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "symbol",
        "type": "string"
      }
    ],
    "name": "getTokenConfigBySymbol",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      }
    ],
    "name": "getTokenConfigBySymbolHash",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "underlying",
        "type": "address"
      }
    ],
    "name": "getTokenConfigByUnderlying",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "underlying",
            "type": "address"
          },
          {
            "internalType": "bytes32",
            "name": "symbolHash",
            "type": "bytes32"
          },
          {
            "internalType": "uint256",
            "name": "baseUnit",
            "type": "uint256"
          },
          {
            "internalType": "enum UniswapConfig.PriceSource",
            "name": "priceSource",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "fixedPrice",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "uniswapMarket",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "reporter",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "reporterMultiplier",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isUniswapReversed",
            "type": "bool"
          }
        ],
        "internalType": "struct UniswapConfig.TokenConfig",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "cToken",
        "type": "address"
      }
    ],
    "name": "getUnderlyingPrice",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "lowerBoundAnchorRatio",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "maxTokens",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "name": "newObservations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "acc",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "numTokens",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "name": "oldObservations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "acc",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "symbolHash",
        "type": "bytes32"
      }
    ],
    "name": "pokeFailedOverPrice",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "symbol",
        "type": "string"
      }
    ],
    "name": "price",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "name": "prices",
    "outputs": [
      {
        "internalType": "uint248",
        "name": "price",
        "type": "uint248"
      },
      {
        "internalType": "bool",
        "name": "failoverActive",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "upperBoundAnchorRatio",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "int256",
        "name": "",
        "type": "int256"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "int256",
        "name": "currentAnswer",
        "type": "int256"
      }
    ],
    "name": "validate",
    "outputs": [
      {
        "internalType": "bool",
        "name": "valid",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
""")
        