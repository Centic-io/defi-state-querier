import json

JUSTLEND_COMPTROLLER_ABI = json.loads('''
[
    {
      "inputs": [
        {
          "name": "action",
          "type": "string"
        },
        {
          "name": "pauseState",
          "type": "bool"
        }
      ],
      "name": "ActionPaused",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "action",
          "type": "string"
        },
        {
          "name": "pauseState",
          "type": "bool"
        }
      ],
      "name": "ActionPaused",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "state",
          "type": "bool"
        }
      ],
      "name": "ActionSupportedCollateralFactorGuardian",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "error",
          "type": "uint256"
        },
        {
          "name": "info",
          "type": "uint256"
        },
        {
          "name": "detail",
          "type": "uint256"
        }
      ],
      "name": "Failure",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "account",
          "type": "address"
        }
      ],
      "name": "MarketEntered",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "account",
          "type": "address"
        }
      ],
      "name": "MarketExited",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        }
      ],
      "name": "MarketListed",
      "type": "event"
    },
    {
      "inputs": [
        {
          "indexed": true,
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "newBorrowCap",
          "type": "uint256"
        }
      ],
      "name": "NewBorrowCap",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldBorrowCapGuardian",
          "type": "address"
        },
        {
          "name": "newBorrowCapGuardian",
          "type": "address"
        }
      ],
      "name": "NewBorrowCapGuardian",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldCloseFactorMantissa",
          "type": "uint256"
        },
        {
          "name": "newCloseFactorMantissa",
          "type": "uint256"
        }
      ],
      "name": "NewCloseFactor",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "oldCollateralFactorMantissa",
          "type": "uint256"
        },
        {
          "name": "newCollateralFactorMantissa",
          "type": "uint256"
        }
      ],
      "name": "NewCollateralFactor",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldCollateralFactorGuardian",
          "type": "address"
        },
        {
          "name": "newCollateralFactorGuardian",
          "type": "address"
        }
      ],
      "name": "NewCollateralFactorGuardian",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldLiquidationIncentiveMantissa",
          "type": "uint256"
        },
        {
          "name": "newLiquidationIncentiveMantissa",
          "type": "uint256"
        }
      ],
      "name": "NewLiquidationIncentive",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldMaxAssets",
          "type": "uint256"
        },
        {
          "name": "newMaxAssets",
          "type": "uint256"
        }
      ],
      "name": "NewMaxAssets",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldPauseGuardian",
          "type": "address"
        },
        {
          "name": "newPauseGuardian",
          "type": "address"
        }
      ],
      "name": "NewPauseGuardian",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "oldPriceOracle",
          "type": "address"
        },
        {
          "name": "newPriceOracle",
          "type": "address"
        }
      ],
      "name": "NewPriceOracle",
      "type": "event"
    },
    {
      "inputs": [
        {
          "name": "unitroller",
          "type": "address"
        }
      ],
      "name": "_become",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "name": "_borrowGuardianPaused",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "name": "_mintGuardianPaused",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "newBorrowCapGuardian",
          "type": "address"
        }
      ],
      "name": "_setBorrowCapGuardian",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "state",
          "type": "bool"
        }
      ],
      "name": "_setBorrowPaused",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "newCloseFactorMantissa",
          "type": "uint256"
        }
      ],
      "name": "_setCloseFactor",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "newCollateralFactorMantissa",
          "type": "uint256"
        }
      ],
      "name": "_setCollateralFactor",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "newCollateralFactorGuardian",
          "type": "address"
        }
      ],
      "name": "_setCollateralFactorGuardian",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "state",
          "type": "bool"
        }
      ],
      "name": "_setCollateralFactorGuardianStateForMarket",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "newLiquidationIncentiveMantissa",
          "type": "uint256"
        }
      ],
      "name": "_setLiquidationIncentive",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cTokens",
          "type": "address[]"
        },
        {
          "name": "newBorrowCaps",
          "type": "uint256[]"
        }
      ],
      "name": "_setMarketBorrowCaps",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "newMaxAssets",
          "type": "uint256"
        }
      ],
      "name": "_setMaxAssets",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "state",
          "type": "bool"
        }
      ],
      "name": "_setMintPaused",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "newPauseGuardian",
          "type": "address"
        }
      ],
      "name": "_setPauseGuardian",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "newOracle",
          "type": "address"
        }
      ],
      "name": "_setPriceOracle",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "inputs": [
        {
          "name": "state",
          "type": "bool"
        }
      ],
      "name": "_setSeizePaused",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "inputs": [
        {
          "name": "state",
          "type": "bool"
        }
      ],
      "name": "_setTransferPaused",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        }
      ],
      "name": "_supportMarket",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        },
        {
          "type": "uint256"
        }
      ],
      "name": "accountAssets",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "admin",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "uint256"
        }
      ],
      "name": "allMarkets",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "borrowAmount",
          "type": "uint256"
        }
      ],
      "name": "borrowAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "borrowCapGuardian",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "borrowCaps",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "borrowGuardianPaused",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "borrowAmount",
          "type": "uint256"
        }
      ],
      "name": "borrowVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "name": "account",
          "type": "address"
        },
        {
          "name": "cToken",
          "type": "address"
        }
      ],
      "name": "checkMembership",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "name": "closeFactorMantissa",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "collateralFactorGuardian",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "collateralFactorGuardianMarkets",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "compAccrued",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "name": "index",
          "type": "uint224"
        },
        {
          "name": "block",
          "type": "uint32"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "compBorrowState",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        },
        {
          "type": "address"
        }
      ],
      "name": "compBorrowerIndex",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "name": "compRate",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "compSpeeds",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        },
        {
          "type": "address"
        }
      ],
      "name": "compSupplierIndex",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "name": "index",
          "type": "uint224"
        },
        {
          "name": "block",
          "type": "uint32"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "compSupplyState",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "comptrollerImplementation",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "_cToken",
          "type": "address"
        }
      ],
      "name": "enterMarket",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256[]"
        }
      ],
      "inputs": [
        {
          "name": "cTokens",
          "type": "address[]"
        }
      ],
      "name": "enterMarkets",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cTokenAddress",
          "type": "address"
        }
      ],
      "name": "exitMarket",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        },
        {
          "type": "uint256"
        },
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "name": "account",
          "type": "address"
        }
      ],
      "name": "getAccountLiquidity",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "outputs": [
        {
          "type": "address[]"
        }
      ],
      "constant": true,
      "name": "getAllMarkets",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address[]"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "name": "account",
          "type": "address"
        }
      ],
      "name": "getAssetsIn",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "name": "getBlockNumber",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "getCompAddress",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        },
        {
          "type": "uint256"
        },
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "name": "account",
          "type": "address"
        },
        {
          "name": "cTokenModify",
          "type": "address"
        },
        {
          "name": "redeemTokens",
          "type": "uint256"
        },
        {
          "name": "borrowAmount",
          "type": "uint256"
        }
      ],
      "name": "getHypotheticalAccountLiquidity",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "name": "isComptroller",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cTokenBorrowed",
          "type": "address"
        },
        {
          "name": "cTokenCollateral",
          "type": "address"
        },
        {
          "name": "liquidator",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "repayAmount",
          "type": "uint256"
        }
      ],
      "name": "liquidateBorrowAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cTokenBorrowed",
          "type": "address"
        },
        {
          "name": "cTokenCollateral",
          "type": "address"
        },
        {
          "name": "liquidator",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "actualRepayAmount",
          "type": "uint256"
        },
        {
          "name": "seizeTokens",
          "type": "uint256"
        }
      ],
      "name": "liquidateBorrowVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        },
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "name": "cTokenBorrowed",
          "type": "address"
        },
        {
          "name": "cTokenCollateral",
          "type": "address"
        },
        {
          "name": "actualRepayAmount",
          "type": "uint256"
        }
      ],
      "name": "liquidateCalculateSeizeTokens",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "name": "liquidationIncentiveMantissa",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "name": "isListed",
          "type": "bool"
        },
        {
          "name": "collateralFactorMantissa",
          "type": "uint256"
        },
        {
          "name": "isComped",
          "type": "bool"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "markets",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "constant": true,
      "name": "maxAssets",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "minter",
          "type": "address"
        },
        {
          "name": "mintAmount",
          "type": "uint256"
        }
      ],
      "name": "mintAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "inputs": [
        {
          "type": "address"
        }
      ],
      "name": "mintGuardianPaused",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "minter",
          "type": "address"
        },
        {
          "name": "actualMintAmount",
          "type": "uint256"
        },
        {
          "name": "mintTokens",
          "type": "uint256"
        }
      ],
      "name": "mintVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "oracle",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "pauseGuardian",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "pendingAdmin",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "address"
        }
      ],
      "constant": true,
      "name": "pendingComptrollerImplementation",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "redeemer",
          "type": "address"
        },
        {
          "name": "redeemTokens",
          "type": "uint256"
        }
      ],
      "name": "redeemAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "redeemer",
          "type": "address"
        },
        {
          "name": "redeemAmount",
          "type": "uint256"
        },
        {
          "name": "redeemTokens",
          "type": "uint256"
        }
      ],
      "name": "redeemVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "payer",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "repayAmount",
          "type": "uint256"
        }
      ],
      "name": "repayBorrowAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "payer",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "actualRepayAmount",
          "type": "uint256"
        },
        {
          "name": "borrowerIndex",
          "type": "uint256"
        }
      ],
      "name": "repayBorrowVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cTokenCollateral",
          "type": "address"
        },
        {
          "name": "cTokenBorrowed",
          "type": "address"
        },
        {
          "name": "liquidator",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "seizeTokens",
          "type": "uint256"
        }
      ],
      "name": "seizeAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "name": "seizeGuardianPaused",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cTokenCollateral",
          "type": "address"
        },
        {
          "name": "cTokenBorrowed",
          "type": "address"
        },
        {
          "name": "liquidator",
          "type": "address"
        },
        {
          "name": "borrower",
          "type": "address"
        },
        {
          "name": "seizeTokens",
          "type": "uint256"
        }
      ],
      "name": "seizeVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "uint256"
        }
      ],
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "src",
          "type": "address"
        },
        {
          "name": "dst",
          "type": "address"
        },
        {
          "name": "transferTokens",
          "type": "uint256"
        }
      ],
      "name": "transferAllowed",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "outputs": [
        {
          "type": "bool"
        }
      ],
      "constant": true,
      "name": "transferGuardianPaused",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "name": "cToken",
          "type": "address"
        },
        {
          "name": "src",
          "type": "address"
        },
        {
          "name": "dst",
          "type": "address"
        },
        {
          "name": "transferTokens",
          "type": "uint256"
        }
      ],
      "name": "transferVerify",
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
''')