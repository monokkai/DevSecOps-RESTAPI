import time
from typing import Union
from fastapi import FastAPI, Request, Depends, HTTPException, security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
security = HTTPBearer()

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


@app.get("/items/{item_id}")
def read_item(item_id: int, quantity: Union[str, None] = None):
    return {"item_id": item_id, "quantity": quantity}


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
    if token != "token11122334455":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "You have an access"}
