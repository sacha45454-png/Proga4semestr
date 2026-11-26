# Паттерн «Наблюдатель» (Observer)

## 1. Категория принципов

Паттерн «Наблюдатель» относится к **поведенческим** паттернам проектирования. Он определяет механизм отношений типа «один ко многим» между объектами, при котором изменение состояния одного объекта (издателя) автоматически уведомляет и обновляет все зависимые от него объекты (наблюдателей). Этот механизм лежит в основе событийно-ориентированных архитектур и является ключевым для реализации принципа **Low Coupling** (слабой связанности).

## 2. Использование

Применение паттерна «Наблюдатель» обеспечивает:

- **Гибкость** — систему уведомлений можно легко расширять, добавляя новых наблюдателей (SMS, Telegram, push), не меняя код источника событий.
- **Слабая связанность** — издатель ничего не знает о конкретных классах наблюдателей, он взаимодействует с ними через общий интерфейс.
- **Динамическое поведение** — наблюдателей можно подписывать и отписывать во время выполнения программы.
- **Соответствие Open/Closed Principle (OCP)** — класс издателя открыт для расширения (новыми типами наблюдателей), но закрыт для изменений.

## 3. Ошибки при использовании (Антипаттерны)

- **God Object (Божественный объект)** — класс, отвечающий за бизнес-логику, самолично отправляет все уведомления. Нарушает SRP и ведёт к жёсткой связанности.
- **Hardcoding зависимостей** — создание конкретных сервисов уведомлений (например, `EmailNotifier()`) напрямую внутри конструктора или метода издателя вместо внедрения абстракции.
- **Утечка памяти** — забывание отписывать наблюдателей, когда они больше не нужны.
- **Непредсказуемый порядок уведомлений** — код не должен полагаться на порядок вызова наблюдателей.

## 4. Графическое представление и участники

![UML диаграмма паттерна Наблюдатель](https://upload.wikimedia.org/wikipedia/commons/0/01/W3sDesign_Observer_Design_Pattern_UML.jpg)
```
**Список участников и их роли:**

| Элемент | Описание |
|---------|----------|
| **Subject** (интерфейс) | Определяет методы для регистрации (`attach`), удаления (`detach`) и оповещения (`notify`) наблюдателей. |
| **ConcreteSubject** (конкретный издатель) | Хранит своё внутреннее состояние и список подписанных наблюдателей. При изменении состояния вызывает `notify()`. |
| **Observer** (интерфейс) | Определяет метод `update()`, который вызывается издателем при изменении состояния. |
| **ConcreteObserver** (конкретный наблюдатель) | Реализует `update()` и определяет реакцию на уведомление. Может хранить ссылку на издателя. |

## 5. Формулировка задачи

**Контекст:** на образовательной онлайн-платформе преподаватели публикуют новые материалы (видео, задания) или изменяют дедлайны. Необходимо уведомлять всех заинтересованных лиц: студентов курса, их родителей (для контроля успеваемости) и администраторов.

**Проблема:** в «плохой» реализации класс `Course` сам отвечает за отправку уведомлений. В его методе `publish_material()` напрямую вызываются методы для отправки email студентам и сообщений родителям. Это нарушает **SRP** (у класса появляется вторая причина для изменения) и создаёт **жёсткую связанность** (добавление нового типа уведомлений требует изменения кода курса).

**Задача:** реорганизовать систему уведомлений с помощью паттерна «Наблюдатель», чтобы отделить бизнес-логику курса от логики уведомлений и сделать систему гибкой для расширения.
## 6. Код решения

### Пример НАРУШЕНИЯ (высокая связанность)

```python
class Course:
    def __init__(self, name: str):
        self.name = name
        self.students = []
        self.parents = []

    def publish_material(self, title: str):
        print(f"\n--- Новый материал: {title} ---")
        # Нарушение SRP: курс сам отвечает за уведомления
        for student in self.students:
            print(f"[EMAIL] {student.email}: новый материал '{title}'")
        for parent in self.parents:
            print(f"[SMS] {parent.phone}: у вашего ребенка новый материал")
```
### ПРАВИЛЬНАЯ РЕАЛИЗАЦИЯ (паттерн «Наблюдатель»)

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# --- Абстракции ---
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        pass

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass
    @abstractmethod
    def notify(self, event_type: str, event_data: Dict[str, Any]) -> None:
        pass

# --- Конкретные наблюдатели ---
class StudentEmailNotifier(Observer):
    def __init__(self, student_name: str, email: str):
        self.student_name = student_name
        self.email = email
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        print(f"[EMAIL] {self.email}: {event_data.get('message', '')}")

class ParentSMSNotifier(Observer):
    def __init__(self, child_name: str, phone: str):
        self.child_name = child_name
        self.phone = phone
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        print(f"[SMS] {self.phone}: у вашего ребенка {self.child_name} {event_data.get('message', '')}")

class AdminLogger(Observer):
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        print(f"[LOG] Событие: {event_type} | {event_data}")

# --- Конкретный издатель ---
class Course(Subject):
    def __init__(self, name: str):
        self.name = name
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, event_type: str, event_data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.update(event_type, event_data)

    def publish_material(self, title: str):
        print(f"\n--- Новый материал в курсе '{self.name}': {title} ---")
        event_data = {"message": f"опубликован новый материал '{title}'"}
        self.notify("material_published", event_data)

# --- Клиентский код ---
if __name__ == "__main__":
    course = Course("Python для начинающих")
    alice = StudentEmailNotifier("Алиса", "alice@mail.com")
    bob = StudentEmailNotifier("Боб", "bob@mail.com")
    parent = ParentSMSNotifier("Боб", "+79998887766")
    logger = AdminLogger()

    course.attach(alice)
    course.attach(bob)
    course.attach(parent)
    course.attach(logger)

    course.publish_material("Урок 1: Переменные")
    course.detach(bob)   # отписка студента
    course.publish_material("Урок 2: Условные операторы")
```
## 7. Результат работы программы
--- Новый материал в курсе 'Python для начинающих': Урок 1: Переменные ---
[EMAIL] alice@mail.com: опубликован новый материал 'Урок 1: Переменные'
[EMAIL] bob@mail.com: опубликован новый материал 'Урок 1: Переменные'
[SMS] +79998887766: у вашего ребенка Боб опубликован новый материал 'Урок 1: Переменные'
[LOG] Событие: material_published | {'message': "опубликован новый материал 'Урок 1: Переменные'"}

--- Новый материал в курсе 'Python для начинающих': Урок 2: Условные операторы ---
[EMAIL] alice@mail.com: опубликован новый материал 'Урок 2: Условные операторы'
[SMS] +79998887766: у вашего ребенка Боб опубликован новый материал 'Урок 2: Условные операторы'
[LOG] Событие: material_published | {'message': "опубликован новый материал 'Урок 2: Условные операторы'"}

## 8. Выводы

- **SRP выполнен** – класс `Course` занимается только управлением курсом и подписками, а не отправкой сообщений.
- **DIP выполнен** – `Course` зависит от абстракции `Observer`, а не от конкретных классов уведомлений.
- **Гибкость** – новый тип наблюдателя (например, Telegram) можно добавить без изменения `Course`.
- **Динамическое поведение** – наблюдателей можно подписывать и отписывать во время выполнения (продемонстрировано отпиской студента Боба).

Таким образом, паттерн «Наблюдатель» позволяет строить расширяемые и слабосвязанные системы событийно-ориентированной архитектуры.
