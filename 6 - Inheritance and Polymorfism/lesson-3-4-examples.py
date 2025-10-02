# Практичні приклади для Заняття 3/4
# ООП: Наслідування, Поліморфізм, Магічні методи, Криптографія

# ============================================================
# ПРИКЛАД 1: Система логування подій безпеки
# ============================================================
from abc import ABC, abstractmethod


class Scanner(ABC):
    @abstractmethod
    def scan(self):
        pass


# ❌ Забули реалізувати scan()
class PortScanner(Scanner):
    pass  # Метод scan() не реалізовано!


# Помилка виникне ТУТ ⬇️ (при створенні об'єкта)
scanner = PortScanner()


class SecurityEvent:
    """Базовий клас для всіх подій безпеки"""
    
    def __init__(self, timestamp, source_ip, description):
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.description = description
        self.severity = "INFO"
    
    def log(self):
        return f"[{self.severity}] {self.timestamp} | {self.source_ip} | {self.description}"
    
    def is_suspicious(self):
        return self.severity in ["WARNING", "CRITICAL"]


class LoginAttempt(SecurityEvent):
    """Спроби входу в систему"""
    
    def __init__(self, timestamp, source_ip, username, success):
        super().__init__(timestamp, source_ip, f"Login attempt by {username}")
        self.username = username
        self.success = success
        self.severity = "INFO" if success else "WARNING"


class BruteForceAttack(SecurityEvent):
    """Атаки методом підбору"""
    def __init__(self, timestamp, source_ip, target_username, attempts):
        super().__init__(timestamp, source_ip, f"Bruteforce attack on {target_username}")
        self.target_username = target_username
        self.attempts = attempts
        self.severity = "CRITICAL" if attempts > 10 else "WARNING"
    
    def log(self):
        base_log = super().log()
        return f"{base_log} | Attempts: {self.attempts}"


# Тестування
if __name__ == "__main__":
    print("=== Приклад 1: Система логування ===\n")
    
    events = [
        LoginAttempt("2025-10-02 14:30:00", "192.168.1.100", "admin", True),
        LoginAttempt("2025-10-02 14:31:00", "203.0.113.45", "root", False),
        BruteForceAttack("2025-10-02 14:35:00", "203.0.113.45", "admin", 15)
    ]
    
    for event in events:
        print(event.log())
        if event.is_suspicious():
            print("  ⚠️  SUSPICIOUS EVENT DETECTED!")
    print()


# ============================================================
# ПРИКЛАД 2: Поліморфізм - Система сканерів безпеки
# ============================================================
import random
from abc import ABC, abstractmethod


class SecurityScanner(ABC):
    """Абстрактний базовий клас для сканерів"""
    def __init__(self, target):
        self.target = target
        self.results = []
    
    @abstractmethod
    def scan(self):
        pass
    
    def report(self):
        return f"Scan results for {self.target}: {len(self.results)} findings"


class PortScanner(SecurityScanner):
    def scan(self):
        common_ports = [21, 22, 80, 443, 3306, 8080]
        self.results = [port for port in common_ports if random.choice([True, False])]
        return self.results


class VulnerabilityScanner(SecurityScanner):
    def scan(self):
        vulnerabilities = [
            "CVE-2024-1234: SQL Injection",
            "CVE-2024-5678: XSS Vulnerability",
            "CVE-2024-9012: Outdated SSL/TLS"
        ]
        self.results = random.sample(vulnerabilities, k=random.randint(0, 3))
        return self.results


def run_security_audit(scanners):
    """Поліморфна функція - працює з будь-яким сканером"""
    print("=== Приклад 2: Поліморфізм сканерів ===\n")
    print("🔍 Starting Security Audit...\n")
    
    for scanner in scanners:
        findings = scanner.scan()
        print(f"✓ {scanner.__class__.__name__}")
        print(f"  {scanner.report()}")
        if findings:
            for finding in findings:
                print(f"  - {finding}")
        print()


if __name__ == "__main__":
    target = "192.168.1.100"
    scanners = [
        PortScanner(target),
        VulnerabilityScanner(target)
    ]
    
    run_security_audit(scanners)




# ============================================================
# ПРИКЛАД 3: Магічні методи - IP-адреса
# ============================================================

class IPAddress:
    """Клас для роботи з IPv4 адресами з магічними методами"""
    
    def __init__(self, ip_string):
        parts = ip_string.split('.')
        if len(parts) != 4:
            raise ValueError("Invalid IP address format")
        
        self.octets = [int(octet) for octet in parts]
        
        for octet in self.octets:
            if not 0 <= octet <= 255:
                raise ValueError(f"Octet {octet} out of range")
    
    def __str__(self):
        """Для print() - зручний вигляд"""
        return '.'.join(map(str, self.octets))
    
    def __repr__(self):
        """Для розробників"""
        return f"IPAddress('{self}')"
    
    def __eq__(self, other):
        """Оператор =="""
        if not isinstance(other, IPAddress):
            return False
        return self.octets == other.octets
    
    def __lt__(self, other):
        """Оператор <"""
        if not isinstance(other, IPAddress):
            return NotImplemented
        return self.octets < other.octets
    
    def __hash__(self):
        """Для використання в set та dict"""
        return hash(tuple(self.octets))
    
    def __int__(self):
        """Конвертація в число"""
        return (self.octets[0] << 24) + (self.octets[1] << 16) + \
               (self.octets[2] << 8) + self.octets[3]
    
    def __add__(self, value):
        """Додавання числа до IP"""
        if not isinstance(value, int):
            return NotImplemented
        
        new_value = int(self) + value
        if new_value > 0xFFFFFFFF:
            raise ValueError("IP address overflow")
        
        return IPAddress(f"{(new_value >> 24) & 0xFF}."
                        f"{(new_value >> 16) & 0xFF}."
                        f"{(new_value >> 8) & 0xFF}."
                        f"{new_value & 0xFF}")
    
    def is_private(self):
        """Перевірка приватної IP (RFC 1918)"""
        first = self.octets[0]
        second = self.octets[1]
        
        return (first == 10 or
                (first == 172 and 16 <= second <= 31) or
                (first == 192 and second == 168))


# if __name__ == "__main__":
#     print("=== Приклад 3: Магічні методи IP ===\n")
#
#     ip1 = IPAddress("192.168.1.1")
#     ip2 = IPAddress("192.168.1.100")
#     ip3 = IPAddress("192.168.1.1")
#
#     print(f"ip1: {ip1}")  # __str__
#     print(f"repr: {repr(ip1)}")  # __repr__
#     print(f"ip1 == ip3: {ip1 == ip3}")  # __eq__
#     print(f"ip1 < ip2: {ip1 < ip2}")  # __lt__
#
#     # Використання в set
#     ip_set = {ip1, ip2, ip3}
#     print(f"Unique IPs in set: {len(ip_set)}")  # __hash__
#
#     # Математичні операції
#     next_ip = ip1 + 10
#     print(f"ip1 + 10 = {next_ip}")  # __add__
#
#     print(f"Is private: {ip1.is_private()}")
#     print()
#
#
# # ============================================================
# # ПРИКЛАД 4: Контейнерні магічні методи - Security Log
# # ============================================================
#
# class SecurityLog:
#     """Колекція подій з підтримкою індексації та ітерації"""
#
#     def __init__(self):
#         self._events = []
#
#     def add_event(self, event):
#         self._events.append(event)
#
#     def __len__(self):
#         """len(log)"""
#         return len(self._events)
#
#     def __getitem__(self, index):
#         self.shift = -self.shift
#         result = self.encrypt(ciphertext)
#         self.shift = original_shift
#         return result


# ============================================================
# ПРИКЛАД 6: XOR шифрування
# ============================================================

import base64

class XORCipher:
    """XOR шифрування - симетричний шифр"""
    
    def __init__(self, key):
        self.key = key.encode()
    
    def _xor_bytes(self, data):
        return bytes([
            data[i] ^ self.key[i % len(self.key)]
            for i in range(len(data))
        ])
    
    def encrypt(self, plaintext):
        data = plaintext.encode('utf-8')
        encrypted = self._xor_bytes(data)
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, ciphertext):
        encrypted = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted = self._xor_bytes(encrypted)
        return decrypted.decode('utf-8')


# if __name__ == "__main__":
#     print("=== Приклад 5-6: Криптографія ===\n")
#     #
#     # # Тест Шифру Цезаря
#     # print("--- Caesar Cipher ---")
#     # caesar = CaesarCipher(shift=13)
#     # message = "HELLO WORLD"
#     # encrypted = caesar.encrypt(message)
#     # decrypted = caesar.decrypt(encrypted)
#     #
#     print(f"Original:  {message}")
#     print(f"Encrypted: {encrypted}")
#     print(f"Decrypted: {decrypted}")
#     print()
#
#     # Тест XOR
#     print("--- XOR Cipher ---")
#     xor = XORCipher("SecretKey2025")
#     secret = "Password123!"
#     encrypted_xor = xor.encrypt(secret)
#     decrypted_xor = xor.decrypt(encrypted_xor)
#
#     print(f"Original:  {secret}")
#     print(f"Encrypted: {encrypted_xor}")
#     print(f"Decrypted: {decrypted_xor}")
#     print()


# ============================================================
# ПРИКЛАД 7: Менеджер паролів з хешуванням
# ============================================================

import hashlib
import secrets
import string

class PasswordManager:
    """Менеджер паролів з безпечним хешуванням"""
    
    def __init__(self):
        self._passwords = {}  # username: (salt, hashed_password)
    
    def _generate_salt(self):
        return secrets.token_hex(16)
    
    def _hash_password(self, password, salt):
        salted = (password + salt).encode('utf-8')
        return hashlib.sha256(salted).hexdigest()
    
    def register_user(self, username, password):
        if username in self._passwords:
            raise ValueError(f"User {username} already exists!")
        
        if not self._validate_password(password):
            raise ValueError("Password doesn't meet security requirements!")
        
        salt = self._generate_salt()
        hashed = self._hash_password(password, salt)
        self._passwords[username] = (salt, hashed)
        print(f"✅ User '{username}' registered successfully!")
    
    def verify_login(self, username, password):
        if username not in self._passwords:
            print(f"❌ User '{username}' not found!")
            return False
        
        salt, stored_hash = self._passwords[username]
        password_hash = self._hash_password(password, salt)
        
        if password_hash == stored_hash:
            print(f"✅ Login successful for '{username}'!")
            return True
        else:
            print(f"❌ Invalid password for '{username}'!")
            return False
    
    def _validate_password(self, password):
        if len(password) < 8:
            print("❌ Password must be at least 8 characters")
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            print("❌ Password must contain: uppercase, lowercase, digit, special char")
            return False
        
        return True
    
    def generate_secure_password(self, length=16):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def __len__(self):
        return len(self._passwords)
    
    def __contains__(self, username):
        return username in self._passwords


if __name__ == "__main__":
    print("=== Приклад 7: Менеджер паролів ===\n")
    
    pm = PasswordManager()
    
    # Спроба зі слабким паролем
    try:
        pm.register_user("john", "weak")
    except ValueError as e:
        print(f"Error: {e}\n")
    
    # Реєстрація з сильними паролями
    pm.register_user("alice", "SecureP@ss123")
    pm.register_user("bob", "MyStr0ng!Pass")
    
    # Генерація безпечного пароля
    secure_pass = pm.generate_secure_password()
    print(f"\n🔐 Generated password: {secure_pass}")
    pm.register_user("charlie", secure_pass)
    
    # Спроби логіну
    print("\n--- Login Attempts ---")
    pm.verify_login("alice", "SecureP@ss123")
    pm.verify_login("alice", "WrongPassword")
    pm.verify_login("unknown", "test")
    
    print(f"\nTotal users: {len(pm)}")
    print(f"Is 'alice' registered: {'alice' in pm}")
    print()


# ============================================================
# ПРИКЛАД 8: Комплексна система з усіма концепціями
# ============================================================

class NetworkMonitor:
    """Система моніторингу мережі з усіма концепціями ООП"""
    
    def __init__(self, network_name):
        self.network_name = network_name
        self.events = SecurityLog()
        self.blocked_ips = set()
    
    def process_event(self, event: SecurityEvent):
        """Обробка події безпеки"""
        self.events.add_event(event)
        
        if event.is_suspicious():
            self._handle_suspicious_event(event)
    
    def _handle_suspicious_event(self, event):
        """Обробка підозрілих подій"""
        print(f"⚠️  ALERT: {event.log()}")
        
        if event.severity == "CRITICAL":
            self.blocked_ips.add(event.source_ip)
            print(f"🚫 Blocked IP: {event.source_ip}")
    
    def generate_report(self):
        """Генерація звіту"""
        total = len(self.events)
        suspicious = sum(1 for e in self.events if e.is_suspicious())
        
        print(f"\n{'='*60}")
        print(f"Security Report for {self.network_name}")
        print(f"{'='*60}")
        print(f"Total events: {total}")
        print(f"Suspicious events: {suspicious}")
        print(f"Blocked IPs: {len(self.blocked_ips)}")
        if self.blocked_ips:
            print(f"  {', '.join(self.blocked_ips)}")
        print(f"{'='*60}\n")
    
    def __repr__(self):
        return f"NetworkMonitor('{self.network_name}', {len(self.events)} events)"


if __name__ == "__main__":
    print("=== Приклад 8: Комплексна система ===\n")
    
    # Створення системи моніторингу
    monitor = NetworkMonitor("Corporate Network")
    
    # Симуляція подій
    events = [
        LoginAttempt("2025-10-02 10:00:00", "192.168.1.50", "user1", True),
        LoginAttempt("2025-10-02 10:05:00", "203.0.113.45", "admin", False),
        BruteForceAttack("2025-10-02 10:10:00", "203.0.113.45", "admin", 15),
        LoginAttempt("2025-10-02 10:15:00", "192.168.1.100", "user2", True),
        BruteForceAttack("2025-10-02 10:20:00", "198.51.100.10", "root", 25),
    ]
    
    for event in events:
        monitor.process_event(event)
    
    # Генерація звіту
    monitor.generate_report()
    
    print(monitor)


# ============================================================
# ГОЛОВНА ФУНКЦІЯ ДЛЯ ЗАПУСКУ ВСІХ ПРИКЛАДІВ
# ============================================================

def main():
    """Запуск всіх прикладів по черзі"""
    print("\n" + "="*60)
    print("PYTHON ДЛЯ КІБЕРБЕЗПЕКИ: ООП, НАСЛІДУВАННЯ ТА КРИПТОГРАФІЯ")
    print("="*60 + "\n")
    
    examples = [
        "Приклад 1: Система логування подій",
        "Приклад 2: Поліморфізм сканерів",
        "Приклад 3: Магічні методи IP",
        "Приклад 4: Контейнерні методи",
        "Приклад 5-6: Криптографія",
        "Приклад 7: Менеджер паролів",
        "Приклад 8: Комплексна система"
    ]
    
    print("Доступні приклади:")
    for i, example in enumerate(examples, 1):
        print(f"  {i}. {example}")
    
    print("\nВсі приклади виконано автоматично вище!")
    print("\nДля окремого запуску, викоментуйте потрібний розділ коду.")
    

if __name__ == "__main__":
    main()
