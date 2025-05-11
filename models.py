from pymongo import MongoClient
from datetime import datetime
import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['voting_system']


class User:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_voter(username, password):
        voter = db.voters.find_one({'username': username})
        if voter and voter['password'] == User.hash_password(password):
            return voter
        return None

    @staticmethod
    def verify_candidate(username, password):
        candidate = db.candidates.find_one({'username': username})
        if candidate and candidate['password'] == User.hash_password(password):
            return candidate
        return None


class Voter:
    collection = db['voters']

    @staticmethod
    def register(username, password, full_name):
        if Voter.collection.find_one({'username': username}):
            return False, "Username already exists"

        Voter.collection.insert_one({
            'username': username,
            'password': User.hash_password(password),
            'full_name': full_name,
            'has_voted': False,
            'registered_at': datetime.utcnow()
        })
        return True, "Voter registered successfully"

    @staticmethod
    def has_voted(username):
        voter = Voter.collection.find_one({'username': username})
        return voter and voter['has_voted']

    @staticmethod
    def get_voter_details(username):
        """NEW METHOD: Get voter details without password"""
        return Voter.collection.find_one(
            {'username': username},
            {'password': 0}  # Exclude password field
        )


class Candidate:
    collection = db['candidates']

    @staticmethod
    def register(username, password, full_name, party):
        if Candidate.collection.find_one({'username': username}):
            return False, "Username already exists"

        Candidate.collection.insert_one({
            'username': username,
            'password': User.hash_password(password),
            'full_name': full_name,
            'party': party,
            'votes_received': 0,
            'registered_at': datetime.utcnow()
        })
        return True, "Candidate registered successfully"

    @staticmethod
    def get_vote_count(username):
        candidate = Candidate.collection.find_one({'username': username})
        return candidate['votes_received'] if candidate else 0

    @staticmethod
    def get_candidate_details(username):
        return Candidate.collection.find_one(
            {'username': username},
            {'password': 0}
        )

    @staticmethod
    def increment_vote_count(username):
        Candidate.collection.update_one(
            {'username': username},
            {'$inc': {'votes_received': 1}}
        )