# Додаток: Абстрактні класи та методи (ABC)

## 🎯 Що таке абстрактний клас?

**Абстрактний клас** (Abstract Base Class, ABC) — це клас, який не можна створити безпосередньо (не можна створити його екземпляр). Він служить як **шаблон** або **контракт** для інших класів.

### Аналогія з реальним світом:

Уявіть, що ви проектуєте систему безпеки. Ви знаєте, що вам потрібні різні типи **сканерів** (портів, вразливостей, малвару), але кожен сканер має працювати по-своєму. При цьому всі сканери **повинні мати метод `scan()`**.

```
Абстрактний клас "Сканер" (неможливо створити)
    ↓
    "Всі сканери МУСЯТЬ мати метод scan()"
    ↓
Конкретні класи (можна створити):
    - PortScanner → реалізує scan() для портів
    - VulnerabilityScanner → реалізує scan() для вразливостей
    - MalwareScanner → реалізує scan() для малвару
```

---

## 📚 Навіщо потрібні абстрактні класи?

### 1. **Гарантія інтерфейсу**
Абстрактний клас **гарантує**, що всі похідні класи реалізують певні методи.

### 2. **Запобігання помилкам**
Python не дозволить створити клас, який не реалізував всі абстрактні методи.

### 3. **Документація коду**
Абстрактний клас чітко показує, які методи повинні бути в похідних класах.

### 4. **Поліморфізм**
Можна писати код, який працює з абстрактним типом, а не з конкретними класами.

---

## 🛠 Як створити абстрактний клас?

### Крок 1: Імпортувати ABC та abstractmethod

```python
from abc import ABC, abstractmethod
```

- **ABC** — базовий клас для всіх абстрактних класів
- **abstractmethod** — декоратор для позначення абстрактних методів

### Крок 2: Успадкувати від ABC

```python
class MyAbstractClass(ABC):
    pass
```

### Крок 3: Позначити методи як абстрактні

```python
from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    
    @abstractmethod
    def my_method(self):
        """Цей метод МУСИТЬ бути реалізований в похідних класах"""
        pass
```

---

## 📝 Базовий приклад

### Приклад без ABC (проблема):

```python
class Scanner:
    """Базовий клас без ABC"""
    def scan(self):
        pass  # Порожня реалізація

class PortScanner(Scanner):
    pass  # Забули реалізувати scan()!

# Проблема: це спрацює, але scan() нічого не робить!
scanner = PortScanner()
scanner.scan()  # Нічого не станеться, помилки немає
```

### Приклад з ABC (правильно):

```python
from abc import ABC, abstractmethod

class Scanner(ABC):
    """Абстрактний клас - шаблон для всіх сканерів"""
    
    @abstractmethod
    def scan(self):
        """Кожен сканер МУСИТЬ реалізувати цей метод"""
        pass

class PortScanner(Scanner):
    pass  # Забули реалізувати scan()

# Помилка! Python не дозволить створити екземпляр
scanner = PortScanner()
# TypeError: Can't instantiate abstract class PortScanner 
# with abstract method scan
```

### Правильна реалізація:

```python
from abc import ABC, abstractmethod

class Scanner(ABC):
    @abstractmethod
    def scan(self):
        pass

class PortScanner(Scanner):
    def scan(self):  # ✅ Реалізували абстрактний метод
        return [22, 80, 443]

# Тепер все працює!
scanner = PortScanner()
print(scanner.scan())  # [22, 80, 443]
```

---

## 🔒 Практичний приклад: Система шифрування

```python
from abc import ABC, abstractmethod

class Encryptor(ABC):
    """
    Абстрактний клас для всіх шифрувальників.
    Гарантує, що кожен шифрувальник може шифрувати та розшифровувати.
    """
    
    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """
        Шифрує текст.
        
        Args:
            plaintext: Текст для шифрування
        
        Returns:
            Зашифрований текст
        """
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """
        Розшифровує текст.
        
        Args:
            ciphertext: Зашифрований текст
        
        Returns:
            Розшифрований текст
        """
        pass


# ❌ НЕ МОЖНА створити екземпляр абстрактного класу
# encryptor = Encryptor()  # TypeError!


# ✅ Конкретна реалізація 1: Шифр Цезаря
class CaesarCipher(Encryptor):
    def __init__(self, shift=3):
        self.shift = shift
    
    def encrypt(self, plaintext: str) -> str:
        result = []
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + self.shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        original_shift = self.shift
        self.shift = -self.shift
        result = self.encrypt(ciphertext)
        self.shift = original_shift
        return result


# ✅ Конкретна реалізація 2: XOR шифрування
import base64

class XORCipher(Encryptor):
    def __init__(self, key: str):
        self.key = key.encode()
    
    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode('utf-8')
        encrypted = bytes([
            data[i] ^ self.key[i % len(self.key)]
            for i in range(len(data))
        ])
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        encrypted = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted = bytes([
            encrypted[i] ^ self.key[i % len(self.key)]
            for i in range(len(encrypted))
        ])
        return decrypted.decode('utf-8')


# Використання - ПОЛІМОРФІЗМ
def test_encryptor(encryptor: Encryptor, message: str):
    """
    Функція приймає БУДЬ-ЯКИЙ Encryptor.
    Не важливо, Caesar чи XOR - головне що є encrypt() та decrypt()
    """
    print(f"Testing: {encryptor.__class__.__name__}")
    print(f"Original:  {message}")
    
    encrypted = encryptor.encrypt(message)
    print(f"Encrypted: {encrypted}")
    
    decrypted = encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    print(f"Success: {message == decrypted}\n")


# Тестуємо різні шифри через єдиний інтерфейс
message = "SECRET MESSAGE"

caesar = CaesarCipher(shift=13)
test_encryptor(caesar, message)

xor = XORCipher("MySecretKey")
test_encryptor(xor, message)
```

**Вивід:**
```
Testing: CaesarCipher
Original:  SECRET MESSAGE
Encrypted: FRPERG ZRFFNTR
Decrypted: SECRET MESSAGE
Success: True

Testing: XORCipher
Original:  SECRET MESSAGE
Encrypted: GxYKBQkXCBsEDg==
Decrypted: SECRET MESSAGE
Success: True
```

---

## 🎓 Детальний розбір

### Що відбувається?

1. **Визначення контракту:**
   ```python
   class Encryptor(ABC):
       @abstractmethod
       def encrypt(self, plaintext: str) -> str:
           pass
   ```
   Це означає: "Будь-який Encryptor МУСИТЬ вміти шифрувати"

2. **Реалізація контракту:**
   ```python
   class CaesarCipher(Encryptor):
       def encrypt(self, plaintext: str) -> str:
           # Реальна реалізація
           return encrypted_text
   ```

3. **Поліморфне використання:**
   ```python
   def test_encryptor(encryptor: Encryptor, message: str):
       # Працює з будь-яким Encryptor!
       encryptor.encrypt(message)
   ```

---

## 🔍 Абстрактні методи з реалізацією

Абстрактні методи **МОЖУТЬ** мати реалізацію за замовчуванням:

```python
from abc import ABC, abstractmethod

class SecurityEvent(ABC):
    def __init__(self, timestamp, ip):
        self.timestamp = timestamp
        self.ip = ip
    
    @abstractmethod
    def is_suspicious(self):
        """
        Базова реалізація, яку можна розширити.
        Але похідні класи ВСЕ ОДНО мусять реалізувати цей метод!
        """
        # Базова логіка
        return False
    
    def log(self):
        """Звичайний метод - не абстрактний"""
        return f"[{self.timestamp}] {self.ip}"


class LoginAttempt(SecurityEvent):
    def __init__(self, timestamp, ip, success):
        super().__init__(timestamp, ip)
        self.success = success
    
    def is_suspicious(self):
        # Можна викликати базову реалізацію через super()
        base_suspicious = super().is_suspicious()
        # І додати власну логіку
        return base_suspicious or not self.success
```

---

## 📊 Порівняльна таблиця

| Аспект | Звичайний клас | Абстрактний клас (ABC) |
|--------|----------------|------------------------|
| Можна створити екземпляр? | ✅ Так | ❌ Ні |
| Може мати абстрактні методи? | ❌ Ні | ✅ Так |
| Може мати звичайні методи? | ✅ Так | ✅ Так |
| Похідні класи мусять реалізувати методи? | ❌ Ні | ✅ Так (абстрактні) |
| Призначення | Створення об'єктів | Визначення інтерфейсу |

---

## 🎯 Коли використовувати ABC?

### ✅ Використовуйте ABC коли:

1. **Потрібен контракт для класів**
   ```python
   # Всі сканери МУСЯТЬ вміти сканувати
   class Scanner(ABC):
       @abstractmethod
       def scan(self):
           pass
   ```

2. **Є спільна логіка, але різна реалізація**
   ```python
   class DatabaseConnector(ABC):
       def connect(self):
           # Спільна логіка
           self.validate_credentials()
       
       @abstractmethod
       def execute_query(self, query):
           # Різна для MySQL, PostgreSQL, MongoDB
           pass
   ```

3. **Хочете запобігти помилкам**
   ```python
   # Python не дозволить забути реалізувати важливий метод
   class PaymentProcessor(ABC):
       @abstractmethod
       def process_payment(self, amount):
           pass
   ```

### ❌ НЕ використовуйте ABC коли:

1. Клас повністю функціональний і його можна використовувати як є
2. Не потрібна гарантія реалізації методів
3. Структура класів проста і зрозуміла без ABC

---

## 🔬 Додаткові можливості ABC

### 1. Множинні абстрактні методи

```python
from abc import ABC, abstractmethod

class DatabaseHandler(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def execute(self, query):
        pass
    
    # Звичайний метод (не абстрактний)
    def log(self, message):
        print(f"[LOG] {message}")


class MySQLHandler(DatabaseHandler):
    # МУСИТЬ реалізувати ВСІ 3 абстрактні методи!
    def connect(self):
        print("Connecting to MySQL...")
    
    def disconnect(self):
        print("Disconnecting from MySQL...")
    
    def execute(self, query):
        print(f"Executing: {query}")
```

### 2. Абстрактні властивості

```python
from abc import ABC, abstractmethod

class User(ABC):
    @property
    @abstractmethod
    def username(self):
        """Кожен користувач МУСИТЬ мати username"""
        pass
    
    @property
    @abstractmethod
    def email(self):
        """Кожен користувач МУСИТЬ мати email"""
        pass


class AdminUser(User):
    def __init__(self, username, email):
        self._username = username
        self._email = email
    
    @property
    def username(self):
        return self._username
    
    @property
    def email(self):
        return self._email
```

### 3. Перевірка чи клас реалізує інтерфейс

```python
from abc import ABC

# Перевірка чи об'єкт є екземпляром ABC класу
scanner = PortScanner()
print(isinstance(scanner, Scanner))  # True

# Перевірка чи клас є підкласом ABC класу
print(issubclass(PortScanner, Scanner))  # True
```

---

## 💡 Практичні поради

### 1. Називайте абстрактні класи зрозуміло
```python
# ✅ Добре
class Encryptor(ABC)
class Scanner(ABC)
class Handler(ABC)

# ❌ Погано (незрозуміло що це абстрактний клас)
class Tool(ABC)
class Thing(ABC)
```

### 2. Документуйте абстрактні методи
```python
class Processor(ABC):
    @abstractmethod
    def process(self, data):
        """
        Обробляє дані.
        
        Args:
            data: Дані для обробки
        
        Returns:
            Оброблені дані
        
        Raises:
            ValueError: Якщо дані невалідні
        """
        pass
```

### 3. Використовуйте type hints
```python
from typing import List

class DataCollector(ABC):
    @abstractmethod
    def collect(self) -> List[dict]:
        """Повертає список словників з даними"""
        pass
```

---

## 🎬 Підсумок

### Ключові моменти:

1. **ABC** = Abstract Base Class = Абстрактний базовий клас
2. **@abstractmethod** = декоратор для позначення методу як абстрактного
3. **Не можна створити екземпляр** абстрактного класу
4. **Похідні класи мусять реалізувати** всі абстрактні методи
5. **Використовуйте для створення контрактів** та гарантії інтерфейсу

### Шаблон для копіювання:

```python
from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    """Опис призначення абстрактного класу"""
    
    @abstractmethod
    def required_method(self):
        """Метод, який МУСЯТЬ реалізувати похідні класи"""
        pass
    
    def optional_method(self):
        """Звичайний метод з реалізацією"""
        return "Some default behavior"


class ConcreteClass(MyAbstractClass):
    """Конкретна реалізація"""
    
    def required_method(self):
        """Реалізація абстрактного методу"""
        return "My implementation"


# Використання
obj = ConcreteClass()
print(obj.required_method())  # My implementation
print(obj.optional_method())   # Some default behavior
```

## Поліморфізм операторів
Суть: Оператори (+, ==, <) працюють по-різному з різними типами.
```python
# + для чисел
5 + 3  # 8

# + для рядків
"Hello" + "World"  # "HelloWorld"

# + для списків
[1, 2] + [3, 4]  # [1, 2, 3, 4]
```
Для своїх класів:
```python
class IPAddress:
    def __init__(self, ip):
        self.ip = ip
    
    def __add__(self, num):  # Визначаємо оператор +
        # IP + число = наступна IP
        return IPAddress(self.ip + num)

ip = IPAddress("192.168.1.1")
next_ip = ip + 1  # 192.168.1.2
```

---

**Автор:** Дмитро Устинов , 2025  
**Тема:** Абстрактні класи та методи (ABC)  
**Версія:** 1.0
