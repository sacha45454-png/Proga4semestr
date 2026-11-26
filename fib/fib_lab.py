"""
Лабораторная работа: Числа Фибоначчи (сопрограммы и итераторы)
Автор: [Кожевников Александр Николаевич]
Группа: [Номер группы]
Дата: [Дата]
"""


# ---------- Задание 1. Сопрограмма ----------

def fib_elem_gen():
    """Генератор бесконечной последовательности чисел Фибоначчи."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fib_coroutine(func):
    """Декоратор для автоматической инициализации корутины."""

    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # продвинуть до первого yield
        return gen

    return wrapper


@fib_coroutine
def my_genn():
    """
    Сопрограмма: принимает число n, возвращает список первых n чисел Фибоначчи.

    Пример:
        >>> gen = my_genn()
        >>> gen.send(3)
        [0, 1, 1]
        >>> gen.send(5)
        [0, 1, 1, 2, 3]
    """
    while True:
        n = yield
        a, b = 0, 1
        result = []
        for _ in range(n):
            result.append(a)
            a, b = b, a + b
        yield result


# ---------- Задание 2. Итератор ----------

class FibonacchiLst:
    """
    Итератор, фильтрующий элементы списка, оставляя только числа Фибоначчи.

    Атрибуты:
        lst (list): исходный список.
        fib_set (set): множество чисел Фибоначчи, не превышающих максимум lst.
    """

    def __init__(self, lst):
        self.lst = lst
        self.index = 0
        # Вычисляем множество чисел Фибоначчи до максимального элемента
        if lst:
            max_val = max(lst)
        else:
            max_val = 0
        fib_set = set()
        a, b = 0, 1
        while a <= max_val:
            fib_set.add(a)
            a, b = b, a + b
        self.fib_set = fib_set

    def __iter__(self):
        return self

    def __next__(self):
        """Возвращает следующий элемент из lst, если он принадлежит fib_set."""
        while self.index < len(self.lst):
            val = self.lst[self.index]
            self.index += 1
            if val in self.fib_set:
                return val
        raise StopIteration


# ---------- Тесты (могут быть в отдельном файле) ----------

def test_fib_1():
    """Проверка: n=3 -> [0,1,1]"""
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]


def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3]


def test_fib_3():
    gen = my_genn()
    assert gen.send(1) == [0]


def test_fib_lst_normal():
    """Обычный список от 0 до 9 -> [0,1,2,3,5,8]"""
    result = list(FibonacchiLst(list(range(10))))
    assert result == [0, 1, 2, 3, 5, 8]


def test_fib_lst_one_element():
    result = list(FibonacchiLst([13]))
    assert result == [13]


def test_fib_lst_no_fib():
    result = list(FibonacchiLst([4, 6, 7, 9]))
    assert result == []


def test_fib_lst_empty():
    result = list(FibonacchiLst([]))
    assert result == []


def test_fib_lst_random_order():
    result = list(FibonacchiLst([13, 4, 21, 10, 3, 8]))
    assert result == [13, 21, 3, 8]


if __name__ == '__main__':
    # Запуск всех тестов
    test_fib_1()
    test_fib_2()
    test_fib_3()
    test_fib_lst_normal()
    test_fib_lst_one_element()
    test_fib_lst_no_fib()
    test_fib_lst_empty()
    test_fib_lst_random_order()
    print("✅ Все тесты пройдены успешно.")