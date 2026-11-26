import httpx
import xml.etree.ElementTree as ET
from typing import List, Tuple

async def fetch_currencies_from_cbr() -> List[Tuple[str, str, float]]:
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        currencies = []
        for valute in root.findall("Valute"):
            code = valute.find("CharCode").text
            name = valute.find("Name").text
            value = float(valute.find("Value").text.replace(",", "."))
            currencies.append((code, name, value))
        return currencies