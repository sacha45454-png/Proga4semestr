"""
Модуль, реализующий паттерн «Декоратор» для форматирования данных о курсах валют.
"""

from abc import ABC, abstractmethod
import json
import csv
from typing import Dict, Union, Any
import yaml
from currency_service import BaseCurrencyProvider


class CurrencyProvider(ABC):
    """Абстрактный интерфейс для компонента и декораторов."""

    @abstractmethod
    def get_rates(self) -> Union[Dict, str]:
        """
        Абстрактный метод для получения курсов валют.
        """
        pass

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """
        Абстрактный метод для сохранения данных в файл.
        """
        pass


class BaseCurrencyComponent(CurrencyProvider):
    """Конкретный компонент, реализующий базовое получение курсов валют."""

    def __init__(self) -> None:
        self._provider = BaseCurrencyProvider()

    def get_rates(self) -> Dict:
        """
        Возвращает курсы валют в виде словаря.
        """
        return self._provider.get_rates()

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные в файл в формате JSON.
        """
        data = self.get_rates()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class CurrencyDecorator(CurrencyProvider):
    """Базовый класс декоратора, оборачивающий объект CurrencyProvider."""

    def __init__(self, wrapped: CurrencyProvider) -> None:
        """
        Инициализирует декоратор.

        Args:
            wrapped: Оборачиваемый объект (компонент или другой декоратор).
        """
        self._wrapped = wrapped

    @abstractmethod
    def get_rates(self) -> Union[Dict, str]:
        """
        Абстрактный метод получения курсов.
        """
        pass

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """
        Абстрактный метод для сохранения данных в файл.
        """
        pass


class YamlDecorator(CurrencyDecorator):
    """Декоратор для преобразования данных в формат YAML."""

    def get_rates(self) -> str:
        """
        Получает данные от обёрнутого объекта и возвращает их в формате YAML.

        Returns:
            Строка в формате YAML.
        """
        data = self._wrapped.get_rates()
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные в YAML-файл.

        Args:
            filename: Имя файла для сохранения.
        """
        data = self.get_rates()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)


class CsvDecorator(CurrencyDecorator):
    """Декоратор для преобразования данных в формат CSV."""

    def get_rates(self) -> str:
        """
        Получает данные от обёрнутого объекта и возвращает их в формате CSV.

        Returns:
            Строка в формате CSV.
        """
        data = self._wrapped.get_rates()
        rates = data.get("rates", {})
        date = data.get("date", "")

        output = []
        output.append(f"date: {date}")

        for code, rate in rates.items():
            output.append(f"{code},{rate}")

        return "\n".join(output)

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет данные в CSV-файл.

        Args:
            filename: Имя файла для сохранения.
        """
        data = self.get_rates()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)