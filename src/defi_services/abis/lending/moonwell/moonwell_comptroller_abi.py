MOONWELL_COMPTROLLER_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "action",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "pauseState",
                "type": "bool"
            }
        ],
        "name": "ActionPaused",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "action",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "pauseState",
                "type": "bool"
            }
        ],
        "name": "ActionPaused",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "error",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "info",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "detail",
                "type": "uint256"
            }
        ],
        "name": "Failure",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "MarketEntered",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "MarketExited",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            }
        ],
        "name": "MarketListed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newBorrowCap",
                "type": "uint256"
            }
        ],
        "name": "NewBorrowCap",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldBorrowCapGuardian",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newBorrowCapGuardian",
                "type": "address"
            }
        ],
        "name": "NewBorrowCapGuardian",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "oldCloseFactorMantissa",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newCloseFactorMantissa",
                "type": "uint256"
            }
        ],
        "name": "NewCloseFactor",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "oldCollateralFactorMantissa",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newCollateralFactorMantissa",
                "type": "uint256"
            }
        ],
        "name": "NewCollateralFactor",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "oldLiquidationIncentiveMantissa",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newLiquidationIncentiveMantissa",
                "type": "uint256"
            }
        ],
        "name": "NewLiquidationIncentive",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldPauseGuardian",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newPauseGuardian",
                "type": "address"
            }
        ],
        "name": "NewPauseGuardian",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract PriceOracle",
                "name": "oldPriceOracle",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "contract PriceOracle",
                "name": "newPriceOracle",
                "type": "address"
            }
        ],
        "name": "NewPriceOracle",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "contract MultiRewardDistributor",
                "name": "oldRewardDistributor",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "contract MultiRewardDistributor",
                "name": "newRewardDistributor",
                "type": "address"
            }
        ],
        "name": "NewRewardDistributor",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newSupplyCap",
                "type": "uint256"
            }
        ],
        "name": "NewSupplyCap",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldSupplyCapGuardian",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newSupplyCapGuardian",
                "type": "address"
            }
        ],
        "name": "NewSupplyCapGuardian",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "contract Unitroller",
                "name": "unitroller",
                "type": "address"
            }
        ],
        "name": "_become",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_tokenAddress",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "_rescueFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newBorrowCapGuardian",
                "type": "address"
            }
        ],
        "name": "_setBorrowCapGuardian",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "state",
                "type": "bool"
            }
        ],
        "name": "_setBorrowPaused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "newCloseFactorMantissa",
                "type": "uint256"
            }
        ],
        "name": "_setCloseFactor",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "newCollateralFactorMantissa",
                "type": "uint256"
            }
        ],
        "name": "_setCollateralFactor",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "newLiquidationIncentiveMantissa",
                "type": "uint256"
            }
        ],
        "name": "_setLiquidationIncentive",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MToken[]",
                "name": "mTokens",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "newBorrowCaps",
                "type": "uint256[]"
            }
        ],
        "name": "_setMarketBorrowCaps",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MToken[]",
                "name": "mTokens",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "newSupplyCaps",
                "type": "uint256[]"
            }
        ],
        "name": "_setMarketSupplyCaps",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "state",
                "type": "bool"
            }
        ],
        "name": "_setMintPaused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newPauseGuardian",
                "type": "address"
            }
        ],
        "name": "_setPauseGuardian",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract PriceOracle",
                "name": "newOracle",
                "type": "address"
            }
        ],
        "name": "_setPriceOracle",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MultiRewardDistributor",
                "name": "newRewardDistributor",
                "type": "address"
            }
        ],
        "name": "_setRewardDistributor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bool",
                "name": "state",
                "type": "bool"
            }
        ],
        "name": "_setSeizePaused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newSupplyCapGuardian",
                "type": "address"
            }
        ],
        "name": "_setSupplyCapGuardian",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bool",
                "name": "state",
                "type": "bool"
            }
        ],
        "name": "_setTransferPaused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            }
        ],
        "name": "_supportMarket",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "accountAssets",
        "outputs": [
            {
                "internalType": "contract MToken",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "admin",
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
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "allMarkets",
        "outputs": [
            {
                "internalType": "contract MToken",
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
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "borrowAmount",
                "type": "uint256"
            }
        ],
        "name": "borrowAllowed",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "borrowCapGuardian",
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
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "borrowCaps",
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
                "name": "",
                "type": "address"
            }
        ],
        "name": "borrowGuardianPaused",
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
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "contract MToken",
                "name": "mToken",
                "type": "address"
            }
        ],
        "name": "checkMembership",
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
                "internalType": "address[]",
                "name": "holders",
                "type": "address[]"
            },
            {
                "internalType": "contract MToken[]",
                "name": "mTokens",
                "type": "address[]"
            },
            {
                "internalType": "bool",
                "name": "borrowers",
                "type": "bool"
            },
            {
                "internalType": "bool",
                "name": "suppliers",
                "type": "bool"
            }
        ],
        "name": "claimReward",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "holder",
                "type": "address"
            },
            {
                "internalType": "contract MToken[]",
                "name": "mTokens",
                "type": "address[]"
            }
        ],
        "name": "claimReward",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "claimReward",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "holder",
                "type": "address"
            }
        ],
        "name": "claimReward",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "closeFactorMantissa",
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
        "name": "comptrollerImplementation",
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
                "internalType": "address[]",
                "name": "mTokens",
                "type": "address[]"
            }
        ],
        "name": "enterMarkets",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "mTokenAddress",
                "type": "address"
            }
        ],
        "name": "exitMarket",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "getAccountLiquidity",
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
        "name": "getAllMarkets",
        "outputs": [
            {
                "internalType": "contract MToken[]",
                "name": "",
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
                "name": "account",
                "type": "address"
            }
        ],
        "name": "getAssetsIn",
        "outputs": [
            {
                "internalType": "contract MToken[]",
                "name": "",
                "type": "address[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getBlockTimestamp",
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
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "mTokenModify",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "redeemTokens",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "borrowAmount",
                "type": "uint256"
            }
        ],
        "name": "getHypotheticalAccountLiquidity",
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
        "name": "isComptroller",
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
                "name": "mTokenBorrowed",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "mTokenCollateral",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "liquidator",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "repayAmount",
                "type": "uint256"
            }
        ],
        "name": "liquidateBorrowAllowed",
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
                "name": "mTokenBorrowed",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "mTokenCollateral",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "actualRepayAmount",
                "type": "uint256"
            }
        ],
        "name": "liquidateCalculateSeizeTokens",
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
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "liquidationIncentiveMantissa",
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
                "name": "",
                "type": "address"
            }
        ],
        "name": "markets",
        "outputs": [
            {
                "internalType": "bool",
                "name": "isListed",
                "type": "bool"
            },
            {
                "internalType": "uint256",
                "name": "collateralFactorMantissa",
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
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "minter",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "mintAmount",
                "type": "uint256"
            }
        ],
        "name": "mintAllowed",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
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
        "name": "mintGuardianPaused",
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
        "inputs": [],
        "name": "oracle",
        "outputs": [
            {
                "internalType": "contract PriceOracle",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "pauseGuardian",
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
        "name": "pendingAdmin",
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
        "name": "pendingComptrollerImplementation",
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
                "internalType": "address",
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "redeemer",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "redeemTokens",
                "type": "uint256"
            }
        ],
        "name": "redeemAllowed",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "redeemer",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "redeemAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "redeemTokens",
                "type": "uint256"
            }
        ],
        "name": "redeemVerify",
        "outputs": [],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "payer",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "repayAmount",
                "type": "uint256"
            }
        ],
        "name": "repayBorrowAllowed",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "rewardDistributor",
        "outputs": [
            {
                "internalType": "contract MultiRewardDistributor",
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
                "name": "mTokenCollateral",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "mTokenBorrowed",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "liquidator",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "borrower",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "seizeTokens",
                "type": "uint256"
            }
        ],
        "name": "seizeAllowed",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "seizeGuardianPaused",
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
        "inputs": [],
        "name": "supplyCapGuardian",
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
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "supplyCaps",
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
                "name": "mToken",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "src",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "dst",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "transferTokens",
                "type": "uint256"
            }
        ],
        "name": "transferAllowed",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "transferGuardianPaused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
