from fastapi import FastAPI
from app.Routes import user_routes

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Include routes
app.include_router(user_routes.router)
