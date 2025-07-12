from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from typing import Union
import time
import jwt

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

    return {"message": f"Hello, {username}! You have an access!"}


@app.post("/register")
def register(
        username: str = Form(..., description="User login"),
        password: str = Form(..., description="User password")
):
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "username": username,
        "access_token": token,
        "message": "User verified"
    }
