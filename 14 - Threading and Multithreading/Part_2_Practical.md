# Частина 2: Практична робота - Сканери та брутфорс

## Зміст
1. [Багатопотоковий сканер портів](#багатопотоковий-сканер-портів)
2. [Багатопотоковий брутфорс паролів](#багатопотоковий-брутфорс-паролів)
3. [Оптимізація та порівняння підходів](#оптимізація-та-порівняння-підходів)
4. [Додаткові завдання](#додаткові-завдання)

---

## Багатопотоковий сканер портів

### Завдання 1: Простий сканер портів (базовий рівень)

Створіть базовий сканер портів, який перевіряє, чи відкритий конкретний порт на хості.

```python
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def scan_port(host, port, timeout=1):
    """
    Сканує один порт на хості

    Args:
        host: IP адреса або доменне ім'я
        port: номер порту для сканування
        timeout: таймаут підключення в секундах

    Returns:
        tuple: (port, is_open, service_name)
    """
    try:
        # Створюємо TCP сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

            if result == 0:
                # Порт відкритий
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return (port, True, service)
            else:
                # Порт закритий
                return (port, False, None)
    except socket.gaierror:
        # Помилка DNS
        return (port, False, None)
    except socket.error:
        # Інша помилка сокету
        return (port, False, None)

def scan_ports_basic(host, ports, max_workers=100):
    """
    Сканує список портів на хості

    Args:
        host: IP адреса або доменне ім'я
        ports: список або діапазон портів
        max_workers: кількість потоків

    Returns:
        list: список відкритих портів
    """
    print(f"🔍 Сканування {host}...")
    print(f"📊 Кількість портів: {len(list(ports))}")
    print(f"🧵 Кількість потоків: {max_workers}")
    print("-" * 60)

    start_time = time.time()
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Запускаємо сканування всіх портів
        futures = {
            executor.submit(scan_port, host, port): port
            for port in ports
        }

        # Обробляємо результати по мірі готовності
        for future in as_completed(futures):
            port = futures[future]
            try:
                port_num, is_open, service = future.result()
                if is_open:
                    open_ports.append(port_num)
                    print(f"✓ Port {port_num:5d} | OPEN | Service: {service}")
            except Exception as e:
                print(f"✗ Port {port} | ERROR: {e}")

    elapsed_time = time.time() - start_time

    print("-" * 60)
    print(f"✅ Сканування завершено за {elapsed_time:.2f} секунд")
    print(f"📈 Знайдено відкритих портів: {len(open_ports)}")
    print(f"⚡ Швидкість: {len(list(ports)) / elapsed_time:.2f} портів/сек")

    return open_ports

# Приклад використання
if __name__ == "__main__":
    # Сканування популярних портів
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3000, 3306, 3389, 5432, 8080]

    # Увага! Сканування тільки localhost або власних систем!
    scan_ports_basic("127.0.0.1", common_ports, max_workers=10)
```

**Завдання для самостійного виконання:**
1. Запустіть сканер на localhost
2. Порівняйте швидкість з різною кількістю потоків (10, 50, 100)
3. Додайте progress bar для відображення прогресу

---

### Завдання 2: Розширений сканер з Banner Grabbing (середній рівень)

Розширте сканер, додавши функцію визначення версії сервісу (banner grabbing).

```python
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def grab_banner(host, port, timeout=2):
    """
    Отримує banner від сервісу для ідентифікації версії

    Args:
        host: IP адреса
        port: порт
        timeout: таймаут

    Returns:
        str: banner сервісу
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))

            # Деякі сервіси одразу надсилають banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

            if not banner:
                # Спробуємо надіслати запит
                sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

            return banner[:100]  # Обмежуємо довжину
    except:
        return None

class PortScanner:
    """Клас для сканування портів з розширеними можливостями"""

    def __init__(self, host, timeout=1):
        self.host = host
        self.timeout = timeout
        self.results = []

    def scan_port(self, port):
        """Сканує один порт з отриманням banner"""
        result = {
            'port': port,
            'is_open': False,
            'service': None,
            'banner': None
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                connection_result = sock.connect_ex((self.host, port))

                if connection_result == 0:
                    result['is_open'] = True

                    # Отримуємо назву сервісу
                    try:
                        result['service'] = socket.getservbyport(port)
                    except:
                        result['service'] = 'unknown'

                    # Отримуємо banner
                    result['banner'] = grab_banner(self.host, port, self.timeout)

        except Exception as e:
            result['error'] = str(e)

        return result

    def scan_range(self, start_port, end_port, max_workers=50):
        """Сканує діапазон портів"""
        print(f"\n{'='*70}")
        print(f"🎯 Target: {self.host}")
        print(f"📊 Port Range: {start_port}-{end_port} ({end_port - start_port + 1} ports)")
        print(f"🧵 Threads: {max_workers}")
        print(f"{'='*70}\n")

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.scan_port, port): port
                for port in range(start_port, end_port + 1)
            }

            completed = 0
            total = len(futures)

            for future in as_completed(futures):
                completed += 1
                result = future.result()

                if result['is_open']:
                    self.results.append(result)
                    banner_info = f" | {result['banner'][:50]}" if result['banner'] else ""
                    print(f"✓ Port {result['port']:5d} | {result['service']:15s}{banner_info}")

                # Progress indicator
                if completed % 100 == 0:
                    progress = (completed / total) * 100
                    print(f"⏳ Progress: {progress:.1f}% ({completed}/{total})")

        elapsed = time.time() - start_time

        self._print_summary(elapsed, total)

        return self.results

    def _print_summary(self, elapsed, total_ports):
        """Виводить підсумкову статистику"""
        print(f"\n{'='*70}")
        print(f"📈 Scan Summary:")
        print(f"  • Total ports scanned: {total_ports}")
        print(f"  • Open ports found: {len(self.results)}")
        print(f"  • Time elapsed: {elapsed:.2f} seconds")
        print(f"  • Speed: {total_ports / elapsed:.2f} ports/sec")
        print(f"{'='*70}\n")

    def save_results(self, filename):
        """Зберігає результати в файл"""
        with open(filename, 'w') as f:
            f.write(f"Port Scan Results for {self.host}\n")
            f.write("="*60 + "\n\n")
            for result in self.results:
                f.write(f"Port: {result['port']}\n")
                f.write(f"Service: {result['service']}\n")
                if result['banner']:
                    f.write(f"Banner: {result['banner']}\n")
                f.write("-"*60 + "\n")

# Приклад використання
if __name__ == "__main__":
    scanner = PortScanner("127.0.0.1", timeout=1)

    # Сканування популярних портів
    scanner.scan_range(1, 1000, max_workers=100)

    # Збереження результатів
    scanner.save_results("scan_results.txt")
```

**Завдання для самостійного виконання:**
1. Додайте підтримку сканування декількох хостів
2. Реалізуйте експорт результатів у JSON формат
3. Додайте колоризацію виводу (використовуйте colorama)

---

## Багатопотоковий брутфорс паролів

### ⚠️ ЕТИЧНЕ ПОПЕРЕДЖЕННЯ

**УВАГА!** Код нижче призначений ВИКЛЮЧНО для:
- Навчальних цілей
- Тестування власних систем
- Авторизованого пентестингу
- CTF змагань

🚫 Використання цих інструментів проти чужих систем без дозволу є НЕЗАКОННИМ!

---

### Завдання 3: HTTP Basic Auth брутфорс (базовий рівень)

```python
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from queue import Queue

class HTTPBruteForcer:
    """Клас для брутфорсу HTTP Basic Authentication"""

    def __init__(self, target_url, username):
        self.target_url = target_url
        self.username = username
        self.found_password = None
        self.attempts = 0

    def try_password(self, password):
        """Спроба входу з паролем"""
        self.attempts += 1

        try:
            response = requests.get(
                self.target_url,
                auth=(self.username, password),
                timeout=5
            )

            if response.status_code == 200:
                return (True, password)
            else:
                return (False, password)

        except requests.RequestException as e:
            return (False, password)

    def brute_force(self, password_list, max_workers=10):
        """Виконує брутфорс з використанням списку паролів"""
        print(f"\n{'='*70}")
        print(f"🎯 Target URL: {self.target_url}")
        print(f"👤 Username: {self.username}")
        print(f"📝 Passwords to try: {len(password_list)}")
        print(f"🧵 Threads: {max_workers}")
        print(f"{'='*70}\n")

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.try_password, password): password
                for password in password_list
            }

            for future in as_completed(futures):
                success, password = future.result()

                if success:
                    self.found_password = password
                    print(f"\n✅ SUCCESS! Password found: {password}")
                    print(f"⏱️  Time: {time.time() - start_time:.2f} seconds")
                    print(f"🔢 Attempts: {self.attempts}")

                    # Скасовуємо інші задачі
                    for f in futures:
                        f.cancel()

                    return password
                else:
                    if self.attempts % 10 == 0:
                        print(f"⏳ Tried {self.attempts} passwords...")

        elapsed = time.time() - start_time
        print(f"\n❌ Password not found")
        print(f"⏱️  Total time: {elapsed:.2f} seconds")
        print(f"🔢 Total attempts: {self.attempts}")

        return None

# Приклад використання
if __name__ == "__main__":
    # ВАЖЛИВО: використовуйте тільки на тестових системах!

    # Створення тестового списку паролів
    common_passwords = [
        "password", "123456", "admin", "letmein", "welcome",
        "monkey", "dragon", "master", "sunshine", "princess",
        "qwerty", "123456789", "12345678", "12345", "1234567"
    ]

    # Приклад для тестового сервера
    # brute_forcer = HTTPBruteForcer(
    #     "http://testserver.local/protected",
    #     "admin"
    # )
    # brute_forcer.brute_force(common_passwords, max_workers=5)

    print("⚠️  Для використання розкоментуйте код вище та вкажіть ваш тестовий сервер")
```

---

### Завдання 4: Словниковий брутфорс з Queue (середній рівень)

```python
from queue import Queue
import threading
import time
import requests
from requests.auth import HTTPBasicAuth

class DictionaryBruteForcer:
    """Брутфорсер з використанням черги та декількох потоків"""

    def __init__(self, target_url, username, num_threads=10):
        self.target_url = target_url
        self.username = username
        self.num_threads = num_threads

        self.password_queue = Queue()
        self.found_password = None
        self.attempts = 0
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def worker(self, worker_id):
        """Робочий потік для перевірки паролів"""
        while not self.stop_event.is_set():
            try:
                password = self.password_queue.get(timeout=1)
            except:
                continue

            if self.found_password:
                self.password_queue.task_done()
                break

            try:
                response = requests.get(
                    self.target_url,
                    auth=HTTPBasicAuth(self.username, password),
                    timeout=5
                )

                with self.lock:
                    self.attempts += 1

                    if response.status_code == 200:
                        self.found_password = password
                        self.stop_event.set()
                        print(f"\n🎉 [Worker-{worker_id}] Found password: {password}")
                        print(f"   Attempts: {self.attempts}")
                    elif self.attempts % 50 == 0:
                        print(f"⏳ Tried {self.attempts} passwords...")

            except Exception as e:
                pass

            finally:
                self.password_queue.task_done()

    def load_dictionary(self, filename):
        """Завантажує словник паролів з файлу"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            return passwords
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
            return []

    def brute_force(self, passwords):
        """Запускає брутфорс"""
        print(f"\n{'='*70}")
        print(f"🎯 Target: {self.target_url}")
        print(f"👤 Username: {self.username}")
        print(f"📝 Dictionary size: {len(passwords)} passwords")
        print(f"🧵 Worker threads: {self.num_threads}")
        print(f"{'='*70}\n")

        start_time = time.time()

        # Додаємо паролі в чергу
        for password in passwords:
            self.password_queue.put(password)

        # Створюємо та запускаємо робочі потоки
        workers = []
        for i in range(self.num_threads):
            worker = threading.Thread(target=self.worker, args=(i,))
            worker.start()
            workers.append(worker)

        # Чекаємо завершення всіх задач
        self.password_queue.join()
        self.stop_event.set()

        # Чекаємо завершення всіх потоків
        for worker in workers:
            worker.join()

        elapsed = time.time() - start_time

        print(f"\n{'='*70}")
        if self.found_password:
            print(f"✅ SUCCESS!")
            print(f"🔑 Password: {self.found_password}")
        else:
            print(f"❌ Password not found")
        print(f"⏱️  Time: {elapsed:.2f} seconds")
        print(f"🔢 Attempts: {self.attempts}")
        print(f"⚡ Speed: {self.attempts / elapsed:.2f} attempts/sec")
        print(f"{'='*70}\n")

        return self.found_password

# Створення тестового словника
def create_test_dictionary(filename="test_passwords.txt"):
    """Створює тестовий словник паролів"""
    common_passwords = [
        "password", "123456", "password123", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "sunshine",
        "princess", "qwerty", "123456789", "12345678", "12345",
        "1234567", "password1", "12345678", "123123", "1234567890",
        "Password1", "1234", "qwerty123", "1q2w3e4r", "admin123"
    ]

    with open(filename, 'w') as f:
        for password in common_passwords:
            f.write(password + '\n')

    print(f"✅ Created test dictionary: {filename}")
    return filename

# Приклад використання
if __name__ == "__main__":
    # Створюємо тестовий словник
    dict_file = create_test_dictionary()

    print("\n⚠️  Remember: Only use on systems you own or have permission to test!")
    print("⚠️  Uncomment and modify the code below to use the brute forcer\n")

    # brute_forcer = DictionaryBruteForcer(
    #     target_url="http://your-test-server/protected",
    #     username="admin",
    #     num_threads=10
    # )
    #
    # passwords = brute_forcer.load_dictionary(dict_file)
    # brute_forcer.brute_force(passwords)
```

---

## Оптимізація та порівняння підходів

### Завдання 5: Порівняння продуктивності (складний рівень)

```python
import time
import socket
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
from queue import Queue
import statistics

class PerformanceTester:
    """Клас для тестування продуктивності різних підходів"""

    def __init__(self, host="127.0.0.1", port_range=(1, 1000)):
        self.host = host
        self.port_range = port_range
        self.results = {}

    def scan_port(self, port):
        """Базова функція сканування порту"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                result = sock.connect_ex((self.host, port))
                return result == 0
        except:
            return False

    def sequential_scan(self):
        """Послідовне сканування (без багатопоточності)"""
        print("\n🔄 Sequential Scan...")
        start = time.time()

        open_ports = []
        for port in range(*self.port_range):
            if self.scan_port(port):
                open_ports.append(port)

        elapsed = time.time() - start
        self.results['sequential'] = {
            'time': elapsed,
            'open_ports': len(open_ports),
            'speed': (self.port_range[1] - self.port_range[0]) / elapsed
        }

        print(f"✓ Time: {elapsed:.2f}s | Speed: {self.results['sequential']['speed']:.2f} ports/s")
        return elapsed

    def threaded_scan(self, num_threads):
        """Сканування з фіксованою кількістю потоків"""
        print(f"\n🧵 Threaded Scan ({num_threads} threads)...")
        start = time.time()

        open_ports = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = executor.map(self.scan_port, range(*self.port_range))
            open_ports = [port for port, is_open in
                         zip(range(*self.port_range), results) if is_open]

        elapsed = time.time() - start
        key = f'threaded_{num_threads}'
        self.results[key] = {
            'time': elapsed,
            'open_ports': len(open_ports),
            'speed': (self.port_range[1] - self.port_range[0]) / elapsed
        }

        print(f"✓ Time: {elapsed:.2f}s | Speed: {self.results[key]['speed']:.2f} ports/s")
        return elapsed

    def queue_based_scan(self, num_workers):
        """Сканування з використанням Queue"""
        print(f"\n📦 Queue-based Scan ({num_workers} workers)...")
        start = time.time()

        port_queue = Queue()
        results_queue = Queue()

        # Заповнюємо чергу портів
        for port in range(*self.port_range):
            port_queue.put(port)

        def worker():
            while not port_queue.empty():
                try:
                    port = port_queue.get(timeout=0.1)
                    if self.scan_port(port):
                        results_queue.put(port)
                    port_queue.task_done()
                except:
                    break

        # Створюємо воркерів
        threads = []
        for _ in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        # Чекаємо завершення
        port_queue.join()
        for t in threads:
            t.join()

        elapsed = time.time() - start
        open_ports = results_queue.qsize()

        key = f'queue_{num_workers}'
        self.results[key] = {
            'time': elapsed,
            'open_ports': open_ports,
            'speed': (self.port_range[1] - self.port_range[0]) / elapsed
        }

        print(f"✓ Time: {elapsed:.2f}s | Speed: {self.results[key]['speed']:.2f} ports/s")
        return elapsed

    def find_optimal_threads(self):
        """Знаходить оптимальну кількість потоків"""
        print("\n🔍 Finding optimal thread count...")

        thread_counts = [10, 25, 50, 100, 200, 500]
        times = []

        for count in thread_counts:
            elapsed = self.threaded_scan(count)
            times.append(elapsed)

        # Знаходимо оптимальну кількість
        optimal_idx = times.index(min(times))
        optimal_count = thread_counts[optimal_idx]

        print(f"\n🎯 Optimal thread count: {optimal_count}")
        print(f"⚡ Best time: {times[optimal_idx]:.2f}s")

        return optimal_count

    def run_all_tests(self):
        """Запускає всі тести"""
        print(f"\n{'='*70}")
        print(f"🧪 Performance Testing")
        print(f"🎯 Target: {self.host}")
        print(f"📊 Port range: {self.port_range[0]}-{self.port_range[1]}")
        print(f"{'='*70}")

        # Послідовне сканування
        self.sequential_scan()

        # Багатопотокове з різною кількістю потоків
        for num_threads in [10, 50, 100, 200]:
            self.threaded_scan(num_threads)

        # Queue-based
        self.queue_based_scan(50)

        # Виводимо порівняльну таблицю
        self.print_comparison()

    def print_comparison(self):
        """Виводить порівняльну таблицю"""
        print(f"\n{'='*70}")
        print(f"📊 Performance Comparison")
        print(f"{'='*70}\n")

        # Сортуємо за часом
        sorted_results = sorted(self.results.items(), key=lambda x: x[1]['time'])

        print(f"{'Method':<20} {'Time (s)':<12} {'Speed (p/s)':<15} {'Speedup':<10}")
        print("-" * 70)

        baseline = self.results.get('sequential', {}).get('time', 1)

        for method, data in sorted_results:
            speedup = baseline / data['time']
            print(f"{method:<20} {data['time']:>10.2f}s  {data['speed']:>12.2f}  {speedup:>8.2f}x")

        print(f"\n{'='*70}\n")

# Приклад використання
if __name__ == "__main__":
    tester = PerformanceTester(
        host="127.0.0.1",
        port_range=(1, 500)  # Меншийдіапазон для швидшого тестування
    )

    # Запускаємо всі тести
    tester.run_all_tests()

    # Знаходимо оптимальну кількість потоків
    # optimal = tester.find_optimal_threads()
```

---

## Додаткові завдання

### Завдання 6: Багатопотоковий vulnerability scanner

Створіть сканер, який перевіряє різні типи вразливостей:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import socket

class VulnerabilityScanner:
    """Простий сканер вразливостей"""

    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []

    def check_open_ports(self, common_ports):
        """Перевіряє відкриті порти"""
        open_ports = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {
                executor.submit(self._check_port, port): port
                for port in common_ports
            }
            for future in as_completed(futures):
                if future.result():
                    open_ports.append(futures[future])
        return open_ports

    def _check_port(self, port):
        """Перевіряє один порт"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((self.target, port))
                return result == 0
        except:
            return False

    def check_http_headers(self):
        """Перевіряє HTTP заголовки безпеки"""
        try:
            response = requests.get(f"http://{self.target}", timeout=5)

            security_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'Strict-Transport-Security',
                'Content-Security-Policy'
            ]

            missing_headers = [
                header for header in security_headers
                if header not in response.headers
            ]

            if missing_headers:
                return {
                    'type': 'Missing Security Headers',
                    'details': missing_headers
                }
        except:
            pass

        return None

    def check_default_credentials(self):
        """Перевіряє дефолтні облікові дані"""
        default_creds = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('root', 'root'),
            ('admin', ''),
        ]

        vulnerabilities = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self._try_login, user, pwd): (user, pwd)
                for user, pwd in default_creds
            }

            for future in as_completed(futures):
                if future.result():
                    user, pwd = futures[future]
                    vulnerabilities.append({
                        'type': 'Default Credentials',
                        'details': f"Username: {user}, Password: {pwd}"
                    })

        return vulnerabilities

    def _try_login(self, username, password):
        """Спроба входу"""
        try:
            response = requests.get(
                f"http://{self.target}/admin",
                auth=(username, password),
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def scan(self):
        """Виконує повне сканування"""
        print(f"\n🔍 Scanning {self.target}...")
        print("="*60)

        # Перевіряємо порти
        print("\n1. Checking open ports...")
        common_ports = [21, 22, 23, 80, 443, 3306, 3389, 8080]
        open_ports = self.check_open_ports(common_ports)
        if open_ports:
            print(f"   ⚠️  Open ports found: {open_ports}")
            self.vulnerabilities.append({
                'type': 'Open Ports',
                'details': open_ports
            })

        # Перевіряємо HTTP заголовки
        print("\n2. Checking HTTP security headers...")
        header_vuln = self.check_http_headers()
        if header_vuln:
            print(f"   ⚠️  {header_vuln}")
            self.vulnerabilities.append(header_vuln)

        # Перевіряємо дефолтні креди
        print("\n3. Checking default credentials...")
        cred_vulns = self.check_default_credentials()
        if cred_vulns:
            self.vulnerabilities.extend(cred_vulns)
            print(f"   ⚠️  Default credentials found!")

        self._print_report()

    def _print_report(self):
        """Виводить звіт"""
        print(f"\n{'='*60}")
        print(f"📋 Vulnerability Report")
        print(f"{'='*60}\n")

        if not self.vulnerabilities:
            print("✅ No vulnerabilities found!")
        else:
            for i, vuln in enumerate(self.vulnerabilities, 1):
                print(f"{i}. {vuln['type']}")
                print(f"   Details: {vuln['details']}\n")

        print(f"Total vulnerabilities: {len(self.vulnerabilities)}")
        print(f"{'='*60}\n")

# Використання
if __name__ == "__main__":
    scanner = VulnerabilityScanner("127.0.0.1")
    scanner.scan()
```

---

## Завдання для самостійної роботи

### Рівень 1: Базовий
1. Створіть сканер, який зберігає результати в CSV файл
2. Додайте можливість сканування з командного рядка
3. Реалізуйте простий progress bar

### Рівень 2: Середній
1. Додайте підтримку IPv6
2. Реалізуйте UDP сканування
3. Створіть систему логування з різними рівнями (INFO, WARNING, ERROR)
4. Додайте можливість зупинки/поновлення сканування

### Рівень 3: Складний
1. Реалізуйте адаптивне регулювання кількості потоків
2. Додайте детектування операційної системи за відкритими портами
3. Створіть веб-інтерфейс для сканера (Flask)
4. Реалізуйте розподілене сканування (декілька машин)

---

## Корисні поради

### Оптимізація продуктивності:
1. **Timeout** - встановлюйте розумні таймаути (0.5-2 секунди)
2. **Кількість потоків** - оптимальна кількість залежить від мережі (50-200)
3. **Rate limiting** - додавайте затримки, щоб не перевантажувати мережу
4. **Connection pooling** - використовуйте session в requests

### Обробка помилок:
1. Завжди обробляйте всі можливі винятки
2. Логуйте помилки для подальшого аналізу
3. Додавайте повторні спроби (retry) для ненадійних операцій

### Етика:
1. Завжди отримуйте дозвіл перед сканування м
2. Використовуйте rate limiting
3. Поважайте robots.txt та інші правила
4. Документуйте всі свої дії

---

## Контрольні запитання

1. Чому багатопоточність прискорює сканування портів?
2. Що таке GIL і як він впливає на продуктивність?
3. Коли краще використовувати потоки, а коли процеси?
4. Що таке race condition і як його уникнути?
5. Яка оптимальна кількість потоків для сканування портів?
6. Чому важливо використовувати таймаути?
7. Які етичні аспекти потрібно враховувати?

---

**Вітаємо! Ви завершили практичну частину заняття з багатопоточності! 🎉**

Тепер ви вмієте:
✅ Створювати багатопотокові додатки
✅ Оптимізувати продуктивність
✅ Будувати інструменти для кібербезпеки
✅ Правильно використовувати threading та Queue

Продовжуйте практикуватися та створювати власні інструменти! 🚀