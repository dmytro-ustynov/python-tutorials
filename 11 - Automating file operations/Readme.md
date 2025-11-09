
## 🎓 **ЗАНЯТТЯ 5.3: Автоматизація файлових операцій**

### 🕐 Загальний час: 2 години (лекція) + 0.75 год самостійна робота

### 🎯 **Мета:**

Навчитися автоматизувати рутинні файлові операції: копіювання, переміщення, архівування файлів, створення резервних копій з мітками часу та впровадження систем ротації файлів.

---

## 🧩 СТРУКТУРА ЗАНЯТТЯ

**План:**

1. Timestamping — додавання міток часу до файлів
2. Масові операції з модулем `shutil`
3. Ротація файлів — що це і навіщо
4. Робота з архівами (ZIP, TAR, стиснення)
5. Практичний проєкт: система автоматичного резервного копіювання

**Самостійна робота:** Створення власної системи backup з ротацією

---

## 🔹 ЧАСТИНА 1. Timestamping — мітки часу для файлів

---

### **Слайд 1. Навіщо потрібні мітки часу?**

**Проблема:**
```python
# Погані назви файлів
backup.zip
backup_new.zip
backup_final.zip
backup_final_v2.zip  # 😱
```

**Рішення:**
```python
# Назви з мітками часу
backup_2024-11-09_14-30-00.zip
backup_2024-11-09_15-45-12.zip
backup_2024-11-10_09-20-33.zip
```

🎯 **Переваги:**
- Легко сортувати (алфавітний порядок = хронологічний)
- Зрозуміло, коли створено файл
- Немає конфліктів імен
- Автоматичне версіонування

**Застосування в кібербезпеці:**
- Логи з мітками часу
- Резервні копії конфігурацій
- Знімки системи (snapshots)
- Форензика — точна часова лінія подій

---

### **Слайд 2. Формати часу в Python**

```python
import datetime

# Поточний час
now = datetime.datetime.now()
print(now)  # 2024-11-09 14:30:45.123456

# Різні формати для файлів
timestamp_1 = now.strftime("%Y-%m-%d_%H-%M-%S")
print(timestamp_1)  # 2024-11-09_14-30-45

timestamp_2 = now.strftime("%Y%m%d_%H%M%S")
print(timestamp_2)  # 20241109_143045

timestamp_3 = now.strftime("%Y-%m-%d")
print(timestamp_3)  # 2024-11-09

# ISO 8601 формат (міжнародний стандарт)
timestamp_iso = now.isoformat()
print(timestamp_iso)  # 2024-11-09T14:30:45.123456

# Unix timestamp (секунди з 1970-01-01)
timestamp_unix = int(now.timestamp())
print(timestamp_unix)  # 1699537845
```

📋 **Коди форматування:**
- `%Y` — рік (4 цифри): 2024
- `%m` — місяць: 01-12
- `%d` — день: 01-31
- `%H` — година (24-год): 00-23
- `%M` — хвилини: 00-59
- `%S` — секунди: 00-59

---

### **Слайд 3. Створення файлів з мітками часу**

```python
from pathlib import Path
import datetime

def create_timestamped_filename(base_name, extension):
    """Створити ім'я файлу з міткою часу"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{base_name}_{timestamp}.{extension}"

# Використання
log_file = create_timestamped_filename("app_log", "txt")
print(log_file)  # app_log_2024-11-09_14-30-45.txt

backup_file = create_timestamped_filename("backup", "zip")
print(backup_file)  # backup_2024-11-09_14-30-45.zip

# Створення файлу
log_path = Path("logs") / log_file
log_path.parent.mkdir(exist_ok=True)
log_path.write_text("Log started\n")
```

---

### **Слайд 4. Lifehack: Сортування за часом**

```python
from pathlib import Path
import datetime

def get_timestamp_from_filename(filename):
    """Витягти timestamp з назви файлу"""
    # Припустимо формат: backup_2024-11-09_14-30-45.zip
    parts = filename.stem.split('_')
    if len(parts) >= 3:
        date_part = parts[-2]  # 2024-11-09
        time_part = parts[-1]  # 14-30-45
        timestamp_str = f"{date_part} {time_part.replace('-', ':')}"
        return datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return None

# Знайти всі backup файли
backups = list(Path("backups").glob("backup_*.zip"))

# Сортування за часом (від найстарішого до найновішого)
sorted_backups = sorted(backups, key=lambda x: get_timestamp_from_filename(x.name))

print("Резервні копії (хронологічно):")
for backup in sorted_backups:
    ts = get_timestamp_from_filename(backup.name)
    print(f"  {backup.name} - {ts}")
```

---

### **Слайд 5. Практичний приклад: Автоматичне логування**

```python
from pathlib import Path
import datetime

class TimestampedLogger:
    """Логер з автоматичними мітками часу"""

    def __init__(self, log_dir="logs", app_name="app"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.app_name = app_name

        # Створити лог-файл на сьогодні
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.log_dir / f"{app_name}_{today}.log"

    def log(self, message):
        """Записати повідомлення з міткою часу"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(log_entry.strip())

# Використання
logger = TimestampedLogger(app_name="security_monitor")
logger.log("System started")
logger.log("Checking for intrusions...")
logger.log("All systems normal")
```

---

## 🔹 ЧАСТИНА 2. Масові операції з модулем `shutil`

---

### **Слайд 6. Модуль shutil — швейцарський ніж для файлів**

**shutil** (shell utilities) — модуль для високорівневих файлових операцій.

```python
import shutil

# Основні функції:
shutil.copy()       # Копіювання файлу
shutil.copy2()      # Копіювання з метаданими
shutil.copytree()   # Копіювання директорії
shutil.move()       # Переміщення/перейменування
shutil.rmtree()     # Видалення директорії
shutil.disk_usage() # Інформація про диск
```

🔹 **Відмінність від os:**
- `os` — низькорівневі операції
- `shutil` — високорівневі, зручніші

---

### **Слайд 7. Копіювання файлів**

```python
import shutil
from pathlib import Path

# copy() — копіює тільки вміст
shutil.copy("source.txt", "destination.txt")

# copy2() — копіює вміст + метадані (mtime, permissions)
shutil.copy2("source.txt", "destination.txt")

# copyfile() — тільки вміст, без прав доступу
shutil.copyfile("source.txt", "destination.txt")
```

**Різниця між copy() та copy2():**

```python
import shutil
import os
from pathlib import Path

source = Path("important.txt")
source.write_text("Important data")

# copy() — втрачає метадані
shutil.copy(source, "copy1.txt")

# copy2() — зберігає метадані
shutil.copy2(source, "copy2.txt")

# Перевірка
print(f"Оригінал mtime: {source.stat().st_mtime}")
print(f"copy() mtime: {Path('copy1.txt').stat().st_mtime}")
print(f"copy2() mtime: {Path('copy2.txt').stat().st_mtime}")
```

🎯 **Коли використовувати copy2():**
- Резервне копіювання
- Збереження форензичних доказів
- Міграція файлів

---

### **Слайд 8. Копіювання директорій**

```python
import shutil
from pathlib import Path

# Копіювання всієї директорії
shutil.copytree("source_folder", "destination_folder")

# З ігноруванням певних файлів
shutil.copytree(
    "source_folder",
    "destination_folder",
    ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git")
)

# Приклад з функцією ignore
def ignore_large_files(directory, files):
    """Ігнорувати файли більше 10 MB"""
    ignore = []
    for file in files:
        file_path = Path(directory) / file
        if file_path.is_file() and file_path.stat().st_size > 10 * 1024 * 1024:
            ignore.append(file)
    return ignore

shutil.copytree(
    "source_folder",
    "destination_folder",
    ignore=ignore_large_files
)
```

---

### **Слайд 9. Переміщення та видалення**

```python
import shutil
from pathlib import Path

# Переміщення файлу або директорії
shutil.move("old_location/file.txt", "new_location/file.txt")

# Перейменування
shutil.move("old_name.txt", "new_name.txt")

# Видалення директорії з усім вмістом
shutil.rmtree("directory_to_delete")

# Безпечне видалення (з перевіркою)
if Path("temp_folder").exists():
    shutil.rmtree("temp_folder")
    print("Директорію видалено")
```

⚠️ **УВАГА:** `rmtree()` видаляє **безповоротно**! Немає "смітника".

---

### **Слайд 10. Інформація про диск**

```python
import shutil

# Отримати інформацію про використання диска
usage = shutil.disk_usage("/")

print(f"Всього: {usage.total / (1024**3):.2f} GB")
print(f"Використано: {usage.used / (1024**3):.2f} GB")
print(f"Вільно: {usage.free / (1024**3):.2f} GB")
print(f"Відсоток використання: {usage.used / usage.total * 100:.1f}%")

# Перевірка перед операцією
def check_disk_space(required_mb):
    """Перевірити, чи достатньо місця на диску"""
    free_mb = shutil.disk_usage("/").free / (1024**2)
    return free_mb > required_mb

if check_disk_space(1000):  # 1 GB
    print("Достатньо місця для backup")
else:
    print("⚠️ Недостатньо вільного місця!")
```

---

### **Слайд 11. Масове копіювання з фільтрацією**

```python
import shutil
from pathlib import Path
import datetime
import time

def backup_recent_files(source_dir, backup_dir, days=7):
    """
    Копіювати тільки файли, змінені за останні N днів
    """
    source = Path(source_dir)
    backup = Path(backup_dir)
    backup.mkdir(exist_ok=True)

    cutoff_time = time.time() - (days * 24 * 60 * 60)
    copied_count = 0

    for file_path in source.rglob("*"):
        if file_path.is_file():
            # Перевірити час модифікації
            if file_path.stat().st_mtime > cutoff_time:
                # Зберегти структуру директорій
                relative_path = file_path.relative_to(source)
                dest_path = backup / relative_path

                # Створити батьківські директорії
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Копіювати з метаданими
                shutil.copy2(file_path, dest_path)
                copied_count += 1

    print(f"Скопійовано {copied_count} файлів")

# Використання
backup_recent_files("/home/user/documents", "/backup/documents", days=7)
```

---

## 🔹 ЧАСТИНА 3. Ротація файлів

---

### **Слайд 12. Що таке ротація файлів?**

**Ротація (rotation)** — це процес автоматичного управління файлами для:
- Контролю розміру
- Економії дискового простору
- Збереження історії
- Відповідності політикам

**Приклад без ротації:**
```
app.log → 5 GB 😱
```

**Приклад з ротацією:**
```
app.log           → 10 MB (поточний)
app.log.1         → 10 MB (вчорашній)
app.log.2         → 10 MB (позавчорашній)
app.log.3         → 10 MB
...
app.log.2024-11-01.gz  → архів
```

---

### **Слайд 13. Види ротації**

**1. Ротація за розміром:**
```
Коли app.log досягає 10 MB:
  app.log → app.log.1
  створити новий app.log
```

**2. Ротація за часом:**
```
Щоденно о 00:00:
  app.log → app.log.2024-11-09
  створити новий app.log
```

**3. Ротація за кількістю:**
```
Зберігати тільки останні N файлів:
  app.log.1, app.log.2, ..., app.log.7
  app.log.8 → видалити
```

**4. Комбінована:**
```
Щодня створювати новий файл +
Зберігати останні 30 днів +
Архівувати старіші файли
```

---

### **Слайд 14. Проста ротація за кількістю**

```python
from pathlib import Path
import shutil

def rotate_files(base_name, max_count=5):
    """
    Ротувати файли: file.log → file.log.1 → file.log.2 ...
    Зберігати максимум max_count старих версій
    """
    base_path = Path(base_name)

    # Видалити найстаріший файл
    oldest = Path(f"{base_name}.{max_count}")
    if oldest.exists():
        oldest.unlink()

    # Зсунути всі файли: .3 → .4, .2 → .3, .1 → .2
    for i in range(max_count - 1, 0, -1):
        old_file = Path(f"{base_name}.{i}")
        new_file = Path(f"{base_name}.{i + 1}")

        if old_file.exists():
            shutil.move(old_file, new_file)

    # Поточний файл → .1
    if base_path.exists():
        shutil.move(base_path, f"{base_name}.1")

    # Створити новий файл
    base_path.touch()

    print(f"Ротація завершена. Зберігається {max_count} версій.")

# Використання
rotate_files("app.log", max_count=5)
```

---

### **Слайд 15. Ротація за часом (щоденна)**

```python
from pathlib import Path
import datetime
import shutil

def rotate_by_date(log_file):
    """
    Ротувати лог-файл щоденно
    app.log → app.log.2024-11-09
    """
    log_path = Path(log_file)

    if not log_path.exists():
        log_path.touch()
        return

    # Отримати дату останньої модифікації
    mtime = log_path.stat().st_mtime
    file_date = datetime.datetime.fromtimestamp(mtime).date()
    today = datetime.date.today()

    # Якщо файл старіший за сьогодні — ротувати
    if file_date < today:
        # Новий файл з датою
        dated_name = f"{log_path.stem}.{file_date}.log"
        dated_path = log_path.parent / dated_name

        # Перемістити
        shutil.move(log_path, dated_path)

        # Створити новий файл
        log_path.touch()

        print(f"Лог заротовано: {dated_name}")

# Використання (викликати щодня, наприклад через cron)
rotate_by_date("app.log")
```

---

### **Слайд 16. Ротація з архівуванням**

```python
from pathlib import Path
import datetime
import shutil
import gzip

def rotate_and_compress(log_file, keep_days=7):
    """
    Ротувати та стиснути старі логи
    Видаляти логи старші за keep_days
    """
    log_path = Path(log_file)

    if not log_path.exists():
        return

    # Створити ім'я з датою
    today = datetime.date.today()
    dated_name = f"{log_path.stem}.{today}.log"
    dated_path = log_path.parent / dated_name

    # Перемістити поточний лог
    if log_path.stat().st_size > 0:
        shutil.move(log_path, dated_path)

        # Стиснути
        gz_path = Path(f"{dated_path}.gz")
        with open(dated_path, 'rb') as f_in:
            with gzip.open(gz_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Видалити нестиснутий
        dated_path.unlink()
        print(f"Лог стиснуто: {gz_path.name}")

    # Створити новий лог
    log_path.touch()

    # Очистити старі логи
    cutoff_date = today - datetime.timedelta(days=keep_days)

    for old_log in log_path.parent.glob(f"{log_path.stem}.*.log.gz"):
        # Витягти дату з імені файлу
        try:
            date_str = old_log.stem.split('.')[-2]  # 2024-11-09
            log_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            if log_date < cutoff_date:
                old_log.unlink()
                print(f"Видалено старий лог: {old_log.name}")
        except:
            pass

# Використання
rotate_and_compress("app.log", keep_days=30)
```

---

### **Слайд 17. 🛡️ Застосування в кібербезпеці**

**Логування подій безпеки:**
```python
class SecurityLogger:
    """Логер подій безпеки з автоматичною ротацією"""

    def __init__(self, log_dir="security_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def log_event(self, event_type, message):
        """Записати подію безпеки"""
        today = datetime.date.today()
        log_file = self.log_dir / f"security_{today}.log"

        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"{timestamp}|{event_type}|{message}\n"

        with open(log_file, 'a') as f:
            f.write(log_entry)

    def rotate_old_logs(self, keep_days=90):
        """Ротувати логи (GDPR compliance: 90 днів)"""
        cutoff = datetime.date.today() - datetime.timedelta(days=keep_days)

        for log_file in self.log_dir.glob("security_*.log"):
            # Витягти дату
            date_str = log_file.stem.split('_')[1]
            log_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            if log_date < cutoff:
                # Архівувати або видалити
                archive_dir = self.log_dir / "archive"
                archive_dir.mkdir(exist_ok=True)
                shutil.move(log_file, archive_dir / log_file.name)

# Використання
sec_log = SecurityLogger()
sec_log.log_event("LOGIN_FAILED", "User admin from 192.168.1.100")
sec_log.log_event("SUSPICIOUS_ACTIVITY", "Multiple failed attempts")
sec_log.rotate_old_logs(keep_days=90)
```

---

## 🔹 ЧАСТИНА 4. Робота з архівами

---

### **Слайд 18. Типи архівів**

**ZIP:**
- Найпопулярніший формат
- Вбудована підтримка в Python (`zipfile`)
- Підтримка стиснення
- Кросплатформний

**TAR (+ стиснення):**
- `.tar` — без стиснення (просто пакування)
- `.tar.gz` (`.tgz`) — стиснення gzip
- `.tar.bz2` — стиснення bzip2 (краще, але повільніше)
- `.tar.xz` — стиснення LZMA (найкраще стиснення)

**Вибір формату:**
```python
# ZIP — для Windows сумісності
# TAR.GZ — для Unix систем (логи, backups)
# TAR.BZ2 — для максимального стиснення
```

---

### **Слайд 19. Створення ZIP архіву**

```python
import zipfile
from pathlib import Path

def create_zip(source_dir, output_zip):
    """Створити ZIP архів директорії"""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        source_path = Path(source_dir)

        for file in source_path.rglob("*"):
            if file.is_file():
                # Відносний шлях для зберігання структури
                arcname = file.relative_to(source_path.parent)
                zipf.write(file, arcname)
                print(f"Додано: {arcname}")

    print(f"Архів створено: {output_zip}")

# Використання
create_zip("my_project", "my_project.zip")
```

---

### **Слайд 20. Розпакування ZIP архіву**

```python
import zipfile
from pathlib import Path

def extract_zip(zip_file, extract_to="."):
    """Розпакувати ZIP архів"""
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        # Показати вміст
        print("Вміст архіву:")
        for info in zipf.filelist:
            print(f"  {info.filename} ({info.file_size} bytes)")

        # Розпакувати
        zipf.extractall(extract_to)
        print(f"\nРозпаковано в: {extract_to}")

# Використання
extract_zip("my_project.zip", "extracted")
```

---

### **Слайд 21. Перегляд вмісту архіву**

```python
import zipfile

def list_zip_contents(zip_file):
    """Показати детальну інформацію про вміст ZIP"""
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        print(f"Архів: {zip_file}")
        print("-" * 70)
        print(f"{'Файл':<40} {'Розмір':>12} {'Стиснутий':>12}")
        print("-" * 70)

        total_size = 0
        total_compressed = 0

        for info in zipf.filelist:
            print(f"{info.filename:<40} {info.file_size:>12} {info.compress_size:>12}")
            total_size += info.file_size
            total_compressed += info.compress_size

        print("-" * 70)
        ratio = (1 - total_compressed / total_size) * 100 if total_size > 0 else 0
        print(f"Всього: {total_size:,} bytes → {total_compressed:,} bytes ({ratio:.1f}% стиснення)")

# Використання
list_zip_contents("my_project.zip")
```

---

### **Слайд 22. Створення TAR.GZ архіву**

```python
import tarfile
from pathlib import Path

def create_targz(source_dir, output_tar):
    """Створити TAR.GZ архів"""
    with tarfile.open(output_tar, "w:gz") as tar:
        source_path = Path(source_dir)

        for file in source_path.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(source_path.parent)
                tar.add(file, arcname=arcname)
                print(f"Додано: {arcname}")

    print(f"Архів створено: {output_tar}")

# Використання
create_targz("logs", "logs_backup.tar.gz")
```

**Варіанти стиснення:**
```python
# Без стиснення
tarfile.open("archive.tar", "w")

# gzip (швидко, середнє стиснення)
tarfile.open("archive.tar.gz", "w:gz")

# bzip2 (повільно, краще стиснення)
tarfile.open("archive.tar.bz2", "w:bz2")

# lzma/xz (найповільніше, найкраще стиснення)
tarfile.open("archive.tar.xz", "w:xz")
```

---

### **Слайд 23. Розпакування TAR архівів**

```python
import tarfile

def extract_tar(tar_file, extract_to="."):
    """Розпакувати TAR архів (автоматично визначає тип стиснення)"""
    with tarfile.open(tar_file, "r:*") as tar:
        # Перевірка безпеки (path traversal attack)
        for member in tar.getmembers():
            if member.name.startswith('/') or '..' in member.name:
                print(f"⚠️ Небезпечний шлях: {member.name}")
                continue

        # Безпечне розпакування
        tar.extractall(extract_to)
        print(f"Розпаковано в: {extract_to}")

# Використання
extract_tar("logs_backup.tar.gz", "restored_logs")
```

⚠️ **Безпека:** Завжди перевіряйте шляхи при розпакуванні!

---

### **Слайд 24. Стиснення окремих файлів (gzip)**

```python
import gzip
import shutil

def compress_file(input_file, output_file=None):
    """Стиснути файл за допомогою gzip"""
    if output_file is None:
        output_file = f"{input_file}.gz"

    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"Стиснуто: {output_file}")

def decompress_file(input_file, output_file=None):
    """Розпакувати gzip файл"""
    if output_file is None:
        output_file = input_file.rsplit('.gz', 1)[0]

    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"Розпаковано: {output_file}")

# Використання
compress_file("large_log.log")  # → large_log.log.gz
decompress_file("large_log.log.gz")  # → large_log.log
```

---

### **Слайд 25. Вибір методу стиснення**

```python
import zipfile
import tarfile
import gzip
import time
from pathlib import Path

def compare_compression(source_dir):
    """Порівняти різні методи стиснення"""
    results = {}

    # ZIP
    start = time.time()
    with zipfile.ZipFile("test.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in Path(source_dir).rglob("*"):
            if file.is_file():
                zipf.write(file)
    results['ZIP'] = {
        'time': time.time() - start,
        'size': Path("test.zip").stat().st_size
    }

    # TAR.GZ
    start = time.time()
    with tarfile.open("test.tar.gz", "w:gz") as tar:
        tar.add(source_dir)
    results['TAR.GZ'] = {
        'time': time.time() - start,
        'size': Path("test.tar.gz").stat().st_size
    }

    # TAR.BZ2
    start = time.time()
    with tarfile.open("test.tar.bz2", "w:bz2") as tar:
        tar.add(source_dir)
    results['TAR.BZ2'] = {
        'time': time.time() - start,
        'size': Path("test.tar.bz2").stat().st_size
    }

    # Результати
    print("Порівняння методів стиснення:")
    print(f"{'Метод':<15} {'Час (сек)':>12} {'Розмір (MB)':>15}")
    print("-" * 45)

    for method, data in results.items():
        print(f"{method:<15} {data['time']:>12.2f} {data['size']/(1024**2):>15.2f}")

# Використання
compare_compression("my_project")
```

---

## 🔹 ЧАСТИНА 5. Практичний проєкт: Система резервного копіювання

---

### **Слайд 26. Вимоги до backup системи**

**Функціональність:**
1. ✅ Створення резервних копій з міткою часу
2. ✅ Стиснення архіву
3. ✅ Ротація старих backup'ів (зберігати останні N)
4. ✅ Перевірка вільного місця перед backup
5. ✅ Логування всіх операцій
6. ✅ Можливість відновлення

**Бонус:**
- Інкрементальні backup'и (тільки змінені файли)
- Конфігураційний файл
- Виключення файлів (ignore patterns)

---

### **Слайд 27. Архітектура backup системи**

```python
from pathlib import Path
import datetime
import shutil
import tarfile
import logging

class BackupSystem:
    """Автоматична система резервного копіювання"""

    def __init__(self, source_dir, backup_dir, keep_count=7):
        self.source = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.keep_count = keep_count

        # Створити директорію для backup
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Налаштувати логування
        self._setup_logging()

    def _setup_logging(self):
        """Налаштувати логер"""
        log_file = self.backup_dir / "backup.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_backup(self):
        """Створити резервну копію"""
        # Генерувати ім'я з timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{self.source.name}_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name

        self.logger.info(f"Початок backup: {self.source} → {backup_path}")

        # Перевірити місце на диску
        if not self._check_disk_space():
            self.logger.error("Недостатньо місця на диску!")
            return False

        try:
            # Створити архів
            with tarfile.open(backup_path, "w:gz") as tar:
                tar.add(self.source, arcname=self.source.name)

            size_mb = backup_path.stat().st_size / (1024 ** 2)
            self.logger.info(f"Backup створено: {backup_name} ({size_mb:.2f} MB)")

            # Ротувати старі backup'и
            self._rotate_backups()

            return True

        except Exception as e:
            self.logger.error(f"Помилка створення backup: {e}")
            return False

    def _check_disk_space(self, required_mb=100):
        """Перевірити вільне місце"""
        usage = shutil.disk_usage(self.backup_dir)
        free_mb = usage.free / (1024 ** 2)
        return free_mb > required_mb

    def _rotate_backups(self):
        """Видалити старі backup'и"""
        # Знайти всі backup файли
        backups = sorted(
            self.backup_dir.glob("backup_*.tar.gz"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        # Видалити старіші за keep_count
        for old_backup in backups[self.keep_count:]:
            old_backup.unlink()
            self.logger.info(f"Видалено старий backup: {old_backup.name}")

    def restore_backup(self, backup_file, restore_to):
        """Відновити з backup"""
        backup_path = self.backup_dir / backup_file
        restore_path = Path(restore_to)

        self.logger.info(f"Відновлення: {backup_file} → {restore_to}")

        try:
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(restore_path)

            self.logger.info("Відновлення успішне")
            return True

        except Exception as e:
            self.logger.error(f"Помилка відновлення: {e}")
            return False

    def list_backups(self):
        """Показати список backup'ів"""
        backups = sorted(
            self.backup_dir.glob("backup_*.tar.gz"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        print(f"\nДоступні backup'и ({len(backups)}):")
        print("-" * 70)
        print(f"{'Файл':<40} {'Дата':>20} {'Розмір':>10}")
        print("-" * 70)

        for backup in backups:
            mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
            size_mb = backup.stat().st_size / (1024 ** 2)
            print(f"{backup.name:<40} {mtime.strftime('%Y-%m-%d %H:%M:%S'):>20} {size_mb:>8.2f} MB")
```

---

### **Слайд 28. Використання backup системи**

```python
# Створити backup систему
backup = BackupSystem(
    source_dir="/home/user/important_data",
    backup_dir="/backup",
    keep_count=7  # Зберігати останні 7 backup'ів
)

# Створити backup
backup.create_backup()

# Показати список backup'ів
backup.list_backups()

# Відновити з backup
backup.restore_backup(
    backup_file="backup_important_data_2024-11-09_14-30-00.tar.gz",
    restore_to="/home/user/restored"
)
```

---

### **Слайд 29. Розширення: Інкрементальний backup**

```python
import hashlib
import json

class IncrementalBackup(BackupSystem):
    """Backup з підтримкою інкрементальних копій"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manifest_file = self.backup_dir / "manifest.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        """Завантажити маніфест (список файлів + hash)"""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_manifest(self):
        """Зберегти маніфест"""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def _calculate_hash(self, file_path):
        """Обчислити MD5 hash файлу"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    def create_incremental_backup(self):
        """Створити інкрементальний backup (тільки змінені файли)"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"incremental_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name

        changed_files = []

        # Знайти змінені файли
        for file in self.source.rglob("*"):
            if file.is_file():
                file_hash = self._calculate_hash(file)
                relative_path = str(file.relative_to(self.source))

                # Перевірити, чи файл змінився
                if relative_path not in self.manifest or self.manifest[relative_path] != file_hash:
                    changed_files.append(file)
                    self.manifest[relative_path] = file_hash

        if not changed_files:
            self.logger.info("Немає змінених файлів")
            return

        # Створити архів тільки зі зміненими файлами
        with tarfile.open(backup_path, "w:gz") as tar:
            for file in changed_files:
                arcname = file.relative_to(self.source)
                tar.add(file, arcname=arcname)

        self._save_manifest()
        self.logger.info(f"Інкрементальний backup: {len(changed_files)} файлів")
```

---

### **Слайд 30. Автоматизація через cron/scheduler**

**Linux/macOS (cron):**
```bash
# Запускати backup щодня о 2:00 ночі
0 2 * * * /usr/bin/python3 /home/user/backup_script.py
```

**Python планувальник:**
```python
import schedule
import time

def daily_backup():
    """Щоденний backup"""
    backup = BackupSystem(
        source_dir="/home/user/documents",
        backup_dir="/backup",
        keep_count=30
    )
    backup.create_backup()

# Запускати щодня о 02:00
schedule.every().day.at("02:00").do(daily_backup)

# Або щотижня в понеділок
schedule.every().monday.at("03:00").do(daily_backup)

# Головний цикл
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📊 Підсумки лекції

✅ **Timestamping**
- Формати часу для файлів
- Автоматичне версіонування
- Сортування за часом

✅ **Модуль shutil**
- copy, copy2, copytree
- move, rmtree
- disk_usage
- Масові операції

✅ **Ротація файлів**
- Види ротації (розмір, час, кількість)
- Практичні реалізації
- Застосування для логів

✅ **Архівування**
- ZIP, TAR, стиснення
- Вибір формату
- Безпека при розпакуванні

✅ **Система backup**
- Автоматизація
- Ротація
- Інкрементальні копії

---

## 🔜 Що далі?

На наступних заняттях:
- **Робота з базами даних** (SQLite, PostgreSQL)
- **Автоматизація з subprocess**
- **Моніторинг системи**
- **Безпека файлових операцій**

---

## 📚 Додаткові матеріали

**Документація:**
- [shutil — офіційна документація](https://docs.python.org/3/library/shutil.html)
- [zipfile — робота з ZIP](https://docs.python.org/3/library/zipfile.html)
- [tarfile — робота з TAR](https://docs.python.org/3/library/tarfile.html)
- [datetime — робота з часом](https://docs.python.org/3/library/datetime.html)

**Корисні бібліотеки:**
- `schedule` — планування задач
- `watchdog` — моніторинг файлової системи
- `send2trash` — безпечне видалення (в смітник)

**Код з лекції:** [code_examples.py](code_examples.py)

**Практичні завдання:** [tasks.md](tasks.md)

---

**🎓 Кінець Заняття 11**