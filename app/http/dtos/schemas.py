from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config('CSRF_KEY')

class BaseTodo(BaseModel):
    id: str
    title: str
    description: str

class Todo(BaseTodo):
    id: str

class TodoBody(BaseTodo):
    pass


class SuccessMsg(BaseModel):
    message: str


class UserBody(BaseModel):
    email: str
    password: str


class UserInfo(BaseModel):
    id: Optional[str] = None
    email: str


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY

class Csrf(BaseModel):
    csrf_token: str