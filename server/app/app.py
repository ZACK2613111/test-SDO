from fastapi import FastAPI
from app.Routes import user_routes, task_routes

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(user_routes.router)
app.include_router(task_routes.router)

