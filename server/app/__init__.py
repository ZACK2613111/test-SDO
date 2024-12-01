from fastapi import FastAPI
from .Routes import user_routes

app = FastAPI()

# You can also include any initialization logic here
# app.include_router(user_routes.router)
