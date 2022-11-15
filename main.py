from fastapi import FastAPI
#from routers import route_todo
from schemas import SuccessMsg
from routers import router

app = FastAPI()
# app.include_router(route_todo.router)
app = router.get_app(app)

@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welcom to Fast API"}
