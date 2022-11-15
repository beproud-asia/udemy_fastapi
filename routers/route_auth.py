# end point 定義
from fastapi import APIRouter
from fastapi import Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo
from database.database import db_signup, db_login
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

### 
@router.post("/api/v1/register", response_model=UserInfo)
async def signup(user: UserBody):
    # ディクショナリ型に変換する
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    return new_user

### 
@router.post("/api/v1/login", response_model=SuccessMsg)
async def login(response:Response, user: UserBody):
    user = jsonable_encoder(user)
    token = await db_login(user)
    response.set_cookie(
        key="access_token", value=f"Bearer {token}", httponly=True, samesite="none", secure=True)
    return {"message": "Successfully logged-in"}
