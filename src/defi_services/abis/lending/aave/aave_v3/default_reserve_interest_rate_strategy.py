
import json

DEFAULT_RESERVE_INTEREST_RATE_STRATEGY_V3 = json.loads("""
[
    {
      "inputs": [
        {
          "internalType": "contract IPoolAddressesProvider",
          "name": "provider",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "optimalUsageRatio",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "baseVariableBorrowRate",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "variableRateSlope1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "variableRateSlope2",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "stableRateSlope1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "stableRateSlope2",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "baseStableRateOffset",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "stableRateExcessOffset",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "optimalStableToTotalDebtRatio",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "ADDRESSES_PROVIDER",
      "outputs": [
        {
          "internalType": "contract IPoolAddressesProvider",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "MAX_EXCESS_STABLE_TO_TOTAL_DEBT_RATIO",
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
      "name": "MAX_EXCESS_USAGE_RATIO",
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
      "name": "OPTIMAL_STABLE_TO_TOTAL_DEBT_RATIO",
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
      "name": "OPTIMAL_USAGE_RATIO",
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
          "components": [
            {
              "internalType": "uint256",
              "name": "unbacked",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "liquidityAdded",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "liquidityTaken",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "totalStableDebt",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "totalVariableDebt",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "averageStableBorrowRate",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "reserveFactor",
              "type": "uint256"
            },
            {
              "internalType": "address",
              "name": "reserve",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "aToken",
              "type": "address"
            }
          ],
          "internalType": "struct DataTypes.CalculateInterestRatesParams",
          "name": "params",
          "type": "tuple"
        }
      ],
      "name": "calculateInterestRates",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
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
      "name": "getBaseStableBorrowRate",
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
      "name": "getBaseVariableBorrowRate",
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
      "name": "getMaxVariableBorrowRate",
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
      "name": "getStableRateExcessOffset",
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
      "name": "getStableRateSlope1",
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
      "name": "getStableRateSlope2",
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
      "name": "getVariableRateSlope1",
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
      "name": "getVariableRateSlope2",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
]
""")
        