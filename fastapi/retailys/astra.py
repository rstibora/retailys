import aiohttp
import io
import os
import redis
import zipfile

import xml.etree.ElementTree as ET

from pydantic import BaseModel


class Item(BaseModel):
    code: str
    name: str
    spare_part_codes: list[str] = list()


def _save_to_cache(items: list[Item]) -> None:
    """Stores Pydantic models to Redis."""
    connection = redis.Redis(host="redis", decode_responses=True)
    code_mapping = dict()
    items_mapping = dict()

    for idx, item in enumerate(sorted(items, key=lambda item: item.name)):
        code_mapping[item.code] = idx
        items_mapping[item.code] = item.json()

    connection.zadd("codes", code_mapping)
    connection.hset("items", mapping=items_mapping)


def _parse_xml(root_node: ET.Element) -> list[Item]:
    """Parses Pydantic models from the xml tree."""
    items = list()
    items_node = root_node.find("items")
    if items_node is None:
        return items

    for item_node in items_node:
        spare_part_codes = list()
        if (parts := item_node.find("parts")) is not None:
            if (spare_parts := parts.find(("part"))) is not None and spare_parts.attrib["categoryId"] == "1":
                for spare_part in spare_parts:
                    spare_part_codes.append(spare_part.attrib["code"])
        items.append(Item(
            code=item_node.attrib["code"],
            name=item_node.attrib["name"],
            spare_part_codes=spare_part_codes))
    return items


async def _extract_xml(zipped: io.BytesIO) -> ET.Element:
    """Extracts data from the zip file."""
    with zipfile.ZipFile(zipped) as extracted_file:
        export_full_xml = io.BytesIO(extracted_file.read("export_full.xml"))
        tree = ET.parse(export_full_xml)
        return tree.getroot()


async def _fetch_zip() -> io.BytesIO:
    """Fetches the zip file."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip") as response:
            return io.BytesIO(await response.read())


def _cache_empty() -> bool:
    """Check whether the cache is empty."""
    return not redis.Redis(host="redis", decode_responses=True).keys("items")


async def fetch_and_store() -> None:
    """Checks if the Redis cache is empty and if so, fills it with data."""
    if _cache_empty():
        in_memory = await _fetch_zip()
        xml = await _extract_xml(in_memory)
        items = _parse_xml(xml)
        _save_to_cache(items)
