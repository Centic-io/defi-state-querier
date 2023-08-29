LIQEE_ETH = {
    "name": "Liqee Lending Pool",
    "rewardToken": "0x431ad2ff6a9C365805eBaD47Ee021148d6f7DBe0",
    "comptrollerAddress": "0x3bA6e5e5dF88b9A88B2c19449778A4754170EA17",
    "lensAddress": "0xa6c8d1c55951e8ac44a0eaa959be5fd21cc07531",
    "poolToken": "0x431ad2ff6a9C365805eBaD47Ee021148d6f7DBe0",
    "type": "LENDING_POOL",
    "forked": "compound",
    "reservesList": {
        "0x4Fabb145d64652a948d72533023f6E7A623C7C53": { #busd
            "cToken": "0x24677e213DeC0Ea53a430404cF4A11a6dc889FCe",
            "liquidationThreshold": 0.8
        },
        "0x6B175474E89094C44Da98b954EedeAC495271d0F": { #DAI
            "cToken": "0x298f243aD592b6027d4717fBe9DeCda668E3c3A8",
            "liquidationThreshold": 0.8
        },
        "0x431ad2ff6a9C365805eBaD47Ee021148d6f7DBe0": { #df
            "cToken": "0xb3dc7425e63E1855Eb41107134D471DD34d7b239",
            "liquidationThreshold": 0.4
        },
        "0x0000000000000000000000000000000000000000": {
            "cToken": "0x5ACD75f21659a59fFaB9AEBAf350351a8bfaAbc0",
            "liquidationThreshold": 0.8
        },
        "0x355C665e101B9DA58704A8fDDb5FeeF210eF20c0": { #goldx
            "cToken": "0x164315EA59169D46359baa4BcC6479bB421764b6",
            "liquidationThreshold": 0.8
        },
        "0x0316EB71485b0Ab14103307bf65a021042c6d380": { #hbtc
            "cToken": "0x47566acD7af49D2a192132314826ed3c3c5f3698",
            "liquidationThreshold": 0.8
        },
        "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984": { #uni
            "cToken": "0xbeC9A824D6dA8d0F923FD9fbec4FAA949d396320",
            "liquidationThreshold": 0.7
        },
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": { #usdc
            "cToken": "0x2f956b2f801c6dad74E87E7f45c94f6283BF0f45",
            "liquidationThreshold": 0.8
        },
        "0xdAC17F958D2ee523a2206206994597C13D831ec7": { # usdt
            "cToken": "0x1180c114f7fAdCB6957670432a3Cf8Ef08Ab5354",
            "liquidationThreshold": 0.0
        },
        # "0xeb269732ab75A6fD61Ea60b06fE994cD32a83549": { # usdx
        #     "cToken": "",
        #     "liquidationThreshold": 0.8
        # },
        "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": { # wbtc
            "cToken": "0x5812fCF91adc502a765E5707eBB3F36a07f63c02",
            "liquidationThreshold": 0.8
        },
        "0x0a5E677a6A24b2F1A2Bf4F3bFfC443231d2fDEc8": { # xusd_sp
            "cToken": "0xF54954BA7e3cdFDA23941753b48039aB5192AEa0",
            "liquidationThreshold": 0.8
        },
        "0x0a5E677a6A24b2F1A2Bf4F3bFfC443231d2fDEc8": { #xusd
            "cToken": "0x1AdC34Af68e970a93062b67344269fD341979eb0",
            "liquidationThreshold": 0.7
        },
        "0x0a5E677a6A24b2F1A2Bf4F3bFfC443231d2fDEc8": { #xusdmsd
            "cToken": "0xd1254d280e7504836e1B0E36535eBFf248483cEE",
            "liquidationThreshold": 0.0
        },
        "0xb986F3a2d91d3704Dc974A24FB735dCc5E3C1E70": { # xeur_sp
            "cToken": "0xab9C8C81228aBd4687078EBDA5AE236789b08673",
            "liquidationThreshold": 0.8
        },
        "0xb986F3a2d91d3704Dc974A24FB735dCc5E3C1E70": { # xeur
            "cToken": "0x44c324970e5CbC5D4C3F3B7604CbC6640C2dcFbF",
            "liquidationThreshold": 0.7
        },
        "0xb986F3a2d91d3704Dc974A24FB735dCc5E3C1E70": { # xeur_msd
            "cToken": "0x591595Bfae3f5d51A820ECd20A1e3FBb6638f34B",
            "liquidationThreshold": 0.0
        },
        "0x527Ec46Ac094B399265d1D71Eff7b31700aA655D": { # xbtc
            "cToken": "0x4013e6754634ca99aF31b5717Fa803714fA07B35",
            "liquidationThreshold": 0.7
        },
        "0x527Ec46Ac094B399265d1D71Eff7b31700aA655D": { # xbtc_gp
            "cToken": "0xfa2e831c674B61475C175B2206e81A5938B298Dd",
            "liquidationThreshold": 0.0
        },
        "0x8d2Cb35893C01fa8B564c84Bd540c5109d9D278e": { # xeth
            "cToken": "0x237C69E082A94d37EBdc92a84b58455872e425d6",
            "liquidationThreshold": 0.7
        },
        "0x8d2Cb35893C01fa8B564c84Bd540c5109d9D278e": { # xeth_gp
            "cToken": "0x028DB7A9d133301bD49f27b5E41F83F56aB0FaA6",
            "liquidationThreshold": 0.3
        },
        "0x32F9063bC2A2A57bCBe26ef662Dc867d5e6446d1": { # coinbase_msd
            "cToken": "0xb0ffBD1E81B60C4e8a8E19cEF3A6A92fe18Be86D",
            "liquidationThreshold": 0.0
        },
        "0x966E726853Ca97449F458A3B012318a08B508202": { # amazon_msd
            "cToken": "0xaab2BAb88ceeDCF6788F45885155B278faD09110",
            "liquidationThreshold": 0.0
        },
        "0x8dc6987F7D8E5aE9c39F767A324C5e46C1f731eB": { # xtsla_msd
            "cToken": "0xa4C13398DAdB3a0A7305647b406ACdCD0689FCC5",
            "liquidationThreshold": 0.0
        },
        "0xc4Ba45BeE9004408403b558a26099134282F2185": { # xaapl_msd
            "cToken": "0x3481E1a5A8014F9C7E03322e4d4532D8ec723409",
            "liquidationThreshold": 0.0
        }

    }
}
