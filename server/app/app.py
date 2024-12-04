from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Routes import user_routes, task_routes, auth_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  # Allow all headers in requests
)

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint to test if the API is running.

    Returns:
        dict: A simple message indicating the API is working.
    """
    return {"message": "Hello, FastAPI!"}

# app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth_route.router, prefix="/auth", tags=["Authentication"])
