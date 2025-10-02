# Заняття 3/4: ООП - Наслідування, Поліморфізм та Магічні Методи

## 📚 Зміст заняття

1. [Наслідування класів](#1-наслідування-класів)
2. [Метод super() та перевизначення методів](#2-метод-super-та-перевизначення-методів)
3. [Поліморфізм](#3-поліморфізм)
4. [Магічні методи (Dunder Methods)](#4-магічні-методи-dunder-methods)
5. [Практика: Криптографія та шифрування](#5-практика-криптографія-та-шифрування)

> 💡 **Додатково:** Детальне пояснення абстрактних класів (ABC) та @abstractmethod дивіться у файлі `lesson-3-4-abc-explanation.md`

---

## 1. Наслідування класів

### Що таке наслідування?

**Наслідування** (Inheritance) — механізм, що дозволяє створювати новий клас на основі існуючого, успадковуючи його атрибути та методи.

### Навіщо потрібне наслідування?

- ♻️ **Повторне використання коду** — не потрібно дублювати код
- 📊 **Ієрархія класів** — логічна організація системи
- 🔧 **Розширюваність** — легко додавати нову функціональність

### Синтаксис наслідування

```python
class БазовийКлас:
    # Код батьківського класу
    pass

class ПохіднийКлас(БазовийКлас):
    # Код дочірнього класу
    # Успадковує всі методи та атрибути БазовийКлас
    pass
```

### 🔒 Приклад 1: Базова система логування подій безпеки

```python
class SecurityEvent:
    """Базовий клас для всіх подій безпеки"""
    
    def __init__(self, timestamp, source_ip, description):
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.description = description
        self.severity = "INFO"
    
    def log(self):
        """Базовий метод для виведення інформації про подію"""
        return f"[{self.severity}] {self.timestamp} | {self.source_ip} | {self.description}"


class LoginAttempt(SecurityEvent):
    """Клас для відстеження спроб входу в систему"""
    
    def __init__(self, timestamp, source_ip, username, success):
        # Виклик конструктора батьківського класу
        super().__init__(timestamp, source_ip, f"Login attempt by {username}")
        self.username = username
        self.success = success
        self.severity = "INFO" if success else "WARNING"


class MalwareDetection(SecurityEvent):
    """Клас для відстеження виявлення зловмисного ПЗ"""
    
    def __init__(self, timestamp, source_ip, malware_type, file_path):
        super().__init__(timestamp, source_ip, f"Malware detected: {malware_type}")
        self.malware_type = malware_type
        self.file_path = file_path
        self.severity = "CRITICAL"


# Використання
login_event = LoginAttempt("2025-10-02 14:30:00", "192.168.1.100", "admin", False)
print(login_event.log())
# Вивід: [WARNING] 2025-10-02 14:30:00 | 192.168.1.100 | Login attempt by admin

malware_event = MalwareDetection("2025-10-02 14:35:00", "192.168.1.50", "Trojan", "/tmp/suspicious.exe")
print(malware_event.log())
# Вивід: [CRITICAL] 2025-10-02 14:35:00 | 192.168.1.50 | Malware detected: Trojan
```

**Переваги цього підходу:**
- ✅ Уся спільна логіка (`timestamp`, `source_ip`, `log()`) в одному місці
- ✅ Легко додавати нові типи подій (просто наслідуємо `SecurityEvent`)
- ✅ Зміни в базовому класі автоматично поширюються на всі дочірні класи

---

## 2. Метод super() та перевизначення методів

### Що таке super()?

`super()` — вбудована функція Python, що дає доступ до методів батьківського класу. Це необхідно для:
- Виклику конструктора батьківського класу
- Розширення функціональності батьківських методів
- Коректної роботи множинного наслідування

### Перевизначення методів (Method Overriding)

Дочірній клас може **перевизначити** (override) метод батьківського класу, створивши метод з тією самою назвою.

### 🔒 Приклад 2: Розширена система логування з фільтрацією

```python
class SecurityEvent:
    """Базовий клас з функцією фільтрації"""
    
    def __init__(self, timestamp, source_ip, description):
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.description = description
        self.severity = "INFO"
    
    def log(self):
        return f"[{self.severity}] {self.timestamp} | {self.source_ip} | {self.description}"
    
    def is_suspicious(self):
        """Базова перевірка на підозрілість"""
        return self.severity in ["WARNING", "CRITICAL"]


class BruteForceAttack(SecurityEvent):
    """Клас для відстеження атак bruteforce"""
    
    def __init__(self, timestamp, source_ip, target_username, attempts):
        super().__init__(timestamp, source_ip, f"Bruteforce attack on {target_username}")
        self.target_username = target_username
        self.attempts = attempts
        self.severity = "CRITICAL" if attempts > 10 else "WARNING"
    
    def log(self):
        """ПЕРЕВИЗНАЧЕНИЙ метод log() з додатковою інформацією"""
        # Викликаємо батьківський метод через super()
        base_log = super().log()
        # Додаємо специфічну інформацію
        return f"{base_log} | Attempts: {self.attempts}"
    
    def is_suspicious(self):
        """ПЕРЕВИЗНАЧЕНИЙ метод перевірки"""
        # Розширюємо логіку батьківського методу
        if super().is_suspicious():
            return True
        # Додаємо власні правила
        return self.attempts > 5


# Використання
attack = BruteForceAttack("2025-10-02 15:00:00", "203.0.113.45", "root", 15)
print(attack.log())
# Вивід: [CRITICAL] 2025-10-02 15:00:00 | 203.0.113.45 | Bruteforce attack on root | Attempts: 15

print(f"Suspicious: {attack.is_suspicious()}")  # Вивід: Suspicious: True
```

**Коли використовувати super():**
- ✅ У конструкторі `__init__()` для виклику батьківського конструктора
- ✅ Коли потрібно розширити, а не повністю замінити батьківський метод
- ✅ При множинному наслідуванні для коректного порядку виклику методів

---

## 3. Поліморфізм

### Що таке поліморфізм?

**Поліморфізм** (від грец. "πολύς" — багато, "μορφή" — форма) — здатність об'єктів різних класів оброблятися через єдиний інтерфейс.

### Типи поліморфізму в Python:

1. **Поліморфізм методів** — різні класи мають методи з однаковими назвами
2. **Поліморфізм операторів** — оператори працюють з різними типами даних
3. **Duck Typing** — "якщо щось виглядає як качка і крякає як качка, то це качка"

### 🔒 Приклад 3: Поліморфізм в системі сканування безпеки

```python
from abc import ABC, abstractmethod

class SecurityScanner(ABC):
    """Абстрактний базовий клас для всіх сканерів"""
    
    def __init__(self, target):
        self.target = target
        self.results = []
    
    @abstractmethod
    def scan(self):
        """Кожен сканер повинен реалізувати метод scan()"""
        pass
    
    def report(self):
        """Загальний метод для звітів"""
        return f"Scan results for {self.target}: {len(self.results)} findings"


class PortScanner(SecurityScanner):
    """Сканер відкритих портів"""
    
    def scan(self):
        """Симулюємо сканування портів"""
        common_ports = [21, 22, 80, 443, 3306, 8080]
        import random
        self.results = [port for port in common_ports if random.choice([True, False])]
        return self.results


class VulnerabilityScanner(SecurityScanner):
    """Сканер вразливостей"""
    
    def scan(self):
        """Симулюємо пошук вразливостей"""
        vulnerabilities = [
            "CVE-2024-1234: SQL Injection",
            "CVE-2024-5678: XSS Vulnerability",
            "CVE-2024-9012: Outdated SSL/TLS"
        ]
        import random
        self.results = random.sample(vulnerabilities, k=random.randint(0, 3))
        return self.results


class MalwareScanner(SecurityScanner):
    """Антивірусний сканер"""
    
    def scan(self):
        """Симулюємо пошук зловмисного ПЗ"""
        threats = ["Trojan.Win32", "Backdoor.Linux", "Ransomware.Generic"]
        import random
        self.results = [threat for threat in threats if random.choice([True, False])]
        return self.results


# ПОЛІМОРФІЗМ В ДІЇ
def run_security_audit(scanners):
    """
    Функція приймає список різних сканерів
    і викликає їхні методи scan() та report()
    """
    print("🔍 Starting Security Audit...\n")
    
    for scanner in scanners:
        # Незалежно від типу сканера, викликаємо scan()
        findings = scanner.scan()
        print(f"✓ {scanner.__class__.__name__}")
        print(f"  {scanner.report()}")
        if findings:
            for finding in findings:
                print(f"  - {finding}")
        print()


# Використання
target_system = "192.168.1.100"
scanners = [
    PortScanner(target_system),
    VulnerabilityScanner(target_system),
    MalwareScanner(target_system)
]

run_security_audit(scanners)

# Приклад виводу:
# 🔍 Starting Security Audit...
# 
# ✓ PortScanner
#   Scan results for 192.168.1.100: 3 findings
#   - 22
#   - 80
#   - 443
# 
# ✓ VulnerabilityScanner
#   Scan results for 192.168.1.100: 2 findings
#   - CVE-2024-1234: SQL Injection
#   - CVE-2024-9012: Outdated SSL/TLS
# 
# ✓ MalwareScanner
#   Scan results for 192.168.1.100: 1 findings
#   - Trojan.Win32
```

**Ключова ідея поліморфізму:**
- Функція `run_security_audit()` не знає, який конкретно тип сканера вона обробляє
- Всі сканери мають метод `scan()` — це і є поліморфізм
- Легко додати новий тип сканера без зміни `run_security_audit()`

---

## 4. Магічні методи (Dunder Methods)


### Що таке магічні методи?

**Магічні методи** (або dunder methods від "double underscore") — спеціальні методи в Python, що починаються і закінчуються двома підкресленнями `__method__`.

Вони дозволяють вашим класам працювати з вбудованими операторами та функціями Python.

### Категорії магічних методів:

| Категорія | Методи | Призначення |
|-----------|---------|-------------|
| **Ініціалізація** | `__init__`, `__new__`, `__del__` | Створення та знищення об'єктів |
| **Представлення** | `__str__`, `__repr__` | Текстове представлення об'єкта |
| **Порівняння** | `__eq__`, `__lt__`, `__gt__`, `__le__`, `__ge__`, `__ne__` | Оператори порівняння |
| **Арифметика** | `__add__`, `__sub__`, `__mul__`, `__truediv__` | Математичні операції |
| **Контейнери** | `__len__`, `__getitem__`, `__setitem__`, `__contains__` | Поведінка як колекція |
| **Контекст** | `__enter__`, `__exit__` | Контекстні менеджери (with) |

### 🔒 Приклад 4: Клас для IP-адрес з магічними методами

```python
class IPAddress:
    """Клас для роботи з IPv4 адресами"""
    
    def __init__(self, ip_string):
        """Ініціалізація об'єкта IP-адреси"""
        parts = ip_string.split('.')
        if len(parts) != 4:
            raise ValueError("Invalid IP address format")
        
        self.octets = [int(octet) for octet in parts]
        
        # Валідація діапазону
        for octet in self.octets:
            if not 0 <= octet <= 255:
                raise ValueError(f"Octet {octet} out of range (0-255)")
    
    def __str__(self):
        """Для print() та str() — зручний вигляд для користувача"""
        return '.'.join(map(str, self.octets))
    
    def __repr__(self):
        """Для розробників — показує, як створити об'єкт"""
        return f"IPAddress('{self}')"
    
    def __eq__(self, other):
        """Оператор == для порівняння IP-адрес"""
        if not isinstance(other, IPAddress):
            return False
        return self.octets == other.octets
    
    def __lt__(self, other):
        """Оператор < для порівняння IP-адрес"""
        if not isinstance(other, IPAddress):
            return NotImplemented
        return self.octets < other.octets
    
    def __hash__(self):
        """Дозволяє використовувати IP в множинах та як ключ в словниках"""
        return hash(tuple(self.octets))
    
    def __int__(self):
        """Конвертація IP в число (для підсумовування)"""
        return (self.octets[0] << 24) + (self.octets[1] << 16) + \
               (self.octets[2] << 8) + self.octets[3]
    
    def __add__(self, value):
        """Додавання числа до IP-адреси (інкремент)"""
        if not isinstance(value, int):
            return NotImplemented
        
        new_value = int(self) + value
        if new_value > 0xFFFFFFFF:  # Максимальна IPv4 адреса
            raise ValueError("IP address overflow")
        
        # Конвертуємо назад в октети
        return IPAddress(f"{(new_value >> 24) & 0xFF}."
                        f"{(new_value >> 16) & 0xFF}."
                        f"{(new_value >> 8) & 0xFF}."
                        f"{new_value & 0xFF}")
    
    def is_private(self):
        """Перевірка чи IP приватна (RFC 1918)"""
        first_octet = self.octets[0]
        second_octet = self.octets[1]
        
        return (first_octet == 10 or
                (first_octet == 172 and 16 <= second_octet <= 31) or
                (first_octet == 192 and second_octet == 168))


# Використання магічних методів
ip1 = IPAddress("192.168.1.1")
ip2 = IPAddress("192.168.1.100")
ip3 = IPAddress("192.168.1.1")

print(ip1)  # __str__: 192.168.1.1
print(repr(ip1))  # __repr__: IPAddress('192.168.1.1')

print(ip1 == ip3)  # __eq__: True
print(ip1 == ip2)  # __eq__: False

print(ip1 < ip2)  # __lt__: True

# Використання в множинах завдяки __hash__
ip_set = {ip1, ip2, ip3}
print(len(ip_set))  # 2 (ip1 і ip3 однакові)

# Математичні операції
next_ip = ip1 + 1  # __add__
print(next_ip)  # 192.168.1.2

print(f"Is private: {ip1.is_private()}")  # True
```

### 🔒 Приклад 5: Клас для логів з контейнерними методами

```python
class SecurityLog:
    """Колекція подій безпеки з можливістю індексації та ітерації"""
    
    def __init__(self):
        self._events = []
    
    def add_event(self, event):
        """Додавання події до логу"""
        self._events.append(event)
    
    def __len__(self):
        """Дозволяє використовувати len(log)"""
        return len(self._events)
    
    def __getitem__(self, index):
        """Дозволяє індексацію: log[0], log[-1], log[1:3]"""
        return self._events[index]
    
    def __iter__(self):
        """Дозволяє ітерацію: for event in log"""
        return iter(self._events)
    
    def __contains__(self, item):
        """Дозволяє оператор 'in': if event in log"""
        return item in self._events
    
    def __repr__(self):
        return f"SecurityLog({len(self)} events)"


# Використання
log = SecurityLog()
log.add_event("Login attempt from 192.168.1.50")
log.add_event("Port scan detected on port 22")
log.add_event("Malware signature found")

print(len(log))  # __len__: 3
print(log[0])  # __getitem__: Login attempt from 192.168.1.50
print(log[-1])  # __getitem__: Malware signature found

# Ітерація
for event in log:  # __iter__
    print(f"- {event}")

# Перевірка наявності
if "Port scan detected on port 22" in log:  # __contains__
    print("⚠️  Port scan found in logs!")
```

### 🔒 Приклад 6: Контекстний менеджер для безпечної роботи з файлами

```python
class SecureFileHandler:
    """Контекстний менеджер для безпечної роботи з конфіденційними файлами"""
    
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None
        self.access_log = []
    
    def __enter__(self):
        """Викликається при вході в блок with"""
        print(f"🔓 Opening secure file: {self.filename}")
        self.file = open(self.filename, self.mode)
        self.access_log.append(f"File opened at {self._get_timestamp()}")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Викликається при виході з блоку with (навіть при помилці)"""
        if self.file:
            self.file.close()
            print(f"🔒 Closed secure file: {self.filename}")
            self.access_log.append(f"File closed at {self._get_timestamp()}")
        
        # Якщо була помилка, логуємо її
        if exc_type is not None:
            self.access_log.append(f"Error: {exc_type.__name__}: {exc_val}")
            print(f"⚠️  Error occurred: {exc_val}")
        
        # Зберігаємо лог доступу
        self._save_audit_log()
        
        # False = пробрасываємо виключення далі
        # True = поглинаємо виключення
        return False
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _save_audit_log(self):
        """Збереження логу аудиту доступу до файлу"""
        audit_filename = f"{self.filename}.audit"
        with open(audit_filename, 'a') as audit:
            for log_entry in self.access_log:
                audit.write(f"{log_entry}\n")


# Використання контекстного менеджера
try:
    with SecureFileHandler('sensitive_data.txt', 'w') as f:
        f.write("Top Secret Information\n")
        f.write("Encryption Key: ABC123XYZ\n")
ування та розшифрування
- Швидке, ефективне
- Проблема: як безпечно передати ключ?
- Приклади: AES, DES, ChaCha20

#### 2. **Асиметричне шифрування** (Asymmetric Encryption)
- Два ключі: публічний (для шифрування) та приватний (для розшифрування)
- Повільніше, але безпечніше для обміну ключами
- Приклади: RSA, ECC, ElGamal

### 🔒 Приклад 7: Система шифрування з ООП

```python
from abc import ABC, abstractmethod
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


class Encryptor(ABC):
    """Абстрактний базовий клас для шифрування"""
    
    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """Шифрування тексту"""
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """Розшифрування тексту"""
        pass


class CaesarCipher(Encryptor):
    """Шифр Цезаря - простий підстановочний шифр (НЕ безпечний!)"""
    
    def __init__(self, shift: int = 3):
        self.shift = shift
    
    def encrypt(self, plaintext: str) -> str:
        """Зсув кожної літери на shift позицій"""
        result = []
        for char in plaintext:
            if char.isalpha():
                # Визначаємо базу (A або a)
                base = ord('A') if char.isupper() else ord('a')
                # Зсуваємо літеру
                shifted = (ord(char) - base + self.shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        """Зворотний зсув для розшифрування"""
        # Просто шифруємо з негативним зсувом
        original_shift = self.shift
        self.shift = -self.shift
        result = self.encrypt(ciphertext)
        self.shift = original_shift
        return result
    
    def __str__(self):
        return f"CaesarCipher(shift={self.shift})"


class XORCipher(Encryptor):
    """XOR шифрування - кожен байт XOR з ключем"""
    
    def __init__(self, key: str):
        self.key = key.encode()
    
    def _xor_bytes(self, data: bytes) -> bytes:
        """XOR операція між даними та ключем"""
        return bytes([
            data[i] ^ self.key[i % len(self.key)]
            for i in range(len(data))
        ])
    
    def encrypt(self, plaintext: str) -> str:
        """Шифрування через XOR"""
        data = plaintext.encode('utf-8')
        encrypted = self._xor_bytes(data)
        # Кодуємо в base64 для зручності передачі
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        """Розшифрування через XOR (та сама операція!)"""
        encrypted = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted = self._xor_bytes(encrypted)
        return decrypted.decode('utf-8')
    
    def __str__(self):
        return f"XORCipher(key_length={len(self.key)})"


class FernetEncryptor(Encryptor):
    """Безпечне симетричне шифрування з бібліотеки cryptography"""
    
    def __init__(self, password: str):
        """Генерація ключа з пароля через KDF"""
        # Використовуємо PBKDF2 для створення сильного ключа з пароля
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'static_salt_change_me',  # В продакшені використовувати випадковий salt!
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """Безпечне шифрування"""
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Безпечне розшифрування"""
        return self.cipher.decrypt(ciphertext.encode()).decode()
    
    def __str__(self):
        return "FernetEncryptor(AES-128 in CBC mode)"


# Демонстрація поліморфізму через єдиний інтерфейс
def test_encryptor(encryptor: Encryptor, message: str):
    """Тестування будь-якого шифровальника"""
    print(f"\n{'='*60}")
    print(f"Testing: {encryptor}")
    print(f"{'='*60}")
    
    print(f"Original:  {message}")
    
    # Шифрування
    encrypted = encryptor.encrypt(message)
    print(f"Encrypted: {encrypted}")
    
    # Розшифрування
    decrypted = encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Перевірка
    if message == decrypted:
        print("✅ Success: Message decrypted correctly!")
    else:
        print("❌ Error: Decryption failed!")


# Використання різних шифрів через єдиний інтерфейс
secret_message = "Password123! - Top Secret Credentials"

# Тестуємо всі шифри
ciphers = [
    CaesarCipher(shift=13),
    XORCipher(key="MySecretKey2025"),
    # FernetEncryptor(password="StrongPassword123!")  # Потрібна бібліотека cryptography
]

for cipher in ciphers:
    test_encryptor(cipher, secret_message)

# Приклад виводу:
# ============================================================
# Testing: CaesarCipher(shift=13)
# ============================================================
# Original:  Password123! - Top Secret Credentials
# Encrypted: Cnffjbeq123! - Gbc Frperg Perqragvnyf
# Decrypted: Password123! - Top Secret Credentials
# ✅ Success: Message decrypted correctly!
```

### 🔒 Приклад 8: Практична система для паролів з хешуванням

```python
import hashlib
import secrets
import string


class PasswordManager:
    """Менеджер паролів з хешуванням та валідацією"""
    
    def __init__(self):
        self._passwords = {}  # username: (salt, hashed_password)
    
    def _generate_salt(self) -> str:
        """Генерація випадкової солі"""
        return secrets.token_hex(16)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Хешування пароля з сіллю"""
        # Комбінуємо пароль та сіль
        salted = (password + salt).encode('utf-8')
        # Хешуємо через SHA-256
        return hashlib.sha256(salted).hexdigest()
    
    def register_user(self, username: str, password: str):
        """Реєстрація нового користувача"""
        if username in self._passwords:
            raise ValueError(f"User {username} already exists!")
        
        # Валідація пароля
        if not self._validate_password(password):
            raise ValueError("Password doesn't meet security requirements!")
        
        # Генерація солі та хешування
        salt = self._generate_salt()
        hashed = self._hash_password(password, salt)
        
        self._passwords[username] = (salt, hashed)
        print(f"✅ User '{username}' registered successfully!")
    
    def verify_login(self, username: str, password: str) -> bool:
        """Перевірка логіну користувача"""
        if username not in self._passwords:
            print(f"❌ User '{username}' not found!")
            return False
        
        # Отримуємо збережену сіль та хеш
        salt, stored_hash = self._passwords[username]
        
        # Хешуємо введений пароль з тією ж сіллю
        password_hash = self._hash_password(password, salt)
        
        # Порівнюємо хеші
        if password_hash == stored_hash:
            print(f"✅ Login successful for '{username}'!")
            return True
        else:
            print(f"❌ Invalid password for '{username}'!")
            return False
    
    def _validate_password(self, password: str) -> bool:
        """Валідація надійності пароля"""
        if len(password) < 8:
            print("❌ Password must be at least 8 characters")
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            print("❌ Password must contain: uppercase, lowercase, digit, and special character")
            return False
        
        return True
    
    def generate_secure_password(self, length: int = 16) -> str:
        """Генерація безпечного випадкового пароля"""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def __len__(self):
        """Кількість зареєстрованих користувачів"""
        return len(self._passwords)
    
    def __contains__(self, username):
        """Перевірка чи користувач існує"""
        return username in self._passwords
    
    def __repr__(self):
        return f"PasswordManager({len(self)} users registered)"


# Використання
pm = PasswordManager()

# Спроба зареєструватися зі слабким паролем
try:
    pm.register_user("john", "weak")
except ValueError as e:
    print(f"Error: {e}")

# Реєстрація з сильним паролем
pm.register_user("alice", "SecureP@ss123")
pm.register_user("bob", "MyStr0ng!Pass")

# Генерація безпечного пароля
secure_pass = pm.generate_secure_password()
print(f"\n🔐 Generated secure password: {secure_pass}")
pm.register_user("charlie", secure_pass)

# Спроби логіну
print("\n--- Login Attempts ---")
pm.verify_login("alice", "SecureP@ss123")  # ✅ Success
pm.verify_login("alice", "WrongPassword")  # ❌ Failed
pm.verify_login("unknown", "test")  # ❌ User not found

# Використання магічних методів
print(f"\nTotal users: {len(pm)}")  # __len__
print(f"Is 'alice' registered: {'alice' in pm}")  # __contains__
print(pm)  # __repr__
```

---

## 📝 Підсумок та ключові концепції


### 1. **Наслідування (Inheritance)**
```python
class Parent:
    def method(self):
        return "Parent method"

class Child(Parent):  # Child наслідує Parent
    pass

child = Child()
child.method()  # Працює! Успадковано від Parent
```

**Коли використовувати:**
- Є спільна функціональність між класами
- Потрібна ієрархія "це є різновид того"
- Приклад: `LoginAttempt` є різновидом `SecurityEvent`

### 2. **Метод super()**
```python
class Child(Parent):
    def __init__(self, value):
        super().__init__()  # Виклик конструктора Parent
        self.value = value
```

**Правила використання:**
- ✅ Завжди викликай `super().__init__()` в конструкторі дочірнього класу
- ✅ Використовуй `super().method()` для розширення батьківського методу
- ❌ Не дублюй код батьківського класу

### 3. **Поліморфізм (Polymorphism)**
```python
def process(scanner):  # Не важливо, який тип scanner
    scanner.scan()  # Головне, що є метод scan()
```

**Переваги:**
- 🔄 Один інтерфейс для різних типів
- 🔧 Легко додавати нові типи без зміни існуючого коду
- 📦 Код стає більш гнучким та розширюваним

### 4. **Магічні методи**

| Метод | Оператор/Функція | Призначення |
|-------|------------------|-------------|
| `__init__` | `obj = Class()` | Ініціалізація |
| `__str__` | `str(obj)`, `print(obj)` | Зручний вигляд |
| `__repr__` | `repr(obj)` | Технічне представлення |
| `__eq__` | `obj1 == obj2` | Порівняння на рівність |
| `__lt__` | `obj1 < obj2` | Порівняння менше |
| `__len__` | `len(obj)` | Довжина |
| `__getitem__` | `obj[key]` | Індексація |
| `__contains__` | `item in obj` | Перевірка наявності |
| `__add__` | `obj1 + obj2` | Додавання |
| `__enter__`, `__exit__` | `with obj:` | Контекстний менеджер |

### 5. **Криптографія**

**Термінологія:**
- **Encoding (Кодування)**: UTF-8, Base64 — зворотне перетворення формату
- **Hashing (Хешування)**: SHA-256, MD5 — необоротний "цифровий відбиток"
- **Encryption (Шифрування)**: AES, RSA — зворотне з ключем

**Принципи безпеки:**
- ✅ Завжди використовуй сіль (salt) для хешування паролів
- ✅ Ніколи не зберігай паролі у відкритому вигляді
- ✅ Використовуй перевірені бібліотеки (cryptography, bcrypt)
- ❌ Не створюй власні криптографічні алгоритми!

---

## 🎯 Практичні завдання

### Завдання 1: Система виявлення атак (⭐⭐)
Створіть ієрархію класів для різних типів мережевих атак:
- `NetworkAttack` (базовий клас)
- `DDoSAttack`, `SQLInjection`, `XSSAttack` (похідні класи)

Кожен клас повинен мати:
- Метод `detect()` для виявлення атаки
- Метод `severity_level()` для визначення рівня небезпеки
- Магічний метод `__str__` для опису атаки

### Завдання 2: Криптографічний калькулятор (⭐⭐⭐)
Створіть клас `CryptoTools` з методами:
- `hash_file(filename)` — обчислення хешу файлу (SHA-256)
- `encrypt_message(message, key)` — шифрування повідомлення
- `decrypt_message(ciphertext, key)` — розшифрування повідомлення
- `generate_key()` — генерація випадкового ключа

Використайте магічний метод `__call__` для виклику об'єкта як функції.

### Завдання 3: Аудит безпеки (⭐⭐⭐⭐)
Створіть систему аудиту з класами:
- `AuditLog` — контейнер для подій (реалізуйте `__len__`, `__getitem__`, `__iter__`)
- `AuditEvent` — базовий клас події
- `FileAccessEvent`, `NetworkEvent`, `AuthEvent` — типи подій


Додайте функцію для пошуку підозрілих подій за критеріями.

---

## 📚 Додаткові ресурси

### Рекомендовані бібліотеки для кібербезпеки:

1. **cryptography** — сучасна криптографія
   ```bash
   pip install cryptography
   ```

2. **hashlib** — вбудований модуль для хешування

3. **secrets** — генерація криптографічно безпечних випадкових чисел

4. **scapy** — маніпулювання мережевими пакетами

5. **paramiko** — SSH клієнт/сервер

### Корисні посилання:
- [Python ABC Documentation](https://docs.python.org/3/library/abc.html)
- [Cryptography.io](https://cryptography.io/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)

---

## ✅ Чеклист для самоперевірки

Після вивчення матеріалу ви повинні вміти:

- [ ] Створювати ієрархію класів через наслідування
- [ ] Використовувати `super()` для виклику методів батьківського класу
- [ ] Пояснити концепцію поліморфізму
- [ ] Реалізовувати абстрактні базові класи (ABC)
- [ ] Використовувати магічні методи (`__str__`, `__eq__`, `__len__` тощо)
- [ ] Створювати контекстні менеджери (`__enter__`, `__exit__`)
- [ ] Пояснити різницю між кодуванням, хешуванням та шифруванням
- [ ] Реалізувати базове шифрування/дешифрування
- [ ] Безпечно хешувати паролі з сіллю
- [ ] Застосовувати ООП для задач кібербезпеки

---

**Автор:** Курс "Крос-платформне програмування"  
**Дата:** Жовтень 2025  
**Заняття:** 3/4 — ООП, Наслідування та Поліморфізм
