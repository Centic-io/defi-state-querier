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
    HOST = "mongodb://klgReaderAnalysis:klgReaderAnalysis_4Lc4kjBs5yykHHbZ@35.198.222.97:27017,34.124.133.164:27017,34.124.205.24:27017/"
    USERNAME = "root"
    PASSWORD = "dev123"
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