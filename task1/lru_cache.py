# lru_cache.py

from collections import OrderedDict

class LRUCache:
    """
    Реалізація кешу з обмеженням по кількості елементів (LRU — найменш нещодавно використовувані).
    Використовує OrderedDict для контролю порядку елементів у кеші.
    """

    def __init__(self, capacity: int):
        """
        Ініціалізація кешу з заданою ємністю.
        """
        self.cache = OrderedDict()  # Використовуємо OrderedDict для збереження порядку
        self.capacity = capacity  # Ємність кешу

    def get(self, key):
        """
        Отримання значення з кешу за ключем.
        Якщо значення є, повертається, і елемент переміщається в кінець.
        Якщо його немає в кеші, повертається -1.
        """
        if key not in self.cache:
            return -1  # Кеш-місс
        else:
            self.cache.move_to_end(key)  # Переміщаємо до кінця (найновіший)
            return self.cache[key]

    def put(self, key, value):
        """
        Додавання елементу до кешу.
        Якщо ключ існує, він переміщується в кінець.
        Якщо кеш переповнений, видаляється найстаріший елемент.
        """
        if key in self.cache:
            self.cache.move_to_end(key)  # Переміщаємо до кінця
        self.cache[key] = value
        if len(self.cache) > self.capacity:  # Якщо кеш переповнений
            self.cache.popitem(last=False)  # Видаляємо найстаріший елемент (перший)
