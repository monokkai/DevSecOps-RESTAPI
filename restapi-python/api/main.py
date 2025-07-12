from fastapi import FastAPI, Request, Depends, HTTPException, security, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
import time
import jwt

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "secret_for_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "egor": {
        "username": "egor",
        "full_name": "Egor Mayer",
        "hashed_password": pwd_context.hash("password123"),
        "disabled": False,
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_bearer_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print("------------------------------------")
    print(f"{request.method}: {request.url}\n completed in: {duration:.2f}\n status: {response.status_code}")
    print("------------------------------------")
    return response


@app.get("/users/{user_id}")
def read_item(user_id: int, quantity: Union[str, None] = None):
    return {"user_id": user_id, "quantity": quantity}


@app.get("/health")
async def read_health():
    return {"healthy": True}


@app.post("/echo")
async def echo(request: Request):
    data = await request.json()
    return {"You sent": data}


@app.get("/secure")
def read_secure(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # giving token from Authorization: Bearer<token>
    try:
        # Decoding token with HS256
        payload = jwt.encode(token, SECRET_KEY, algorithm=[ALGORITHM])
        # Getting user from "sub" field of token
        username = payload.get("sub")
        # Not user? Go away
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid token payload!")
    # Now don't know what's the error with jwt.exceptions... due to that problem made static error text for error filters!
    except Exception as e:
        if "Signature has expired" in str(e):
            raise HTTPException(status_code=401, detail="Token expired")
        else:
            raise HTTPException(status_code=403, detail="Invalid token")
    return {"message:" f"Hello, {username}! You have an access!"}


@app.post("/token")
def get_token(
        username: str = Form(..., description="User login"),
        password: str = Form(..., description="User password")
):
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_bearer_token(data={"data": username}, expires_delta=access_token_expires)

    return {
        "username": username,
        "access_token": access_token,
        "message": "User verified"
    }