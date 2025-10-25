# main.py

import random
import time
from lru_cache import LRUCache
from test_results import make_queries


def range_sum_no_cache(array, left, right):
    """
    Обчислення суми елементів масиву без використання кешу.
    """
    return sum(array[left:right+1])


def update_no_cache(array, index, value):
    """
    Оновлення елементу масиву без використання кешу.
    """
    array[index] = value


def range_sum_with_cache(array, left, right, cache):
    """
    Обчислення суми елементів масиву з використанням LRU кешу.
    Якщо запит вже є в кеші — використовуємо кеш.
    Якщо ні — обчислюємо суму та зберігаємо в кеш.
    """
    key = (left, right)
    result = cache.get(key)
    
    if result != -1:
        return result  # Якщо кеш потрапив

    result = sum(array[left:right+1])  # Якщо кеш пропустив
    cache.put(key, result)  # Зберігаємо результат у кеш
    return result


def update_with_cache(array, index, value, cache):
    """
    Оновлення елементу масиву з очищенням кешу для всіх запитів,
    які містять оновлений індекс.
    """
    array[index] = value
    to_remove = [key for key in cache.cache if key[0] <= index <= key[1] or key[1] <= index <= key[0]]
    for key in to_remove:
        del cache.cache[key]


def test():
    """
    Тестування кешування та порівняння часу виконання без кешу та з кешем.
    """
    n = 100000
    q = 50000
    array = [random.randint(1, 100) for _ in range(n)]  # Генерація початкового масиву

    # Створення кешу з ємністю 1000
    cache = LRUCache(1000)

    # Генерація запитів
    queries = make_queries(n, q)

    # Без кешу
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    end_time = time.time()
    time_no_cache = end_time - start_time

    # З кешем
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array, query[1], query[2], cache)
        else:
            update_with_cache(array, query[1], query[2], cache)
    end_time = time.time()
    time_with_cache = end_time - start_time

    # Виведення результатів
    speedup = time_no_cache / time_with_cache
    print(f"Без кешу :  {time_no_cache:.2f} c")
    print(f"LRU-кеш  :   {time_with_cache:.2f} c  (прискорення ×{speedup:.1f})")


if __name__ == "__main__":
    test()
