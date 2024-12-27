from pymongo import MongoClient
import os

# Database URL from environment or config file
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.todo_db

# Collections
users_collection = db["users"]
todos_collection = db["todos"]
