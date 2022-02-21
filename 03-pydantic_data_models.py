from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str
    email: str | None = None
    age: int | None = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users/")
async def create_user(user: User):
    print(f"User name: {user.name}")
    if user.age:
        print(f"User age: {user.age}")

    return user

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
