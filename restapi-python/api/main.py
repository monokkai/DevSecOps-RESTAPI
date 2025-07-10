from typing import Union
from fastapi import FastAPI, Request, Depends, HTTPException, security, Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import time

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
    token = credentials.credentials
    if token != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "You have an access"}


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

    return {"message": "User verified"}
