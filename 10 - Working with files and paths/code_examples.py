"""
Заняття 10.1: Робота з файловими шляхами та пошук файлів
Приклади коду для демонстрації на лекції
"""

# ============================================================================
# ЧАСТИНА 1: Сучасний підхід з pathlib
# ============================================================================

def example_01_basic_pathlib():
    """Основи роботи з Path"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 1: Основи pathlib")
    print("=" * 50)

    # Поточна директорія
    current = Path.cwd()
    print(f"Поточна директорія: {current}")

    # Домашня директорія
    home = Path.home()
    print(f"Домашня директорія: {home}")

    # Створення шляху
    config_path = Path.home() / ".config" / "app" / "settings.json"
    print(f"Шлях до конфігурації: {config_path}")

    # Перевірка існування
    print(f"Існує: {config_path.exists()}")
    print()


def example_02_path_properties():
    """Властивості Path об'єкта"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 2: Властивості Path")
    print("=" * 50)

    file_path = Path("/var/log/application/app.log.2024")

    print(f"Повний шлях: {file_path}")
    print(f"Ім'я файлу: {file_path.name}")
    print(f"Без розширення: {file_path.stem}")
    print(f"Розширення: {file_path.suffix}")
    print(f"Всі розширення: {file_path.suffixes}")
    print(f"Батьківська папка: {file_path.parent}")

    # Зміна розширення
    new_path = file_path.with_suffix('.txt')
    print(f"З новим розширенням: {new_path}")

    # Зміна імені
    renamed = file_path.with_name('error.log')
    print(f"З новим іменем: {renamed}")
    print()


def example_03_path_checks():
    """Перевірка типів та створення директорій"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 3: Перевірки та створення")
    print("=" * 50)

    # Створення тестового файлу
    test_file = Path("test_example.txt")
    test_file.touch()  # Створити порожній файл

    print(f"Існує: {test_file.exists()}")
    print(f"Це файл: {test_file.is_file()}")
    print(f"Це директорія: {test_file.is_dir()}")
    print(f"Абсолютний шлях: {test_file.is_absolute()}")

    # Створення директорій
    log_dir = Path("logs/2025/november")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"Створено директорію: {log_dir}")

    # Очищення
    test_file.unlink()
    print("Тестовий файл видалено")
    print()


# ============================================================================
# ЧАСТИНА 2: Властивості файлів (atime, mtime, ctime)
# ============================================================================

def example_04_file_timestamps():
    """Робота з часовими мітками файлів"""
    from pathlib import Path
    import datetime
    import time

    print("=" * 50)
    print("Приклад 4: Часові мітки файлів")
    print("=" * 50)

    # Створимо тестовий файл
    test_file = Path("timestamp_test.txt")
    test_file.write_text("Test content")

    # Трохи почекаємо
    time.sleep(1)

    # Прочитаємо файл (оновить atime)
    content = test_file.read_text()

    # Отримаємо статистику
    stat_info = test_file.stat()

    atime = datetime.datetime.fromtimestamp(stat_info.st_atime)
    mtime = datetime.datetime.fromtimestamp(stat_info.st_mtime)
    ctime = datetime.datetime.fromtimestamp(stat_info.st_ctime)

    print(f"Останній доступ (atime): {atime}")
    print(f"Остання зміна (mtime): {mtime}")
    print(f"Change/Creation time (ctime): {ctime}")

    # Очищення
    test_file.unlink()
    print()


def example_05_file_stats():
    """Додаткова інформація з stat()"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 5: Детальна статистика файлу")
    print("=" * 50)

    # Створимо файл з вмістом
    test_file = Path("stats_test.txt")
    test_file.write_text("Some content for testing\n" * 100)

    stat_info = test_file.stat()

    print(f"Розмір файлу: {stat_info.st_size} байт")
    print(f"Розмір у КБ: {stat_info.st_size / 1024:.2f} КБ")
    print(f"Права доступу: {oct(stat_info.st_mode)}")

    # На Unix системах
    try:
        print(f"UID власника: {stat_info.st_uid}")
        print(f"GID групи: {stat_info.st_gid}")
    except AttributeError:
        print("UID/GID доступні тільки на Unix")

    # Очищення
    test_file.unlink()
    print()


def example_06_find_old_files():
    """Знайти файли, які давно не відкривали"""
    from pathlib import Path
    import time

    print("=" * 50)
    print("Приклад 6: Пошук старих файлів")
    print("=" * 50)

    # Створимо кілька тестових файлів
    test_dir = Path("test_old_files")
    test_dir.mkdir(exist_ok=True)

    # Створимо файли з різним часом
    for i in range(3):
        file = test_dir / f"file_{i}.txt"
        file.write_text(f"Content {i}")

    threshold = time.time() - (1 * 24 * 60 * 60)  # 1 день тому

    print(f"Пошук файлів старших за 1 день:")
    for file_path in test_dir.rglob("*.txt"):
        if file_path.stat().st_atime < threshold:
            days_ago = (time.time() - file_path.stat().st_atime) / (24 * 60 * 60)
            print(f"  {file_path.name}: {days_ago:.1f} днів тому")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


# ============================================================================
# ЧАСТИНА 3: Обхід директорій
# ============================================================================

def example_07_os_walk():
    """Класичний обхід з os.walk()"""
    import os
    from pathlib import Path

    print("=" * 50)
    print("Приклад 7: os.walk()")
    print("=" * 50)

    # Створимо тестову структуру
    test_dir = Path("test_walk")
    (test_dir / "dir1").mkdir(parents=True, exist_ok=True)
    (test_dir / "dir2").mkdir(parents=True, exist_ok=True)
    (test_dir / "file1.txt").write_text("test")
    (test_dir / "dir1" / "file2.txt").write_text("test")

    print("Обхід директорії:")
    for root, dirs, files in os.walk(test_dir):
        print(f"\n📁 Директорія: {root}")
        print(f"   Піддиректорії: {dirs}")
        print(f"   Файли: {files}")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


def example_08_path_glob():
    """Сучасний підхід з Path.glob() та rglob()"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 8: Path.glob() та rglob()")
    print("=" * 50)

    # Створимо тестову структуру
    test_dir = Path("test_glob")
    (test_dir / "subdir").mkdir(parents=True, exist_ok=True)

    (test_dir / "file1.txt").write_text("test")
    (test_dir / "file2.log").write_text("test")
    (test_dir / "subdir" / "file3.txt").write_text("test")

    print("glob() - тільки в поточній директорії:")
    for file in test_dir.glob("*.txt"):
        print(f"  {file}")

    print("\nrglob() - рекурсивний пошук:")
    for file in test_dir.rglob("*.txt"):
        print(f"  {file}")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


def example_09_find_large_files():
    """Пошук великих файлів"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 9: Пошук великих файлів")
    print("=" * 50)

    def find_large_files(directory, min_size_mb=0.001):  # Понизимо для тесту
        """Знайти файли більше заданого розміру"""
        min_size_bytes = min_size_mb * 1024 * 1024
        large_files = []

        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size > min_size_bytes:
                    size_mb = size / (1024 ** 2)
                    large_files.append((file_path, size_mb))

        return sorted(large_files, key=lambda x: x[1], reverse=True)

    # Створимо тестові файли
    test_dir = Path("test_large")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "small.txt").write_text("x" * 100)
    (test_dir / "medium.txt").write_text("x" * 5000)
    (test_dir / "large.txt").write_text("x" * 10000)

    print("Файли більше 0.001 MB:")
    for file_path, size in find_large_files(test_dir):
        print(f"  {size:.4f} MB - {file_path.name}")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


# ============================================================================
# ЧАСТИНА 4: Розширений пошук файлів
# ============================================================================

def example_10_search_by_pattern():
    """Пошук за масками"""
    from pathlib import Path

    print("=" * 50)
    print("Приклад 10: Пошук за патернами")
    print("=" * 50)

    # Створимо тестові файли
    test_dir = Path("test_patterns")
    test_dir.mkdir(exist_ok=True)

    files_to_create = [
        "app-2024-11-01.log",
        "app-2024-11-09.log",
        "error.log",
        "config.conf",
        "data.json"
    ]

    for filename in files_to_create:
        (test_dir / filename).write_text("test")

    print("Файли app-*.log:")
    for f in test_dir.glob("app-*.log"):
        print(f"  {f.name}")

    print("\nВсі .log файли:")
    for f in test_dir.glob("*.log"):
        print(f"  {f.name}")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


def example_11_search_by_date():
    """Пошук за датою модифікації"""
    from pathlib import Path
    import datetime
    import time

    print("=" * 50)
    print("Приклад 11: Пошук за датою")
    print("=" * 50)

    def find_modified_recently(directory, days=7):
        """Знайти файли, змінені за останні N днів"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        recent_files = []

        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                mtime = file_path.stat().st_mtime
                if mtime > cutoff_time:
                    mod_date = datetime.datetime.fromtimestamp(mtime)
                    recent_files.append((file_path, mod_date))

        return sorted(recent_files, key=lambda x: x[1], reverse=True)

    # Створимо тестовий каталог
    test_dir = Path("test_dates")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "recent.txt").write_text("new")

    print("Файли, змінені за останні 7 днів:")
    for path, mod_date in find_modified_recently(test_dir, days=7):
        print(f"  {mod_date.strftime('%Y-%m-%d %H:%M')} - {path.name}")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


def example_12_advanced_search():
    """Комбінований пошук"""
    from pathlib import Path
    import time

    print("=" * 50)
    print("Приклад 12: Комбінований пошук")
    print("=" * 50)

    def advanced_search(directory, pattern="*", min_mb=None, max_mb=None,
                        modified_days=None, extension=None):
        """Універсальна функція пошуку"""
        results = []

        for file_path in Path(directory).rglob(pattern):
            if not file_path.is_file():
                continue

            # Фільтр за розширенням
            if extension and file_path.suffix != extension:
                continue

            stat_info = file_path.stat()
            size_mb = stat_info.st_size / (1024 ** 2)

            # Фільтр за розміром
            if min_mb and size_mb < min_mb:
                continue
            if max_mb and size_mb > max_mb:
                continue

            # Фільтр за датою
            if modified_days:
                cutoff = time.time() - (modified_days * 24 * 60 * 60)
                if stat_info.st_mtime < cutoff:
                    continue

            results.append(file_path)

        return results

    # Тест
    test_dir = Path("test_advanced")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "small.txt").write_text("x" * 100)
    (test_dir / "large.txt").write_text("x" * 10000)

    print("Пошук .txt файлів:")
    for file in advanced_search(test_dir, extension=".txt"):
        print(f"  {file.name}")

    # Очищення
    import shutil
    shutil.rmtree(test_dir)
    print()


# ============================================================================
# ЧАСТИНА 5: Відмінності Windows vs Unix
# ============================================================================

def example_13_path_separators():
    """Роздільники шляхів"""
    from pathlib import Path
    import os
    import platform

    print("=" * 50)
    print("Приклад 13: Роздільники шляхів")
    print("=" * 50)

    print(f"Операційна система: {platform.system()}")
    print(f"Роздільник шляхів: {os.sep!r}")
    print(f"Роздільник PATH: {os.pathsep!r}")

    # Кросплатформний шлях
    path = Path.home() / "documents" / "file.txt"
    print(f"Кросплатформний шлях: {path}")

    print()


def example_14_drive_letters():
    """Букви дисків (Windows)"""
    from pathlib import Path
    import platform

    print("=" * 50)
    print("Приклад 14: Букви дисків")
    print("=" * 50)

    path = Path.home()
    print(f"Домашня директорія: {path}")
    print(f"Drive: {path.drive!r}")
    print(f"Root: {path.root!r}")

    if platform.system() == "Windows":
        print("На Windows є букви дисків (C:, D:, etc.)")
    else:
        print("На Unix немає букв дисків, все монтується в /")

    print()


def example_15_case_sensitivity():
    """Чутливість до регістру"""
    from pathlib import Path
    import platform

    print("=" * 50)
    print("Приклад 15: Чутливість до регістру")
    print("=" * 50)

    print(f"Операційна система: {platform.system()}")

    if platform.system() == "Windows":
        print("Windows НЕ чутлива до регістру")
        print("file.txt == File.txt == FILE.TXT")
    else:
        print("Unix чутлива до регістру")
        print("file.txt ≠ File.txt ≠ FILE.TXT")

    # Безпечна перевірка
    test_file = Path("test_case.txt")
    test_file.touch()

    print(f"\nФайл існує: {test_file.exists()}")
    print(f"TEST_CASE.TXT існує: {Path('TEST_CASE.TXT').exists()}")

    # Очищення
    test_file.unlink()
    print()


def example_16_sanitize_filename():
    """Очищення імен файлів"""
    import re

    print("=" * 50)
    print("Приклад 16: Безпечні імена файлів")
    print("=" * 50)

    def sanitize_filename(filename):
        """Очистити ім'я файлу для кросплатформності"""
        # Видалити небезпечні символи
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

        # Видалити керуючі символи
        filename = re.sub(r'[\x00-\x1f]', '', filename)

        # Обмежити довжину
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:255 - len(ext) - 1] + '.' + ext

        return filename

    test_names = [
        'report:2024/11/09|v2.txt',
        'file<with>bad:chars.doc',
        'normal_file.txt'
    ]

    print("Очищення небезпечних імен:")
    for name in test_names:
        safe = sanitize_filename(name)
        print(f"  {name!r:40} -> {safe!r}")

    print()


def example_17_system_info():
    """Інформація про систему"""
    import platform
    import sys
    import os

    print("=" * 50)
    print("Приклад 17: Інформація про систему")
    print("=" * 50)

    info = {
        "Платформа": platform.system(),
        "Реліз": platform.release(),
        "Версія": platform.version(),
        "Архітектура": platform.machine(),
        "Python версія": platform.python_version(),
        "Роздільник шляхів": os.sep,
        "Роздільник PATH": os.pathsep,
    }

    for key, value in info.items():
        print(f"{key:20}: {value}")

    print()


# ============================================================================
# ГОЛОВНА ФУНКЦІЯ
# ============================================================================

def main():
    """Запустити всі приклади"""
    examples = [
        example_01_basic_pathlib,
        example_02_path_properties,
        example_03_path_checks,
        example_04_file_timestamps,
        example_05_file_stats,
        example_06_find_old_files,
        example_07_os_walk,
        example_08_path_glob,
        example_09_find_large_files,
        example_10_search_by_pattern,
        example_11_search_by_date,
        example_12_advanced_search,
        example_13_path_separators,
        example_14_drive_letters,
        example_15_case_sensitivity,
        example_16_sanitize_filename,
        example_17_system_info,
    ]

    print("\n" + "=" * 70)
    print(" ЗАНЯТТЯ 10.1: Робота з файловими шляхами та пошук файлів")
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