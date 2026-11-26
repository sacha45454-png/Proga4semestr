"""
Модуль с юнит-тестами для проверки работы декораторов.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import json
import yaml
from currency_service import BaseCurrencyProvider
from decorators import BaseCurrencyComponent, YamlDecorator, CsvDecorator


class TestBaseCurrencyComponent(unittest.TestCase):
    """Тесты для базового компонента."""

    @patch('currency_service.requests.get')
    def test_get_rates_success(self, mock_get):
        """Тест успешного получения курсов валют."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '''<?xml version="1.0" encoding="windows-1251"?>
        <ValCurs Date="01.01.2023">
            <Valute ID="R01235">
                <CharCode>USD</CharCode>
                <Value>70,0000</Value>
            </Valute>
        </ValCurs>'''
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        component = BaseCurrencyComponent()
        rates = component.get_rates()
        self.assertIn('USD', rates['rates'])
        self.assertEqual(rates['rates']['USD'], 70.0)

    @patch('currency_service.requests.get')
    def test_get_rates_failure(self, mock_get):
        """Тест ошибки при получении курсов."""
        mock_get.side_effect = Exception("Network error")
        component = BaseCurrencyComponent()
        with self.assertRaises(Exception):
            component.get_rates()


class TestYamlDecorator(unittest.TestCase):
    """Тесты для YAML-декоратора."""

    @patch('decorators.BaseCurrencyComponent.get_rates')
    def test_yaml_format(self, mock_get_rates):
        """Тест форматирования в YAML."""
        mock_get_rates.return_value = {
            "date": "2023-01-01",
            "rates": {"USD": 70.0, "EUR": 80.0}
        }
        component = BaseCurrencyComponent()
        yaml_decorator = YamlDecorator(component)
        result = yaml_decorator.get_rates()
        expected = "date: '2023-01-01'\nrates:\n  EUR: 80.0\n  USD: 70.0\n"
        self.assertEqual(result, expected)

    def test_yaml_save_to_file(self):
        """Тест сохранения в YAML-файл."""
        with patch('decorators.BaseCurrencyComponent.get_rates') as mock_get_rates:
            mock_get_rates.return_value = {"date": "2023-01-01", "rates": {"USD": 70.0}}
            component = BaseCurrencyComponent()
            yaml_decorator = YamlDecorator(component)
            filename = "test_rates.yaml"
            yaml_decorator.save_to_file(filename)
            self.assertTrue(os.path.exists(filename))
            with open(filename, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.assertEqual(data['rates']['USD'], 70.0)
            os.remove(filename)


class TestCsvDecorator(unittest.TestCase):
    """Тесты для CSV-декоратора."""

    @patch('decorators.BaseCurrencyComponent.get_rates')
    def test_csv_format(self, mock_get_rates):
        """Тест форматирования в CSV."""
        mock_get_rates.return_value = {
            "date": "2023-01-01",
            "rates": {"USD": 70.0, "EUR": 80.0}
        }
        component = BaseCurrencyComponent()
        csv_decorator = CsvDecorator(component)
        result = csv_decorator.get_rates()
        self.assertIn("date: 2023-01-01", result)
        self.assertIn("USD,70.0", result)
        self.assertIn("EUR,80.0", result)

    def test_csv_save_to_file(self):
        """Тест сохранения в CSV-файл."""
        with patch('decorators.BaseCurrencyComponent.get_rates') as mock_get_rates:
            mock_get_rates.return_value = {"date": "2023-01-01", "rates": {"USD": 70.0}}
            component = BaseCurrencyComponent()
            csv_decorator = CsvDecorator(component)
            filename = "test_rates.csv"
            csv_decorator.save_to_file(filename)
            self.assertTrue(os.path.exists(filename))
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("USD,70.0", content)
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()