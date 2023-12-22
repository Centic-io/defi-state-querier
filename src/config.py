import os
from dotenv import load_dotenv

load_dotenv()


class MongoDBConfig:
    HOST = os.environ.get("MONGODB_HOST", '0.0.0.0')
    PORT = os.environ.get("MONGODB_PORT", '8529')
    USERNAME = os.environ.get("MONGODB_USERNAME", "root")
    PASSWORD = os.environ.get("MONGODB_PASSWORD", "dev123")
    CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL") or f"mongodb@{USERNAME}:{PASSWORD}@http://{HOST}:{PORT}"
    DATABASE = os.getenv('MONGODB_DATABASE', 'knowledge_graph')

class MongoDbKLGConfig:
    HOST =os.environ.get("MONGODB_KLG_HOST", '0.0.0.0')
    USERNAME = os.environ.get("MONGODB_USERNAME", "root")
    PASSWORD = os.environ.get("MONGODB_PASSWORD", "dev123")
    # KLG_DATABASE = "klg_database"
    KLG_DATABASE = "knowledge_graph"
    KLG = "knowledge_graph"
    WALLETS = "wallets"
    MULTICHAIN_WALLETS = "multichain_wallets"
    DEPOSITS = "deposits"
    BORROWS = "borrows"
    REPAYS = "repays"
    WITHDRAWS = "withdraws"
    LIQUIDATES = "liquidates"
    SMART_CONTRACTS = "smart_contracts"