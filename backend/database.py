from pymongo import MongoClient
import os

def get_client():
    return MongoClient(os.getenv("MONGODB_HOST", "mongodb://localhost"))
