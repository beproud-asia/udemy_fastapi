# end point 定義
from fastapi import APIRouter, Depends
from fastapi import Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from app.http.dtos.schemas import Todo, TodoBody, SuccessMsg
from app.services.database import db_create_todo, db_get_single_todo, db_get_todos, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED
from typing import List
from fastapi_csrf_protect import CsrfProtect
from app.http.authorizations.auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

###


@router.post("/api/v1/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers)

    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Create task failed"
    )

###


@router.get("/api/v1/todo", response_model=List[Todo])
async def get_todos(request: Request):
    # auth.verify_jwt(request)
    res = await db_get_todos()
    return res

###


@router.get("/api/v1/{id}/todo", response_model=Todo)
async def get_single_todo(request: Request, response: Response, id: str):
    new_token, _ = auth.verify_csrf_update_jwt(request)
    res = await db_get_single_todo(id)
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Task of ID:{id} doesn't exist"
    )

# 更新


@router.put("/api/v1/{id}/todo", response_model=Todo)
async def uodate_todo(request: Request, response: Response, id: str, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers)

    todo = jsonable_encoder(data)
    res = await db_update_todo(id, todo)
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)

    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Upate task failed"
    )

# 削除


@router.delete("/api/v1/{id}/todo", response_model=SuccessMsg)
async def delete_todo(request: Request, response: Response, id: str, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers)

    res = await db_delete_todo(id)
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True)

    if res:
        return {"message": "削除成功"}
    raise HTTPException(
        status_code=404, detail="Delete task failed"
    )
