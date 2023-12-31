import json

WEPIGGY_LENS_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "contract ComptrollerLensInterface",
        "name": "_comptroller",
        "type": "address"
      },
      {
        "internalType": "contract PiggyDistributionInterface",
        "name": "_distribution",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "_pNativeToken",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_nativeToken",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_nativeName",
        "type": "string"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "all",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "pTokenAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "pTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "underlyingSymbol",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "underlyingName",
            "type": "string"
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
            "name": "collateralFactorMantissa",
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
            "name": "price",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "mintCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "blockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accrualBlockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowIndex",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenMetadata[]",
        "name": "",
        "type": "tuple[]"
      },
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "blocksPerYear",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "multiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "baseRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "jumpMultiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "kink",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.InterestRateModel[]",
        "name": "",
        "type": "tuple[]"
      },
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "wpcSpeed",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenWpcSpeed[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "allForAccount",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface[]",
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
        "internalType": "struct WePiggyLensV2.AccountLimits",
        "name": "",
        "type": "tuple"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "pToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateMantissa",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenBalances[]",
        "name": "",
        "type": "tuple[]"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "pTokenAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "pTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "underlyingSymbol",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "underlyingName",
            "type": "string"
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
            "name": "collateralFactorMantissa",
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
            "name": "price",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "mintCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "blockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accrualBlockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowIndex",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenMetadata[]",
        "name": "",
        "type": "tuple[]"
      },
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "blocksPerYear",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "multiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "baseRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "jumpMultiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "kink",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.InterestRateModel[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "comptroller",
    "outputs": [
      {
        "internalType": "contract ComptrollerLensInterface",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "distribution",
    "outputs": [
      {
        "internalType": "contract PiggyDistributionInterface",
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
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "getAccountLimits",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface[]",
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
        "internalType": "struct WePiggyLensV2.AccountLimits",
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
        "internalType": "contract PTokenLensInterface",
        "name": "pToken",
        "type": "address"
      }
    ],
    "name": "getInterestRateModel",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "blocksPerYear",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "multiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "baseRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "jumpMultiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "kink",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.InterestRateModel",
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
        "internalType": "contract PTokenLensInterface[]",
        "name": "pTokens",
        "type": "address[]"
      }
    ],
    "name": "getInterestRateModels",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "blocksPerYear",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "multiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "baseRatePerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "jumpMultiplierPerBlock",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "kink",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.InterestRateModel[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "contract PTokenLensInterface",
        "name": "pToken",
        "type": "address"
      }
    ],
    "name": "getWpcSpeed",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "wpcSpeed",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenWpcSpeed",
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
        "internalType": "contract PTokenLensInterface[]",
        "name": "pTokens",
        "type": "address[]"
      }
    ],
    "name": "getWpcSpeeds",
    "outputs": [
      {
        "components": [
          {
            "internalType": "contract PTokenLensInterface",
            "name": "market",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "wpcSpeed",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenWpcSpeed[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "nativeName",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "nativeToken",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
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
    "inputs": [],
    "name": "pNativeToken",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "contract PTokenLensInterface",
        "name": "pToken",
        "type": "address"
      },
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "pTokenBalances",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "pToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateMantissa",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenBalances",
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
        "internalType": "contract PTokenLensInterface[]",
        "name": "pTokens",
        "type": "address[]"
      },
      {
        "internalType": "address payable",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "pTokenBalancesAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "pToken",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "balance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowBalance",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "exchangeRateMantissa",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenBalances[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "contract PTokenLensInterface",
        "name": "pToken",
        "type": "address"
      }
    ],
    "name": "pTokenMetadata",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "pTokenAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "pTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "underlyingSymbol",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "underlyingName",
            "type": "string"
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
            "name": "collateralFactorMantissa",
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
            "name": "price",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "mintCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "blockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accrualBlockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowIndex",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenMetadata",
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
        "internalType": "contract PTokenLensInterface[]",
        "name": "pTokens",
        "type": "address[]"
      }
    ],
    "name": "pTokenMetadataAll",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "pTokenAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "pTokenDecimals",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "underlyingAddress",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "underlyingDecimals",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "underlyingSymbol",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "underlyingName",
            "type": "string"
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
            "name": "collateralFactorMantissa",
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
            "name": "price",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "mintCap",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowCap",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isListed",
            "type": "bool"
          },
          {
            "internalType": "uint256",
            "name": "blockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accrualBlockNumber",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "borrowIndex",
            "type": "uint256"
          }
        ],
        "internalType": "struct WePiggyLensV2.PTokenMetadata[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "contract ComptrollerLensInterface",
        "name": "_comptroller",
        "type": "address"
      },
      {
        "internalType": "contract PiggyDistributionInterface",
        "name": "_distribution",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "_pNativeToken",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_nativeToken",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_nativeName",
        "type": "string"
      }
    ],
    "name": "updateProperties",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
''')