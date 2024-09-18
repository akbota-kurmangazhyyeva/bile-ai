from pymongo import MongoClient
from datetime import datetime, timezone
from app.core.config import settings

client = MongoClient(settings.MONGODB_URI)
db = client.dancegen

def save_dance_data(song_name, s3_url):
    dance_collection = db.dances
    dance_collection.insert_one({
        "song_name": song_name,
        "s3_url": s3_url,
        "created_at": datetime.now(timezone.utc) 
    })
