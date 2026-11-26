from decorators import BaseCurrencyComponent, YamlDecorator, CsvDecorator

# Базовый компонент
base = BaseCurrencyComponent()
print("=== JSON (по умолчанию) ===")
print(base.get_rates())

# YAML-декоратор
yaml_decorator = YamlDecorator(base)
print("\n=== YAML ===")
print(yaml_decorator.get_rates())

# CSV-декоратор
csv_decorator = CsvDecorator(base)
print("\n=== CSV ===")
print(csv_decorator.get_rates())

# Сохраняем в файлы
yaml_decorator.save_to_file("kurs.yaml")
csv_decorator.save_to_file("kurs.csv")
print("\nФайлы kurs.yaml и kurs.csv созданы.")