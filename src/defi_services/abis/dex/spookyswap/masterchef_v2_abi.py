SPOOKYSWAP_MASTERCHEF_V2_ABI = [{
    "inputs": [{
        "internalType": "contract IMasterChef", "name": "_MASTER_CHEF",
        "type": "address"},
        {"internalType": "contract IERC20", "name": "_boo", "type": "address"},
        {"internalType": "uint256", "name": "_MASTER_PID", "type": "uint256"}],
    "stateMutability": "nonpayable", "type": "constructor"}, {
    "anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "by", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"}], "name": "AddAuth",
    "type": "event"}, {
    "anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
        {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"}], "name": "Deposit",
    "type": "event"}, {
    "anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
        {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"}], "name": "EmergencyWithdraw",
    "type": "event"}, {
    "anonymous": False, "inputs": [
        {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
        {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "Harvest",
    "type": "event"},
    {"anonymous": False, "inputs": [], "name": "LogInit", "type": "event"}, {
        "anonymous": False, "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "allocPoint", "type": "uint256"},
            {"indexed": True, "internalType": "contract IERC20", "name": "lpToken", "type": "address"},
            {"indexed": False, "internalType": "contract IRewarder", "name": "rewarder", "type": "address"},
            {"indexed": False, "internalType": "bool", "name": "update", "type": "bool"}], "name": "LogPoolAddition",
        "type": "event"}, {
        "anonymous": False, "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "allocPoint", "type": "uint256"},
            {"indexed": False, "internalType": "contract IRewarder", "name": "rewarder", "type": "address"},
            {"indexed": False, "internalType": "bool", "name": "overwrite", "type": "bool"},
            {"indexed": False, "internalType": "bool", "name": "update", "type": "bool"}], "name": "LogSetPool",
        "type": "event"}, {
        "anonymous": False, "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "lastRewardTime", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "lpSupply", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "accBooPerShare", "type": "uint256"}],
        "name": "LogUpdatePool", "type": "event"}, {
        "anonymous": False, "inputs": [
            {"indexed": True, "internalType": "address", "name": "by", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"}], "name": "RevokeAuth",
        "type": "event"}, {
        "anonymous": False, "inputs": [
            {"indexed": True, "internalType": "address", "name": "by", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"}], "name": "SetAdmin",
        "type": "event"}, {
        "anonymous": False, "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": True, "internalType": "uint256", "name": "pid", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"}], "name": "Withdraw",
        "type": "event"}, {
        "inputs": [], "name": "BOO",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "MASTER_CHEF", "outputs": [
            {"internalType": "contract IMasterChef", "name": "", "type": "address"}], "stateMutability": "view",
        "type": "function"}, {
        "inputs": [], "name": "MASTER_PID",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "V1_HARVEST_QUERY_TIME",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint64", "name": "allocPoint", "type": "uint64"}, {
            "internalType": "contract IERC20", "name": "_lpToken", "type": "address"}, {
                       "internalType": "contract IRewarder", "name": "_rewarder",
                       "type": "address"},
                   {"internalType": "bool", "name": "update", "type": "bool"}],
        "name": "add", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {
        "inputs": [{"internalType": "address", "name": "_auth", "type": "address"}],
        "name": "addAuth", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [], "name": "admin",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "authorized",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "booPerSecond",
        "outputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"},
                   {"internalType": "uint256", "name": "amount", "type": "uint256"},
                   {"internalType": "address", "name": "to", "type": "address"}],
        "name": "deposit", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"},
                   {"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "deposit", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"},
                   {"internalType": "address", "name": "to", "type": "address"}],
        "name": "emergencyWithdraw", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"}],
        "name": "emergencyWithdraw", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"}],
        "name": "getFarmData", "outputs": [{
            "components": [{
                "internalType": "uint128",
                "name": "accBooPerShare",
                "type": "uint128"}, {
                "internalType": "uint64",
                "name": "lastRewardTime",
                "type": "uint64"}, {
                "internalType": "uint64",
                "name": "allocPoint",
                "type": "uint64"}],
            "internalType": "struct MasterChefV2.PoolInfo",
            "name": "", "type": "tuple"}, {
            "internalType": "uint256", "name": "",
            "type": "uint256"}, {
            "internalType": "contract IRewarder",
            "name": "", "type": "address"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "harvestAll", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [], "name": "harvestFromMasterChef", "outputs": [],
        "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "uint256[]", "name": "pids", "type": "uint256[]"}],
        "name": "harvestMultiple", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [
            {"internalType": "contract IERC20", "name": "dummyToken", "type": "address"}],
        "name": "init", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "isAuth", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "name": "isLpToken",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "lastV1HarvestTimestamp",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "lpSupplies",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "lpToken",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "massUpdateAllPools", "outputs": [],
        "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "uint256[]", "name": "pids", "type": "uint256[]"}],
        "name": "massUpdatePools", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "bytes[]", "name": "data", "type": "bytes[]"}],
        "name": "multicall",
        "outputs": [{"internalType": "bytes[]", "name": "results", "type": "bytes[]"}],
        "stateMutability": "payable", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "_pid", "type": "uint256"},
                   {"internalType": "address", "name": "_user", "type": "address"}],
        "name": "pendingBOO",
        "outputs": [{"internalType": "uint256", "name": "pending", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "poolInfo", "outputs": [
            {"internalType": "uint128", "name": "accBooPerShare", "type": "uint128"},
            {"internalType": "uint64", "name": "lastRewardTime", "type": "uint64"},
            {"internalType": "uint64", "name": "allocPoint", "type": "uint64"}], "stateMutability": "view",
        "type": "function"}, {
        "inputs": [], "name": "poolInfoAmount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "poolLength",
        "outputs": [{"internalType": "uint256", "name": "pools", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [], "name": "queryHarvestFromMasterChef", "outputs": [],
        "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "address", "name": "_auth", "type": "address"}],
        "name": "revokeAuth", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "rewarder",
        "outputs": [{"internalType": "contract IRewarder", "name": "", "type": "address"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"},
                   {"internalType": "uint256", "name": "value", "type": "uint256"},
                   {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                   {"internalType": "uint8", "name": "v", "type": "uint8"},
                   {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                   {"internalType": "bytes32", "name": "s", "type": "bytes32"}],
        "name": "selfPermit", "outputs": [], "stateMutability": "payable",
        "type": "function"}, {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"},
                   {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                   {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                   {"internalType": "uint8", "name": "v", "type": "uint8"},
                   {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                   {"internalType": "bytes32", "name": "s", "type": "bytes32"}],
        "name": "selfPermitAllowed", "outputs": [], "stateMutability": "payable",
        "type": "function"}, {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"},
                   {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                   {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                   {"internalType": "uint8", "name": "v", "type": "uint8"},
                   {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                   {"internalType": "bytes32", "name": "s", "type": "bytes32"}],
        "name": "selfPermitAllowedIfNecessary", "outputs": [], "stateMutability": "payable",
        "type": "function"}, {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"},
                   {"internalType": "uint256", "name": "value", "type": "uint256"},
                   {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                   {"internalType": "uint8", "name": "v", "type": "uint8"},
                   {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                   {"internalType": "bytes32", "name": "s", "type": "bytes32"}],
        "name": "selfPermitIfNecessary", "outputs": [], "stateMutability": "payable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "_pid", "type": "uint256"},
                   {"internalType": "uint64", "name": "_allocPoint", "type": "uint64"}, {
                       "internalType": "contract IRewarder", "name": "_rewarder",
                       "type": "address"},
                   {"internalType": "bool", "name": "overwrite", "type": "bool"},
                   {"internalType": "bool", "name": "update", "type": "bool"}],
        "name": "set", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {
        "inputs": [{"internalType": "address", "name": "newAdmin", "type": "address"}],
        "name": "setAdmin", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256[]", "name": "_pid", "type": "uint256[]"},
                   {"internalType": "uint64[]", "name": "_allocPoint", "type": "uint64[]"},
                   {
                       "internalType": "contract IRewarder[]", "name": "_rewarders",
                       "type": "address[]"},
                   {"internalType": "bool[]", "name": "overwrite", "type": "bool[]"},
                   {"internalType": "bool", "name": "update", "type": "bool"}],
        "name": "setBatch", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256[]", "name": "_pid", "type": "uint256[]"},
                   {"internalType": "uint64[]", "name": "_allocPoint", "type": "uint64[]"},
                   {"internalType": "bool", "name": "update", "type": "bool"}],
        "name": "setBatchSlim", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "newTime", "type": "uint256"},
                   {"internalType": "bool", "name": "inDays", "type": "bool"}],
        "name": "setV1HarvestQueryTime", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"}],
        "name": "supportsPermits", "outputs": [
            {"internalType": "bytes32", "name": "domainSeparator", "type": "bytes32"}], "stateMutability": "view",
        "type": "function"}, {
        "inputs": [], "name": "totalAllocPoint",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"}],
        "name": "updatePool", "outputs": [{
            "components": [{
                "internalType": "uint128",
                "name": "accBooPerShare",
                "type": "uint128"}, {
                "internalType": "uint64",
                "name": "lastRewardTime",
                "type": "uint64"}, {
                "internalType": "uint64",
                "name": "allocPoint",
                "type": "uint64"}],
            "internalType": "struct MasterChefV2.PoolInfo",
            "name": "pool", "type": "tuple"}],
        "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"},
                   {"internalType": "address", "name": "", "type": "address"}],
        "name": "userInfo",
        "outputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "uint256", "name": "rewardDebt", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"},
                   {"internalType": "uint256", "name": "amount", "type": "uint256"},
                   {"internalType": "address", "name": "to", "type": "address"}],
        "name": "withdraw", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}, {
        "inputs": [{"internalType": "uint256", "name": "pid", "type": "uint256"},
                   {"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "withdraw", "outputs": [], "stateMutability": "nonpayable",
        "type": "function"}]