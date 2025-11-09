
## 🎓 **ЗАНЯТТЯ 5.2. Робота з файловими шляхами та пошук файлів**

### 🕐 Загальний час: 2 години (лекція) + 0.75 год самостійна робота

### 🎯 **Мета:**

Навчитися ефективно працювати з файловими шляхами у кросплатформний спосіб, розуміти властивості файлів, здійснювати пошук файлів за різними критеріями та усвідомлювати відмінності між Windows та Unix-системами.

---

## 🧩 СТРУКТУРА ЗАНЯТТЯ

**План:**

1. Сучасний підхід з модулем `pathlib`
2. Властивості файлів (atime, mtime, ctime)
3. Обхід директорій (`os.walk`, `Path.rglob`)
4. Розширений пошук файлів
5. Відмінності Windows vs Unix

**Самостійна робота:** Створення утиліти для пошуку файлів

---

## 🔹 ЧАСТИНА 1. Сучасний підхід з `pathlib`

---

### **Слайд 1. Чому `pathlib` краще за `os.path`**

**Проблема старого підходу:**

```python
import os

# Складно читати, легко помилитися
path = os.path.join(os.path.dirname(__file__), "data", "logs", "app.log")
if os.path.exists(path) and os.path.isfile(path):
    size = os.path.getsize(path)
```

**Сучасний підхід з `pathlib`:**

```python
from pathlib import Path

# Зрозуміло, виразно, об'єктно-орієнтовано
path = Path(__file__).parent / "data" / "logs" / "app.log"
if path.exists() and path.is_file():
    size = path.stat().st_size
```

🎯 **Переваги:**
- Кросплатформність "з коробки"
- Об'єктно-орієнтований підхід
- Інтуїтивний синтаксис з оператором `/`
- Більшість операцій — методи об'єкта Path

---

### **Слайд 2. Основи роботи з Path**

```python
from pathlib import Path

# Поточна директорія
current = Path.cwd()
print(current)  # /home/user/project

# Домашня директорія користувача
home = Path.home()
print(home)  # /home/user (Linux) або C:\Users\User (Windows)

# Створення шляху
config_path = Path.home() / ".config" / "app" / "settings.json"
print(config_path)

# Перевірка існування
if config_path.exists():
    print("Конфігурація знайдена")
```

🔹 **Основні властивості Path:**
- `path.name` — ім'я файлу з розширенням
- `path.stem` — ім'я файлу без розширення
- `path.suffix` — розширення файлу
- `path.parent` — батьківська директорія
- `path.parents` — всі предки

---

### **Слайд 3. Приклади маніпуляцій з Path**

```python
from pathlib import Path

file_path = Path("/var/log/application/app.log.2024")

print(f"Повний шлях: {file_path}")
print(f"Ім'я файлу: {file_path.name}")          # app.log.2024
print(f"Без розширення: {file_path.stem}")      # app.log
print(f"Розширення: {file_path.suffix}")        # .2024
print(f"Всі розширення: {file_path.suffixes}")  # ['.log', '.2024']
print(f"Батьківська папка: {file_path.parent}") # /var/log/application
print(f"Абсолютний шлях: {file_path.absolute()}")

# Зміна розширення
new_path = file_path.with_suffix('.txt')
print(new_path)  # /var/log/application/app.log.txt

# Зміна імені
renamed = file_path.with_name('error.log')
print(renamed)  # /var/log/application/error.log
```

---

### **Слайд 4. Перевірка типів та властивостей**

```python
from pathlib import Path

path = Path("/etc/passwd")

# Перевірки існування
print(path.exists())       # True/False
print(path.is_file())      # Чи це файл?
print(path.is_dir())       # Чи це директорія?
print(path.is_symlink())   # Чи це символічне посилання?
print(path.is_absolute())  # Чи це абсолютний шлях?

# Створення директорій
log_dir = Path("logs/2024/november")
log_dir.mkdir(parents=True, exist_ok=True)
# parents=True — створює всі проміжні папки
# exist_ok=True — не викидає помилку, якщо вже існує
```

🛡️ **Застосування в кібербезпеці:**
- Перевірка конфігураційних файлів перед їх читанням
- Створення структури для логів та звітів
- Валідація шляхів перед операціями

---

## 🔹 ЧАСТИНА 2. Властивості файлів (atime, mtime, ctime)

---

### **Слайд 5. Розуміння часових міток файлів**

Кожен файл у файловій системі має три важливі часові мітки:

```python
from pathlib import Path
import datetime

file_path = Path("example.log")

# Отримання статистики файлу
stat_info = file_path.stat()

# Три важливі мітки:
atime = datetime.datetime.fromtimestamp(stat_info.st_atime)  # Access time
mtime = datetime.datetime.fromtimestamp(stat_info.st_mtime)  # Modification time
ctime = datetime.datetime.fromtimestamp(stat_info.st_ctime)  # Change/Creation time

print(f"Останній доступ (atime): {atime}")
print(f"Остання зміна (mtime): {mtime}")
print(f"Час створення/зміни метаданих (ctime): {ctime}")
```

📋 **Пояснення:**
- **atime** (Access Time) — коли файл востаннє **відкривали для читання**
- **mtime** (Modification Time) — коли **вміст файлу** останній раз змінювався
- **ctime** (Change Time) — має **різне значення** в Unix та Windows!

---

### **Слайд 6. ⚠️ Важливо: ctime в Unix vs Windows**

**🐧 Unix/Linux:**
```
ctime = час зміни метаданих (права доступу, власник, жорстке посилання)
НЕ час створення!
```

**🪟 Windows:**
```
ctime = час створення файлу (creation time)
```

**Приклад:**

```python
from pathlib import Path
import platform
import datetime

file_path = Path("document.txt")
stat_info = file_path.stat()
ctime = datetime.datetime.fromtimestamp(stat_info.st_ctime)

if platform.system() == "Windows":
    print(f"Файл створено: {ctime}")
else:  # Unix/Linux/macOS
    print(f"Метадані змінено: {ctime}")
    print("⚠️ На Unix немає надійного способу дізнатися час створення!")
```

🔎 **Для судової експертизи:**
Розуміння різниці між ctime на різних ОС критично важливе при аналізі цифрових доказів!

---

### **Слайд 7. Додаткова інформація з stat()**

```python
from pathlib import Path

file_path = Path("data.db")
stat_info = file_path.stat()

print(f"Розмір файлу: {stat_info.st_size} байт")
print(f"Розмір у МБ: {stat_info.st_size / (1024**2):.2f} МБ")
print(f"Права доступу (восьмерковий): {oct(stat_info.st_mode)}")
print(f"UID власника: {stat_info.st_uid}")
print(f"GID групи: {stat_info.st_gid}")
print(f"Кількість жорстких посилань: {stat_info.st_nlink}")
```

**💡 Практичне застосування:**
```python
# Знайти файли, які не відкривали більше 30 днів
import time
from pathlib import Path

threshold = time.time() - (30 * 24 * 60 * 60)  # 30 днів тому

for file_path in Path("/var/log").rglob("*.log"):
    if file_path.stat().st_atime < threshold:
        print(f"Старий лог (не відкривався 30+ днів): {file_path}")
```

---

## 🔹 ЧАСТИНА 3. Обхід директорій

---

### **Слайд 8. Класичний підхід: os.walk()**

```python
import os

# os.walk() обходить дерево директорій рекурсивно
for root, dirs, files in os.walk("/var/log"):
    print(f"📁 Директорія: {root}")
    print(f"  Піддиректорії: {dirs}")
    print(f"  Файли: {files}")
    print("-" * 50)
```

**Як це працює:**
- `root` — поточна директорія (str)
- `dirs` — список піддиректорій (list of str)
- `files` — список файлів (list of str)

**Приклад: знайти всі Python-файли**

```python
import os

python_files = []
for root, dirs, files in os.walk("/home/user/projects"):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(root, file)
            python_files.append(full_path)

print(f"Знайдено {len(python_files)} Python файлів")
```

---

### **Слайд 9. Сучасний підхід: Path.rglob() та Path.glob()**

```python
from pathlib import Path

# glob() — пошук у поточній директорії (без рекурсії)
for file in Path("/var/log").glob("*.log"):
    print(file)

# rglob() — рекурсивний пошук (recursive glob)
for file in Path("/var/log").rglob("*.log"):
    print(file)

# Те саме, що ** в glob
for file in Path("/var/log").glob("**/*.log"):
    print(file)
```

🎯 **Патерни glob:**
- `*.py` — всі Python файли в поточній папці
- `**/*.py` — всі Python файли рекурсивно
- `test_*.py` — файли, що починаються з "test_"
- `**/[Cc]onfig.*` — файли Config.* або config.* в усіх папках

---

### **Слайд 10. Порівняння os.walk vs pathlib**

**os.walk — коли використовувати:**
```python
import os

# ✅ Добре для складної логіки обходу
for root, dirs, files in os.walk("/etc"):
    # Можна модифікувати dirs на місці, щоб пропустити певні папки
    dirs[:] = [d for d in dirs if not d.startswith('.')]

    for file in files:
        if file.endswith('.conf'):
            print(os.path.join(root, file))
```

**pathlib — коли використовувати:**
```python
from pathlib import Path

# ✅ Добре для простого пошуку за патерном
for config_file in Path("/etc").rglob("*.conf"):
    print(config_file)

# ✅ Працюємо з Path об'єктами одразу
for py_file in Path(".").rglob("*.py"):
    if py_file.stat().st_size > 1024:  # Більше 1KB
        print(f"{py_file.name}: {py_file.stat().st_size} bytes")
```

---

### **Слайд 11. Практичний приклад: обхід з фільтрацією**

```python
from pathlib import Path

def find_large_files(directory, min_size_mb=10):
    """Знайти файли більше заданого розміру"""
    min_size_bytes = min_size_mb * 1024 * 1024
    large_files = []

    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            if file_path.stat().st_size > min_size_bytes:
                size_mb = file_path.stat().st_size / (1024**2)
                large_files.append((file_path, size_mb))

    return sorted(large_files, key=lambda x: x[1], reverse=True)

# Використання
for file_path, size in find_large_files("/home/user", min_size_mb=100):
    print(f"{size:.2f} MB - {file_path}")
```

---

## 🔹 ЧАСТИНА 4. Розширений пошук файлів

---

### **Слайд 12. Пошук за масками (wildcards)**

```python
from pathlib import Path

# Прості маски
print("=== .log файли ===")
for f in Path("/var/log").glob("*.log"):
    print(f.name)

# Складні патерни
print("\n=== Лог-файли з датами ===")
for f in Path("/var/log").glob("app-*.log"):
    print(f.name)  # app-2024-11-09.log

# Рекурсивний пошук з множинними розширеннями
print("\n=== Конфігураційні файли ===")
for ext in ["*.conf", "*.cfg", "*.ini"]:
    for f in Path("/etc").rglob(ext):
        print(f)
```

**Wildcard символи:**
- `*` — будь-яка кількість будь-яких символів
- `?` — один будь-який символ
- `[abc]` — один символ з множини
- `[0-9]` — одна цифра
- `**` — рекурсивний обхід директорій

---

### **Слайд 13. Пошук за властивостями: розмір**

```python
from pathlib import Path

def find_by_size(directory, min_mb=None, max_mb=None):
    """Пошук файлів за розміром"""
    results = []

    for file_path in Path(directory).rglob("*"):
        if not file_path.is_file():
            continue

        size_mb = file_path.stat().st_size / (1024**2)

        # Перевірка діапазону
        if min_mb and size_mb < min_mb:
            continue
        if max_mb and size_mb > max_mb:
            continue

        results.append((file_path, size_mb))

    return results

# Знайти файли від 1 до 10 МБ
for path, size in find_by_size("/home/user/Downloads", min_mb=1, max_mb=10):
    print(f"{size:.2f} MB: {path.name}")
```

---

### **Слайд 14. Пошук за датою модифікації**

```python
from pathlib import Path
import datetime
import time

def find_modified_recently(directory, days=7):
    """Знайти файли, змінені за останні N днів"""
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    recent_files = []

    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            mtime = file_path.stat().st_mtime
            if mtime > cutoff_time:
                # Конвертуємо в читабельний формат
                mod_date = datetime.datetime.fromtimestamp(mtime)
                recent_files.append((file_path, mod_date))

    # Сортуємо за датою (найновіші спочатку)
    return sorted(recent_files, key=lambda x: x[1], reverse=True)

# Файли, змінені за останній тиждень
print("Файли змінені за останні 7 днів:")
for path, mod_date in find_modified_recently("/var/log", days=7):
    print(f"{mod_date.strftime('%Y-%m-%d %H:%M')} - {path}")
```

---

### **Слайд 15. Пошук за датою доступу (atime)**

```python
from pathlib import Path
import time

def find_unused_files(directory, days=90):
    """Знайти файли, до яких не зверталися N днів"""
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    unused = []

    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            atime = file_path.stat().st_atime
            if atime < cutoff_time:
                days_ago = (time.time() - atime) / (24 * 60 * 60)
                unused.append((file_path, days_ago))

    return sorted(unused, key=lambda x: x[1], reverse=True)

# Знайти файли, до яких не зверталися 90+ днів
print("Файли не використовувалися 90+ днів:")
for path, days in find_unused_files("/var/tmp", days=90):
    print(f"{int(days)} днів тому - {path}")
```

🛡️ **Застосування в безпеці:** Виявлення старих файлів для очищення, пошук підозрілих файлів за часовими мітками.

---

### **Слайд 16. Комбінований пошук**

```python
from pathlib import Path
import time

def advanced_search(directory, pattern="*", min_mb=None, max_mb=None,
                   modified_days=None, extension=None):
    """
    Універсальна функція пошуку з множинними критеріями
    """
    results = []

    # Базовий пошук за патерном
    for file_path in Path(directory).rglob(pattern):
        if not file_path.is_file():
            continue

        # Фільтр за розширенням
        if extension and not file_path.suffix == extension:
            continue

        stat_info = file_path.stat()
        size_mb = stat_info.st_size / (1024**2)

        # Фільтр за розміром
        if min_mb and size_mb < min_mb:
            continue
        if max_mb and size_mb > max_mb:
            continue

        # Фільтр за датою модифікації
        if modified_days:
            cutoff = time.time() - (modified_days * 24 * 60 * 60)
            if stat_info.st_mtime < cutoff:
                continue

        results.append(file_path)

    return results

# Приклад: знайти великі лог-файли, змінені за останні 7 днів
logs = advanced_search(
    "/var/log",
    pattern="*.log",
    min_mb=5,
    modified_days=7
)

for log in logs:
    print(log)
```

---

### **Слайд 17. 🛡️ Практичний кейс: Пошук підозрілих файлів**

```python
from pathlib import Path
import time

def find_suspicious_files(directory):
    """
    Знайти потенційно підозрілі файли:
    - Виконувані файли в незвичних місцях
    - Файли з подвійним розширенням
    - Приховані виконувані файли
    - Нещодавно створені/змінені системні файли
    """
    suspicious = []
    recent_threshold = time.time() - (24 * 60 * 60)  # Останні 24 години

    for file_path in Path(directory).rglob("*"):
        if not file_path.is_file():
            continue

        # Приховані виконувані файли
        if file_path.name.startswith('.') and file_path.suffix in ['.exe', '.sh', '.bat']:
            suspicious.append((file_path, "Прихований виконуваний файл"))

        # Подвійні розширення (file.pdf.exe)
        if len(file_path.suffixes) > 1:
            suspicious.append((file_path, "Подвійне розширення"))

        # Нещодавно змінені в системних директоріях
        if file_path.stat().st_mtime > recent_threshold:
            if "/etc/" in str(file_path) or "/bin/" in str(file_path):
                suspicious.append((file_path, "Нещодавня зміна системного файлу"))

    return suspicious

# Аналіз
for file_path, reason in find_suspicious_files("/home/user"):
    print(f"⚠️ {reason}: {file_path}")
```

---

## 🔹 ЧАСТИНА 5. Відмінності Windows vs Unix

---

### **Слайд 18. Роздільники шляхів**

**🐧 Unix/Linux/macOS:**
```python
# Роздільник: /
path = "/home/user/documents/file.txt"
```

**🪟 Windows:**
```python
# Роздільник: \
path = "C:\\Users\\User\\Documents\\file.txt"
# або можна використовувати /
path = "C:/Users/User/Documents/file.txt"  # Теж працює!
```

**✅ Кросплатформне рішення:**
```python
from pathlib import Path
import os

# Варіант 1: pathlib (рекомендовано)
path = Path.home() / "documents" / "file.txt"
print(path)  # Автоматично використає правильний роздільник

# Варіант 2: os.path.join
path = os.path.join(os.path.expanduser("~"), "documents", "file.txt")
print(path)

# Варіант 3: os.sep для явного роздільника
separator = os.sep  # '/' на Unix, '\\' на Windows
```

---

### **Слайд 19. Букви дисків (тільки Windows)**

**🪟 Windows:**
```python
from pathlib import Path

# Windows має букви дисків
path = Path("C:/Users/User/file.txt")
print(path.drive)  # "C:"
print(path.root)   # "\\"

# Різні диски
c_drive = Path("C:/")
d_drive = Path("D:/Data")
```

**🐧 Unix/Linux:**
```python
from pathlib import Path

# Unix не має дисків, все монтується в єдине дерево
path = Path("/home/user/file.txt")
print(path.drive)  # "" (порожній рядок)
print(path.root)   # "/"

# Монтування дисків/розділів
mounted = Path("/mnt/external_drive")
```

**✅ Кросплатформна перевірка:**
```python
from pathlib import Path
import platform

path = Path("/some/path")

if platform.system() == "Windows":
    # На Windows можуть бути диски
    if path.drive:
        print(f"Диск: {path.drive}")
else:
    # На Unix все починається з /
    print(f"Корінь: {path.root}")
```

---

### **Слайд 20. Чутливість до регістру**

**🐧 Unix/Linux:**
```python
# ЧУТЛИВИЙ до регістру
# file.txt ≠ File.txt ≠ FILE.TXT
# Всі три можуть існувати в одній папці!

from pathlib import Path
Path("readme.txt").touch()
Path("README.txt").touch()
Path("ReadMe.txt").touch()
# Створено 3 різні файли!
```

**🪟 Windows:**
```python
# НЕчутливий до регістру
# file.txt == File.txt == FILE.TXT

from pathlib import Path
Path("readme.txt").touch()
Path("README.txt").touch()  # Перезапише попередній!
# Існує тільки один файл
```

**✅ Безпечний код:**
```python
from pathlib import Path

def safe_file_check(filename):
    """Перевірка файлу з урахуванням регістру"""
    path = Path(filename)

    # Завжди використовуйте однаковий регістр
    # або перевіряйте існування перед створенням
    if path.exists():
        print(f"Файл вже існує: {path}")
        return True
    return False
```

---

### **Слайд 21. Права доступу (Permissions)**

**🐧 Unix/Linux — складна система прав:**
```python
import os
from pathlib import Path

file_path = Path("/etc/passwd")
stat_info = file_path.stat()

# Права доступу (rwxrwxrwx)
mode = oct(stat_info.st_mode)[-3:]
print(f"Права: {mode}")  # наприклад, "644"

# Власник та група
print(f"UID: {stat_info.st_uid}")
print(f"GID: {stat_info.st_gid}")

# Зміна прав
os.chmod("/tmp/test.txt", 0o644)  # rw-r--r--
```

**🪟 Windows — атрибути файлів:**
```python
import os
from pathlib import Path

# Windows використовує атрибути
file_path = Path("C:/Users/User/file.txt")

# Перевірка атрибутів
import stat
mode = file_path.stat().st_mode

is_readonly = not (mode & stat.S_IWRITE)
print(f"Тільки для читання: {is_readonly}")

# Windows має додаткові атрибути: Hidden, System, Archive
# Доступ через win32api (окрема бібліотека)
```

**✅ Кросплатформна робота:**
```python
import platform
from pathlib import Path

def make_readonly(file_path):
    """Зробити файл тільки для читання на будь-якій ОС"""
    path = Path(file_path)

    if platform.system() == "Windows":
        import stat
        path.chmod(stat.S_IREAD)
    else:  # Unix
        path.chmod(0o444)  # r--r--r--
```

---

### **Слайд 22. Закінчення рядків (Line Endings)**

**⚠️ Критична різниця!**

**🐧 Unix/Linux/macOS:**
```python
# LF (Line Feed): \n
text = "Рядок 1\nРядок 2\nРядок 3"
```

**🪟 Windows:**
```python
# CRLF (Carriage Return + Line Feed): \r\n
text = "Рядок 1\r\nРядок 2\r\nРядок 3"
```

**Проблема:**
```python
# Файл створений на Windows
with open("file.txt", "w") as f:
    f.write("Line 1\nLine 2")  # Windows додасть \r автоматично!

# Читання на Linux може дати: "Line 1\r\nLine 2"
```

**✅ Правильне рішення:**
```python
# Варіант 1: Текстовий режим (автоматична конвертація)
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()  # Python автоматично конвертує \r\n → \n

# Варіант 2: Явне видалення
lines = [line.rstrip('\r\n') for line in f]

# Варіант 3: Універсальний запис
with open("file.txt", "w", encoding="utf-8", newline='\n') as f:
    f.write("Line 1\nLine 2")  # Завжди \n
```

---

### **Слайд 23. Символічні посилання**

**🐧 Unix — повна підтримка symlinks:**
```python
from pathlib import Path

# Створення символічного посилання
source = Path("/var/log/app.log")
link = Path("/home/user/current_log")
link.symlink_to(source)

# Перевірка
print(link.is_symlink())  # True
print(link.resolve())     # /var/log/app.log (реальний шлях)
```

**🪟 Windows — обмежена підтримка:**
```python
from pathlib import Path

# На Windows потрібні права адміністратора!
# Або ввімкнений Developer Mode (Windows 10+)

try:
    source = Path("C:/logs/app.log")
    link = Path("C:/Users/User/current_log")
    link.symlink_to(source)
except OSError as e:
    print(f"Помилка: {e}")
    print("Потрібні права адміністратора на Windows")
```

---

### **Слайд 24. Заборонені символи в іменах файлів**

**🪟 Windows — жорсткіші обмеження:**
```python
# Заборонені символи: < > : " / \ | ? *
invalid_chars = '<>:"/\\|?*'

# Також заборонені імена:
reserved_names = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "LPT1", "LPT2"
]
```

**🐧 Unix — менше обмежень:**
```python
# Заборонені тільки: / та \0 (null byte)
# Всі інші символи дозволені (але не рекомендовані)
```

**✅ Безпечне створення імен:**
```python
import re
from pathlib import Path

def sanitize_filename(filename):
    """Очистити ім'я файлу для кросплатформності"""
    # Видалити всі небезпечні символи
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Видалити керуючі символи
    filename = re.sub(r'[\x00-\x1f]', '', filename)

    # Обмежити довжину (255 символів — max для більшості ФС)
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext

    return filename

# Приклад
unsafe_name = 'report:2024/11/09|v2.txt'
safe_name = sanitize_filename(unsafe_name)
print(safe_name)  # "report_2024_11_09_v2.txt"
```

---

### **Слайд 25. Визначення ОС і кросплатформний код**

```python
import platform
import sys
from pathlib import Path

def get_system_info():
    """Отримати інформацію про систему"""
    return {
        "platform": platform.system(),      # Windows, Linux, Darwin (macOS)
        "release": platform.release(),      # Версія ОС
        "version": platform.version(),      # Детальна версія
        "machine": platform.machine(),      # x86_64, AMD64, etc.
        "python_version": sys.version,
        "path_separator": os.sep,           # / або \
        "pathsep": os.pathsep,              # : або ;
    }

# Використання
info = get_system_info()
for key, value in info.items():
    print(f"{key}: {value}")
```

**Умовна логіка:**
```python
import platform

if platform.system() == "Windows":
    log_dir = Path("C:/Logs")
elif platform.system() == "Linux":
    log_dir = Path("/var/log/myapp")
elif platform.system() == "Darwin":  # macOS
    log_dir = Path("/usr/local/var/log/myapp")
else:
    log_dir = Path.home() / "logs"  # Резервний варіант

log_dir.mkdir(parents=True, exist_ok=True)
```

---

### **Слайд 26. 🔧 Best Practices для кросплатформності**

**✅ DO (Робити):**

```python
from pathlib import Path

# 1. Використовуйте pathlib
config = Path.home() / ".config" / "app" / "settings.json"

# 2. Використовуйте Path.home() замість хардкоду
home = Path.home()  # Працює на всіх ОС

# 3. Перевіряйте існування перед операціями
if config.exists():
    data = config.read_text()

# 4. Використовуйте exist_ok для створення директорій
Path("logs/2024").mkdir(parents=True, exist_ok=True)

# 5. Обробляйте помилки
try:
    file_path.unlink()
except PermissionError:
    print("Немає прав для видалення")
```

**❌ DON'T (Не робити):**

```python
# ❌ Хардкод шляхів
config = "C:\\Users\\User\\.config\\app\\settings.json"

# ❌ Ручне склеювання шляхів
path = directory + "/" + filename  # Не працює на Windows

# ❌ Припущення про регістр
if filename == "README.txt":  # Може не працювати на Unix

# ❌ Ігнорування помилок ОС
file_path.unlink()  # Може вибухнути на Windows, якщо файл відкритий
```

---

## 🔹 Самостійна робота

---

### **Слайд 27. Завдання: Утиліта пошуку файлів**

**Створіть програму `file_finder.py`, яка:**

1. Приймає аргументи командного рядка:
   - Шлях до директорії для пошуку
   - Маску файлів (наприклад, `*.log`)
   - Мінімальний/максимальний розмір
   - Період модифікації (останні N днів)

2. Шукає файли за критеріями

3. Виводить результати у вигляді таблиці:
   ```
   Знайдено 15 файлів:

   Розмір    Дата модифікації    Шлях
   -------   -----------------   ----
   2.5 MB    2024-11-08 14:23    /var/log/app.log
   1.2 MB    2024-11-07 09:15    /var/log/error.log
   ```

4. Опціонально: експорт результатів у JSON/CSV

---

### **Слайд 28. Додаткове завдання (advanced)**

**Створіть інструмент аналізу файлової системи:**

```python
"""
Програма повинна:
1. Проаналізувати задану директорію рекурсивно
2. Зібрати статистику:
   - Кількість файлів за типами (розширеннями)
   - Розподіл за розміром (0-1MB, 1-10MB, 10-100MB, 100MB+)
   - Топ-10 найбільших файлів
   - Файли, старші за 1 рік
   - Дублікати (за розміром і іменем)
3. Вивести звіт у форматі:
   - Консоль (форматована таблиця)
   - JSON файл
   - HTML звіт з графіками (опціонально)
"""
```

**Підказка:** Використайте `collections.Counter` для підрахунку.

---

## 📊 Підсумки лекції

✅ **Освоїли сучасний підхід з `pathlib`**
- Об'єктно-орієнтована робота зі шляхами
- Кросплатформність "з коробки"

✅ **Розуміємо властивості файлів**
- atime, mtime, ctime та їх відмінності
- Різниця ctime між Unix та Windows!

✅ **Вміємо обходити директорії**
- `os.walk()` для складної логіки
- `Path.rglob()` для простого пошуку

✅ **Можемо шукати файли за критеріями**
- За маскою/патерном
- За розміром, датою, властивостями
- Комбінований пошук

✅ **Усвідомлюємо відмінності ОС**
- Шляхи, диски, регістр
- Права доступу та атрибути
- Написання кросплатформного коду

---

## 🔜 Далі (Заняття 11: Автоматизація файлових операцій)

На наступному занятті ми вивчимо:
- Timestamping (додавання міток часу до файлів)
- Масові операції з файлами через `shutil`
- Ротацію файлів (що це і навіщо)
- Архівування та компресію
- Створення систем резервного копіювання

---

## 📚 Додаткові матеріали

**Документація:**
- [pathlib — офіційна документація](https://docs.python.org/3/library/pathlib.html)
- [os — модуль для роботи з ОС](https://docs.python.org/3/library/os.html)
- [glob — Unix style pathname pattern expansion](https://docs.python.org/3/library/glob.html)

**Для поглибленого вивчення:**
- [Real Python: Python's pathlib Module](https://realpython.com/python-pathlib/)
- [File permissions explained](https://www.redhat.com/sysadmin/linux-file-permissions-explained)

**Код з лекції:** [code_examples.py](code_examples.py)

**Практичні завдання:** [tasks.md](tasks.md)
