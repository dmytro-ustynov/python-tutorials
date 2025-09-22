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
        self._username = None  # Захищений атрибут
        self._password_hash = None
        self._failed_attempts = 0
        self._locked = False
        
        # Використовуємо setter для валідації
        self.set_username(username)
        self.set_password(password)
    
    def set_username(self, username):
        """Встановлення імені користувача з валідацією"""
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not username.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Username can only contain letters, numbers, - and _")
        self._username = username
    
    def get_username(self):
        """Отримання імені користувача"""
        return self._username
    
    def set_password(self, password):
        """Встановлення пароля з валідацією та хешуванням"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain digit")
        if not any(c in "!@#$%^&*" for c in password):
            raise ValueError("Password must contain special character")
        
        # Зберігаємо безпечний хеш
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Перевірка пароля з захистом від брут-форсу"""
        if self._locked:
            raise Exception("Account is locked due to too many failed attempts")
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if self._password_hash == password_hash:
            self._failed_attempts = 0  # Скидаємо лічильник
            return True
        else:
            self._failed_attempts += 1
            if self._failed_attempts >= 3:
                self._locked = True
            return False
    
    def is_locked(self):
        """Перевірка блокування акаунта"""
        return self._locked

# Тестування
try:
    user = SecureUser("admin", "SecurePass123!")
    print(f"User created: {user.get_username()}")
    
    # Тест правильного пароля
    print("Correct password:", user.verify_password("SecurePass123!"))
    
    # Тест неправильних паролів
    for i in range(4):
        result = user.verify_password("wrongpass")
        print(f"Attempt {i+1}: {result}, Locked: {user.is_locked()}")
        
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
