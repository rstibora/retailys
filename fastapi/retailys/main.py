import io
import json
import os
import redis

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from retailys.astra import fetch_and_store, Item

app = FastAPI()


class ListResponse(BaseModel):
    items: list[Item]
    items_count: int


@app.get("/items/")
async def root(items_from: int, items_to: int) -> ListResponse:
    await fetch_and_store()
    connection = redis.Redis(host="redis", decode_responses=True)
    connection.zrange("items", items_from, items_to)
    count = connection.zcard("items")
    items = [Item.parse_obj(json.loads(serialized_item)) for serialized_item in connection.zrange("items", items_from, items_to)]
    return ListResponse(items=items, items_count=count)


@app.get("/items/{code}")
async def item(code: str) -> Item:
    await fetch_and_store()
    connection = redis.Redis(host="redis", decode_responses=True)
    serialized_item = connection.get(f"item:{code}")
    if not serialized_item:
        raise HTTPException(404)
    return Item.parse_obj(json.loads(serialized_item))
