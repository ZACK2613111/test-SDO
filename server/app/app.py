from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Routes import user_routes, task_routes, auth_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(user_routes.router)
app.include_router(task_routes.router)
app.include_router(auth_route.router)
