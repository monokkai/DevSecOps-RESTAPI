from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Union
import time
from sqlalchemy.orm import Session
import database, db_requests, auth

app = FastAPI()
security = HTTPBearer()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print("------------------------------------")
    print(f"{request.method}: {request.url}\n completed in: {duration:.2f}\n status: {response.status_code}")
    print("------------------------------------")
    return response


# TODO: make full access for admin to see all users
@app.get("/users/{user_id}")
def read_item(user_id: int, quantity: Union[str, None] = None):
    return {"user_id": user_id, "quantity": quantity}


# TODO: make access ONLY for admin
@app.get("/health")
async def read_health():
    return {"healthy": True}


# TODO: make access ONLY for admin
@app.post("/echo")
async def echo(request: Request):
    data = await request.json()
    return {"You sent": data}


@app.get("/secure")
def read_secure(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # giving token from Authorization: Bearer<token>
    username = auth.decode_bearer_token(token)

    return {"message": f"Hello, {username}! You have an access!"}


@app.post("/register")
def register(
        username: str = Form(..., description="User login"),
        password: str = Form(..., description="User password"),
        db: Session = Depends(database.get_db)
):
    user = db_requests.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = auth.create_bearer_token({"sub": username})
    return {"username": username, "token": token, "message": "User verified!"}
