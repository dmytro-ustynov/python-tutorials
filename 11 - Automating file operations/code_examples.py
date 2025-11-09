"""
Заняття 11: Автоматизація файлових операцій
Приклади коду для демонстрації на лекції
"""

import shutil
from pathlib import Path
import datetime
import time

# ============================================================================
# ЧАСТИНА 1: Timestamping
# ============================================================================

def example_01_basic_timestamps():
    """Основи роботи з мітками часу"""
    print("=" * 50)
    print("Приклад 1: Формати часу")
    print("=" * 50)

    now = datetime.datetime.now()

    formats = {
        "ISO 8601": now.isoformat(),
        "Для файлів": now.strftime("%Y-%m-%d_%H-%M-%S"),
        "Компактний": now.strftime("%Y%m%d_%H%M%S"),
        "Тільки дата": now.strftime("%Y-%m-%d"),
        "Unix timestamp": int(now.timestamp()),
    }

    for format_name, formatted in formats.items():
        print(f"{format_name:15}: {formatted}")

    print()


def example_02_timestamped_files():
    """Створення файлів з мітками часу"""
    print("=" * 50)
    print("Приклад 2: Файли з timestamp")
    print("=" * 50)

    def create_timestamped_filename(base_name, extension):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{base_name}_{timestamp}.{extension}"

    # Створити тестові файли
    test_dir = Path("timestamped_files")
    test_dir.mkdir(exist_ok=True)

    for i in range(3):
        filename = create_timestamped_filename("log", "txt")
        file_path = test_dir / filename
        file_path.write_text(f"Log entry {i}\n")
        print(f"Створено: {filename}")
        time.sleep(1)  # Пауза між файлами

    # Очищення
    shutil.rmtree(test_dir)
    print()


def example_03_timestamped_logger():
    """Логер з автоматичними мітками часу"""
    print("=" * 50)
    print("Приклад 3: Timestamped Logger")
    print("=" * 50)

    class TimestampedLogger:
        def __init__(self, log_dir="logs", app_name="app"):
            self.log_dir = Path(log_dir)
            self.log_dir.mkdir(exist_ok=True)
            self.app_name = app_name

            today = datetime.datetime.now().strftime("%Y-%m-%d")
            self.log_file = self.log_dir / f"{app_name}_{today}.log"

        def log(self, message):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"

            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            print(log_entry.strip())

    # Використання
    logger = TimestampedLogger(app_name="demo")
    logger.log("Application started")
    logger.log("Processing data...")
    logger.log("Operation completed")

    # Очищення
    shutil.rmtree("logs")
    print()


# ============================================================================
# ЧАСТИНА 2: Модуль shutil
# ============================================================================

def example_04_copy_operations():
    """Операції копіювання"""
    print("=" * 50)
    print("Приклад 4: Копіювання файлів")
    print("=" * 50)

    # Створити тестовий файл
    source = Path("source.txt")
    source.write_text("Test content")

    # copy() — тільки вміст
    shutil.copy(source, "copy1.txt")
    print(f"copy(): створено copy1.txt")

    # copy2() — вміст + метадані
    shutil.copy2(source, "copy2.txt")
    print(f"copy2(): створено copy2.txt")

    # Порівняння mtime
    print(f"\nПорівняння mtime:")
    print(f"Оригінал: {source.stat().st_mtime}")
    print(f"copy():    {Path('copy1.txt').stat().st_mtime}")
    print(f"copy2():   {Path('copy2.txt').stat().st_mtime}")

    # Очищення
    source.unlink()
    Path("copy1.txt").unlink()
    Path("copy2.txt").unlink()
    print()


def example_05_copytree():
    """Копіювання директорій"""
    print("=" * 50)
    print("Приклад 5: Копіювання директорій")
    print("=" * 50)

    # Створити тестову структуру
    source_dir = Path("source_folder")
    source_dir.mkdir(exist_ok=True)
    (source_dir / "file1.txt").write_text("File 1")
    (source_dir / "file2.txt").write_text("File 2")
    (source_dir / "subdir").mkdir(exist_ok=True)
    (source_dir / "subdir" / "file3.txt").write_text("File 3")

    # Копіювати з ігноруванням
    shutil.copytree(
        source_dir,
        "destination_folder",
        ignore=shutil.ignore_patterns("*.pyc", "__pycache__")
    )

    print("Директорію скопійовано")
    print("\nВміст destination_folder:")
    for item in Path("destination_folder").rglob("*"):
        print(f"  {item}")

    # Очищення
    shutil.rmtree(source_dir)
    shutil.rmtree("destination_folder")
    print()


def example_06_move_and_delete():
    """Переміщення та видалення"""
    print("=" * 50)
    print("Приклад 6: Переміщення та видалення")
    print("=" * 50)

    # Створити файл
    test_file = Path("test.txt")
    test_file.write_text("Test")
    print(f"Створено: {test_file}")

    # Перейменувати
    shutil.move(test_file, "renamed.txt")
    print(f"Перейменовано: test.txt → renamed.txt")

    # Створити директорію і перемістити туди
    Path("temp_dir").mkdir(exist_ok=True)
    shutil.move("renamed.txt", "temp_dir/file.txt")
    print(f"Переміщено: renamed.txt → temp_dir/file.txt")

    # Видалити директорію
    shutil.rmtree("temp_dir")
    print(f"Видалено: temp_dir/")

    print()


def example_07_disk_usage():
    """Інформація про диск"""
    print("=" * 50)
    print("Приклад 7: Використання диска")
    print("=" * 50)

    usage = shutil.disk_usage(".")

    print(f"Всього:       {usage.total / (1024**3):>10.2f} GB")
    print(f"Використано:  {usage.used / (1024**3):>10.2f} GB")
    print(f"Вільно:       {usage.free / (1024**3):>10.2f} GB")
    print(f"Відсоток:     {usage.used / usage.total * 100:>10.1f}%")

    print()


# ============================================================================
# ЧАСТИНА 3: Ротація файлів
# ============================================================================

def example_08_simple_rotation():
    """Проста ротація файлів"""
    print("=" * 50)
    print("Приклад 8: Ротація файлів")
    print("=" * 50)

    def rotate_files(base_name, max_count=3):
        base_path = Path(base_name)

        # Видалити найстаріший
        oldest = Path(f"{base_name}.{max_count}")
        if oldest.exists():
            oldest.unlink()
            print(f"Видалено найстаріший: {oldest.name}")

        # Зсунути файли
        for i in range(max_count - 1, 0, -1):
            old_file = Path(f"{base_name}.{i}")
            new_file = Path(f"{base_name}.{i + 1}")

            if old_file.exists():
                shutil.move(old_file, new_file)
                print(f"Ротація: {old_file.name} → {new_file.name}")

        # Поточний файл → .1
        if base_path.exists():
            shutil.move(base_path, f"{base_name}.1")
            print(f"Ротація: {base_path.name} → {base_name}.1")

        # Створити новий
        base_path.touch()
        print(f"Створено новий: {base_path.name}")

    # Створити тестові файли
    Path("app.log").write_text("Current log")
    Path("app.log.1").write_text("Yesterday")
    Path("app.log.2").write_text("Two days ago")

    print("Файли до ротації:")
    for f in sorted(Path(".").glob("app.log*")):
        print(f"  {f.name}")

    print("\nРотація:")
    rotate_files("app.log", max_count=3)

    print("\nФайли після ротації:")
    for f in sorted(Path(".").glob("app.log*")):
        print(f"  {f.name}")

    # Очищення
    for f in Path(".").glob("app.log*"):
        f.unlink()

    print()


def example_09_rotate_by_date():
    """Ротація за датою"""
    print("=" * 50)
    print("Приклад 9: Ротація за датою")
    print("=" * 50)

    def rotate_by_date(log_file):
        log_path = Path(log_file)

        if not log_path.exists():
            log_path.touch()
            return

        # Отримати дату файлу
        mtime = log_path.stat().st_mtime
        file_date = datetime.datetime.fromtimestamp(mtime).date()
        today = datetime.date.today()

        # Якщо файл старіший — ротувати
        if file_date < today:
            dated_name = f"{log_path.stem}.{file_date}.log"
            dated_path = log_path.parent / dated_name

            shutil.move(log_path, dated_path)
            log_path.touch()

            print(f"Заротовано: {log_file} → {dated_name}")
        else:
            print(f"Файл актуальний, ротація не потрібна")

    # Тест
    test_log = Path("daily.log")
    test_log.write_text("Old content")

    # Змінити mtime на вчорашній день
    yesterday = time.time() - (24 * 60 * 60)
    Path("daily.log").touch()
    import os
    os.utime(test_log, (yesterday, yesterday))

    rotate_by_date("daily.log")

    # Очищення
    for f in Path(".").glob("daily.log*"):
        f.unlink()

    print()


# ============================================================================
# ЧАСТИНА 4: Архівування
# ============================================================================

def example_10_create_zip():
    """Створення ZIP архіву"""
    print("=" * 50)
    print("Приклад 10: Створення ZIP")
    print("=" * 50)

    import zipfile

    # Створити тестові файли
    test_dir = Path("test_project")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "file1.txt").write_text("Content 1")
    (test_dir / "file2.txt").write_text("Content 2")
    (test_dir / "subdir").mkdir(exist_ok=True)
    (test_dir / "subdir" / "file3.txt").write_text("Content 3")

    # Створити ZIP
    with zipfile.ZipFile("project.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in test_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(test_dir.parent)
                zipf.write(file, arcname)
                print(f"Додано: {arcname}")

    print(f"\nАрхів створено: project.zip")
    print(f"Розмір: {Path('project.zip').stat().st_size} bytes")

    # Очищення
    shutil.rmtree(test_dir)
    Path("project.zip").unlink()

    print()


def example_11_extract_zip():
    """Розпакування ZIP"""
    print("=" * 50)
    print("Приклад 11: Розпакування ZIP")
    print("=" * 50)

    import zipfile

    # Створити тестовий архів
    test_dir = Path("archive_test")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "file.txt").write_text("Test")

    with zipfile.ZipFile("test.zip", 'w') as zipf:
        zipf.write(test_dir / "file.txt", "file.txt")

    shutil.rmtree(test_dir)

    # Розпакувати
    with zipfile.ZipFile("test.zip", 'r') as zipf:
        print("Вміст архіву:")
        for info in zipf.filelist:
            print(f"  {info.filename} ({info.file_size} bytes)")

        zipf.extractall("extracted")

    print("\nРозпаковано в: extracted/")

    # Очищення
    Path("test.zip").unlink()
    shutil.rmtree("extracted")

    print()


def example_12_create_targz():
    """Створення TAR.GZ архіву"""
    print("=" * 50)
    print("Приклад 12: Створення TAR.GZ")
    print("=" * 50)

    import tarfile

    # Створити тестову директорію
    test_dir = Path("logs")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "app.log").write_text("Log content")
    (test_dir / "error.log").write_text("Error content")

    # Створити TAR.GZ
    with tarfile.open("logs.tar.gz", "w:gz") as tar:
        for file in test_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(test_dir.parent)
                tar.add(file, arcname=arcname)
                print(f"Додано: {arcname}")

    print(f"\nАрхів створено: logs.tar.gz")
    print(f"Розмір: {Path('logs.tar.gz').stat().st_size} bytes")

    # Очищення
    shutil.rmtree(test_dir)
    Path("logs.tar.gz").unlink()

    print()


def example_13_compress_file():
    """Стиснення окремого файлу"""
    print("=" * 50)
    print("Приклад 13: Стиснення gzip")
    print("=" * 50)

    import gzip

    # Створити тестовий файл
    test_file = Path("large_file.txt")
    test_file.write_text("Test content\n" * 1000)

    original_size = test_file.stat().st_size

    # Стиснути
    with open(test_file, 'rb') as f_in:
        with gzip.open("large_file.txt.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    compressed_size = Path("large_file.txt.gz").stat().st_size

    print(f"Оригінал:  {original_size:>10} bytes")
    print(f"Стиснутий: {compressed_size:>10} bytes")
    print(f"Стиснення: {(1 - compressed_size/original_size)*100:>10.1f}%")

    # Очищення
    test_file.unlink()
    Path("large_file.txt.gz").unlink()

    print()


# ============================================================================
# ЧАСТИНА 5: Система backup
# ============================================================================

def example_14_simple_backup():
    """Проста система backup"""
    print("=" * 50)
    print("Приклад 14: Система backup")
    print("=" * 50)

    import tarfile

    class SimpleBackup:
        def __init__(self, source_dir, backup_dir):
            self.source = Path(source_dir)
            self.backup_dir = Path(backup_dir)
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        def create_backup(self):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_name = f"backup_{self.source.name}_{timestamp}.tar.gz"
            backup_path = self.backup_dir / backup_name

            with tarfile.open(backup_path, "w:gz") as tar:
                tar.add(self.source, arcname=self.source.name)

            size_mb = backup_path.stat().st_size / (1024 ** 2)
            print(f"Backup створено: {backup_name}")
            print(f"Розмір: {size_mb:.2f} MB")

            return backup_path

        def list_backups(self):
            backups = sorted(
                self.backup_dir.glob("backup_*.tar.gz"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )

            print(f"\nДоступні backup'и ({len(backups)}):")
            for backup in backups:
                mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
                size_mb = backup.stat().st_size / (1024 ** 2)
                print(f"  {backup.name} ({size_mb:.2f} MB) - {mtime}")

    # Створити тестову директорію
    test_source = Path("my_data")
    test_source.mkdir(exist_ok=True)
    (test_source / "file1.txt").write_text("Data 1")
    (test_source / "file2.txt").write_text("Data 2")

    # Створити backup
    backup_system = SimpleBackup("my_data", "backups")
    backup_system.create_backup()
    backup_system.list_backups()

    # Очищення
    shutil.rmtree(test_source)
    shutil.rmtree("backups")

    print()


# ============================================================================
# ГОЛОВНА ФУНКЦІЯ
# ============================================================================

def main():
    """Запустити всі приклади"""
    examples = [
        example_01_basic_timestamps,
        example_02_timestamped_files,
        example_03_timestamped_logger,
        example_04_copy_operations,
        example_05_copytree,
        example_06_move_and_delete,
        example_07_disk_usage,
        example_08_simple_rotation,
        example_09_rotate_by_date,
        example_10_create_zip,
        example_11_extract_zip,
        example_12_create_targz,
        example_13_compress_file,
        example_14_simple_backup,
    ]

    print("\n" + "=" * 70)
    print(" ЗАНЯТТЯ 11: Автоматизація файлових операцій")
    print("=" * 70 + "\n")

    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"❌ Помилка в прикладі {i}: {e}")

        input("Натисніть Enter для наступного прикладу...")

    print("\n" + "=" * 70)
    print(" Всі приклади виконано!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()