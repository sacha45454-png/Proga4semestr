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


# --- Клиентский код (демонстрация) ---
if __name__ == "__main__":
    # Создаём курс
    course = Course("Python для начинающих")

    # Создаём наблюдателей
    alice = StudentEmailNotifier("Алиса", "alice@mail.com")
    bob = StudentEmailNotifier("Боб", "bob@mail.com")
    parent = ParentSMSNotifier("Боб", "+79998887766")
    logger = AdminLogger()

    # Подписываем
    course.attach(alice)
    course.attach(bob)
    course.attach(parent)
    course.attach(logger)

    # Публикуем материал
    course.publish_material("Урок 1: Переменные")

    # Отписываем Боба
    course.detach(bob)

    # Публикуем ещё материал
    course.publish_material("Урок 2: Условные операторы")