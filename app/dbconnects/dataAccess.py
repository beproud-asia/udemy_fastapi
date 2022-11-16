from decouple import config
from typing import Union
import motor.motor_asyncio #mongoDBとの連携
import asyncio

MONGO_API_KEY = config('MONGO_API_KEY')

def db_connect():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
    client.get_io_loop = asyncio.get_event_loop
    
    database = client.API_DB
    try:
        return database
    except Exception:
        print("⭐Unable to connect to the server.")
        return "Unable to connect to the server."
