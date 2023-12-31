import json

IRON_LENS_ABI = json.loads('''
[
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken",
        "name": "cToken",
        "type": "address"
      },
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "cTokenBalances",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balanceOf",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalanceCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "balanceOfUnderlying",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenAllowance",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "collateralEnabled",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "collateralBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "nativeTokenBalance",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenBalances",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken[]",
        "name": "cTokens",
        "type": "address[]"
      },
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "cTokenBalancesAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balanceOf",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalanceCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "balanceOfUnderlying",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "tokenAllowance",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "collateralEnabled",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "collateralBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "nativeTokenBalance",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenBalances[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken",
        "name": "cToken",
        "type": "address"
      }
    ],
    "name": "cTokenMetadata",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "supplyRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "reserveFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrows",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalReserves",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalSupply",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalCash",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalCollateralTokens",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "collateralFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAssetAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "cTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "enum ComptrollerV1Storage.Version",
            "name": "version",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "collateralCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingPrice",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "supplyPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "borrowPaused",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "supplyCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenMetadata",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CToken[]",
        "name": "cTokens",
        "type": "address[]"
      }
    ],
    "name": "cTokenMetadataAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "cToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateCurrent",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "supplyRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "reserveFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalBorrows",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalReserves",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalSupply",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalCash",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "totalCollateralTokens",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "collateralFactorMantissa",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAssetAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "cTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "enum ComptrollerV1Storage.Version",
            "name": "version",
            "type": "uint8"
          },
          {
            "internalType": "uint256",
            "name": "collateralCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingPrice",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "supplyPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "borrowPaused",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "supplyCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.CTokenMetadata[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract Comptroller",
        "name": "comptroller",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getAccountLimits",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract CToken[]",
            "name": "markets",
            "type": "address[]"
          },
          {
            "internalType": "uint256",
            "name": "liquidity",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "shortfall",
            "type": "uint256"
          }
        ],
        "internalType": "struct CompoundLens.AccountLimits",
        "name": "",
        "type": "tuple"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CCTokenInterface[]",
        "name": "cTokens",
        "type": "address[]"
      },
      {
        "internalType": "address",
        "name": "comp",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getClaimableCompRewards",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "",
        "type": "uint256[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "contract CSLPInterface[]",
        "name": "cTokens",
        "type": "address[]"
      },
      {
        "internalType": "address",
        "name": "sushi",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getClaimableSushiRewards",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "",
        "type": "uint256[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
''')