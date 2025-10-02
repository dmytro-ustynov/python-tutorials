# Поліморфізм в Python: Детальне пояснення

## 🔄 Що таке поліморфізм?

**Поліморфізм** (від грецького "πολύς" — багато, "μορφή" — форма) — здатність об'єктів різних класів відповідати на один і той самий виклик методу або оператора по-різному.

### Простими словами:
- **Один інтерфейс** — багато реалізацій
- **Одна дія** — різні результати залежно від типу об'єкта
- **Універсальний код** — працює з різними типами даних

---

## 📚 Типи поліморфізму в Python

### 1. Поліморфізм методів
### 2. Поліморфізм операторів
### 3. Duck Typing

---

## 1️⃣ Поліморфізм методів

**Суть:** Різні класи мають методи з однаковими назвами, але різною реалізацією.

### Приклад: Система сканування безпеки

```python
class PortScanner:
    def __init__(self, target):
        self.target = target
    
    def scan(self):
        """Сканування портів"""
        return {
            'type': 'port_scan',
            'target': self.target,
            'open_ports': [22, 80, 443]
        }

class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
    
    def scan(self):
        """Пошук вразливостей"""
        return {
            'type': 'vulnerability_scan',
            'target': self.target,
            'vulnerabilities': ['CVE-2024-1234', 'CVE-2024-5678']
        }

class MalwareScanner:
    def __init__(self, target):
        self.target = target
    
    def scan(self):
        """Пошук малвару"""
        return {
            'type': 'malware_scan',
            'target': self.target,
            'threats': ['Trojan.Win32', 'Backdoor.Linux']
        }


# ПОЛІМОРФНА функція - працює з БУДЬ-ЯКИМ сканером!
def run_security_audit(scanners):
    """
    Функція не знає конкретний тип сканера.
    Вона просто викликає scan() - це і є поліморфізм!
    """
    results = []
    for scanner in scanners:
        result = scanner.scan()  # Поліморфний виклик!
        results.append(result)
    return results


# Використання
target = "192.168.1.100"
scanners = [
    PortScanner(target),
    VulnerabilityScanner(target),
    MalwareScanner(target)
]

# Одна функція обробляє різні типи сканерів
audit_results = run_security_audit(scanners)

for result in audit_results:
    print(f"{result['type']}: {result}")
```

**Вивід:**
```
port_scan: {'type': 'port_scan', 'target': '192.168.1.100', 'open_ports': [22, 80, 443]}
vulnerability_scan: {'type': 'vulnerability_scan', 'target': '192.168.1.100', 'vulnerabilities': ['CVE-2024-1234', 'CVE-2024-5678']}
malware_scan: {'type': 'malware_scan', 'target': '192.168.1.100', 'threats': ['Trojan.Win32', 'Backdoor.Linux']}
```

### Переваги:
- ✅ Один інтерфейс для різних об'єктів
- ✅ Легко додавати нові типи (просто додайте клас з методом `scan()`)
- ✅ Код стає більш гнучким та розширюваним

---

## 2️⃣ Поліморфізм операторів

**Суть:** Оператори (`+`, `-`, `*`, `/`, `|`, `==`, `<` тощо) працюють по-різному з різними типами.

### Вбудовані приклади:

```python
# Оператор + (додавання)
5 + 3           # 8 (числа)
"Hello" + " World"  # "Hello World" (рядки)
[1, 2] + [3, 4]     # [1, 2, 3, 4] (списки)

# Оператор * (множення)
5 * 3           # 15 (числа)
"Ha" * 3        # "HaHaHa" (рядки)
[1, 2] * 3      # [1, 2, 1, 2, 1, 2] (списки)
```

### Магічні методи для операторів:

| Оператор | Магічний метод | Приклад |
|----------|----------------|---------|
| `+` | `__add__` | `a + b` |
| `-` | `__sub__` | `a - b` |
| `*` | `__mul__` | `a * b` |
| `/` | `__truediv__` | `a / b` |
| `//` | `__floordiv__` | `a // b` |
| `%` | `__mod__` | `a % b` |
| `**` | `__pow__` | `a ** b` |
| `==` | `__eq__` | `a == b` |
| `<` | `__lt__` | `a < b` |
| `>` | `__gt__` | `a > b` |
| `|` | `__or__` | `a | b` |
| `&` | `__and__` | `a & b` |

---

### 🔒 Приклад 1: IP-адреса з арифметикою

```python
class IPAddress:
    def __init__(self, ip_string):
        parts = ip_string.split('.')
        self.octets = [int(x) for x in parts]
    
    def __str__(self):
        return '.'.join(map(str, self.octets))
    
    def __int__(self):
        """Конвертація IP в число"""
        return (self.octets[0] << 24) + (self.octets[1] << 16) + \
               (self.octets[2] << 8) + self.octets[3]
    
    def __add__(self, value):
        """Оператор + : IP + число = наступна IP"""
        if not isinstance(value, int):
            return NotImplemented
        
        new_value = int(self) + value
        if new_value > 0xFFFFFFFF:
            raise ValueError("IP overflow")
        
        return IPAddress(f"{(new_value >> 24) & 0xFF}."
                        f"{(new_value >> 16) & 0xFF}."
                        f"{(new_value >> 8) & 0xFF}."
                        f"{new_value & 0xFF}")
    
    def __sub__(self, other):
        """Оператор - : різниця між IP"""
        if isinstance(other, IPAddress):
            return int(self) - int(other)
        elif isinstance(other, int):
            return self + (-other)
        return NotImplemented
    
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


# Використання поліморфізму операторів
ip1 = IPAddress("192.168.1.1")
ip2 = IPAddress("192.168.1.10")

print(ip1 + 5)      # 192.168.1.6 (додавання)
print(ip2 - ip1)    # 9 (різниця)
print(ip1 == ip2)   # False (порівняння)
print(ip1 < ip2)    # True (порівняння)
```

---

### 📁 Приклад 2: Оператор `/` для формування шляхів (як в pathlib)

Python використовує оператор `/` для зручної роботи зі шляхами!

```python
from pathlib import Path

class FilePath:
    """Клас для роботи зі шляхами файлів"""
    
    def __init__(self, path):
        self.path = str(path)
    
    def __truediv__(self, other):
        """
        Оператор / для об'єднання шляхів
        Приклад: path / "folder" / "file.txt"
        """
        import os
        new_path = os.path.join(self.path, str(other))
        return FilePath(new_path)
    
    def __str__(self):
        return self.path
    
    def exists(self):
        import os
        return os.path.exists(self.path)


# Використання - дуже зручно!
base = FilePath("/var/log")
log_file = base / "security" / "auth.log"
print(log_file)  # /var/log/security/auth.log

# Реальний приклад з pathlib
from pathlib import Path
path = Path("/home") / "user" / "documents" / "report.pdf"
print(path)  # /home/user/documents/report.pdf
```

**Чому це корисно:**
- ✅ Інтуїтивний синтаксис
- ✅ Кросплатформність (автоматично використовує правильні роздільники)
- ✅ Легко читається: `base / "folder" / "file"` замість `os.path.join(base, "folder", "file")`

---

### 🔗 Приклад 3: Оператор `|` для формування пайпів (pipes)

Оператор `|` використовується для створення ланцюжків обробки даних!

```python
class DataPipeline:
    """Конвеєр обробки даних"""
    
    def __init__(self, data=None):
        self.data = data if data is not None else []
    
    def __or__(self, function):
        """
        Оператор | для створення pipeline
        Приклад: data | filter | map | reduce
        """
        if self.data is None:
            return DataPipeline()
        
        result = function(self.data)
        return DataPipeline(result)
    
    def __repr__(self):
        return f"DataPipeline({self.data})"


# Функції обробки
def filter_suspicious(data):
    """Фільтрує підозрілі IP"""
    return [ip for ip in data if ip.startswith("203.")]

def to_uppercase(data):
    """Конвертує в великі літери"""
    return [ip.upper() for ip in data]

def sort_data(data):
    """Сортує дані"""
    return sorted(data)


# Використання оператора | для створення pipeline
ips = ["192.168.1.1", "203.0.113.45", "192.168.1.50", "203.0.113.10"]
pipeline = DataPipeline(ips)

# Створюємо ланцюжок обробки
result = pipeline | filter_suspicious | to_uppercase | sort_data

print(result)  # DataPipeline(['203.0.113.10', '203.0.113.45'])
```

**Реальний приклад з бібліотеками:**

```python
# pandas використовує | для Query API
import pandas as pd

# df | query | filter | transform
# Це схоже на SQL запити!
```

**Переваги пайпів:**
- ✅ Читабельний код зліва направо
- ✅ Легко додавати нові етапи обробки
- ✅ Функціональний стиль програмування

---

### 🎨 Приклад 4: Комплексна система з множинними операторами

```python
class SecurityRule:
    """Правило безпеки з підтримкою операторів"""
    
    def __init__(self, name, severity):
        self.name = name
        self.severity = severity  # 1-10
    
    def __add__(self, other):
        """Об'єднання правил (OR)"""
        return CompositeRule([self, other], "OR")
    
    def __and__(self, other):
        """Перетин правил (AND)"""
        return CompositeRule([self, other], "AND")
    
    def __or__(self, other):
        """Альтернатива (|)"""
        return self.__add__(other)
    
    def __lt__(self, other):
        """Порівняння за severity"""
        return self.severity < other.severity
    
    def __repr__(self):
        return f"Rule('{self.name}', severity={self.severity})"


class CompositeRule:
    """Композитне правило"""
    
    def __init__(self, rules, operator):
        self.rules = rules
        self.operator = operator
    
    def __repr__(self):
        rules_str = f" {self.operator} ".join(str(r) for r in self.rules)
        return f"({rules_str})"


# Використання
rule1 = SecurityRule("BlockSuspiciousIP", 8)
rule2 = SecurityRule("LogFailedLogin", 5)
rule3 = SecurityRule("AlertAdmin", 9)

# Комбінуємо правила за допомогою операторів!
complex_rule = (rule1 | rule2) & rule3
print(complex_rule)
# ((Rule('BlockSuspiciousIP', severity=8) OR Rule('LogFailedLogin', severity=5)) AND Rule('AlertAdmin', severity=9))

# Порівняння
print(rule1 < rule3)  # True (8 < 9)
print(sorted([rule3, rule1, rule2]))  # Сортування за severity
```

---

## 3️⃣ Duck Typing

**Суть:** "Якщо щось виглядає як качка і крякає як качка, то це качка"

Python **не перевіряє тип об'єкта** - перевіряє чи є потрібний метод/атрибут.

### Приклад:

```python
def process_data(handler):
    """
    Функція не перевіряє ТИП handler.
    Вона просто викликає методи - Duck Typing!
    """
    handler.connect()
    data = handler.fetch()
    handler.disconnect()
    return data


class DatabaseHandler:
    def connect(self):
        print("Connecting to database...")
    
    def fetch(self):
        return ["data1", "data2"]
    
    def disconnect(self):
        print("Disconnecting from database...")


class APIHandler:
    def connect(self):
        print("Connecting to API...")
    
    def fetch(self):
        return {"status": "ok", "data": [1, 2, 3]}
    
    def disconnect(self):
        print("Closing API connection...")


class FileHandler:
    def connect(self):
        print("Opening file...")
    
    def fetch(self):
        return "File contents..."
    
    def disconnect(self):
        print("Closing file...")


# Всі три працюють з одною функцією!
process_data(DatabaseHandler())
process_data(APIHandler())
process_data(FileHandler())
```

**Переваги Duck Typing:**
- ✅ Гнучкість - працює з будь-яким об'єктом з потрібними методами
- ✅ Простота - не потрібно наслідування або інтерфейси
- ✅ Pythonic - природний стиль для Python

**Недоліки:**
- ❌ Помилки виявляються тільки в рантаймі
- ❌ Немає гарантій що об'єкт має потрібні методи

**Рішення:** Використовуйте ABC для гарантій!

---

## 🔗 Зв'язок поліморфізму з абстрактними класами

### Проблема без ABC:

```python
class Scanner:
    pass

class PortScanner(Scanner):
    # Забули реалізувати scan()!
    pass

def audit(scanner):
    return scanner.scan()  # ❌ AttributeError в рантаймі!

audit(PortScanner())  # ПОМИЛКА!
```

### Рішення з ABC:

```python
from abc import ABC, abstractmethod

class Scanner(ABC):
    """Абстрактний клас - гарантує інтерфейс"""
    
    @abstractmethod
    def scan(self):
        """Кожен сканер МУСИТЬ реалізувати цей метод"""
        pass


class PortScanner(Scanner):
    # Забули реалізувати scan()
    pass

# ❌ Помилка при створенні об'єкта!
scanner = PortScanner()
# TypeError: Can't instantiate abstract class PortScanner with abstract method scan
```

### Правильна реалізація:

```python
class PortScanner(Scanner):
    def scan(self):  # ✅ Реалізували абстрактний метод
        return [22, 80, 443]

# ✅ Тепер працює!
scanner = PortScanner()
```

---

## 📊 Порівняння підходів

| Аспект | Без ABC (Duck Typing) | З ABC |
|--------|----------------------|-------|
| **Гнучкість** | ✅ Максимальна | ⚠️ Потрібно наслідування |
| **Безпека** | ❌ Помилки в рантаймі | ✅ Помилки при створенні |
| **Документація** | ❌ Неясний інтерфейс | ✅ Чіткий контракт |
| **Рефакторинг** | ❌ Складно | ✅ Легко знайти проблеми |
| **Перевірка типів** | ❌ Немає гарантій | ✅ Гарантований інтерфейс |

---

## 🎯 Коли використовувати що?

### Використовуйте Duck Typing:
- ✅ Прості скрипти
- ✅ Прототипування
- ✅ Коли потрібна максимальна гнучкість
- ✅ Робота з сторонніми об'єктами

### Використовуйте ABC:
- ✅ Великі проекти
- ✅ Публічні API/бібліотеки
- ✅ Командна розробка
- ✅ Коли потрібна гарантія інтерфейсу
- ✅ Складні ієрархії класів

---

## 💡 Практичні поради

### 1. Комбінуйте підходи

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    """ABC гарантує базовий інтерфейс"""
    
    @abstractmethod
    def process(self, data):
        pass
    
    # Duck Typing для опціональних методів
    def log(self, message):
        # Перевіряємо чи є метод (Duck Typing)
        if hasattr(self, 'logger'):
            self.logger.info(message)
```

### 2. Використовуйте isinstance() для перевірки

```python
def safe_process(obj):
    if isinstance(obj, DataProcessor):
        return obj.process(data)
    else:
        raise TypeError(f"{obj} is not a DataProcessor")
```

### 3. Документуйте очікувані методи

```python
def process_items(container):
    """
    Обробляє елементи з контейнера.
    
    Args:
        container: Об'єкт з методами __iter__ та __len__
    """
    print(f"Processing {len(container)} items...")
    for item in container:
        print(item)
```

---

## 📝 Підсумок

### Поліморфізм = Гнучкість + Універсальність

1. **Поліморфізм методів:**
   - Різні класи → однакові назви методів
   - Одна функція → працює з усіма

2. **Поліморфізм операторів:**
   - Магічні методи (`__add__`, `__truediv__`, `__or__`)
   - `/` для шляхів, `|` для пайпів
   - Інтуїтивний синтаксис

3. **Duck Typing:**
   - "Якщо крякає як качка..."
   - Гнучко, але без гарантій
   - Pythonic стиль

4. **ABC для надійності:**
   - Гарантований інтерфейс
   - Помилки на етапі створення
   - Чітка документація

### Золоте правило:

**Duck Typing для гнучкості + ABC для гарантій = Ідеальний баланс**

```python
from abc import ABC, abstractmethod

# ABC для критичних методів
class Plugin(ABC):
    @abstractmethod
    def execute(self):
        """МУСИТЬ бути реалізовано"""
        pass
    
    # Duck Typing для опціональних
    def setup(self):
        """Опціонально, якщо є - буде викликано"""
        pass

# Використання
def run_plugin(plugin):
    # Перевірка ABC
    if isinstance(plugin, Plugin):
        if hasattr(plugin, 'setup'):  # Duck Typing
            plugin.setup()
        return plugin.execute()
```

---

**Автор:** Курс "Крос-платформне програмування"  
**Тема:** Поліморфізм в Python  
**Версія:** 1.0
