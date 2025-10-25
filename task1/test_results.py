# test_results.py

import random

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    """
    Генерація запитів для тестування.
    Генерує список із 50 000 запитів до масиву з 100 000 елементів.
    ~3% запитів є оновленнями, решта — запити на підрахунок суми.
    95% запитів на діапазони — з "гарячих" діапазонів.
    """
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]  # Генерація гарячих діапазонів
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries
