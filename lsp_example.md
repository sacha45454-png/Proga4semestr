# Задание: Принцип подстановки Лисков (LSP) — пример нарушения и исправления

## Предметная область
Система управления финансами: банковские счета и депозитные счета (с ограничением на снятие).

## ❌ Пример нарушения LSP

```python
class BankAccount:
    def __init__(self, balance: float):
        self._balance = balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        return self._balance

class DepositAccount(BankAccount):
    def __init__(self, balance: float, lock_until: str):
        super().__init__(balance)
        self.lock_until = lock_until

    def withdraw(self, amount: float) -> bool:
        if self._is_locked():
            return False
        return super().withdraw(amount)

    def _is_locked(self) -> bool:
        # заглушка: true – срок ещё не наступил
        return True

def process_withdrawal(account: BankAccount, amount: float) -> None:
    if account.withdraw(amount):
        print(f"Снято {amount}. Баланс: {account.get_balance()}")
    else:
        print("Недостаточно средств или ошибка")

# Клиентский код
normal_acc = BankAccount(1000)
deposit_acc = DepositAccount(1000, "2026-12-31")
process_withdrawal(normal_acc, 200)   # OK
process_withdrawal(deposit_acc, 200)  # Неожиданный отказ
В чём нарушение?
Функция process_withdrawal ожидает, что любой BankAccount позволит снять деньги при наличии баланса. DepositAccount добавляет скрытое ограничение (дата блокировки), из-за чего подстановка дочернего класса вместо родительского приводит к неожиданному поведению (отказ в снятии без уведомления о причине). Это нарушает LSP.

✅ Исправление (соблюдение LSP)
Вводим интерфейсы Account и Withdrawable, разделяем обязанности. Депозитный счёт не реализует Withdrawable.

python
from abc import ABC, abstractmethod

class Account(ABC):
    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass
    @abstractmethod
    def get_balance(self) -> float:
        pass

class Withdrawable(ABC):
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        pass

class BankAccount(Account, Withdrawable):
    def __init__(self, balance: float):
        self._balance = balance
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self._balance += amount
    def withdraw(self, amount: float) -> bool:
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            return True
        return False
    def get_balance(self) -> float:
        return self._balance

class DepositAccount(Account):
    def __init__(self, balance: float, lock_until: str):
        self._balance = balance
        self.lock_until = lock_until
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self._balance += amount
    def get_balance(self) -> float:
        return self._balance
    # Не реализует Withdrawable – снятие не поддерживается

def process_withdrawal(account: Withdrawable, amount: float) -> None:
    if account.withdraw(amount):
        print(f"Снято {amount}. Баланс: {account.get_balance()}")
    else:
        print("Недостаточно средств")

# Клиентский код
normal_acc = BankAccount(1000)
# deposit_acc = DepositAccount(1000, "2026-12-31") – не может быть передан в process_withdrawal
process_withdrawal(normal_acc, 200)   # OK
Комментарий к исправлению:
Нарушение LSP вызвано попыткой унаследовать DepositAccount от BankAccount с изменением контракта метода withdraw. Исправление основано на принципе разделения интерфейсов (ISP) и композиции: мы создали отдельный интерфейс Withdrawable. Теперь функция process_withdrawal принимает только те объекты, которые гарантируют возможность снятия. Депозитный счёт не реализует Withdrawable, поэтому его нельзя ошибочно подставить туда, где ожидается снятие. LSP соблюдён, так как иерархия не требует заменяемости там, где она не имеет смысла.