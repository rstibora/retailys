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


class Part(BaseModel):
    code: str
    name: str



def _save_to_cache(items: list[Item]) -> None:
    connection = redis.Redis(host="redis", decode_responses=True)
    mapping = {item.json(): idx for idx, item in enumerate(sorted(items, key=lambda item: item.name))}
    connection.zadd("items", mapping)


def _parse_xml(root_node: ET.Element) -> list[Item]:
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
    with zipfile.ZipFile(zipped) as extracted_file:
        export_full_xml = io.BytesIO(extracted_file.read("export_full.xml"))
        tree = ET.parse(export_full_xml)
        return tree.getroot()


async def _fetch_zip() -> io.BytesIO:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip") as response:
            return io.BytesIO(await response.read())


async def fetch_and_store() -> None:
    if not redis.Redis(host="redis", decode_responses=True).keys("items"):
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/tests/astra_export_xml.zip", "rb") as zipped:
            in_memory = io.BytesIO(zipped.read())
            xml = await _extract_xml(in_memory)
            items = _parse_xml(xml)
            _save_to_cache(items)
