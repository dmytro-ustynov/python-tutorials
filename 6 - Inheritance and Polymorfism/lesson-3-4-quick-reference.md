# Швидкий довідник: ООП в Python для Кібербезпеки

## 🔗 Наслідування (Inheritance)

### Базовий синтаксис
```python
class Parent:
    def __init__(self, value):
        self.value = value
    
    def method(self):
        return f"Parent: {self.value}"

class Child(Parent):
    def __init__(self, value, extra):
        super().__init__(value)  # ✅ ОБОВ'ЯЗКОВО!
        self.extra = extra
```

### Приклад для кібербезпеки
```python
class SecurityEvent:
    def __init__(self, ip, severity):
        self.ip = ip
        self.severity = severity

class LoginAttempt(SecurityEvent):
    def __init__(self, ip, username, success):
        super().__init__(ip, "WARNING" if not success else "INFO")
        self.username = username
```

---

## ⚡ Метод super()

### Виклик батьківського конструктора
```python
super().__init__(args)  # В конструкторі
```

### Розширення батьківського методу
```python
def method(self):
    result = super().method()  # Викликаємо батьківський
    return result + " + додаткова логіка"
```

---

## 🔄 Поліморфізм (Polymorphism)

### Один інтерфейс - різні реалізації
```python
from abc import ABC, abstractmethod

class Scanner(ABC):
    @abstractmethod
    def scan(self):
        pass

class PortScanner(Scanner):
    def scan(self):
        return [22, 80, 443]

class VulnScanner(Scanner):
    def scan(self):
        return ["CVE-2024-1234"]

# Поліморфізм в дії
def run_scan(scanner):  # Працює з будь-яким сканером!
    return scanner.scan()
```

---

## ✨ Магічні методи (Dunder Methods)

### Основні методи

#### Ініціалізація та представлення
```python
def __init__(self, value):
    """Конструктор: obj = MyClass(value)"""
    self.value = value

def __str__(self):
    """Для print(obj) та str(obj)"""
    return f"MyClass: {self.value}"

def __repr__(self):
    """Для розробників: repr(obj)"""
    return f"MyClass({self.value!r})"
```

#### Порівняння
```python
def __eq__(self, other):
    """obj1 == obj2"""
    if not isinstance(other, MyClass):
        return False
    return self.value == other.value

def __lt__(self, other):
    """obj1 < obj2"""
    return self.value < other.value

def __le__(self, other):  # <=
def __gt__(self, other):  # >
def __ge__(self, other):  # >=
def __ne__(self, other):  # !=
```

#### Контейнерні методи
```python
def __len__(self):
    """len(obj)"""
    return len(self._items)

def __getitem__(self, index):
    """obj[0], obj[1:3]"""
    return self._items[index]

def __setitem__(self, index, value):
    """obj[0] = value"""
    self._items[index] = value

def __iter__(self):
    """for item in obj"""
    return iter(self._items)

def __contains__(self, item):
    """if item in obj"""
    return item in self._items
```

#### Математичні операції
```python
def __add__(self, other):
    """obj1 + obj2"""
    return MyClass(self.value + other.value)

def __sub__(self, other):  # obj1 - obj2
def __mul__(self, other):  # obj1 * obj2
def __truediv__(self, other):  # obj1 / obj2
```

#### Інші корисні методи
```python
def __hash__(self):
    """Для використання в set та dict"""
    return hash(self.value)

def __call__(self, *args):
    """obj() - виклик об'єкта як функції"""
    return self.process(*args)

def __enter__(self):
    """with obj: - вхід в контекст"""
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    """with obj: - вихід з контексту"""
    self.cleanup()
    return False
```

---

## 🔐 Криптографія

### Хешування (необоротне)
```python
import hashlib

# SHA-256
text = "password"
hash_result = hashlib.sha256(text.encode()).hexdigest()

# З сіллю (для паролів)
import secrets
salt = secrets.token_hex(16)
salted = (password + salt).encode()
hashed = hashlib.sha256(salted).hexdigest()
```

### Шифрування XOR (навчальний приклад)
```python
import base64

def xor_encrypt(data, key):
    key_bytes = key.encode()
    data_bytes = data.encode()
    encrypted = bytes([
        data_bytes[i] ^ key_bytes[i % len(key_bytes)]
        for i in range(len(data_bytes))
    ])
    return base64.b64encode(encrypted).decode()

def xor_decrypt(encrypted, key):
    data = base64.b64decode(encrypted)
    # XOR - та сама операція для шифрування та розшифрування!
    return xor_encrypt(data.decode(), key)
```

### Безпечна криптографія (cryptography library)
```python
from cryptography.fernet import Fernet

# Генерація ключа
key = Fernet.generate_key()
cipher = Fernet(key)

# Шифрування
encrypted = cipher.encrypt(b"secret data")

# Розшифрування
decrypted = cipher.decrypt(encrypted)
```

---

## 📝 Швидкі шаблони

### Базовий клас з наслідуванням
```python
class Base:
    def __init__(self, value):
        self.value = value
    
    def process(self):
        return self.value
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"

class Derived(Base):
    def __init__(self, value, extra):
        super().__init__(value)
        self.extra = extra
    
    def process(self):
        base_result = super().process()
        return f"{base_result} + {self.extra}"
```

### Контейнерний клас
```python
class Container:
    def __init__(self):
        self._items = []
    
    def add(self, item):
        self._items.append(item)
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __iter__(self):
        return iter(self._items)
    
    def __contains__(self, item):
        return item in self._items
```

### Контекстний менеджер
```python
class FileManager:
    def __init__(self, filename):
        self.filename = filename
    
    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # Не поглинаємо виключення

# Використання
with FileManager('data.txt') as f:
    content = f.read()
```

---

## ⚠️ Частіпомилки

### ❌ Забули super()
```python
class Child(Parent):
    def __init__(self, value):
        self.value = value  # ПОМИЛКА! Батьківський __init__ не викликано
```

### ✅ Правильно
```python
class Child(Parent):
    def __init__(self, value):
        super().__init__()  # ✅ Правильно!
        self.value = value
```

### ❌ Не перевіряємо тип
```python
def __eq__(self, other):
    return self.value == other.value  # Помилка якщо other не того типу!
```

### ✅ Правильно
```python
def __eq__(self, other):
    if not isinstance(other, MyClass):
        return False
    return self.value == other.value
```

---

## 🎯 Корисні ідіоми

### Порожній абстрактний клас
```python
from abc import ABC, abstractmethod

class Interface(ABC):
    @abstractmethod
    def method(self):
        pass
```

### Singleton через __new__
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Іммутабельний клас
```python
class Immutable:
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def __hash__(self):
        return hash(self._value)
```

---

**Завантажити PDF версію:** [oop-quick-reference.pdf](#)  
**Роздрукувати для використання на занятті** ✅
