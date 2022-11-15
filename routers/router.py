from fastapi import FastAPI
from routers import route_todo
#from fastapi import APIRouter

def get_app(app):
    app.include_router(route_todo.router)
    return app