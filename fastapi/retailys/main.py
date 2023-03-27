import io
import json
import os
import redis

from fastapi import FastAPI, HTTPException

from retailys.astra import fetch_and_store, Item

app = FastAPI()

@app.get("/items/")
async def root() -> list[Item]:
    await fetch_and_store()
    connection = redis.Redis(host="redis", decode_responses=True)
    items = list()
    for key in connection.keys("item:*"):
        serialized_item = connection.get(key)
        if serialized_item:
            items.append(Item.parse_obj(json.loads(serialized_item)))
    return items


@app.get("/items/{code}")
async def item(code: str) -> Item:
    await fetch_and_store()
    connection = redis.Redis(host="redis", decode_responses=True)
    serialized_item = connection.get(f"item:{code}")
    if not serialized_item:
        raise HTTPException(404)
    return Item.parse_obj(json.loads(serialized_item))
