import hashlib
import json
from datetime import datetime
from pymongo import MongoClient
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['voting_system']
blocks_collection = db['blocks']


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': str(self.timestamp),
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        print(f"⛏️ Mining block #{self.index}...", end='')
        start_time = time.time()

        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        mining_time = time.time() - start_time
        print(f" Done in {mining_time:.2f}s (Nonce: {self.nonce})")
        return self

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce
        }


class Blockchain:
    def __init__(self, difficulty=3):
        self.difficulty = difficulty
        self.chain = []
        self.initialize_chain()

    def initialize_chain(self):
        """Initialize or load the chain from DB"""
        if blocks_collection.count_documents({}) == 0:
            self.create_genesis_block()
        else:
            self.load_chain_from_db()

    def load_chain_from_db(self):
        """Load existing chain from MongoDB"""
        for block_data in blocks_collection.find().sort('index'):
            self.chain.append(Block(
                block_data['index'],
                block_data['timestamp'],
                block_data['data'],
                block_data['previous_hash'],
                block_data.get('nonce', 0)
            ))
        print(f"📦 Loaded {len(self.chain)} blocks from database")

    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, datetime.utcnow(), {"message": "Genesis Block"}, "0")
        genesis_block.mine_block(self.difficulty)
        blocks_collection.insert_one(genesis_block.to_dict())
        self.chain.append(genesis_block)
        print("🔗 Genesis block created")

    def get_latest_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1] if self.chain else None

    def add_block(self, new_data):
        """Add a new block to the chain"""
        latest_block = self.get_latest_block()
        if not latest_block:
            raise Exception("No blocks in chain")

        new_block = Block(
            index=latest_block.index + 1,
            timestamp=datetime.utcnow(),
            data=new_data,
            previous_hash=latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        blocks_collection.insert_one(new_block.to_dict())
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def get_all_blocks(self):
        """Return all blocks as dictionaries"""
        return [block.to_dict() for block in self.chain]


# Initialize blockchain
try:
    blockchain = Blockchain(difficulty=3)
    print(f"✅ Blockchain ready (Difficulty: {blockchain.difficulty})")
except Exception as e:
    print(f"❌ Blockchain initialization failed: {str(e)}")
    raise