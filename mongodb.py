# mongodb.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client.quickbooks
tokens_collection = db.tokens

def save_tokens(tokens):
    try:
        result = tokens_collection.replace_one({}, tokens, upsert=True)
        print(f"💾 Token save result: matched={result.matched_count}, modified={result.modified_count}")
    except Exception as e:
        print(f"❌ Failed to save tokens to MongoDB: {e}")

def load_tokens():
    try:
        return tokens_collection.find_one()
    except Exception as e:
        print(f"❌ Failed to load tokens from MongoDB: {e}")
        return None
