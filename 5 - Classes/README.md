# Заняття 3.2: Створення та використання класів для кібербезпеки

## Цілі заняття
- Навчитися створювати практичні класи для задач кібербезпеки
- Освоїти декоратори `@property` та `@staticmethod`
- Розробити реальні приклади класів для SIEM систем та моніторингу безпеки
- Практикувати інкапсуляцію та валідацію даних

---

## Частина 1: Основи класів через призму безпеки (45 хв)

### 1.1 Атрибути класу vs екземпляра (15 хв)

Почнемо з простого класу для відстеження сповіщень безпеки:

```python
from datetime import datetime

class SecurityAlert:
    # Атрибути класу - спільні для всіх об'єктів
    total_alerts_created = 0
    severity_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    def __init__(self, ip, severity, alert_type):
        # Атрибути екземпляра - унікальні для кожного об'єкта
        self.ip = ip
        self.severity = severity
        self.alert_type = alert_type
        self.created_at = datetime.now()
        
        # Збільшуємо лічильник класу
        SecurityAlert.total_alerts_created += 1
    
    def get_info(self):
        return f"Alert #{SecurityAlert.total_alerts_created}: {self.alert_type} from {self.ip}"

# Демонстрація
alert1 = SecurityAlert("192.168.1.100", "HIGH", "MALWARE")
alert2 = SecurityAlert("10.0.0.5", "LOW", "PORT_SCAN")

print(f"Total alerts created: {SecurityAlert.total_alerts_created}")  # 2
print(alert1.get_info())  # Alert #2: MALWARE from 192.168.1.100
```

### 1.2 Методи екземпляра та валідація (15 хв)

Додаємо методи для обробки сповіщень:

```python
class SecurityAlert:
    total_alerts_created = 0
    
    def __init__(self, ip, severity, alert_type):
        if not self._validate_ip(ip):
            raise ValueError(f"Invalid IP address: {ip}")
        if severity not in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            raise ValueError(f"Invalid severity: {severity}")
            
        self.ip = ip
        self.severity = severity
        self.alert_type = alert_type
        self.created_at = datetime.now()
        self.processed = False
        SecurityAlert.total_alerts_created += 1
    
    def _validate_ip(self, ip):
        """Приватний метод для валідації IP"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False
    
    def mark_as_processed(self):
        """Метод екземпляра - працює з конкретним об'єктом"""
        self.processed = True
        print(f"Alert for {self.ip} marked as processed")
    
    def get_age_minutes(self):
        """Розрахунок віку сповіщення в хвилинах"""
        return (datetime.now() - self.created_at).total_seconds() / 60

# Тестування
try:
    alert = SecurityAlert("192.168.1.100", "HIGH", "MALWARE")
    alert.mark_as_processed()
    print(f"Alert age: {alert.get_age_minutes():.1f} minutes")
    
    # Це викличе помилку
    bad_alert = SecurityAlert("999.999.999.999", "HIGH", "MALWARE")
except ValueError as e:
    print(f"Error: {e}")
```

### 1.3 Статичні методи та методи класу (15 хв)

Розширюємо функціонал утилітарними методами:

```python
class SecurityAlert:
    total_alerts_created = 0
    severity_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    def __init__(self, ip, severity, alert_type):
        self.ip = ip
        self.severity = severity
        self.alert_type = alert_type
        self.created_at = datetime.now()
        SecurityAlert.total_alerts_created += 1
    
    @classmethod
    def get_statistics(cls):
        """Метод класу - повертає статистику"""
        return {
            'total_alerts': cls.total_alerts_created,
            'available_severities': cls.severity_levels
        }
    
    @classmethod
    def create_from_log_line(cls, log_line):
        """Альтернативний конструктор - створює об'єкт з рядка логу"""
        # Приклад: "192.168.1.1 HIGH MALWARE_DETECTED"
        parts = log_line.strip().split()
        if len(parts) >= 3:
            ip, severity, alert_type = parts[0], parts[1], ' '.join(parts[2:])
            return cls(ip, severity, alert_type)
        else:
            raise ValueError("Invalid log line format")
    
    @staticmethod
    def is_private_ip(ip):
        """Статичний метод - перевірка приватної IP"""
        try:
            parts = list(map(int, ip.split('.')))
            return (parts[0] == 10 or 
                    (parts[0] == 172 and 16 <= parts[1] <= 31) or
                    (parts[0] == 192 and parts[1] == 168))
        except:
            return False
    
    @staticmethod
    def calculate_risk_score(severity, is_internal=True):
        """Статичний метод - розрахунок ризику"""
        base_scores = {'LOW': 25, 'MEDIUM': 50, 'HIGH': 75, 'CRITICAL': 100}
        score = base_scores.get(severity, 0)
        # Зовнішні IP більш ризикові
        if not is_internal:
            score *= 1.5
        return min(100, score)

# Використання різних типів методів
print("Statistics:", SecurityAlert.get_statistics())

# Створення з логу
alert = SecurityAlert.create_from_log_line("10.0.0.5 HIGH MALWARE_DETECTED")
print(f"Created alert: {alert.ip}, {alert.severity}")

# Статичні методи
print(f"Is 192.168.1.1 private? {SecurityAlert.is_private_ip('192.168.1.1')}")
print(f"Risk score: {SecurityAlert.calculate_risk_score('HIGH', False)}")
```

---

## Частина 2: Інкапсуляція та Properties (45 хв)

### 2.1 Захищені атрибути та валідація (20 хв)

Створюємо клас користувача з належною інкапсуляцією:

```python
import hashlib

class SecureUser:
    def __init__(self, username, password):
        # 🔒 Захищені атрибути (конвенція Python)
        # Одне підкреслення (_) = "protected" - для внутрішнього використання
        # НЕ справжня приватність! Можна отримати як user._username
        self._username = None          # Захищений атрибут - ім'я користувача  
        self._failed_attempts = 0      # Захищений атрибут - кількість невдалих спроб
        self._locked = False           # Захищений атрибут - статус блокування
        
        # 🔐 "Приватні" атрибути (name mangling Python)
        # Два підкреслення (__) = "private" - Python змінює назву атрибута
        # Стає user._SecureUser__password_hash замість user.__password_hash
        self.__password_hash = None    # "Приватний" атрибут - хеш пароля
        self.__salt = "security_salt_2024"  # "Приватний" атрибут - сіль для хешування
        self.__max_attempts = 3        # "Приватна" константа - максимум спроб
        
        # Використовуємо методи для валідації при створенні
        self.set_username(username)
        self.set_password(password)
    
    def set_username(self, username):
        """Публічний метод - встановлення імені користувача з валідацією"""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not username.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Username can only contain letters, numbers, - and _")
        self._username = username
    
    def get_username(self):
        """Публічний метод - отримання імені користувача"""
        return self._username
    
    def _validate_password_strength(self, password):
        """🛡️ Захищений метод - валідація міцності пароля
        
        Конвенція: одне підкреслення = метод для внутрішнього використання
        Але все одно доступний як user._validate_password_strength()
        """
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain uppercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain digit")
        if not any(c in "!@#$%^&*" for c in password):
            errors.append("Password must contain special character")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def __generate_hash(self, password):
        """🔐 "Приватний" метод - генерація безпечного хешу
        
        Два підкреслення = name mangling: стає _SecureUser__generate_hash()
        Python "приховує" цей метод, але все одно можна отримати!
        """
        salted_password = password + self.__salt
        return hashlib.sha256(salted_password.encode()).hexdigest()
    
    def __reset_security_state(self):
        """🔐 "Приватний" метод - скидання стану безпеки"""
        self._failed_attempts = 0
        self._locked = False
        self.__log_private_event("Security state reset")
    
    def __log_private_event(self, event):
        """🔐 "Приватний" метод - приватне логування"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[PRIVATE LOG {timestamp}] {self._username}: {event}")
    
    def set_password(self, password):
        """Публічний метод - встановлення пароля з валідацією та хешуванням"""
        # Використовуємо захищений метод для валідації
        self._validate_password_strength(password)
        
        # Використовуємо "приватний" метод для генерації хешу
        self.__password_hash = self.__generate_hash(password)
        
        # Скидаємо стан безпеки при зміні пароля
        self.__reset_security_state()
    
    def verify_password(self, password):
        """Публічний метод - перевірка пароля з захистом від брут-форсу"""
        if self._locked:
            raise Exception("Account is locked due to too many failed attempts")
        
        # Використовуємо "приватний" метод для генерації хешу для порівняння
        password_hash = self.__generate_hash(password)
        
        if self.__password_hash == password_hash:
            self._failed_attempts = 0  # Скидаємо лічильник при успіху
            self.__log_private_event("Successful login")
            return True
        else:
            self._failed_attempts += 1
            if self._failed_attempts >= self.__max_attempts:
                self._locked = True
                self._log_security_event("Account locked due to brute force")
                self.__log_private_event(f"Account locked after {self.__max_attempts} attempts")
            return False
    
    def _log_security_event(self, event):
        """🛡️ Захищений метод - логування подій безпеки
        
        Внутрішній метод для записування безпекових подій
        Доступний зовні, але порушує конвенцію
        """
        print(f"SECURITY EVENT [{self._username}]: {event}")
    
    def is_locked(self):
        """Публічний метод - перевірка статусу блокування"""
        return self._locked

# Тестування та демонстрація "приватності" Python
try:
    user = SecureUser("admin", "SecurePass123!")
    print(f"User created: {user.get_username()}")
    
    # ✅ Правильне використання - публічні методи
    print("Correct password:", user.verify_password("SecurePass123!"))
    
    print("\n=== ДЕМОНСТРАЦІЯ ЗАХИЩЕНИХ (_) АТРИБУТІВ/МЕТОДІВ ===")
    # ⚠️ Порушення конвенції - доступ до "захищених" атрибутів
    print(f"Direct access to 'protected' username: {user._username}")
    print(f"Direct access to 'protected' attempts: {user._failed_attempts}")
    
    # ⚠️ Виклик "захищеного" методу (порушує конвенцію, але працює)
    user._log_security_event("Manual security event")
    
    print("\n=== ДЕМОНСТРАЦІЯ 'ПРИВАТНИХ' (__) АТРИБУТІВ/МЕТОДІВ ===")
    # ❌ Спроба доступу до "приватних" атрибутів - не працює
    try:
        print(f"Direct access to __password_hash: {user.__password_hash}")
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")
    
    try:
        print(f"Direct access to __salt: {user.__salt}")
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")
    
    # ❌ Спроба виклику "приватного" методу - не працює
    try:
        user.__generate_hash("test")
    except AttributeError as e:
        print(f"❌ AttributeError calling __generate_hash: {e}")
    
    print("\n=== АЛЕ! NAME MANGLING МОЖНА ОБІЙТИ ===")
    # 😱 Python змінює назви, але їх все одно можна отримати!
    print("Name mangling creates these attributes:")
    private_attrs = [attr for attr in dir(user) if 'SecureUser__' in attr]
    for attr in private_attrs:
        print(f"  - {attr}")
    
    # 😱 Доступ через name mangling
    print(f"'Private' salt via name mangling: {user._SecureUser__salt}")
    print(f"'Private' max attempts: {user._SecureUser__max_attempts}")
    
    # 😱 Виклик "приватного" методу через name mangling
    test_hash = user._SecureUser__generate_hash("test_password")
    print(f"'Private' method result: {test_hash[:20]}...")
    
    # 😱 Можна навіть змінити "приватні" дані!
    print(f"Max attempts before: {user._SecureUser__max_attempts}")
    user._SecureUser__max_attempts = 10  # Змінюємо "приватну" константу
    print(f"Max attempts after modification: {user._SecureUser__max_attempts}")
    
    print("\n=== ВАЖЛИВА ПРИМІТКА ===")
    print("Python НЕ має справжньої приватності!")
    print("• _attribute - 'захищений' (конвенція, легко доступний)")
    print("• __attribute - 'приватний' (name mangling, складніше, але доступний)")
    print("• Це філософія Python: 'Ми всі дорослі люди' (We're all consenting adults)")
    print("• Для справжньої безпеки використовуйте правильну авторизацію на рівні додатка!")
        
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Security error: {e}")
```

### 2.2 Декоратор @property в дії (25 хв)

Створюємо клас мережевого з'єднання з розумними властивостями:

```python
from datetime import datetime

class NetworkConnection:
    # Відомі порти сервісів
    WELL_KNOWN_PORTS = {
        22: "SSH", 80: "HTTP", 443: "HTTPS", 25: "SMTP", 
        53: "DNS", 3389: "RDP", 3306: "MySQL"
    }
    
    # Підозрілі порти
    SUSPICIOUS_PORTS = {4444, 31337, 12345, 54321}
    
    def __init__(self, source_ip, dest_ip, dest_port, protocol="TCP"):
        self._source_ip = source_ip
        self._dest_ip = dest_ip
        self._dest_port = None
        self._protocol = protocol.upper()
        self._start_time = datetime.now()
        self._bytes_transferred = 0
        self._status = "ACTIVE"
        
        # Використовуємо setter для валідації
        self.dest_port = dest_port
    
    @property
    def dest_port(self):
        """Порт призначення"""
        return self._dest_port
    
    @dest_port.setter
    def dest_port(self, value):
        """Встановлення порту з валідацією"""
        try:
            port = int(value)
            if not 1 <= port <= 65535:
                raise ValueError("Port must be between 1 and 65535")
            self._dest_port = port
        except (ValueError, TypeError):
            raise ValueError("Port must be a valid integer")
    
    @property
    def connection_string(self):
        """Рядкове представлення з'єднання (тільки читання)"""
        return f"{self._source_ip} -> {self._dest_ip}:{self._dest_port}"
    
    @property
    def service_name(self):
        """Назва сервісу на основі порту (тільки читання)"""
        return self.WELL_KNOWN_PORTS.get(self._dest_port, "Unknown")
    
    @property
    def is_suspicious(self):
        """Перевірка підозрілості з'єднання (тільки читання)"""
        return (self._dest_port in self.SUSPICIOUS_PORTS or 
                self._is_external_connection())
    
    @property
    def duration_seconds(self):
        """Тривалість з'єднання в секундах (тільки читання)"""
        return (datetime.now() - self._start_time).total_seconds()
    
    @property
    def bytes_transferred(self):
        """Кількість переданих байтів"""
        return self._bytes_transferred
    
    @bytes_transferred.setter
    def bytes_transferred(self, value):
        """Встановлення кількості байтів з валідацією"""
        if value < 0:
            raise ValueError("Bytes transferred cannot be negative")
        self._bytes_transferred = value
    
    @staticmethod
    def is_private_ip(ip):
        """Перевірка приватної IP адреси"""
        try:
            parts = list(map(int, ip.split('.')))
            return (parts[0] == 10 or 
                    (parts[0] == 172 and 16 <= parts[1] <= 31) or
                    (parts[0] == 192 and parts[1] == 168))
        except:
            return False
    
    def _is_external_connection(self):
        """Приватний метод - перевірка зовнішнього з'єднання"""
        return (self.is_private_ip(self._source_ip) and 
                not self.is_private_ip(self._dest_ip))
    
    def close_connection(self):
        """Закриття з'єднання"""
        self._status = "CLOSED"
    
    def __str__(self):
        return f"{self.connection_string} [{self.service_name}] {'⚠️SUSPICIOUS' if self.is_suspicious else '✅OK'}"

# Приклад використання
conn1 = NetworkConnection("192.168.1.100", "8.8.8.8", 80)
print("Connection 1:", conn1)
print(f"Duration: {conn1.duration_seconds:.1f} seconds")

conn2 = NetworkConnection("10.0.0.5", "192.168.1.200", 4444)
print("Connection 2:", conn2)
print(f"Is suspicious: {conn2.is_suspicious}")

# Тестування валідації
try:
    conn3 = NetworkConnection("192.168.1.1", "8.8.8.8", 99999)  # Неправильний порт
except ValueError as e:
    print(f"Validation error: {e}")

# Робота з properties
conn1.bytes_transferred = 1024
print(f"Bytes transferred: {conn1.bytes_transferred}")

# Спроба змінити read-only property викличе помилку
# conn1.service_name = "CUSTOM"  # AttributeError!
```

---

## Частина 3: Комплексний приклад - SecurityAlert (30 хв)

Тепер створимо повнофункціональну систему сповіщень безпеки:

```python
from datetime import datetime
from enum import Enum
import hashlib
import json

class AlertSeverity(Enum):
    """Рівні критичності сповіщень безпеки"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class SecurityAlert:
    """
    Повнофункціональний клас для сповіщень SIEM системи
    Демонструє всі вивчені концепції OOP
    """
    
    # Атрибути класу
    _alert_counter = 0
    VALID_STATUSES = ["OPEN", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE"]
    
    def __init__(self, title, description, severity, source_ip, destination_ip=None):
        # Генерація унікального ID
        SecurityAlert._alert_counter += 1
        self._alert_id = f"ALR-{SecurityAlert._alert_counter:06d}"
        
        # Базові атрибути
        self._title = title
        self._description = description
        self._source_ip = source_ip
        self._destination_ip = destination_ip
        self._timestamp = datetime.now()
        self._assigned_analyst = None
        self._evidence = []
        
        # Використовуємо properties для валідації
        self.severity = severity
        self.status = "OPEN"
    
    # Properties з валідацією
    @property
    def alert_id(self):
        """Унікальний ідентифікатор (read-only)"""
        return self._alert_id
    
    @property
    def severity(self):
        """Рівень критичності"""
        return self._severity
    
    @severity.setter
    def severity(self, value):
        """Встановлення критичності з валідацією"""
        if isinstance(value, AlertSeverity):
            self._severity = value
        elif isinstance(value, int) and 1 <= value <= 4:
            self._severity = AlertSeverity(value)
        else:
            raise ValueError("Severity must be AlertSeverity enum or integer 1-4")
    
    @property
    def status(self):
        """Статус обробки сповіщення"""
        return self._status
    
    @status.setter
    def status(self, value):
        """Встановлення статусу з валідацією"""
        if value.upper() in self.VALID_STATUSES:
            self._status = value.upper()
        else:
            raise ValueError(f"Status must be one of: {self.VALID_STATUSES}")
    
    @property
    def age_hours(self):
        """Вік сповіщення в годинах (read-only)"""
        return (datetime.now() - self._timestamp).total_seconds() / 3600
    
    @property
    def is_critical(self):
        """Чи є сповіщення критичним (read-only)"""
        return self._severity == AlertSeverity.CRITICAL
    
    @property
    def is_expired(self):
        """Чи застаріле сповіщення (>24 години) (read-only)"""
        return self.age_hours > 24
    
    # Статичні методи
    @staticmethod
    def validate_ip(ip_address):
        """Валідація IP адреси"""
        if not ip_address:
            return False
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False
    
    @staticmethod
    def calculate_risk_score(severity, source_reputation=0.5, has_response_plan=True):
        """Розрахунок оцінки ризику"""
        base_score = severity.value * 25  # 25, 50, 75, 100
        reputation_modifier = (1 - source_reputation) * 20
        plan_modifier = -10 if has_response_plan else 0
        
        risk_score = base_score + reputation_modifier + plan_modifier
        return max(0, min(100, risk_score))
    
    # Методи екземпляра
    def assign_analyst(self, analyst_name):
        """Призначення аналітика"""
        self._assigned_analyst = analyst_name
        if self._status == "OPEN":
            self.status = "INVESTIGATING"
    
    def escalate(self):
        """Підвищення критичності"""
        if self._severity.value < 4:
            self.severity = AlertSeverity(self._severity.value + 1)
            return True
        return False
    
    def add_evidence(self, evidence_type, evidence_data):
        """Додавання доказів"""
        evidence = {
            'type': evidence_type,
            'data': evidence_data,
            'timestamp': datetime.now().isoformat()
        }
        self._evidence.append(evidence)
    
    def generate_hash(self):
        """Генерація хешу для дедуплікації"""
        data = f"{self._title}{self._source_ip}{self._destination_ip}{self._severity.name}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def to_dict(self):
        """Серіалізація в словник"""
        return {
            'alert_id': self._alert_id,
            'title': self._title,
            'description': self._description,
            'severity': self._severity.name,
            'source_ip': self._source_ip,
            'destination_ip': self._destination_ip,
            'timestamp': self._timestamp.isoformat(),
            'status': self._status,
            'assigned_analyst': self._assigned_analyst,
            'age_hours': round(self.age_hours, 2),
            'evidence_count': len(self._evidence)
        }
    
    def __str__(self):
        return f"Alert {self._alert_id}: {self._title} [{self._severity.name}] from {self._source_ip}"

# Демонстрація повного функціоналу
if __name__ == "__main__":
    # Створення сповіщення
    alert = SecurityAlert(
        title="Suspected Brute Force Attack",
        description="Multiple failed login attempts detected",
        severity=AlertSeverity.HIGH,
        source_ip="192.168.1.100",
        destination_ip="10.0.0.5"
    )
    
    print("=== SECURITY ALERT DEMO ===")
    print(f"Alert: {alert}")
    print(f"Age: {alert.age_hours:.2f} hours")
    print(f"Is critical: {alert.is_critical}")
    print(f"Is expired: {alert.is_expired}")
    
    # Призначення аналітика
    alert.assign_analyst("John Smith")
    print(f"Status after assignment: {alert.status}")
    
    # Додавання доказів
    alert.add_evidence("log_entry", "Failed login from 192.168.1.100 at 10:30:15")
    alert.add_evidence("network_scan", "Port scan detected on target server")
    
    # Ескалація
    escalated = alert.escalate()
    print(f"Escalated: {escalated}, New severity: {alert.severity.name}")
    
    # Розрахунок ризику
    risk = SecurityAlert.calculate_risk_score(
        alert.severity, 
        source_reputation=0.2, 
        has_response_plan=True
    )
    print(f"Risk Score: {risk}")
    
    # Серіалізація
    print("\n=== ALERT DATA ===")
    alert_data = alert.to_dict()
    print(json.dumps(alert_data, indent=2, ensure_ascii=False))
```

---

## Практичні завдання (30 хв)

### Завдання 1: Клас FirewallRule
Створіть клас `FirewallRule` з наступними вимогами:

```python
class FirewallRule:
    """
    Завдання: реалізуйте клас для правил файрвола
    
    Вимоги:
    1. Properties: source_ip, dest_ip, port, action (ALLOW/DENY), priority
    2. Метод matches(connection) - перевірка відповідності правила
    3. Статичний метод parse_rule(rule_string) - парсинг з рядка
    4. Валідація всіх введених даних
    5. Метод to_iptables() - експорт в формат iptables
    """
    
    def __init__(self, source_ip, dest_ip, port, action, priority=100):
        # Ваша реалізація
        pass
    
    @property
    def priority(self):
        # Ваша реалізація
        pass
    
    @priority.setter  
    def priority(self, value):
        # Валідація: 1-1000
        pass
        
    def matches(self, connection):
        # Перевірка чи відповідає правило з'єднанню
        pass
    
    @staticmethod
    def parse_rule(rule_string):
        # Парсинг: "ALLOW 192.168.1.0/24 -> any:80 priority:100"
        pass

# Тест
rule = FirewallRule("192.168.1.0/24", "any", 80, "ALLOW", 50)
# connection = NetworkConnection(...)
# print(rule.matches(connection))
```

### Завдання 2: Клас LogAnalyzer 
Спростіть та адаптуйте наданий раніше клас `LogAnalyzer`:

```python
class SimpleLogAnalyzer:
    """
    Завдання: створити спрощений аналізатор логів
    
    Вимоги:
    1. Property total_entries (read-only)
    2. Метод add_log_entry(log_line)
    3. Property suspicious_ips (read-only) - список підозрілих IP
    4. Статичний метод extract_ip(log_line) - витяг IP з рядка
    5. Метод get_ip_statistics() - статистика по IP
    """
    pass
```

---

## Підсумок

### Що ми вивчили:
1. **Атрибути класу vs екземпляра** - коли використовувати кожен тип
2. **Методи екземпляра** - робота з конкретними об'єктами
3. **@staticmethod** - утилітарні функції класу
4. **@classmethod** - альтернативні конструктори та роботу з класом
5. **@property** - контрольований доступ до атрибутів
6. **Інкапсуляція** - захист даних через приватні атрибути
7. **Валідація** - перевірка коректності даних

### Ключові принципи:
- **Інкапсуляція**: Приховування внутрішньої реалізації
- **Валідація**: Перевірка даних при встановленні
- **Separation of Concerns**: Різні типи методів для різних завдань
- **Properties**: Розумні атрибути з логікою

### Практичне застосування:
Створені класи можуть використовуватись у реальних системах безпеки для:
- Обробки сповіщень SIEM систем
- Аналізу мережевого трафіку
- Управління правилами файрвола
- Аналізу логів безпеки

---

## Домашнє завдання

1. **Завершіть завдання 1 і 2** з практичної частини
2. **Створіть клас `VulnerabilityScanner`** з методами:
   - `scan_port(ip, port)` - сканування порту
   - `scan_range(ip, start_port, end_port)` - сканування діапазону
   - Property `scan_results` - результати сканування
   - Статичний метод `is_port_open(ip, port)` - перевірка порту

3. **Розробіть клас `IncidentResponse`** для управління інцидентами:
   - Властивості: incident_id, severity, status, assigned_team
   - Методи для зміни статусу із валідацією
   - Розрахунок часу реагування
   - Генерація звітів

4. **Додайте до SecurityAlert**:
   - Метод `export_to_csv()` - експорт у CSV
   - Класметод `from_json()` - створення з JSON
   - Метод `correlate_with(other_alert)` - пошук зв'язків між сповіщеннями


---

## 📚 Додаткові матеріали для самостійного вивчення

*Ці техніки виходять за рамки базового курсу, але корисні для розуміння повних можливостей Python*

### 🔒 1. Слоти (__slots__) - Обмеження атрибутів класу

```python
class RestrictedSecurityEvent:
    """Клас з обмеженими атрибутами через __slots__"""
    # Дозволені атрибути - тільки ці!
    __slots__ = ['_event_id', '_timestamp', '_severity', '_source_ip', '_processed']
    
    def __init__(self, event_id, severity, source_ip):
        self._event_id = event_id
        self._timestamp = datetime.now()
        self._severity = severity
        self._source_ip = source_ip
        self._processed = False
    
    @property
    def event_id(self):
        return self._event_id
    
    @property
    def severity(self):
        return self._severity
    
    @severity.setter
    def severity(self, value):
        if value not in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            raise ValueError(f"Invalid severity: {value}")
        self._severity = value

# Демонстрація slots
event = RestrictedSecurityEvent("EVT-001", "HIGH", "192.168.1.100")
print(f"Event: {event.event_id}")

# ✅ Дозволені операції
event.severity = "CRITICAL"  # Працює
print(f"Updated severity: {event.severity}")

# ❌ Заборонені операції
try:
    event.new_attribute = "test"  # AttributeError!
except AttributeError as e:
    print(f"Slots restriction: {e}")

# 💡 Переваги slots:
# - Економія пам'яті (особливо для багатьох об'єктів)
# - Швидший доступ до атрибутів
# - Запобігання створенню нових атрибутів випадково

print(f"Memory usage comparison:")
print(f"  Without slots: object has __dict__ (~280 bytes)")
print(f"  With slots: fixed attributes (~48 bytes)")
```

### ❄️ 2. Frozen Dataclasses - Незмінні об'єкти

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass(frozen=True)  # Незмінний після створення!
class ImmutableSecurityLog:
    """Незмінний лог подій безпеки"""
    log_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    source_ip: str = "unknown"
    events: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Валідація при створенні"""
        if not self.log_id.startswith("LOG-"):
            raise ValueError("Log ID must start with 'LOG-'")
        
        # Для frozen класів використовуємо object.__setattr__
        if len(self.events) == 0:
            object.__setattr__(self, 'events', ["Log initialized"])

# Демонстрація frozen dataclass
log = ImmutableSecurityLog("LOG-001", source_ip="192.168.1.1")
print(f"Log created: {log.log_id} at {log.timestamp}")
print(f"Initial events: {log.events}")

# ❌ Спроба зміни викличе помилку
try:
    log.source_ip = "10.0.0.1"  # FrozenInstanceError!
except Exception as e:
    print(f"Frozen restriction: {type(e).__name__}: {e}")

try:
    log.events.append("New event")  # Це працює! List сам не frozen
    print(f"Events after append: {log.events}")
except Exception as e:
    print(f"Error: {e}")

# 💡 Коли використовувати frozen:
# - Конфігураційні об'єкти
# - Результати, які не повинні змінюватись
# - Об'єкти для передачі між потоками
# - Ключі словників (якщо всі поля hashable)
```

### 🚀 3. Бібліотека attrs - Потужні незмінні класи

```python
# pip install attrs
try:
    import attr
    from attr import validators

    @attr.s(frozen=True, slots=True)  # Комбінація frozen + slots
    class PowerfulSecurityAlert:
        """Потужний клас сповіщення з attrs"""
        
        # Атрибути з валідаторами та конвертерами
        alert_id: str = attr.ib(validator=validators.matches_re(r'^ALR-\d{6}$'))
        severity: str = attr.ib(validator=validators.in_(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']))
        source_ip: str = attr.ib(validator=validators.matches_re(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
        timestamp: datetime = attr.ib(factory=datetime.now)
        
        # Автоматичні конвертери
        priority: int = attr.ib(converter=int, validator=validators.instance_of(int))
        
        # Приватні атрибути (не показуються в repr)
        _hash_cache: str = attr.ib(init=False, repr=False, default=None)
        
        def __attrs_post_init__(self):
            """Пост-ініціалізація для frozen об'єктів"""
            import hashlib
            data = f"{self.alert_id}{self.source_ip}{self.severity}"
            # Для frozen класів використовуємо object.__setattr__
            object.__setattr__(self, '_hash_cache', hashlib.md5(data.encode()).hexdigest())
        
        @classmethod
        def from_log_entry(cls, log_entry):
            """Альтернативний конструктор"""
            parts = log_entry.split('|')
            return cls(
                alert_id=parts[0],
                severity=parts[1], 
                source_ip=parts[2],
                priority=parts[3]
            )
        
        def get_hash(self):
            """Отримання кешованого хешу"""
            return self._hash_cache

    # Демонстрація attrs
    alert = PowerfulSecurityAlert(
        alert_id="ALR-123456",
        severity="HIGH", 
        source_ip="192.168.1.100",
        priority="85"  # Автоматично конвертується в int
    )
    
    print(f"Alert created: {alert}")
    print(f"Hash: {alert.get_hash()}")
    print(f"Priority type: {type(alert.priority)} = {alert.priority}")
    
    # Створення з альтернативного конструктора
    log_alert = PowerfulSecurityAlert.from_log_entry("ALR-654321|CRITICAL|10.0.0.5|95")
    print(f"From log: {log_alert}")
    
    # ❌ Всі спроби зміни заблоковані
    try:
        alert.severity = "LOW"  # FrozenInstanceError
    except Exception as e:
        print(f"Attrs frozen: {type(e).__name__}")
    
    try:
        alert.new_attr = "test"  # AttributeError (slots)
    except AttributeError as e:
        print(f"Attrs slots: {e}")
    
    # 💡 Переваги attrs:
    # - Автоматична генерація __init__, __repr__, __eq__
    # - Потужні валідатори та конвертери
    # - Комбінація frozen + slots
    # - Кращий контроль над атрибутами

except ImportError:
    print("attrs library not installed. Run: pip install attrs")
    
    # Альтернатива без attrs - ручна реалізація
    class ManualImmutableAlert:
        """Ручна реалізація незмінного класу"""
        __slots__ = ['_alert_id', '_severity', '_timestamp', '_frozen']
        
        def __init__(self, alert_id, severity):
            self._alert_id = alert_id
            self._severity = severity
            self._timestamp = datetime.now()
            self._frozen = True
        
        def __setattr__(self, name, value):
            if hasattr(self, '_frozen') and self._frozen:
                raise AttributeError(f"Cannot modify frozen object")
            super().__setattr__(name, value)
        
        @property
        def alert_id(self):
            return self._alert_id
        
        @property 
        def severity(self):
            return self._severity
    
    # Тест ручної реалізації
    manual_alert = ManualImmutableAlert("ALR-999999", "HIGH")
    print(f"Manual immutable: {manual_alert.alert_id}")
    
    try:
        manual_alert._severity = "LOW"  # AttributeError
    except AttributeError as e:
        print(f"Manual frozen: {e}")
```

### 🎯 Порівняння підходів

```python
import sys
from datetime import datetime

# 1. Звичайний клас
class RegularAlert:
    def __init__(self, alert_id, severity):
        self.alert_id = alert_id
        self.severity = severity
        self.timestamp = datetime.now()

# 2. Клас зі slots
class SlottedAlert:
    __slots__ = ['alert_id', 'severity', 'timestamp']
    
    def __init__(self, alert_id, severity):
        self.alert_id = alert_id
        self.severity = severity
        self.timestamp = datetime.now()

# 3. Frozen dataclass
@dataclass(frozen=True)
class FrozenAlert:
    alert_id: str
    severity: str
    timestamp: datetime = field(default_factory=datetime.now)

# Порівняння розміру в пам'яті
regular = RegularAlert("ALR-001", "HIGH")
slotted = SlottedAlert("ALR-002", "HIGH") 
frozen = FrozenAlert("ALR-003", "HIGH")

print("=== ПОРІВНЯННЯ ПІДХОДІВ ===")
print(f"Regular class size: ~{sys.getsizeof(regular.__dict__)} bytes (має __dict__)")
print(f"Slotted class size: ~{sys.getsizeof(slotted)} bytes (без __dict__)")
print(f"Frozen dataclass size: ~{sys.getsizeof(frozen.__dict__)} bytes")

print("\n=== МОЖЛИВОСТІ МОДИФІКАЦІЇ ===")
# Модифікація regular
regular.severity = "LOW"
regular.new_attr = "allowed"
print(f"Regular: можна змінювати та додавати атрибути ✅")

# Модифікація slotted
slotted.severity = "LOW"
try:
    slotted.new_attr = "denied"
except AttributeError:
    print(f"Slotted: можна змінювати, але не можна додавати нові атрибути ⚠️")

# Модифікація frozen  
try:
    frozen.severity = "LOW"
except:
    print(f"Frozen: не можна змінювати атрибути ❌")

print("\n=== КОЛИ ВИКОРИСТОВУВАТИ ===")
print("🏃 Regular classes: загальне використання, гнучкість")
print("💾 __slots__: економія пам'яті, багато об'єктів") 
print("🔒 frozen: незмінні дані, безпека, багатопотоковість")
print("🚀 attrs: максимальний контроль, валідація, продуктивність")
```

### 📖 Підсумок додаткових технік

**Для кібербезпеки ці підходи корисні коли:**

1. **__slots__**: 
   - Обробка великих об'ємів мережевого трафіку
   - Зберігання мільйонів записів логу в пам'яті
   - Запобігання випадковому створенню атрибутів

2. **Frozen objects**:
   - Конфігураційні дані безпеки
   - Незмінні правила файрвола  
   - Результати аналізу, які не повинні змінюватись
   - Багатопоточна обробка даних

3. **attrs library**:
   - Складні моделі даних з валідацією
   - API для системи безпеки
   - Високопродуктивні додатки

**Пам'ятайте**: це додаткові інструменти. Для більшості завдань достатньо звичайних класів з `@property` та правильною інкапсуляцією! 🎯

---

## 📝 Домашнє завдання

Для виконання домашнього завдання на створення класів з відносинами композиції, перегляньте файл:
👉 **[ClassesHomeTask.md](./ClassesHomeTask.md)** - Завдання на створення класів з відносинами HAS-MANY та HAS-ONE
