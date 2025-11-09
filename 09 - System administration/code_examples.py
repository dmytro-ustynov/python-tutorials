import os, sys
import shutil
from pathlib import Path
from typing import Iterator, Tuple

# ---- Базова інформація про ОС і поточну директорію ----
print("os.name:", os.name)      # 'posix' (Linux/macOS) або 'nt' (Windows)
print("sys.platform:", sys.platform)
print("current working dir:", os.getcwd())
print("home dir (Path.home()):", Path.home())

# ---- Список файлів у поточній директорії (детально) ----
cwd = Path(".").resolve()
print("\nФайли/папки в", cwd)
for p in cwd.iterdir():
    print(" ", p.name, "(dir)" if p.is_dir() else "(file)")


# ---- Фільтрація: тільки файли з певним розширенням ----
def list_files_with_ext(root: Path, ext: str) -> Iterator[Path]:
    """Ітератор по файлах з розширенням ext у root (нелікально)."""
    for p in root.iterdir():
        if p.is_file() and p.suffix.lower() == ext.lower():
            yield p


print("\nФайли .py у поточній директорії:")
for f in list_files_with_ext(cwd, ".py"):
    print(" ", f.name)


# ---- Рекурсивний обхід директорій (os.walk та pathlib) ----
def walk_and_summarize(root: Path) -> Tuple[int, int]:
    """
    Повертає кортеж (кількість файлів, сумарний розмір у байтах) в дереві root.
    Демонстрація os.walk.
    """
    total_files = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # можна пропускати приховані каталоги:
        # dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in filenames:
            total_files += 1
            try:
                fp = Path(dirpath) / fn
                total_size += fp.stat().st_size
            except (FileNotFoundError, PermissionError):
                # файл міг бути видалений під час обходу або доступ обмежений
                continue
    return total_files, total_size


files, size = walk_and_summarize(cwd)
print(f"\nРекурсивно: {files} файлів, сумарно {size} байт")

# ---- Приклад: створення структури резервної копії (без перезапису) ----
backup_dir = Path.cwd() / "backup_demo"
print("\nСтворюємо резервну теку:", backup_dir)
backup_dir.mkdir(parents=True, exist_ok=True)


def safe_copy(src: Path, dst_dir: Path):
    """Копіює src в dst_dir, уникаючи перезапису (додає суфікс при конфлікті)."""
    dst = dst_dir / src.name
    if dst.exists():
        base = dst.stem
        suffix = dst.suffix
        i = 1
        while True:
            candidate = dst_dir / f"{base}.{i}{suffix}"
            if not candidate.exists():
                dst = candidate
                break
            i += 1
    shutil.copy2(src, dst)  # копіює з метаданими
    return dst


# копіюємо перші 3 файли з cwd (як демонстрацію)
copied = []
for i, f in enumerate([p for p in cwd.iterdir() if p.is_file()][:3]):
    dst = safe_copy(f, backup_dir)
    copied.append(dst)
    print("Скопійовано:", f.name, "->", dst.name)


# ---- Приклад видалення (з безпечною перевіркою) ----
def safe_remove(path: Path):
    if not path.exists():
        print("Не знайдено:", path)
        return
    if path.is_dir():
        # ризик видалити великі дерева — підтвердження або додаткові перевірки
        print("Видаляємо каталог рекурсивно:", path)
        shutil.rmtree(path)
    else:
        print("Видаляємо файл:", path)
        path.unlink()


# Розкоментуй для тесту (не запускай безпечно!):
# safe_remove(backup_dir)

# ---- Права доступу (chmod) — кросплатформні нюанси ----
sample = Path("sample_perm.txt")
sample.write_text("permission demo\n", encoding="utf-8")
print("\nФайл створено:", sample.resolve())
if os.name == "posix":
    # на POSIX змінюємо права
    print("POSIX: показуємо права та міняємо на 0o644")
    st = sample.stat()
    print(" current mode:", oct(st.st_mode & 0o777))
    sample.chmod(0o644)
    print(" new mode:", oct(sample.stat().st_mode & 0o777))
else:
    print("Windows: chmod обмежений; деякі права не застосовуються на NTFS таким чином.")

# ---- Змінні середовища ----
print("\nКілька змінних середовища (приклади):")
print("  PATH:", os.environ.get("PATH", "")[:60], "...")
print("  HOME:", os.environ.get("HOME") or os.environ.get("USERPROFILE"))

# Безпечно зчитуємо секрети (не хардкодити у коді!)
db_pass = os.environ.get("MY_APP_DB_PASS")
if db_pass is None:
    print("  MY_APP_DB_PASS не встановлено (це добре для демонстрації).")
else:
    print("  MY_APP_DB_PASS встановлено (не виводимо значення).")

# ---- Інформація про процес (корисно для моніторингу) ----
print("\nІнформація про поточний процес:")
print("  PID:", os.getpid())
print("  UID (POSIX):", getattr(os, "getuid", lambda: None)())

# ---- Завершення програми з кодом повернення ----
# os._exit(0)  # екстрене завершення (використовувати дуже обережно)
print("\nГотово.")
