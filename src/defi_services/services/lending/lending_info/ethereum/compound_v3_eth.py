COMPOUND_V3_ETH = {
    "name": "Compound V3 Lending Pool",
    "rewardToken": "0xc00e94cb662c3520282e6f5717214004a7f26888",
    "rewardAddress": "0x1b0e765f6224c21223aea2af16c1c46e38885a40",
    "factoryAddress": "0xa7f7de6ccad4d83d81676717053883337ac2c1b4",
    "poolToken": "0xc00e94cb662c3520282e6f5717214004a7f26888",
    "type": "LENDING_POOL",
    "forked": "compound-v3",
    "reservesList": {
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {
            "comet": "0xa17581a9e3356d9a858b789d68b4d866e593ae94",
            "assets": {
                "0xbe9895146f7af43049ca1c1ae358b0541ea49704": {
                    "priceFeed": "0x23a982b74a3236a5f2297856d4391b2edbbb5549",
                    "loanToValue": 0.9,
                    "liquidationThreshold": 0.93
                },
                "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0": {
                    "priceFeed": "0x4f67e4d9bd67efa28236013288737d39aef48e79",
                    "loanToValue": 0.9,
                    "liquidationThreshold": 0.93
                }
            }
        },
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {
            "comet": "0xc3d688b66703497daa19211eedff47f25384cdc3",
            "assets": {
                "0xc00e94cb662c3520282e6f5717214004a7f26888": {
                    "priceFeed": "0xdbd020caef83efd542f4de03e3cf0c28a4428bd5",
                    "loanToValue": 0.65,
                    "liquidationThreshold": 0.7
                },
                "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": {
                    "priceFeed": "0xf4030086522a5beea4988f8ca5b36dbc97bee88c",
                    "loanToValue": 0.7,
                    "liquidationThreshold": 0.77
                },
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {
                    "priceFeed": "0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419",
                    "loanToValue": 0.825,
                    "liquidationThreshold": 0.895
                },
                "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": {
                    "priceFeed": "0x553303d460ee0afb37edff9be42922d8ff63220e",
                    "loanToValue": 0.75,
                    "liquidationThreshold": 0.81
                },
                "0x514910771af9ca656af840dff83e8264ecf986ca": {
                    "priceFeed": "0x2c1d072e956affc0d435cb7ac38ef18d24d9127c",
                    "loanToValue": 0.79,
                    "liquidationThreshold": 0.85
                }
            }
        }
    }
}
