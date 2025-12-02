# 🔐 Заняття 5.5: Криптографія та шифрування в Python

## 🎯 Мета заняття (2 години)

Навчитися використовувати криптографічні інструменти Python для забезпечення безпеки даних: хешування для перевірки цілісності, симетричне та асиметричне шифрування для захисту конфіденційних даних.

---

## 📚 План заняття

1. **Recap:** Кодування vs Хешування vs Шифрування (10 хв)
2. **Хешування для перевірки цілісності файлів** (20 хв)
3. **Симетричне шифрування (Fernet)** (30 хв)
4. **Асиметричне шифрування (RSA)** (30 хв)
5. **Безпечна робота з паролями** (20 хв)
6. **Практичні сценарії** (10 хв)

---

## 🔹 ЧАСТИНА 1: Recap - Кодування vs Хешування vs Шифрування

### Швидке нагадування

```python
# 1️⃣ КОДУВАННЯ (Encoding) - двостороннє перетворення
import base64

text = "Secret Message"
encoded = base64.b64encode(text.encode())
print(f"Encoded: {encoded}")  # b'U2VjcmV0IE1lc3NhZ2U='

decoded = base64.b64decode(encoded).decode()
print(f"Decoded: {decoded}")  # Secret Message

# ⚠️ НЕ для безпеки! Легко розшифрувати
```

```python
# 2️⃣ ХЕШУВАННЯ (Hashing) - одностороннє перетворення
import hashlib

password = "my_password"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(f"Hash: {hash_value}")
# Hash: 2c26b46b68ffc68ff99b453c1d30413413422d706...

# ❌ Неможливо повернути назад: hash → password
# ✅ Використання: перевірка цілісності, зберігання паролів
```

```python
# 3️⃣ ШИФРУВАННЯ (Encryption) - двостороннє з ключем
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = "Secret Message"
encrypted = cipher.encrypt(message.encode())
print(f"Encrypted: {encrypted}")

decrypted = cipher.decrypt(encrypted).decode()
print(f"Decrypted: {decrypted}")

# ✅ Безпечне двостороннє перетворення
# 🔑 Потрібен ключ для розшифрування
```

### Коли що використовувати?

| Задача | Метод | Приклад |
|--------|-------|---------|
| Передача даних (не секретних) | Encoding | Base64 для email attachments |
| Перевірка цілісності файлів | Hashing | Checksums, file verification |
| Зберігання паролів | Hashing + Salt | bcrypt, argon2 |
| Захист конфіденційних даних | Encryption | Шифрування файлів, повідомлень |

---

## 🔹 ЧАСТИНА 2: Хешування для перевірки цілісності

### Встановлення бібліотеки

```bash
# Не потрібно встановлювати - hashlib вбудований!
```

### Приклад 1: Хешування тексту

```python
import hashlib

def hash_text(text, algorithm='sha256'):
    """
    Хешувати текст різними алгоритмами
    """
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }

    if algorithm not in algorithms:
        raise ValueError(f"Algorithm must be one of {list(algorithms.keys())}")

    hash_func = algorithms[algorithm]
    hash_obj = hash_func(text.encode('utf-8'))
    return hash_obj.hexdigest()

# Приклад використання
text = "Hello, Cybersecurity!"

print(f"MD5:    {hash_text(text, 'md5')}")
print(f"SHA1:   {hash_text(text, 'sha1')}")
print(f"SHA256: {hash_text(text, 'sha256')}")
print(f"SHA512: {hash_text(text, 'sha512')}")
```

**Вивід:**
```
MD5:    c8b26a1e8e8e8e9c7e8e8e8e8e8e8e8e
SHA1:   a1b2c3d4e5f6...
SHA256: 3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea
SHA512: 8a7f5d2e... (128 символів)
```

### Приклад 2: Перевірка цілісності файлу

```python
import hashlib

def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Обчислити hash файлу
    Читає файл частинами для економії пам'яті
    """
    hash_func = getattr(hashlib, algorithm)()

    with open(file_path, 'rb') as f:
        # Читати файл блоками по 8KB
        while chunk := f.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()

def verify_file_integrity(file_path, expected_hash, algorithm='sha256'):
    """
    Перевірити чи не змінився файл
    """
    actual_hash = calculate_file_hash(file_path, algorithm)

    if actual_hash == expected_hash:
        print(f"✅ File integrity verified!")
        return True
    else:
        print(f"❌ File has been modified!")
        print(f"   Expected: {expected_hash}")
        print(f"   Got:      {actual_hash}")
        return False

# Приклад використання
file_path = "important_document.pdf"

# Зберегти hash оригінального файлу
original_hash = calculate_file_hash(file_path)
print(f"Original hash: {original_hash}")

# Пізніше перевірити чи файл не змінився
verify_file_integrity(file_path, original_hash)
```

### Приклад 3: Checksums для завантажень

```python
def download_and_verify(url, expected_checksum):
    """
    Завантажити файл та перевірити його checksum
    """
    import requests
    from pathlib import Path

    # Завантажити файл
    filename = Path(url).name
    print(f"Downloading {filename}...")

    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

    # Перевірити checksum
    actual_checksum = calculate_file_hash(filename, 'sha256')

    if actual_checksum == expected_checksum:
        print(f"✅ Download verified! Checksum matches.")
        return True
    else:
        print(f"❌ WARNING! Checksum mismatch!")
        print(f"   File may be corrupted or tampered with!")
        Path(filename).unlink()  # Видалити підозрілий файл
        return False

# Приклад
download_and_verify(
    url="https://example.com/tool.zip",
    expected_checksum="3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea"
)
```

---

## 🔹 ЧАСТИНА 3: Симетричне шифрування (Fernet)

### Встановлення

```bash
pip install cryptography
```

### Що таке Fernet?

- **Симетричне шифрування**: один ключ для encrypt і decrypt
- **Безпечний**: використовує AES-128 під капотом
- **Простий у використанні**: високорівневий API
- **Включає автентифікацію**: захист від модифікацій

### Приклад 1: Базове шифрування

```python
from cryptography.fernet import Fernet

# 1. Генерувати ключ (зберігати в безпечному місці!)
key = Fernet.generate_key()
print(f"Key: {key}")
# Key: b'gAAAAABh...' (44 символи)

# 2. Створити cipher object
cipher = Fernet(key)

# 3. Зашифрувати повідомлення
message = "This is a secret message"
encrypted = cipher.encrypt(message.encode())
print(f"Encrypted: {encrypted}")

# 4. Розшифрувати
decrypted = cipher.decrypt(encrypted).decode()
print(f"Decrypted: {decrypted}")
```

### Приклад 2: Шифрування файлів

```python
from cryptography.fernet import Fernet
from pathlib import Path

class FileEncryptor:
    """Шифрування та дешифрування файлів"""

    def __init__(self, key_file='secret.key'):
        self.key_file = Path(key_file)

        if self.key_file.exists():
            # Завантажити існуючий ключ
            self.key = self.key_file.read_bytes()
        else:
            # Створити новий ключ
            self.key = Fernet.generate_key()
            self.key_file.write_bytes(self.key)
            print(f"🔑 New key created: {key_file}")

        self.cipher = Fernet(self.key)

    def encrypt_file(self, file_path):
        """Зашифрувати файл"""
        file_path = Path(file_path)

        # Читати оригінальний файл
        data = file_path.read_bytes()

        # Зашифрувати
        encrypted_data = self.cipher.encrypt(data)

        # Зберегти з розширенням .encrypted
        encrypted_file = file_path.with_suffix(file_path.suffix + '.encrypted')
        encrypted_file.write_bytes(encrypted_data)

        print(f"✅ File encrypted: {encrypted_file}")
        return encrypted_file

    def decrypt_file(self, encrypted_file_path):
        """Розшифрувати файл"""
        encrypted_file = Path(encrypted_file_path)

        # Читати зашифрований файл
        encrypted_data = encrypted_file.read_bytes()

        try:
            # Розшифрувати
            decrypted_data = self.cipher.decrypt(encrypted_data)

            # Зберегти без .encrypted
            if encrypted_file.suffix == '.encrypted':
                decrypted_file = encrypted_file.with_suffix('')
            else:
                decrypted_file = encrypted_file.with_suffix('.decrypted')

            decrypted_file.write_bytes(decrypted_data)
            print(f"✅ File decrypted: {decrypted_file}")
            return decrypted_file

        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return None

# Використання
encryptor = FileEncryptor('my_secret.key')

# Зашифрувати файл
encryptor.encrypt_file('sensitive_data.txt')

# Розшифрувати файл
encryptor.decrypt_file('sensitive_data.txt.encrypted')
```

### Приклад 3: Захист конфігураційних файлів

```python
import json
from cryptography.fernet import Fernet
from pathlib import Path

class SecureConfig:
    """Безпечне зберігання конфігурацій (API keys, passwords)"""

    def __init__(self, key_file='config.key'):
        self.key_file = Path(key_file)

        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)

        self.cipher = Fernet(self.key_file.read_bytes())

    def save_config(self, config_data, filename='config.encrypted'):
        """Зберегти конфіг у зашифрованому вигляді"""
        # Конвертувати в JSON
        json_data = json.dumps(config_data, indent=2)

        # Зашифрувати
        encrypted = self.cipher.encrypt(json_data.encode())

        # Зберегти
        Path(filename).write_bytes(encrypted)
        print(f"✅ Config saved securely to {filename}")

    def load_config(self, filename='config.encrypted'):
        """Завантажити та розшифрувати конфіг"""
        try:
            # Читати зашифровані дані
            encrypted = Path(filename).read_bytes()

            # Розшифрувати
            decrypted = self.cipher.decrypt(encrypted)

            # Парсити JSON
            config = json.loads(decrypted.decode())
            return config

        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return None

# Використання
secure_config = SecureConfig()

# Зберегти секретні дані
config = {
    "api_key": "sk-1234567890abcdef",
    "database_password": "super_secret_pass",
    "secret_token": "my_token_here"
}
secure_config.save_config(config)

# Завантажити назад
loaded_config = secure_config.load_config()
print(f"API Key: {loaded_config['api_key']}")
```

---

## 🔹 ЧАСТИНА 4: Асиметричне шифрування (RSA)

### Що таке RSA?

- **Асиметричне шифрування**: пара ключів (публічний + приватний)
- **Публічний ключ**: для шифрування (можна ділитися)
- **Приватний ключ**: для розшифрування (тримати в секреті)
- **Використання**: безпечний обмін даними, цифрові підписи

### Приклад 1: Генерація пари ключів

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Генерувати приватний ключ
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048  # 2048 або 4096 для високої безпеки
)

# Отримати публічний ключ
public_key = private_key.public_key()

# Зберегти приватний ключ
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('private_key.pem', 'wb') as f:
    f.write(private_pem)

# Зберегти публічний ключ
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open('public_key.pem', 'wb') as f:
    f.write(public_pem)

print("✅ RSA key pair generated!")
```

### Приклад 2: Шифрування з RSA

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def encrypt_with_public_key(message, public_key_file='public_key.pem'):
    """Зашифрувати повідомлення публічним ключем"""
    # Завантажити публічний ключ
    with open(public_key_file, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Зашифрувати
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_with_private_key(encrypted_message, private_key_file='private_key.pem'):
    """Розшифрувати повідомлення приватним ключем"""
    # Завантажити приватний ключ
    with open(private_key_file, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Розшифрувати
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# Використання
message = "Secret message for you"

# Alice шифрує для Bob (використовує публічний ключ Bob)
encrypted = encrypt_with_public_key(message, 'bob_public_key.pem')
print(f"Encrypted: {encrypted[:50]}...")

# Bob розшифровує (використовує свій приватний ключ)
decrypted = decrypt_with_private_key(encrypted, 'bob_private_key.pem')
print(f"Decrypted: {decrypted}")
```

### Приклад 3: Цифрові підписи

```python
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def sign_message(message, private_key_file='private_key.pem'):
    """Підписати повідомлення приватним ключем"""
    with open(private_key_file, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(message, signature, public_key_file='public_key.pem'):
    """Перевірити підпис публічним ключем"""
    with open(public_key_file, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# Використання
message = "I authorize this transaction"

# Alice підписує повідомлення
signature = sign_message(message, 'alice_private_key.pem')

# Bob перевіряє підпис (використовує публічний ключ Alice)
is_valid = verify_signature(message, signature, 'alice_public_key.pem')
print(f"Signature valid: {is_valid}")
```

### 📝 Поглиблене вивчення RSA

Для детального розуміння математики RSA та покрокових обчислень дивіться:
- [RSA_WORKSHEET.md](RSA_WORKSHEET.md) - покроковий worksheet з місцем для відповідей
- [RSA_EDUCATION_README.md](RSA_EDUCATION_README.md) - повний посібник з навчальними матеріалами
- [rsa_educational.py](rsa_educational.py) - інтерактивна демонстрація RSA
- [rsa_calculator.py](rsa_calculator.py) - калькулятор для перевірки обчислень

---

## 🔹 ЧАСТИНА 5: Безпечна робота з паролями

### Встановлення bcrypt

```bash
pip install bcrypt
```

### Чому не просто hash?

```python
import hashlib

# ❌ ПОГАНА практика
password = "mypassword123"
hash1 = hashlib.sha256(password.encode()).hexdigest()

# Проблема: однакові паролі → однакові хеші
hash2 = hashlib.sha256("mypassword123".encode()).hexdigest()
print(hash1 == hash2)  # True - легко зламати через rainbow tables!
```

### Рішення: Salt + bcrypt

```python
import bcrypt

# ✅ ПРАВИЛЬНА практика
password = "mypassword123"

# Хешувати з автоматичним salt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(f"Hashed: {hashed}")

# Кожен раз новий hash (завдяки випадковому salt)
hashed2 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(f"Hashed again: {hashed2}")
print(f"Same? {hashed == hashed2}")  # False - різні salt!

# Але обидва валідні для перевірки
print(bcrypt.checkpw(password.encode(), hashed))   # True
print(bcrypt.checkpw(password.encode(), hashed2))  # True
```

### Приклад: Система реєстрації/входу

```python
import bcrypt
import json
from pathlib import Path

class UserAuth:
    """Проста система аутентифікації"""

    def __init__(self, db_file='users.json'):
        self.db_file = Path(db_file)
        self.users = self._load_users()

    def _load_users(self):
        """Завантажити базу користувачів"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        """Зберегти базу користувачів"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=2)

    def register(self, username, password):
        """Зареєструвати нового користувача"""
        if username in self.users:
            print(f"❌ User {username} already exists!")
            return False

        # Хешувати пароль
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Зберегти (bcrypt повертає bytes, треба декодувати для JSON)
        self.users[username] = {
            'password_hash': hashed.decode('utf-8'),
            'created_at': str(datetime.datetime.now())
        }
        self._save_users()

        print(f"✅ User {username} registered successfully!")
        return True

    def login(self, username, password):
        """Перевірити credentials"""
        if username not in self.users:
            print(f"❌ User {username} not found!")
            return False

        # Отримати збережений hash
        stored_hash = self.users[username]['password_hash'].encode('utf-8')

        # Перевірити пароль
        if bcrypt.checkpw(password.encode(), stored_hash):
            print(f"✅ Welcome back, {username}!")
            return True
        else:
            print(f"❌ Invalid password!")
            return False

# Використання
auth = UserAuth()

# Реєстрація
auth.register('alice', 'super_secret_password')
auth.register('bob', 'bob_password_123')

# Спроба входу
auth.login('alice', 'super_secret_password')  # ✅ Success
auth.login('alice', 'wrong_password')         # ❌ Fail
auth.login('bob', 'bob_password_123')         # ✅ Success
```

---

## 🔹 ЧАСТИНА 6: Практичні сценарії

### Сценарій 1: Безпечний обмін файлами

```python
"""
Alice хоче надіслати секретний файл Bob через незахищений канал
"""
from cryptography.fernet import Fernet

# Alice генерує ключ
key = Fernet.generate_key()

# Alice шифрує файл
encryptor = FileEncryptor(key)
encrypted_file = encryptor.encrypt_file('secret_document.pdf')

# Alice надсилає:
# 1. Зашифрований файл через email/cloud
# 2. Ключ через безпечний канал (Signal, WhatsApp, особисто)

# Bob розшифровує
bob_encryptor = FileEncryptor(key)  # Використовує ключ від Alice
bob_encryptor.decrypt_file(encrypted_file)
```

### Сценарій 2: Перевірка завантажень

```python
"""
Перевірка чи завантажений файл не підроблений
"""
# Сайт публікує:
file_url = "https://example.com/security_tool.zip"
official_sha256 = "3f79bb7b435b05321651daefd374cdc681dc06faa65e374e38337b88ca046dea"

# Користувач завантажує та перевіряє
download_and_verify(file_url, official_sha256)
```

### Сценарій 3: Підписання звітів

```python
"""
Аналітик підписує звіт, щоб довести його автентичність
"""
# Analyst підписує звіт
report = "Security audit results: System is secure."
signature = sign_message(report, 'analyst_private_key.pem')

# Manager перевіряє підпис
is_authentic = verify_signature(
    report,
    signature,
    'analyst_public_key.pem'
)
print(f"Report is authentic: {is_authentic}")
```

---

## 📊 Порівняльна таблиця

| Метод | Швидкість | Безпека | Використання | Приклади |
|-------|-----------|---------|--------------|----------|
| **Base64** | ⚡⚡⚡ | ❌ | Кодування, не шифрування | Email attachments, URLs |
| **MD5** | ⚡⚡⚡ | ⚠️ Зламаний | Checksums (не для паролів!) | File integrity |
| **SHA-256** | ⚡⚡ | ✅ | Хеші, checksums | File verification, blockchain |
| **bcrypt** | ⚡ | ✅✅ | Паролі з salt | User passwords |
| **Fernet** | ⚡⚡ | ✅✅ | Симетричне шифрування | Encrypt files, configs |
| **RSA** | ⚡ | ✅✅✅ | Асиметричне шифрування | Secure communication, signatures |
| **EC (ED25519/X25519)** | ⚡⚡⚡ | ✅✅✅ | Підписи (ED25519), обмін ключами (X25519) | SSH keys, modern crypto |

---

## 🏠 Практичні завдання

### Завдання 1: File Integrity Checker (легке)

Створити програму, яка:
1. Обчислює SHA-256 checksums для всіх файлів у директорії
2. Зберігає їх у файл `checksums.txt`
3. Може пізніше перевірити чи файли не змінилися

### Завдання 2: Secure Note App (середнє)

Створити CLI додаток для зберігання зашифрованих нотаток:
```bash
python notes.py add "My secret note" --password mypass
python notes.py list --password mypass
python notes.py read 1 --password mypass
```

### Завдання 3: Password Manager (складне)

Створити password manager:
- Зберігає паролі у зашифрованому вигляді (Fernet)
- Master password захищений bcrypt
- Генерує сильні паролі
- Copy-paste у clipboard

### Завдання 4: Secure File Transfer (продвинуте)

Створити систему для безпечного обміну файлами:
- Sender шифрує файл публічним ключем отримувача
- Підписує файл своїм приватним ключем
- Receiver перевіряє підпис та розшифровує

---

## 📚 Додаткові матеріали

### Бібліотеки Python

- **cryptography** - сучасна, рекомендована
- **pycryptodome** - альтернатива
- **bcrypt** - для паролів
- **hashlib** - вбудована, для хешування

### Best Practices

1. ✅ **Ніколи не пишіть власну криптографію** - використовуйте перевірені бібліотеки
2. ✅ **Зберігайте ключі окремо** від зашифрованих даних
3. ✅ **Використовуйте salt** для паролів
4. ✅ **Оновлюйте бібліотеки** - криптографія швидко застаріває
5. ❌ **Не використовуйте MD5 або SHA1** для безпеки (тільки для checksums)

### Корисні посилання

- [Cryptography library docs](https://cryptography.io/)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [bcrypt documentation](https://github.com/pyca/bcrypt/)

---

## ✅ Що ми вивчили

- 🔹 Різниця між encoding, hashing, encryption
- 🔹 Хешування для перевірки цілісності файлів
- 🔹 Симетричне шифрування з Fernet
- 🔹 Асиметричне шифрування з RSA
- 🔹 Безпечне зберігання паролів з bcrypt
- 🔹 Практичні сценарії застосування криптографії

**Пам'ятайте**: Криптографія - це інструмент. Важливо розуміти коли і як його використовувати!
