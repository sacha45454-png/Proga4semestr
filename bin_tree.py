import collections
import pprint

# ==========================================
# НАСТРОЙКИ ВАРИАНТА (Измените под свой номер)
# ==========================================
# Пример для Варианта 1: Root=1, height=5, left=root*2, right=root+3
# Для других вариантов просто измените лямбда-функции ниже.
# Например, для Варианта 2: LEFT_RULE = lambda x: x * 3, RIGHT_RULE = lambda x: x + 4

DEFAULT_ROOT = 1
DEFAULT_HEIGHT = 5
LEFT_RULE = lambda x: x * 2
RIGHT_RULE = lambda x: x + 3


# ==========================================
# 1. РЕКУРСИВНЫЙ ВАРИАНТ (Словарь)
# ==========================================
def gen_bin_tree_recursive(height, root, left_rule, right_rule):
    """
    Рекурсивно строит бинарное дерево в виде вложенных словарей.
    height: высота дерева (количество уровней)
    root: значение корня
    """
    if height <= 0:
        return None

    return {
        "root": root,
        "left": gen_bin_tree_recursive(height - 1, left_rule(root), left_rule, right_rule),
        "right": gen_bin_tree_recursive(height - 1, right_rule(root), left_rule, right_rule)
    }


# ==========================================
# 2. НЕРЕКУРСИВНЫЙ ВАРИАНТ (Словарь + deque)
# ==========================================
def gen_bin_tree_iterative(height, root, left_rule, right_rule):
    """
    Итеративно строит бинарное дерево в виде вложенных словарей.
    Использует collections.deque для обхода в ширину (BFS).
    """
    if height <= 0:
        return None

    # Инициализируем корень
    tree = {"root": root, "left": None, "right": None}

    # Очередь хранит кортежи: (узел_словарь, текущая_высота_узла)
    queue = collections.deque([(tree, 1)])

    while queue:
        node, current_height = queue.popleft()

        # Если мы еще не достигли максимальной высоты, создаем потомков
        if current_height < height:
            left_val = left_rule(node["root"])
            right_val = right_rule(node["root"])

            # Создаем узлы-потомки как отдельные переменные
            # Это исправляет предупреждения PyCharm о несоответствии типов
            left_node = {"root": left_val, "left": None, "right": None}
            right_node = {"root": right_val, "left": None, "right": None}

            # Присваиваем их текущему узлу
            node["left"] = left_node
            node["right"] = right_node

            # Добавляем потомков в очередь для дальнейшей обработки
            queue.append((left_node, current_height + 1))
            queue.append((right_node, current_height + 1))

    return tree


# ==========================================
# 3. ИССЛЕДОВАНИЕ ДРУГИХ СТРУКТУР (collections.namedtuple)
# ==========================================
# Создаем именованный кортеж для представления узла
Node = collections.namedtuple('Node', ['value', 'left', 'right'])


def gen_bin_tree_namedtuple(height, root, left_rule, right_rule):
    """
    Рекурсивное построение дерева с использованием namedtuple.
    Демонстрирует альтернативный контейнер из модуля collections.
    """
    if height <= 0:
        return None

    return Node(
        value=root,
        left=gen_bin_tree_namedtuple(height - 1, left_rule(root), left_rule, right_rule),
        right=gen_bin_tree_namedtuple(height - 1, right_rule(root), left_rule, right_rule)
    )


# ==========================================
# ФУНКЦИЯ ОБЕРТКА (Согласно заданию)
# ==========================================
def gen_bin_tree(height=DEFAULT_HEIGHT, root=DEFAULT_ROOT, left_rule=LEFT_RULE, right_rule=RIGHT_RULE,
                 method='recursive'):
    """
    Основная функция, принимающая параметры.
    Если параметры не переданы, используются значения по умолчанию (из варианта).
    """
    if method == 'recursive':
        return gen_bin_tree_recursive(height, root, left_rule, right_rule)
    elif method == 'iterative':
        return gen_bin_tree_iterative(height, root, left_rule, right_rule)
    elif method == 'namedtuple':
        return gen_bin_tree_namedtuple(height, root, left_rule, right_rule)
    else:
        raise ValueError("Неизвестный метод. Используйте 'recursive', 'iterative' или 'namedtuple'.")


# ==========================================
# ДЕМОНСТРАЦИЯ РАБОТЫ
# ==========================================
if __name__ == "__main__":
    print("=== 1. Рекурсивный метод (dict) ===")
    tree_rec = gen_bin_tree(method='recursive')
    pprint.pprint(tree_rec, width=60)

    print("\n=== 2. Нерекурсивный метод (dict + deque) ===")
    tree_iter = gen_bin_tree(method='iterative')
    pprint.pprint(tree_iter, width=60)

    print("\n=== 3. Альтернативная структура (namedtuple) ===")
    tree_nt = gen_bin_tree(method='namedtuple')
    print(tree_nt)

    # Проверка: передача своих параметров (например, Root=10, height=3)
    print("\n=== 4. Проверка с пользовательскими параметрами (Root=10, height=3) ===")
    custom_tree = gen_bin_tree(height=3, root=10, method='recursive')
    pprint.pprint(custom_tree, width=60)