from decouple import config
from typing import Union
from fastapi import HTTPException
from bson import ObjectId 
from database.dataAccess import db_connect
from auth_utils import AuthJwtCsrf
from bson import ObjectId


MONGO_API_KEY = config('MONGO_API_KEY')

# DBアクセス
database = db_connect()
collection_todo = database.todo
collection_user = database.user
auth = AuthJwtCsrf()

### user_serializer
def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user['email'],
    }

### todo_serializer
def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": str(todo["title"]),
        "description": str(todo["description"]),
    }

####
async def db_create_todo(data: dict) -> Union[dict, bool]:
    todo = await collection_todo.insert_one(data)
    new_todo = await collection_todo.find_one({"_id": todo.inserted_id})
    if new_todo:
        return todo_serializer(new_todo)
    return False

### 
async def db_get_todos() -> list:
    todos = []
    for todo in await collection_todo.find().to_list(length=100):
        todos.append(todo_serializer(todo))
    return todos

###
async def db_get_single_todo(id: str) ->  Union[dict, bool]:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_serializer(todo)
    return False

###
async def db_update_todo(id: str, data: dict) -> Union[dict, bool]:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        update_todo = await collection_todo.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if (update_todo.modified_count > 0):
            new_todo = await collection_todo.find_one({"_id": ObjectId(id)})
            return todo_serializer(new_todo);
    return False

###
async def db_delete_todo(id: str) -> bool:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        delete_todo = await collection_todo.delete_one(
            {"_id": ObjectId(id)}
        )
        if (delete_todo.deleted_count > 0):
            return True
    return False

###
async def db_signup(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    overlap_user = await collection_user.find_one({"email": email})
    if overlap_user:
        raise HTTPException(status_code=400, detail='Email is already taken.')  
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail='Password too Short!')

    user = await collection_user.insert_one({"email": email, "password": auth.generate_hashed_pw(password)})
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    if new_user:
        return user_serializer(new_user)
    return False

###
async def db_login(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    user = await collection_user.find_one({"email": email})
    if not user or not auth.verify_pw(password, user['password']):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    token = auth.encode_jwt(user['email'])
    return token
