import json

SILO_REPOSITORY_ABI = json.loads('''
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_siloFactory",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_tokensFactory",
        "type": "address"
      },
      {
        "internalType": "uint64",
        "name": "_defaultMaxLTV",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "_defaultLiquidationThreshold",
        "type": "uint64"
      },
      {
        "internalType": "address[]",
        "name": "_initialBridgeAssets",
        "type": "address[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "AssetAlreadyAdded",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "AssetIsNotABridge",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "AssetIsZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "BridgeAssetIsZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ConfigDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "EmptyBridgeAssets",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "FeesDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "GlobalLimitDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "GlobalPauseDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InterestRateModelDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidEntryFee",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidInterestRateModel",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidLTV",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidLiquidationThreshold",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidNotificationReceiver",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidPriceProvidersRepository",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidProtocolLiquidationFee",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidProtocolShareFee",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidSiloFactory",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidSiloRouter",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidSiloVersion",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "InvalidTokensFactory",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "LastBridgeAsset",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "LiquidationThresholdDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ManagerDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ManagerIsZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "MaxLiquidityDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "MaximumLTVDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NoPriceProviderForAsset",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "NotificationReceiverDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "OnlyManager",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "OnlyOwnerOrManager",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "PriceProviderRepositoryDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "RouterDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloAlreadyExistsForAsset",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloAlreadyExistsForBridgeAssets",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloDoesNotExist",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloIsZero",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloMaxLiquidityDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloNotAllowedForBridgeAsset",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloPauseDidNotChange",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "SiloVersionDoesNotExist",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "TokenIsNotAContract",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "VersionForAssetDidNotChange",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "silo",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "components": [
          {
            "internalType": "uint64",
            "name": "maxLoanToValue",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "liquidationThreshold",
            "type": "uint64"
          },
          {
            "internalType": "contract IInterestRateModel",
            "name": "interestRateModel",
            "type": "address"
          }
        ],
        "indexed": false,
        "internalType": "struct ISiloRepository.AssetConfig",
        "name": "assetConfig",
        "type": "tuple"
      }
    ],
    "name": "AssetConfigUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "newBridgeAsset",
        "type": "address"
      }
    ],
    "name": "BridgeAssetAdded",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "bridgeAssetRemoved",
        "type": "address"
      }
    ],
    "name": "BridgeAssetRemoved",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "pool",
        "type": "address"
      }
    ],
    "name": "BridgePool",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newMaxDeposits",
        "type": "uint256"
      }
    ],
    "name": "DefaultSiloMaxDepositsLimitUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint64",
        "name": "newEntryFee",
        "type": "uint64"
      },
      {
        "indexed": false,
        "internalType": "uint64",
        "name": "newProtocolShareFee",
        "type": "uint64"
      },
      {
        "indexed": false,
        "internalType": "uint64",
        "name": "newProtocolLiquidationFee",
        "type": "uint64"
      }
    ],
    "name": "FeeUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bool",
        "name": "globalPause",
        "type": "bool"
      }
    ],
    "name": "GlobalPause",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "contract IInterestRateModel",
        "name": "newModel",
        "type": "address"
      }
    ],
    "name": "InterestRateModel",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bool",
        "name": "newLimitedMaxLiquidityState",
        "type": "bool"
      }
    ],
    "name": "LimitedMaxLiquidityToggled",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address",
        "name": "manager",
        "type": "address"
      }
    ],
    "name": "ManagerChanged",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint64",
        "name": "defaultLiquidationThreshold",
        "type": "uint64"
      }
    ],
    "name": "NewDefaultLiquidationThreshold",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint64",
        "name": "defaultMaximumLTV",
        "type": "uint64"
      }
    ],
    "name": "NewDefaultMaximumLTV",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "silo",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "siloVersion",
        "type": "uint128"
      }
    ],
    "name": "NewSilo",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "contract INotificationReceiver",
        "name": "newIncentiveContract",
        "type": "address"
      }
    ],
    "name": "NotificationReceiverUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "newPendingOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipPending",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
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
        "internalType": "contract IPriceProvidersRepository",
        "name": "newProvider",
        "type": "address"
      }
    ],
    "name": "PriceProvidersRepositoryUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "factory",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "siloLatestVersion",
        "type": "uint128"
      },
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "siloDefaultVersion",
        "type": "uint128"
      }
    ],
    "name": "RegisterSiloVersion",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "newRouter",
        "type": "address"
      }
    ],
    "name": "RouterUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "newDefaultVersion",
        "type": "uint128"
      }
    ],
    "name": "SiloDefaultVersion",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "silo",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "newMaxDeposits",
        "type": "uint256"
      }
    ],
    "name": "SiloMaxDepositsLimitsUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address",
        "name": "silo",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "bool",
        "name": "pauseValue",
        "type": "bool"
      }
    ],
    "name": "SiloPause",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "newTokensFactory",
        "type": "address"
      }
    ],
    "name": "TokensFactoryUpdate",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "factory",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "siloVersion",
        "type": "uint128"
      }
    ],
    "name": "UnregisterSiloVersion",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint128",
        "name": "version",
        "type": "uint128"
      }
    ],
    "name": "VersionForAsset",
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
        "internalType": "address",
        "name": "_newBridgeAsset",
        "type": "address"
      }
    ],
    "name": "addBridgeAsset",
    "outputs": [],
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
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "assetConfigs",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "maxLoanToValue",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "liquidationThreshold",
        "type": "uint64"
      },
      {
        "internalType": "contract IInterestRateModel",
        "name": "interestRateModel",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "bridgePool",
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
        "name": "_manager",
        "type": "address"
      }
    ],
    "name": "changeManager",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "defaultAssetConfig",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "maxLoanToValue",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "liquidationThreshold",
        "type": "uint64"
      },
      {
        "internalType": "contract IInterestRateModel",
        "name": "interestRateModel",
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
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "_assetIsABridge",
        "type": "bool"
      }
    ],
    "name": "ensureCanCreateSiloFor",
    "outputs": [],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "entryFee",
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
    "name": "fees",
    "outputs": [
      {
        "internalType": "uint64",
        "name": "entryFee",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "protocolShareFee",
        "type": "uint64"
      },
      {
        "internalType": "uint64",
        "name": "protocolLiquidationFee",
        "type": "uint64"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getBridgeAssets",
    "outputs": [
      {
        "internalType": "address[]",
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
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "getInterestRateModel",
    "outputs": [
      {
        "internalType": "contract IInterestRateModel",
        "name": "model",
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
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "getLiquidationThreshold",
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
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "getMaxSiloDepositsValue",
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
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "getMaximumLTV",
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
    "name": "getNotificationReceiver",
    "outputs": [
      {
        "internalType": "contract INotificationReceiver",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getRemovedBridgeAssets",
    "outputs": [
      {
        "internalType": "address[]",
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
        "name": "",
        "type": "address"
      }
    ],
    "name": "getSilo",
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
    "name": "getVersionForAsset",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "isPaused",
    "outputs": [
      {
        "internalType": "bool",
        "name": "globalPause",
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
        "name": "_silo",
        "type": "address"
      }
    ],
    "name": "isSilo",
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
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      }
    ],
    "name": "isSiloPaused",
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
    "name": "manager",
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
    "name": "maxLiquidity",
    "outputs": [
      {
        "internalType": "bool",
        "name": "globalLimit",
        "type": "bool"
      },
      {
        "internalType": "uint256",
        "name": "defaultMaxLiquidity",
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
        "name": "_siloAsset",
        "type": "address"
      },
      {
        "internalType": "bytes",
        "name": "_siloData",
        "type": "bytes"
      }
    ],
    "name": "newSilo",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
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
    "name": "pendingOwner",
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
    "name": "priceProvidersRepository",
    "outputs": [
      {
        "internalType": "contract IPriceProvidersRepository",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "protocolLiquidationFee",
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
    "name": "protocolShareFee",
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
        "internalType": "contract ISiloFactory",
        "name": "_factory",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "_isDefault",
        "type": "bool"
      }
    ],
    "name": "registerSiloVersion",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_bridgeAssetToRemove",
        "type": "address"
      }
    ],
    "name": "removeBridgeAsset",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "removePendingOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_siloAsset",
        "type": "address"
      },
      {
        "internalType": "uint128",
        "name": "_siloVersion",
        "type": "uint128"
      },
      {
        "internalType": "bytes",
        "name": "_siloData",
        "type": "bytes"
      }
    ],
    "name": "replaceSilo",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "router",
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
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "components": [
          {
            "internalType": "uint64",
            "name": "maxLoanToValue",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "liquidationThreshold",
            "type": "uint64"
          },
          {
            "internalType": "contract IInterestRateModel",
            "name": "interestRateModel",
            "type": "address"
          }
        ],
        "internalType": "struct ISiloRepository.AssetConfig",
        "name": "_assetConfig",
        "type": "tuple"
      }
    ],
    "name": "setAssetConfig",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "contract IInterestRateModel",
        "name": "_defaultInterestRateModel",
        "type": "address"
      }
    ],
    "name": "setDefaultInterestRateModel",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint64",
        "name": "_defaultLiquidationThreshold",
        "type": "uint64"
      }
    ],
    "name": "setDefaultLiquidationThreshold",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint64",
        "name": "_defaultMaxLTV",
        "type": "uint64"
      }
    ],
    "name": "setDefaultMaximumLTV",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_maxDeposits",
        "type": "uint256"
      }
    ],
    "name": "setDefaultSiloMaxDepositsLimit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint128",
        "name": "_defaultVersion",
        "type": "uint128"
      }
    ],
    "name": "setDefaultSiloVersion",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "uint64",
            "name": "entryFee",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "protocolShareFee",
            "type": "uint64"
          },
          {
            "internalType": "uint64",
            "name": "protocolLiquidationFee",
            "type": "uint64"
          }
        ],
        "internalType": "struct ISiloRepository.Fees",
        "name": "_fees",
        "type": "tuple"
      }
    ],
    "name": "setFees",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "_globalPause",
        "type": "bool"
      }
    ],
    "name": "setGlobalPause",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "_globalLimit",
        "type": "bool"
      }
    ],
    "name": "setLimitedMaxLiquidity",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "contract INotificationReceiver",
        "name": "_newNotificationReceiver",
        "type": "address"
      }
    ],
    "name": "setNotificationReceiver",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "contract IPriceProvidersRepository",
        "name": "_repository",
        "type": "address"
      }
    ],
    "name": "setPriceProvidersRepository",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_router",
        "type": "address"
      }
    ],
    "name": "setRouter",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_maxDeposits",
        "type": "uint256"
      }
    ],
    "name": "setSiloMaxDepositsLimit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_silo",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_asset",
        "type": "address"
      },
      {
        "internalType": "bool",
        "name": "_pauseValue",
        "type": "bool"
      }
    ],
    "name": "setSiloPause",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_tokensFactory",
        "type": "address"
      }
    ],
    "name": "setTokensFactory",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_siloAsset",
        "type": "address"
      },
      {
        "internalType": "uint128",
        "name": "_version",
        "type": "uint128"
      }
    ],
    "name": "setVersionForAsset",
    "outputs": [],
    "stateMutability": "nonpayable",
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
    "name": "siloFactory",
    "outputs": [
      {
        "internalType": "contract ISiloFactory",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "siloRepositoryPing",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
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
    "name": "siloReverse",
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
    "name": "siloVersion",
    "outputs": [
      {
        "internalType": "uint128",
        "name": "byDefault",
        "type": "uint128"
      },
      {
        "internalType": "uint128",
        "name": "latest",
        "type": "uint128"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "tokensFactory",
    "outputs": [
      {
        "internalType": "contract ITokensFactory",
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
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newPendingOwner",
        "type": "address"
      }
    ],
    "name": "transferPendingOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint128",
        "name": "_siloVersion",
        "type": "uint128"
      }
    ],
    "name": "unregisterSiloVersion",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
''')