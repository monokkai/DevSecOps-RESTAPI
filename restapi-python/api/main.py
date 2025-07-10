from typing import Union
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

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