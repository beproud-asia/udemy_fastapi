from fastapi import FastAPI
from app.http.routers import route_todo, route_auth
#from fastapi import APIRouter

def get_app(app):
    app.include_router(route_todo.router)
    app.include_router(route_auth.router)
    return app