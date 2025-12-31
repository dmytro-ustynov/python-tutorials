# Частина 1: Теоретична основа багатопоточності

## Зміст
1. [Що таке багатопоточність?](#що-таке-багатопоточність)
2. [Основи модуля threading](#основи-модуля-threading)
3. [Сучасні інструменти: ThreadPoolExecutor](#сучасні-інструменти-threadpoolexecutor)
4. [Потокобезпечна комунікація: Queue](#потокобезпечна-комунікація-queue)
5. [GIL - Global Interpreter Lock](#gil---global-interpreter-lock)
6. [Потоки vs Процеси](#потоки-vs-процеси)

---

## Що таке багатопоточність?

### Основні концепції

**Багатопоточність (Multithreading)** - це здатність програми виконувати декілька операцій паралельно в межах одного процесу.

### Навіщо потрібна багатопоточність?

```python
# Без багатопоточності - послідовне виконання
import time

def scan_port(host, port):
    # Сканування одного порту займає ~1 секунду
    time.sleep(1)
    return f"Port {port}: open"

# Сканування 100 портів послідовно
start = time.time()
for port in range(1, 101):
    scan_port("example.com", port)
print(f"Час виконання: {time.time() - start:.2f} секунд")  # ~100 секунд!
```

```python
# З багатопоточністю - паралельне виконання
import threading
import time

def scan_port(host, port):
    time.sleep(1)
    print(f"Port {port}: open")

# Сканування 100 портів паралельно
start = time.time()
threads = []
for port in range(1, 101):
    thread = threading.Thread(target=scan_port, args=("example.com", port))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f"Час виконання: {time.time() - start:.2f} секунд")  # ~1-2 секунди!
```

### Коли використовувати багатопоточність?

✅ **Ідеально для I/O-bound задач:**
- Мережеві операції (HTTP запити, сканування портів)
- Робота з файлами
- Робота з базами даних
- Очікування на зовнішні ресурси

❌ **Не підходить для CPU-bound задач:**
- Математичні обчислення
- Обробка зображень
- Криптографічні операції
- Для таких задач краще використовувати `multiprocessing`

---

## Основи модуля threading

### Створення простого потоку

```python
import threading
import time

def worker(name, delay):
    """Функція, яка буде виконуватися в окремому потоці"""
    print(f"[{name}] Почав роботу")
    time.sleep(delay)
    print(f"[{name}] Завершив роботу")

# Створення та запуск потоку
thread = threading.Thread(target=worker, args=("Worker-1", 2))
thread.start()  # Запуск потоку

print("Головний потік продовжує працювати...")

thread.join()  # Чекаємо завершення потоку
print("Всі потоки завершені")
```

**Вивід:**
```
[Worker-1] Почав роботу
Головний потік продовжує працювати...
[Worker-1] Завершив роботу
Всі потоки завершені
```

### Створення класу-потоку

```python
import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        """Метод, який буде виконуватися при запуску потоку"""
        print(f"[{self.name}] Почав роботу")
        time.sleep(self.delay)
        print(f"[{self.name}] Завершив роботу")

# Використання
worker = WorkerThread("Worker-1", 2)
worker.start()
worker.join()
```

### Daemon потоки

**Daemon потік** - це фоновий потік, який автоматично завершується, коли завершується головний потік.

```python
import threading
import time

def background_task():
    while True:
        print("Фонова задача працює...")
        time.sleep(1)

# Звичайний потік (НЕ daemon)
# thread = threading.Thread(target=background_task)
# thread.start()
# Програма НЕ завершиться, поки не завершиться цей потік

# Daemon потік
thread = threading.Thread(target=background_task, daemon=True)
thread.start()

time.sleep(3)
print("Головний потік завершується")
# Daemon потік автоматично завершиться разом з головним
```

### Отримання інформації про потоки

```python
import threading
import time

def worker():
    current = threading.current_thread()
    print(f"Ім'я потоку: {current.name}")
    print(f"ID потоку: {current.ident}")
    print(f"Daemon: {current.daemon}")
    time.sleep(2)

thread = threading.Thread(target=worker, name="MyWorker")
thread.start()

print(f"Активних потоків: {threading.active_count()}")
print(f"Список потоків: {[t.name for t in threading.enumerate()]}")

thread.join()
```

---

## Сучасні інструменти: ThreadPoolExecutor

### Що таке ThreadPoolExecutor?

`ThreadPoolExecutor` - це високорівневий інтерфейс для роботи з пулом потоків. Він автоматично керує створенням, використанням та завершенням потоків.

### Переваги ThreadPoolExecutor:

✅ Автоматичне керування пулом потоків
✅ Простота використання
✅ Можливість отримання результатів
✅ Обробка винятків
✅ Context manager підтримка

### Базове використання

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(name, delay):
    print(f"[{name}] Почав виконання")
    time.sleep(delay)
    print(f"[{name}] Завершив виконання")
    return f"Результат від {name}"

# Створення пулу з 3 потоків
with ThreadPoolExecutor(max_workers=3) as executor:
    # Запуск задач
    future1 = executor.submit(task, "Task-1", 1)
    future2 = executor.submit(task, "Task-2", 2)
    future3 = executor.submit(task, "Task-3", 1)

    # Отримання результатів
    print(future1.result())
    print(future2.result())
    print(future3.result())

print("Всі задачі завершені")
```

### map() - для пакетної обробки

```python
from concurrent.futures import ThreadPoolExecutor
import time

def process_item(item):
    time.sleep(1)
    return item * 2

items = [1, 2, 3, 4, 5]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(process_item, items)
    print(list(results))  # [2, 4, 6, 8, 10]
```

### as_completed() - обробка результатів по мірі готовності

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def scan_port(port):
    delay = random.uniform(0.5, 2)
    time.sleep(delay)
    return f"Port {port}: {'open' if random.random() > 0.5 else 'closed'}"

ports = range(1, 21)

with ThreadPoolExecutor(max_workers=10) as executor:
    # Запускаємо всі задачі
    futures = {executor.submit(scan_port, port): port for port in ports}

    # Обробляємо результати по мірі готовності
    for future in as_completed(futures):
        port = futures[future]
        try:
            result = future.result()
            print(f"✓ {result}")
        except Exception as e:
            print(f"✗ Port {port}: error - {e}")
```

### Обробка винятків

```python
from concurrent.futures import ThreadPoolExecutor
import random

def risky_task(n):
    if random.random() > 0.7:
        raise ValueError(f"Помилка в задачі {n}")
    return f"Успіх {n}"

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(risky_task, i) for i in range(10)]

    for future in futures:
        try:
            result = future.result()
            print(f"✓ {result}")
        except Exception as e:
            print(f"✗ Помилка: {e}")
```

---

## Потокобезпечна комунікація: Queue

### Навіщо потрібна Queue?

Коли декілька потоків працюють з спільними даними, можуть виникнути **race conditions** (умови перегонів).

```python
# НЕБЕЗПЕЧНИЙ КОД - race condition!
counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1  # НЕ атомарна операція!

import threading
threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # Очікуємо 1000000, але отримаємо менше!
```

### Queue - потокобезпечна черга

```python
from queue import Queue
import threading
import time
import random

# Створення черги
task_queue = Queue()

def producer(queue, n):
    """Виробник - додає задачі в чергу"""
    for i in range(n):
        item = f"Task-{i}"
        queue.put(item)
        print(f"[Producer] Додав: {item}")
        time.sleep(random.uniform(0.1, 0.5))

def consumer(queue, name):
    """Споживач - бере задачі з черги та обробляє"""
    while True:
        item = queue.get()  # Блокується, поки черга не порожня
        if item is None:  # Сигнал завершення
            break
        print(f"[{name}] Обробляє: {item}")
        time.sleep(random.uniform(0.5, 1))
        queue.task_done()  # Позначаємо задачу як виконану

# Створюємо виробника
producer_thread = threading.Thread(target=producer, args=(task_queue, 10))
producer_thread.start()

# Створюємо споживачів
consumers = []
for i in range(3):
    consumer_thread = threading.Thread(
        target=consumer,
        args=(task_queue, f"Consumer-{i}")
    )
    consumer_thread.start()
    consumers.append(consumer_thread)

# Чекаємо виробника
producer_thread.join()

# Чекаємо, поки всі задачі будуть оброблені
task_queue.join()

# Зупиняємо споживачів
for _ in consumers:
    task_queue.put(None)
for c in consumers:
    c.join()

print("Всі задачі оброблені!")
```

### Типи черг

```python
from queue import Queue, LifoQueue, PriorityQueue

# FIFO (First In First Out) - звичайна черга
fifo = Queue()
fifo.put(1)
fifo.put(2)
fifo.put(3)
print(fifo.get())  # 1

# LIFO (Last In First Out) - стек
lifo = LifoQueue()
lifo.put(1)
lifo.put(2)
lifo.put(3)
print(lifo.get())  # 3

# Priority Queue - черга з пріоритетами
pq = PriorityQueue()
pq.put((3, "низький пріоритет"))
pq.put((1, "високий пріоритет"))
pq.put((2, "середній пріоритет"))
print(pq.get())  # (1, "високий пріоритет")
```

---

## GIL - Global Interpreter Lock

### Що таке GIL?

**GIL (Global Interpreter Lock)** - це м'ютекс, який захищає доступ до об'єктів Python, запобігаючи одночасному виконанню байт-коду Python декількома потоками.

### Як GIL впливає на продуктивність?

```python
import threading
import time

# CPU-bound задача (обчислення)
def cpu_intensive():
    total = 0
    for i in range(10_000_000):
        total += i ** 2
    return total

# Послідовне виконання
start = time.time()
result1 = cpu_intensive()
result2 = cpu_intensive()
sequential_time = time.time() - start
print(f"Послідовне: {sequential_time:.2f} секунд")

# Багатопотокове виконання
start = time.time()
thread1 = threading.Thread(target=cpu_intensive)
thread2 = threading.Thread(target=cpu_intensive)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
threaded_time = time.time() - start
print(f"Багатопотокове: {threaded_time:.2f} секунд")

# Результат: багатопотокове НЕ швидше через GIL!
```

### Чому GIL існує?

1. **Спрощення управління пам'яттю** - Python використовує reference counting
2. **Історичні причини** - більшість C-бібліотек не є thread-safe
3. **Простота реалізації** - легше писати розширення

### Коли GIL НЕ проблема?

✅ **I/O-bound операції:**
- Мережеві запити
- Робота з файлами
- Робота з БД
- **Причина:** GIL звільняється під час очікування I/O

```python
import threading
import time
import requests

def fetch_url(url):
    response = requests.get(url)  # GIL звільняється під час очікування
    return len(response.content)

urls = ["https://example.com"] * 10

# З потоками - швидше!
start = time.time()
threads = [threading.Thread(target=fetch_url, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()
print(f"З потоками: {time.time() - start:.2f} сек")
```

---

## Потоки vs Процеси

### Порівняння

| Характеристика | Потоки (threading) | Процеси (multiprocessing) |
|----------------|-------------------|---------------------------|
| **Пам'ять** | Спільна пам'ять | Окрема пам'ять для кожного |
| **GIL** | Обмежує CPU-bound задачі | Немає GIL |
| **Overhead** | Низький | Високий |
| **Комунікація** | Проста (спільна пам'ять) | Складніша (IPC) |
| **Підходить для** | I/O-bound задачі | CPU-bound задачі |

### Вибір правильного підходу

```python
# I/O-bound задачі - використовуйте ПОТОКИ
import threading

def network_request(url):
    # Робота з мережею, файлами, БД
    pass

threads = [threading.Thread(target=network_request, args=(url,)) for url in urls]

# CPU-bound задачі - використовуйте ПРОЦЕСИ
import multiprocessing

def heavy_computation(data):
    # Складні обчислення, обробка даних
    pass

processes = [multiprocessing.Process(target=heavy_computation, args=(data,)) for data in dataset]
```

### Практичний приклад: коли використовувати що

```python
# Сканування портів - I/O bound, використовуємо потоки
from concurrent.futures import ThreadPoolExecutor
import socket

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))  # I/O операція
            return f"Port {port}: OPEN"
    except:
        return f"Port {port}: CLOSED"

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(lambda p: scan_port("example.com", p), range(1, 1001))

# Брутфорс хешів - CPU bound, використовуємо процеси
from concurrent.futures import ProcessPoolExecutor
import hashlib

def crack_hash(target_hash, start, end):
    for i in range(start, end):
        password = str(i)
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        if hash_value == target_hash:
            return password
    return None

with ProcessPoolExecutor() as executor:
    # Розподіляємо роботу між процесами
    pass
```

---

## Резюме частини 1

### Ключові поняття:

1. **threading.Thread** - базовий клас для створення потоків
2. **ThreadPoolExecutor** - сучасний високорівневий інтерфейс
3. **Queue** - потокобезпечна черга для комунікації
4. **GIL** - обмеження Python для CPU-bound задач
5. **I/O-bound vs CPU-bound** - вибір між потоками та процесами

### Коли використовувати потоки:

✅ Мережеві операції (сканування, HTTP запити)
✅ Робота з файлами
✅ Робота з БД
✅ Будь-які операції з очікуванням

### Best Practices:

1. Використовуйте `ThreadPoolExecutor` замість ручного керування потоками
2. Використовуйте `Queue` для комунікації між потоками
3. Уникайте спільного стану - використовуйте immutable об'єкти
4. Правильно обробляйте винятки в потоках
5. Для CPU-bound задач використовуйте `multiprocessing`

---

**Готові до практики?** Переходьте до [Part_2_Practical.md](Part_2_Practical.md)!