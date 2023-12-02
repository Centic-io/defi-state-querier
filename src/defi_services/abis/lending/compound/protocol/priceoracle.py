
import json

PRICEORACLE = json.loads("""
[
  {
    "constant": true,
    "inputs": [],
    "name": "anchorAdmin",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "maxSwingMantissa",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "name": "_assetPrices",
    "outputs": [
      {
        "name": "mantissa",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "pendingAnchorAdmin",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "numBlocksPerPeriod",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "name": "readers",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "paused",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "name": "anchors",
    "outputs": [
      {
        "name": "period",
        "type": "uint256"
      },
      {
        "name": "priceMantissa",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "poster",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "name": "pendingAnchors",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "maxSwing",
    "outputs": [
      {
        "name": "mantissa",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "name": "_poster",
        "type": "address"
      },
      {
        "name": "addr0",
        "type": "address"
      },
      {
        "name": "reader0",
        "type": "address"
      },
      {
        "name": "addr1",
        "type": "address"
      },
      {
        "name": "reader1",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "payable": true,
    "stateMutability": "payable",
    "type": "fallback"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "msgSender",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "error",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "info",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "detail",
        "type": "uint256"
      }
    ],
    "name": "OracleFailure",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "anchorAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "oldScaledPrice",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "newScaledPrice",
        "type": "uint256"
      }
    ],
    "name": "NewPendingAnchor",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "previousPriceMantissa",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "requestedPriceMantissa",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "newPriceMantissa",
        "type": "uint256"
      }
    ],
    "name": "PricePosted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "asset",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "requestedPriceMantissa",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "anchorPriceMantissa",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "cappedPriceMantissa",
        "type": "uint256"
      }
    ],
    "name": "CappedPricePosted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "newState",
        "type": "bool"
      }
    ],
    "name": "SetPaused",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "oldPendingAnchorAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "newPendingAnchorAdmin",
        "type": "address"
      }
    ],
    "name": "NewPendingAnchorAdmin",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "oldAnchorAdmin",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "newAnchorAdmin",
        "type": "address"
      }
    ],
    "name": "NewAnchorAdmin",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "error",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "info",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "detail",
        "type": "uint256"
      }
    ],
    "name": "Failure",
    "type": "event"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "asset",
        "type": "address"
      },
      {
        "name": "newScaledPrice",
        "type": "uint256"
      }
    ],
    "name": "_setPendingAnchor",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
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
        "name": "requestedState",
        "type": "bool"
      }
    ],
    "name": "_setPaused",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
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
        "name": "newPendingAnchorAdmin",
        "type": "address"
      }
    ],
    "name": "_setPendingAnchorAdmin",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "_acceptAnchorAdmin",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "asset",
        "type": "address"
      }
    ],
    "name": "assetPrices",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "asset",
        "type": "address"
      }
    ],
    "name": "getPrice",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "asset",
        "type": "address"
      },
      {
        "name": "requestedPriceMantissa",
        "type": "uint256"
      }
    ],
    "name": "setPrice",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
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
        "name": "assets",
        "type": "address[]"
      },
      {
        "name": "requestedPriceMantissas",
        "type": "uint256[]"
      }
    ],
    "name": "setPrices",
    "outputs": [
      {
        "name": "",
        "type": "uint256[]"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
""")
        