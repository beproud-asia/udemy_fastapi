from decouple import config
from typing import Union
import motor.motor_asyncio #mongoDBとの連携
from bson import ObjectId 

MONGO_API_KEY = config('MONGO_API_KEY')

def db_connect():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
    database = client.API_DB
    try:
        return database
    except Exception:
        print("⭐Unable to connect to the server.")
        return "Unable to connect to the server."
