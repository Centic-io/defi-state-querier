import json

MORPHO_COMPOUND_LENS_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_morpho",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "CompoundOracleFailed",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidPoolToken",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "MAX_BASIS_POINTS",
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
    "name": "WAD",
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
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "_getUpdatedIndexes",
        "type": "bool"
      },
      {
        "internalType": "contract ICompoundOracle",
        "name": "_oracle",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_withdrawnAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_borrowedAmount",
        "type": "uint256"
      }
    ],
    "name": "_getUserHypotheticalLiquidityDataForAsset",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "collateralValue",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxDebtValue",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "debtValue",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingPrice",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "collateralFactor",
            "type": "uint256"
          }
        ],
        "internalType": "struct Types.AssetLiquidityData",
        "name": "assetData",
        "type": "tuple"
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
        "internalType": "contract IComptroller",
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
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolTokenBorrowed",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolTokenCollateral",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_updatedMarkets",
        "type": "address[]"
      }
    ],
    "name": "computeLiquidationRepayAmount",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "toRepay",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_borrower",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getAccruedBorrowerComp",
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
        "internalType": "address",
        "name": "_borrower",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_balance",
        "type": "uint256"
      }
    ],
    "name": "getAccruedBorrowerComp",
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
        "internalType": "address",
        "name": "_supplier",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getAccruedSupplierComp",
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
        "internalType": "address",
        "name": "_supplier",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_balance",
        "type": "uint256"
      }
    ],
    "name": "getAccruedSupplierComp",
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
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getAdvancedMarketData",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "p2pSupplyIndex",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "p2pBorrowIndex",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "poolSupplyIndex",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "poolBorrowIndex",
            "type": "uint256"
          }
        ],
        "internalType": "struct Types.Indexes",
        "name": "indexes",
        "type": "tuple"
      },
      {
        "internalType": "uint32",
        "name": "lastUpdateBlockNumber",
        "type": "uint32"
      },
      {
        "internalType": "uint256",
        "name": "p2pSupplyDelta",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "p2pBorrowDelta",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAllMarkets",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "marketsCreated",
        "type": "address[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getAverageBorrowRatePerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "avgBorrowRatePerBlock",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "p2pBorrowAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolBorrowAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getAverageSupplyRatePerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "avgSupplyRatePerBlock",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "p2pSupplyAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolSupplyAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "getCurrentBorrowBalanceInOf",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "balanceOnPool",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "balanceInP2P",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalBalance",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getCurrentCompBorrowIndex",
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
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getCurrentCompSupplyIndex",
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
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getCurrentP2PBorrowIndex",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pBorrowIndex",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getCurrentP2PSupplyIndex",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pSupplyIndex",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getCurrentPoolIndexes",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "poolSupplyIndex",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolBorrowIndex",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "getCurrentSupplyBalanceInOf",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "balanceOnPool",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "balanceInP2P",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalBalance",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "getCurrentUserBorrowRatePerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "borrowRatePerBlock",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "getCurrentUserSupplyRatePerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "supplyRatePerBlock",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "getEnteredMarkets",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "enteredMarkets",
        "type": "address[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "_updated",
        "type": "bool"
      }
    ],
    "name": "getIndexes",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "p2pSupplyIndex",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "p2pBorrowIndex",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "poolSupplyIndex",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "poolBorrowIndex",
            "type": "uint256"
          }
        ],
        "internalType": "struct Types.Indexes",
        "name": "indexes",
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
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getMainMarketData",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "avgSupplyRatePerBlock",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "avgBorrowRatePerBlock",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "p2pSupplyAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "p2pBorrowAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolSupplyAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolBorrowAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getMarketConfiguration",
    "outputs": [
      {
        "internalType": "address",
        "name": "underlying",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "isCreated",
        "type": "bool"
      },
      {
        "internalType": "bool",
        "name": "p2pDisabled",
        "type": "bool"
      },
      {
        "internalType": "bool",
        "name": "isPaused",
        "type": "bool"
      },
      {
        "internalType": "bool",
        "name": "isPartiallyPaused",
        "type": "bool"
      },
      {
        "internalType": "uint16",
        "name": "reserveFactor",
        "type": "uint16"
      },
      {
        "internalType": "uint16",
        "name": "p2pIndexCursor",
        "type": "uint16"
      },
      {
        "internalType": "uint256",
        "name": "collateralFactor",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getMarketPauseStatus",
    "outputs": [
      {
        "components": [
          {
            "internalType": "bool",
            "name": "isSupplyPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isBorrowPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isWithdrawPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isRepayPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isLiquidateCollateralPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isLiquidateBorrowPaused",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isDeprecated",
            "type": "bool"
          }
        ],
        "internalType": "struct Types.MarketPauseStatus",
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
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "getNextUserBorrowRatePerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "nextBorrowRatePerBlock",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "balanceOnPool",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "balanceInP2P",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalBalance",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "getNextUserSupplyRatePerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "nextSupplyRatePerBlock",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "balanceOnPool",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "balanceInP2P",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalBalance",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getRatesPerBlock",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pSupplyRate",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "p2pBorrowRate",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolSupplyRate",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolBorrowRate",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalBorrow",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pBorrowAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolBorrowAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalBorrowAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getTotalMarketBorrow",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pBorrowAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolBorrowAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getTotalMarketSupply",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pSupplyAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolSupplyAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalSupply",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "p2pSupplyAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "poolSupplyAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalSupplyAmount",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_updatedMarkets",
        "type": "address[]"
      }
    ],
    "name": "getUserBalanceStates",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "collateralValue",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "debtValue",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "maxDebtValue",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_updatedMarkets",
        "type": "address[]"
      }
    ],
    "name": "getUserHealthFactor",
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
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_withdrawnAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_borrowedAmount",
        "type": "uint256"
      }
    ],
    "name": "getUserHypotheticalBalanceStates",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "debtValue",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "maxDebtValue",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "_getUpdatedIndexes",
        "type": "bool"
      },
      {
        "internalType": "contract ICompoundOracle",
        "name": "_oracle",
        "type": "address"
      }
    ],
    "name": "getUserLiquidityDataForAsset",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "collateralValue",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxDebtValue",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "debtValue",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "underlyingPrice",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "collateralFactor",
            "type": "uint256"
          }
        ],
        "internalType": "struct Types.AssetLiquidityData",
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
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "getUserMaxCapacitiesForAsset",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "withdrawable",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "borrowable",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address[]",
        "name": "_poolTokens",
        "type": "address[]"
      },
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      }
    ],
    "name": "getUserUnclaimedRewards",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "unclaimedRewards",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_poolToken",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_updatedMarkets",
        "type": "address[]"
      }
    ],
    "name": "isLiquidatable",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
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
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_updatedMarkets",
        "type": "address[]"
      }
    ],
    "name": "isLiquidatable",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
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
        "name": "_poolToken",
        "type": "address"
      }
    ],
    "name": "isMarketCreated",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
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
        "name": "",
        "type": "address"
      }
    ],
    "name": "isMarketCreatedAndNotPaused",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "isMarketCreatedAndNotPausedNorPartiallyPaused",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "morpho",
    "outputs": [
      {
        "internalType": "contract IMorpho",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "rewardsManager",
    "outputs": [
      {
        "internalType": "contract IRewardsManager",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
''')