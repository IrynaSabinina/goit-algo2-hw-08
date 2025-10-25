import random
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        """
        Ініціалізація класу для обмеження частоти повідомлень.
        
        :param window_size: Розмір вікна у секундах.
        :param max_requests: Максимальна кількість повідомлень в вікні.
        """
        self.window_size = window_size  # Розмір вікна (10 секунд)
        self.max_requests = max_requests  # Максимальна кількість запитів
        self.user_requests = {}  # Словник для зберігання запитів користувачів

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """
        Очищає застарілі запити з вікна користувача.
        
        :param user_id: Ідентифікатор користувача.
        :param current_time: Поточний час.
        """
        # Отримуємо чергу запитів для користувача
        requests = self.user_requests.get(user_id, deque())

        # Видаляємо всі запити, які стали занадто старими
        while requests and current_time - requests[0] > self.window_size:
            requests.popleft()

        # Оновлюємо список запитів для користувача
        self.user_requests[user_id] = requests

    def can_send_message(self, user_id: str) -> bool:
        """
        Перевіряє, чи може користувач відправити повідомлення.
        
        :param user_id: Ідентифікатор користувача.
        :return: True, якщо можна відправити повідомлення; False — якщо ліміт перевищено.
        """
        current_time = time.time()  # Поточний час
        self._cleanup_window(user_id, current_time)  # Очищаємо застарілі запити

        # Отримуємо список запитів для користувача
        requests = self.user_requests.get(user_id, deque())

        # Перевіряємо, чи можна відправити повідомлення
        if len(requests) < self.max_requests:
            return True  # Можна відправити повідомлення
        return False  # Ліміт перевищено

    def record_message(self, user_id: str) -> bool:
        """
        Записує нове повідомлення для користувача.
        
        :param user_id: Ідентифікатор користувача.
        :return: True, якщо повідомлення записано; False — якщо ліміт перевищено.
        """
        if self.can_send_message(user_id):
            current_time = time.time()
            if user_id not in self.user_requests:
                self.user_requests[user_id] = deque()
            self.user_requests[user_id].append(current_time)  # Записуємо час повідомлення
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Рахує, скільки часу залишилось до можливості відправити нове повідомлення.
        
        :param user_id: Ідентифікатор користувача.
        :return: Час в секундах до можливості відправлення наступного повідомлення.
        """
        current_time = time.time()  # Поточний час
        self._cleanup_window(user_id, current_time)  # Очищаємо застарілі запити

        requests = self.user_requests.get(user_id, deque())

        if len(requests) < self.max_requests:
            return 0  # Можна відправити повідомлення зараз

        # Якщо ліміт перевищено, розраховуємо час до наступного дозволеного повідомлення
        oldest_message_time = requests[0]
        return self.window_size - (current_time - oldest_message_time)


# Демонстрація роботи
def test_rate_limiter():
    # Створюємо rate limiter: вікно 10 секунд, 1 повідомлення
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Симулюємо потік повідомлень від користувачів (послідовні ID від 1 до 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        # Симулюємо різних користувачів (ID від 1 до 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Невелика затримка між повідомленнями для реалістичності
        time.sleep(random.uniform(0.1, 1.0))

    # Чекаємо, поки вікно очиститься
    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
