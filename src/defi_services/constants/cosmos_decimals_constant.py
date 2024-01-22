class Denoms:
    def __init__(self, denom: str, decimal: int):
        self.denom = denom
        self.decimal = decimal

    data = {
        "uatom": {
            "name": "ATOM",
            "denom": "uatom",
            "decimal": 6
        },
        "ibc/0025f8a87464a471e66b234c4f93aec5b4da3d42d7986451a059273426290dd5": {
            "name": "NTRN",
            "denom": "ibc/0025f8a87464a471e66b234c4f93aec5b4da3d42d7986451a059273426290dd5",
            "decimal": 6
        },
        "ibc/f663521bf1836b00f5f177680f74bfb9a8b5654a694d0d2bc249e03cf2509013": {
            "name": "USDC",
            "denom": "ibc/f663521bf1836b00f5f177680f74bfb9a8b5654a694d0d2bc249e03cf2509013",
            "decimal": 6
        },
        "ibc/b05539b66b72e2739b986b86391e5d08f12b8d5d2c2a7f8f8cf9adf674dfa231": {
            "name": "stATOM",
            "denom": "ibc/b05539b66b72e2739b986b86391e5d08f12b8d5d2c2a7f8f8cf9adf674dfa231",
            "decimal": 6
        },
        "ibc/2181aab0218eac24bc9f86bd1364fbbfa3e6e3fcc25e88e3e68c15dc6e752d86": {
            "name": "AKT",
            "denom": "ibc/2181aab0218eac24bc9f86bd1364fbbfa3e6e3fcc25e88e3e68c15dc6e752d86",
            "decimal": 6
        },
        "ibc/6b8a3f5c2ad51cd6171fa41a7e8c35ad594ab69226438db94450436ea57b3a89": {
            "name": "STRD",
            "denom": "ibc/6b8a3f5c2ad51cd6171fa41a7e8c35ad594ab69226438db94450436ea57b3a89",
            "decimal": 6
        },
        "ibc/14f9bc3e44b8a9c1be1fb08980fab87034c9905ef17cf2f5008fc085218811cc": {
            "name": "OSMO",
            "denom": "ibc/14f9bc3e44b8a9c1be1fb08980fab87034c9905ef17cf2f5008fc085218811cc",
            "decimal": 6
        },
        "ibc/e7d5e9d0e9bf8b7354929a817dd28d4d017e745f638954764aa88522a7a409ec": {
            "name": "BTSG",
            "denom": "ibc/e7d5e9d0e9bf8b7354929a817dd28d4d017e745f638954764aa88522a7a409ec",
            "decimal": 6
        },
        "ibc/054892d6bb43af8b93aac28aa5fd7019d2c59a15dafd6f45c1fa2bf9bda22454": {
            "name": "stOSMO",
            "denom": "ibc/054892d6bb43af8b93aac28aa5fd7019d2c59a15dafd6f45c1fa2bf9bda22454",
            "decimal": 6
        },
        "ibc/adbec1a7ac2fef73e06b066a1c94dab6c27924ef7ea3f5a43378150009620284": {
            "name": "BCNA",
            "denom": "ibc/adbec1a7ac2fef73e06b066a1c94dab6c27924ef7ea3f5a43378150009620284",
            "decimal": 6
        },
        "ibc/12da42304ee1ce96071f712aa4d58186ad11c3165c0dcda71e017a54f3935e66": {
            "name": "IRIS",
            "denom": "ibc/12da42304ee1ce96071f712aa4d58186ad11c3165c0dcda71e017a54f3935e66",
            "decimal": 6
        },
        "ibc/b011c1a0ad5e717f674ba59fd8e05b2f946e4fd41c9cb3311c95f7ed4b815620": {
            "name": "stINJ",
            "denom": "ibc/b011c1a0ad5e717f674ba59fd8e05b2f946e4fd41c9cb3311c95f7ed4b815620",
            "decimal": 18
        },
        "ibc/81d08bc39fb520ebd948cf017910dd69702d34bf5ac160f76d3b5cfc444ebce0": {
            "name": "XPRT",
            "denom": "ibc/81d08bc39fb520ebd948cf017910dd69702d34bf5ac160f76d3b5cfc444ebce0",
            "decimal": 6
        },
        "ibc/c932adfe2b4216397a4f17458b6e4468499b86c3bc8116180f85d799d6f5cc1b": {
            "name": "CRO",
            "denom": "ibc/c932adfe2b4216397a4f17458b6e4468499b86c3bc8116180f85d799d6f5cc1b",
            "decimal": 8
        },
        "ibc/42e47a5ba708ebe6e0c227006254f2784e209f4dbd3c6bb77edc4b29ef875e8e": {
            "name": "DVPN",
            "denom": "ibc/42e47a5ba708ebe6e0c227006254f2784e209f4dbd3c6bb77edc4b29ef875e8e",
            "decimal": 6
        },
        "ibc/1fbdd58d438b4d04d26cbfb2e722c18984a0f1a52468c4f42f37d102f3d3f399": {
            "name": "REGEN",
            "denom": "ibc/1fbdd58d438b4d04d26cbfb2e722c18984a0f1a52468c4f42f37d102f3d3f399",
            "decimal": 6
        },
        "ibc/19dd710119533524061885a6f190b18af28d9537e2bae37f32a62c1a25979287": {
            "name": "EVMOS",
            "denom": "ibc/19dd710119533524061885a6f190b18af28d9537e2bae37f32a62c1a25979287",
            "decimal": 18
        },
        "ibc/88dcaa43a9cd099e1f9bbb80b9a90f64782eba115a84b2cd8398757ada4f4b40": {
            "name": "stJUNO",
            "denom": "ibc/88dcaa43a9cd099e1f9bbb80b9a90f64782eba115a84b2cd8398757ada4f4b40",
            "decimal": 6
        },
        "ibc/715bd634cf4d914c3ee93b0f8a9d2514b743f6fe36bc80263d1bc5ee4b3c5d40": {
            "name": "stSTARS",
            "denom": "ibc/715bd634cf4d914c3ee93b0f8a9d2514b743f6fe36bc80263d1bc5ee4b3c5d40",
            "decimal": 6
        },
        "ibc/6469bda6f62c4f4b8f76629fa1e72a02a3d1dd9e2b22ddb3c3b2296dead29ab8": {
            "name": "INJ",
            "denom": "ibc/6469bda6f62c4f4b8f76629fa1e72a02a3d1dd9e2b22ddb3c3b2296dead29ab8",
            "decimal": 18
        },
        "ibc/5bb694d466ccf099ef73f165f88472af51d9c4991eaa42bd1168c5304712cc0d": {
            "name": "ION",
            "denom": "ibc/5bb694d466ccf099ef73f165f88472af51d9c4991eaa42bd1168c5304712cc0d",
            "decimal": 6
        },
        "ibc/533e5ffc606fd11b8dca309c66afd6a1f046ef784a73f323a332cf6823f0ea87": {
            "name": "XKI",
            "denom": "ibc/533e5ffc606fd11b8dca309c66afd6a1f046ef784a73f323a332cf6823f0ea87",
            "decimal": 6
        },
        "ibc/1542f8dc70e7999691e991e1edeb1b47e65e3a217b1649d347098ee48acb580f": {
            "name": "SCRT",
            "denom": "ibc/1542f8dc70e7999691e991e1edeb1b47e65e3a217b1649d347098ee48acb580f",
            "decimal": 6
        },
        "ibc/cdab23da5495290063363bd1c3499e26189036302dc689985a7e23f8df8d8db0": {
            "name": "JUNO",
            "denom": "ibc/cdab23da5495290063363bd1c3499e26189036302dc689985a7e23f8df8d8db0",
            "decimal": 6
        },
        "ibc/68a333688e5b07451f95555f8fe510e43ef9d3d44df0909964f92081ef9be5a7": {
            "name": "IOV",
            "denom": "ibc/68a333688e5b07451f95555f8fe510e43ef9d3d44df0909964f92081ef9be5a7",
            "decimal": 6
        },
        "ibc/1d5826f7ede6e3b13009fef994dc9caaf15cc24ca7a9ff436ffb2e56fd72f54f": {
            "name": "LIKE",
            "denom": "ibc/1d5826f7ede6e3b13009fef994dc9caaf15cc24ca7a9ff436ffb2e56fd72f54f",
            "decimal": 9
        },
        "ibc/dec41a02e47658d40fc71e5a35a9c807111f5a6662a3fb5da84c4e6f53e616b3": {
            "name": "UMEE",
            "denom": "ibc/dec41a02e47658d40fc71e5a35a9c807111f5a6662a3fb5da84c4e6f53e616b3",
            "decimal": 6
        },
        "ibc/f5ed5f3dc6f0ef73fa455337c027fe91abcb375116bf51a228e44c493e020a09": {
            "name": "ROWAN",
            "denom": "ibc/f5ed5f3dc6f0ef73fa455337c027fe91abcb375116bf51a228e44c493e020a09",
            "decimal": 18
        },
        "ibc/5cae744c89bc70ae7b38019a1edf83199b7e10f00f160e7f4f12bca7a32a7ee5": {
            "name": "stLUNA",
            "denom": "ibc/5cae744c89bc70ae7b38019a1edf83199b7e10f00f160e7f4f12bca7a32a7ee5",
            "decimal": 6
        },
        "ibc/8870c4203cebf2279ba065e3de95fc3f8e05a4a93424e7dc707a21514be353a0": {
            "name": "KAVA",
            "denom": "ibc/8870c4203cebf2279ba065e3de95fc3f8e05a4a93424e7dc707a21514be353a0",
            "decimal": 6
        },
        "ibc/e070ce91cc4bd15aec9b5788c0826755aad35052a3037e9ac62be70b4c9a7dbb": {
            "name": "EEUR",
            "denom": "ibc/b93f321238f7bb15ab5b882660aae72286c8e9035de34e2b30f60e54c623c63c",
            "decimal": 6
        },
        "": {
            "name": "NGM",
            "denom": "ibc/e070ce91cc4bd15aec9b5788c0826755aad35052a3037e9ac62be70b4c9a7dbb",
            "decimal": 6
        },
        "ibc/835ee9d00c35d72128f195b50f8a89eb83e5011c43ea0aa00d16348e2208febb": {
            "name": "bCRE",
            "denom": "ibc/835ee9d00c35d72128f195b50f8a89eb83e5011c43ea0aa00d16348e2208febb",
            "decimal": 6
        },
        "ibc/3f18d520ce791a40357d061fad657ced6b21d023f229eaf131d7fe7ce6f488bd": {
            "name": "CRE",
            "denom": "ibc/3f18d520ce791a40357d061fad657ced6b21d023f229eaf131d7fe7ce6f488bd",
            "decimal": 6
        },
        "ibc/db9aaadfbe21e014373ef97141d451f453b9b9a2c8b65f5cf8e7ce57531b6850": {
            "name": "CRO",
            "denom": "ibc/db9aaadfbe21e014373ef97141d451f453b9b9a2c8b65f5cf8e7ce57531b6850",
            "decimal": 8
        },
        "ibc/20a7dc8e24709e6f1ee0f4e832c2ed345add77425890482a349ae3c43cac6b2c": {
            "name": "ATOLO",
            "denom": "ibc/20a7dc8e24709e6f1ee0f4e832c2ed345add77425890482a349ae3c43cac6b2c",
            "decimal": 6
        }
    }
