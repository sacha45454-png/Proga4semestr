"""
Модуль для получения курсов валют с сайта Центрального Банка России.
"""

import xml.etree.ElementTree as ET
from typing import Dict, Union
from datetime import datetime
import requests


class BaseCurrencyProvider:
    """Базовый класс для получения курсов валют."""

    def get_rates(self) -> Dict[str, Union[str, float]]:
        """
        Получает курсы валют с сайта ЦБ РФ и возвращает их в виде словаря.

        Returns:
            Словарь с курсами валют, где ключ — код валюты (USD, EUR),
            значение — курс.

        Raises:
            Exception: Если не удалось получить данные от API ЦБ РФ.
        """
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        try:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            rates = {}
            for valute in root.findall("Valute"):
                char_code = valute.find("CharCode").text
                value = float(valute.find("Value").text.replace(",", "."))
                rates[char_code] = value

            return {"date": datetime.now().strftime("%Y-%m-%d"), "rates": rates}
        except Exception as e:
            raise Exception(f"Не удалось получить курсы валют: {e}")

    def save_to_file(self, filename: str, data: Union[str, Dict]) -> None:
        """
        Сохраняет полученные данные в текстовый файл.

        Args:
            filename: Имя файла для сохранения.
            data: Данные для сохранения (строка или словарь).
        """
        with open(filename, "w", encoding="utf-8") as f:
            if isinstance(data, dict):
                import json
                json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                f.write(data)