
## 🎓 **ЗАНЯТТЯ 5.4: Моніторинг системних процесів**

### 🕐 Загальний час: 2 години (практичне заняття) + 0.5 год самостійна робота

### 🎯 **Мета:**

Навчитися моніторити системні процеси та ресурси, створювати звіти про стан системи, а також опанувати важливі lifehacks: запобігання дублюванню запуску процесів (Single Instance) та створення конфігурованих скриптів з аргументами командного рядка.

---

## 🧩 СТРУКТУРА ЗАНЯТТЯ

**План:**

1. Моніторинг процесів з `psutil`
2. Збір інформації про системні ресурси
3. Створення звітів про стан системи
4. **Lifehack 1:** Запобігання дублюванню процесів (Single Instance)
5. **Lifehack 2:** Конфігуровані скрипти з argparse

**Самостійна робота:** Створення системи моніторингу з автозапуском

---

## 🔹 ЧАСТИНА 1. Моніторинг процесів з psutil

---

### **Слайд 1. Бібліотека psutil — швейцарський ніж системного адміністратора**

**Що таке psutil?**

`psutil` (Python System and Process Utilities) — потужна кросплатформна бібліотека для отримання інформації про:
- Системні ресурси (CPU, пам'ять, диски, мережа)
- Запущені процеси
- Користувачів системи
- Температуру та батарею (на деяких платформах)

**Встановлення:**
```bash
pip install psutil
```

🎯 **Переваги:**
- Працює на Linux, Windows, macOS, BSD
- Простий API
- Активно підтримується
- Використовується в багатьох інструментах моніторингу

---

### **Слайд 2. Основна інформація про систему**

```python
import psutil
from datetime import datetime

# Інформація про CPU
print(f"CPU ядер (фізичних): {psutil.cpu_count(logical=False)}")
print(f"CPU ядер (логічних): {psutil.cpu_count(logical=True)}")
print(f"Завантаження CPU: {psutil.cpu_percent(interval=1)}%")

# Використання по ядрах
per_cpu = psutil.cpu_percent(interval=1, percpu=True)
for i, percent in enumerate(per_cpu):
    print(f"  Ядро {i}: {percent}%")

# Інформація про пам'ять
memory = psutil.virtual_memory()
print(f"\nПам'ять:")
print(f"  Всього: {memory.total / (1024**3):.2f} GB")
print(f"  Доступно: {memory.available / (1024**3):.2f} GB")
print(f"  Використано: {memory.percent}%")

# Час роботи системи
boot_time = datetime.fromtimestamp(psutil.boot_time())
print(f"\nСистема запущена: {boot_time}")
print(f"Час роботи: {datetime.now() - boot_time}")
```

---

### **Слайд 3. Моніторинг дисків та мережі**

```python
import psutil

# Інформація про диски
print("Диски:")
for partition in psutil.disk_partitions():
    print(f"\n  Пристрій: {partition.device}")
    print(f"  Точка монтування: {partition.mountpoint}")
    print(f"  Файлова система: {partition.fstype}")

    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"  Всього: {usage.total / (1024**3):.2f} GB")
        print(f"  Використано: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
        print(f"  Вільно: {usage.free / (1024**3):.2f} GB")
    except PermissionError:
        print("  Немає доступу")

# Мережева статистика
net_io = psutil.net_io_counters()
print(f"\nМережа:")
print(f"  Відправлено: {net_io.bytes_sent / (1024**2):.2f} MB")
print(f"  Отримано: {net_io.bytes_recv / (1024**2):.2f} MB")
```

---

### **Слайд 4. Робота з процесами**

```python
import psutil

# Отримання всіх процесів
for proc in psutil.process_iter(['pid', 'name', 'username']):
    try:
        print(f"PID: {proc.info['pid']}, "
              f"Ім'я: {proc.info['name']}, "
              f"Користувач: {proc.info['username']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# Детальна інформація про процес
pid = psutil.Process().pid  # Поточний процес
process = psutil.Process(pid)

print(f"\nІнформація про процес {pid}:")
print(f"  Ім'я: {process.name()}")
print(f"  Статус: {process.status()}")
print(f"  Створений: {datetime.fromtimestamp(process.create_time())}")
print(f"  CPU: {process.cpu_percent(interval=1)}%")
print(f"  Пам'ять: {process.memory_info().rss / (1024**2):.2f} MB")
print(f"  Потоків: {process.num_threads()}")
```


Самостійно : порахувати загальну кількість процесів та вивести процес з найбільшим використанням памʼяті.
---

### **Слайд 5. Пошук та фільтрація процесів**

```python
import psutil

def find_processes_by_name(name):
    """Знайти всі процеси за іменем"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if name.lower() in proc.info['name'].lower():
                processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def get_top_memory_processes(n=5):
    """Отримати топ N процесів за використанням пам'яті"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            if proc.info['memory_percent'] is not None:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory': proc.info['memory_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Сортування за пам'яттю
    processes.sort(key=lambda x:  x['memory'], reverse=True)
    return processes[:n]

# Використання
python_procs = find_processes_by_name('python')
print(f"Знайдено {len(python_procs)} Python процесів")

print("\nТоп-5 процесів за пам'яттю:")
for i, proc in enumerate(get_top_memory_processes(5), 1):
    print(f"{i}. {proc['name']} (PID: {proc['pid']}): {proc['memory']:.2f}%")
```

---

## 🔹 ЧАСТИНА 2. Створення звітів про стан системи

---

### **Слайд 6. Структурування даних для звіту**

```python
import psutil
from datetime import datetime
from typing import Dict, List

def collect_system_info() -> Dict:
    """Збір всієї системної інформації"""

    # CPU інформація
    cpu_info = {
        'physical_cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True),
        'total_usage': psutil.cpu_percent(interval=1),
        'per_core_usage': psutil.cpu_percent(interval=1, percpu=True),
        'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None
    }

    # Пам'ять
    memory = psutil.virtual_memory()
    memory_info = {
        'total_gb': memory.total / (1024**3),
        'available_gb': memory.available / (1024**3),
        'used_gb': memory.used / (1024**3),
        'percent': memory.percent
    }

    # Диски
    disk_info = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'percent': usage.percent
            })
        except PermissionError:
            continue

    # Мережа
    net = psutil.net_io_counters()
    network_info = {
        'bytes_sent_mb': net.bytes_sent / (1024**2),
        'bytes_recv_mb': net.bytes_recv / (1024**2),
        'packets_sent': net.packets_sent,
        'packets_recv': net.packets_recv
    }

    # Загальна інформація
    return {
        'timestamp': datetime.now().isoformat(),
        'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        'cpu': cpu_info,
        'memory': memory_info,
        'disks': disk_info,
        'network': network_info
    }
```

---

### **Слайд 7. Генерація текстового звіту**

```python
def generate_text_report() -> str:
    """Генерація текстового звіту"""
    info = collect_system_info()

    report = []
    report.append("=" * 60)
    report.append("ЗВІТ ПРО СТАН СИСТЕМИ")
    report.append("=" * 60)
    report.append(f"Дата: {info['timestamp']}")
    report.append(f"Час запуску системи: {info['boot_time']}")
    report.append("")

    # CPU
    report.append("CPU:")
    report.append(f"  Фізичних ядер: {info['cpu']['physical_cores']}")
    report.append(f"  Логічних ядер: {info['cpu']['logical_cores']}")
    report.append(f"  Завантаження: {info['cpu']['total_usage']:.1f}%")
    if info['cpu']['frequency']:
        report.append(f"  Частота: {info['cpu']['frequency']:.0f} MHz")
    report.append("")

    # Пам'ять
    mem = info['memory']
    report.append("ПАМ'ЯТЬ:")
    report.append(f"  Всього: {mem['total_gb']:.2f} GB")
    report.append(f"  Використано: {mem['used_gb']:.2f} GB ({mem['percent']:.1f}%)")
    report.append(f"  Доступно: {mem['available_gb']:.2f} GB")
    report.append("")

    # Диски
    report.append("ДИСКИ:")
    for disk in info['disks']:
        report.append(f"  {disk['mountpoint']} ({disk['device']}):")
        report.append(f"    Всього: {disk['total_gb']:.2f} GB")
        report.append(f"    Використано: {disk['used_gb']:.2f} GB ({disk['percent']:.1f}%)")
        report.append(f"    Вільно: {disk['free_gb']:.2f} GB")
    report.append("")

    # Мережа
    net = info['network']
    report.append("МЕРЕЖА:")
    report.append(f"  Відправлено: {net['bytes_sent_mb']:.2f} MB ({net['packets_sent']} пакетів)")
    report.append(f"  Отримано: {net['bytes_recv_mb']:.2f} MB ({net['packets_recv']} пакетів)")
    report.append("")
    report.append("=" * 60)

    return "\n".join(report)

# Використання
print(generate_text_report())
```

---

### **Слайд 8. Збереження звіту в JSON та CSV**

```python
import json
import csv
from pathlib import Path
from datetime import datetime

def save_report_json(output_dir: Path = Path("reports")):
    """Зберегти звіт у JSON форматі"""
    output_dir.mkdir(exist_ok=True)

    info = collect_system_info()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"system_report_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

    print(f"Звіт збережено: {filename}")
    return filename

def save_monitoring_csv(output_file: Path = Path("monitoring.csv")):
    """Додати поточні дані моніторингу до CSV файлу"""
    info = collect_system_info()

    # Формування рядка даних
    row = {
        'timestamp': info['timestamp'],
        'cpu_percent': info['cpu']['total_usage'],
        'memory_percent': info['memory']['percent'],
        'memory_used_gb': info['memory']['used_gb'],
        'network_sent_mb': info['network']['bytes_sent_mb'],
        'network_recv_mb': info['network']['bytes_recv_mb']
    }

    # Додавання інформації про диски
    for i, disk in enumerate(info['disks']):
        row[f'disk_{i}_percent'] = disk['percent']

    # Перевірка чи файл існує
    file_exists = output_file.exists()

    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(f"Дані додано до: {output_file}")

# Використання
save_report_json()
save_monitoring_csv()
```

---

## 🔹 ЧАСТИНА 3. LIFEHACK 1 — Запобігання дублюванню процесів (Single Instance)

---

### **Слайд 9. Проблема дублювання процесів**

**Сценарій:**
```python
# monitoring_script.py - запускається кожну хвилину через cron
import time

print("Запуск моніторингу...")
while True:
    # Якась робота
    time.sleep(60)
```

**Проблема:**
- Якщо скрипт не встиг завершитись за 1 хвилину
- Запуститься другий екземпляр
- Потім третій, четвертий...
- Система перевантажиться 😱

**Рішення:**
Реалізація патерну **Single Instance** — гарантія, що запущений лише один екземпляр програми.

---

### **Слайд 10. Метод 1: PID-файл (Lock File)**

```python
import os
import sys
from pathlib import Path

class SingleInstance:
    """Гарантує, що запущений лише один екземпляр програми"""

    def __init__(self, lockfile: str = "/tmp/my_app.lock"):
        self.lockfile = Path(lockfile)
        self.pid = os.getpid()

    def __enter__(self):
        # Перевірка чи існує lock файл
        if self.lockfile.exists():
            # Читання PID з файлу
            try:
                old_pid = int(self.lockfile.read_text().strip())

                # Перевірка чи процес з таким PID існує
                if self._is_process_running(old_pid):
                    print(f"Програма вже запущена (PID: {old_pid})")
                    sys.exit(1)
                else:
                    print(f"Знайдено старий lock файл (PID: {old_pid} не існує), видаляю...")
                    self.lockfile.unlink()
            except (ValueError, FileNotFoundError):
                self.lockfile.unlink()

        # Створення нового lock файлу
        self.lockfile.write_text(str(self.pid))
        print(f"Lock файл створено: {self.lockfile} (PID: {self.pid})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Видалення lock файлу при виході
        if self.lockfile.exists():
            self.lockfile.unlink()
            print(f"Lock файл видалено")

    @staticmethod
    def _is_process_running(pid: int) -> bool:
        """Перевірка чи процес з таким PID запущений"""
        try:
            # Сигнал 0 не вбиває процес, а тільки перевіряє його існування
            os.kill(pid, 0)
            return True
        except OSError:
            return False

# Використання
def main():
    with SingleInstance("/tmp/my_monitoring_app.lock"):
        print("Програма запущена!")
        # Основна логіка програми
        import time
        time.sleep(10)
        print("Робота завершена")

if __name__ == "__main__":
    main()
```

**Переваги:**
- Простота реалізації
- Працює навіть після краху програми
- Можна побачити PID запущеного процесу

**Недоліки:**
- Потрібно очищати старі lock файли
- На Windows інші механізми перевірки процесів

---

### **Слайд 11. Метод 2: Використання psutil**

```python
import psutil
import os
import sys
from pathlib import Path

class SingleInstancePsutil:
    """Single Instance з використанням psutil"""

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.current_pid = os.getpid()

    def __enter__(self):
        # Пошук інших екземплярів програми
        current_process = psutil.Process(self.current_pid)
        current_cmdline = current_process.cmdline()

        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                if proc.info['pid'] == self.current_pid:
                    continue

                # Порівняння командного рядка
                if proc.info['cmdline'] == current_cmdline:
                    print(f"Програма вже запущена (PID: {proc.info['pid']})")
                    print(f"Командний рядок: {' '.join(current_cmdline)}")
                    sys.exit(1)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print(f"Програма запущена (PID: {self.current_pid})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Програма завершена")

# Використання
def main():
    with SingleInstancePsutil("my_monitoring_app"):
        print("Виконання роботи...")
        import time
        time.sleep(10)

if __name__ == "__main__":
    main()
```

**Переваги:**
- Не залишає файлів на диску
- Більш надійна перевірка через psutil
- Працює на всіх платформах

---

### **Слайд 12. Метод 3: Сокет-блокування (для Linux/Unix)**

```python
import socket
import sys

class SingleInstanceSocket:
    """Single Instance через мережевий сокет"""

    def __init__(self, port: int = 9999):
        self.port = port
        self.socket = None

    def __enter__(self):
        try:
            # Створення сокету та біндинг на localhost
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('127.0.0.1', self.port))
            print(f"Програма запущена (порт {self.port} зайнято)")
            return self
        except socket.error:
            print(f"Програма вже запущена (порт {self.port} зайнято іншим процесом)")
            sys.exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()
            print("Сокет закрито")

# Використання
def main():
    with SingleInstanceSocket(port=9999):
        print("Виконання роботи...")
        import time
        time.sleep(10)

if __name__ == "__main__":
    main()
```

**Переваги:**
- Дуже простий код
- Автоматичне звільнення при краху
- ОС сама очищає ресурси

**Недоліки:**
- Займає порт
- Може конфліктувати з іншими програмами

---

## 🔹 ЧАСТИНА 4. LIFEHACK 2 — Конфігуровані скрипти з argparse

---

### **Слайд 13. Навіщо потрібні аргументи командного рядка?**

**Погана практика:**
```python
# monitoring.py
CPU_THRESHOLD = 80  # Хардкод 😱
MEMORY_THRESHOLD = 90
CHECK_INTERVAL = 60

def monitor():
    # Щоб змінити параметри — треба редагувати код!
    pass
```

**Хороша практика:**
```bash
# Гнучке налаштування через аргументи
python monitoring.py --cpu-threshold 80 --memory-threshold 90 --interval 60
python monitoring.py --cpu-threshold 70 --memory-threshold 85 --interval 30
python monitoring.py --help
```

🎯 **Переваги:**
- Один скрипт для різних сценаріїв
- Легше тестувати
- Не потрібно редагувати код
- Можна використовувати в cron/скриптах

---

### **Слайд 14. Основи argparse**

```python
import argparse

def create_parser():
    """Створення парсера аргументів"""
    parser = argparse.ArgumentParser(
        description='Моніторинг системних ресурсів',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Позиційний аргумент (обов'язковий)
    parser.add_argument(
        'output_file',
        help='Файл для збереження звіту'
    )

    # Опціональні аргументи
    parser.add_argument(
        '--cpu-threshold',
        type=float,
        default=80.0,
        help='Поріг CPU для попередження (%)'
    )

    parser.add_argument(
        '--memory-threshold',
        type=float,
        default=90.0,
        help='Поріг пам\'яті для попередження (%)'
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Інтервал між перевірками (секунди)'
    )

    # Прапорець (boolean)
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Виводити детальну інформацію'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Формат звіту'
    )

    return parser

# Використання
if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    print(f"Вихідний файл: {args.output_file}")
    print(f"CPU поріг: {args.cpu_threshold}%")
    print(f"Memory поріг: {args.memory_threshold}%")
    print(f"Інтервал: {args.interval}s")
    print(f"Verbose: {args.verbose}")
    print(f"Формат: {args.format}")
```

**Приклади запуску:**
```bash
python script.py report.txt
python script.py report.txt --cpu-threshold 70 --interval 30
python script.py report.txt --verbose --format json
python script.py --help
```

---

### **Слайд 15. Типи аргументів та валідація**

```python
import argparse
from pathlib import Path

def positive_int(value):
    """Валідатор для позитивних цілих чисел"""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} не є позитивним числом")
    return ivalue

def percentage(value):
    """Валідатор для відсотків (0-100)"""
    fvalue = float(value)
    if not 0 <= fvalue <= 100:
        raise argparse.ArgumentTypeError(f"{value} має бути між 0 та 100")
    return fvalue

def existing_directory(value):
    """Валідатор для існуючої директорії"""
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Директорія {value} не існує")
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{value} не є директорією")
    return path

def create_advanced_parser():
    parser = argparse.ArgumentParser(description='Розширений моніторинг')

    # З валідацією
    parser.add_argument(
        '--cpu-threshold',
        type=percentage,
        default=80.0,
        help='Поріг CPU (0-100%%)'
    )

    parser.add_argument(
        '--interval',
        type=positive_int,
        default=60,
        help='Інтервал між перевірками (позитивне число)'
    )

    parser.add_argument(
        '--output-dir',
        type=existing_directory,
        default=Path('.'),
        help='Директорія для звітів'
    )

    # Взаємовиключні аргументи
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--json', action='store_true', help='Формат JSON')
    group.add_argument('--csv', action='store_true', help='Формат CSV')

    # Аргументи з множинними значеннями
    parser.add_argument(
        '--processes',
        nargs='+',
        help='Процеси для моніторингу (один або більше)'
    )

    return parser

# Використання
parser = create_advanced_parser()
args = parser.parse_args()
```

---

### **Слайд 16. Підкоманди (subcommands)**

```python
import argparse

def create_parser_with_subcommands():
    """Парсер з підкомандами (як у git: git commit, git push)"""
    parser = argparse.ArgumentParser(
        description='Утиліта моніторингу системи'
    )

    subparsers = parser.add_subparsers(
        dest='command',
        help='Доступні команди'
    )

    # Підкоманда: monitor
    monitor_parser = subparsers.add_parser(
        'monitor',
        help='Запустити моніторинг'
    )
    monitor_parser.add_argument('--interval', type=int, default=60)
    monitor_parser.add_argument('--threshold', type=float, default=80.0)

    # Підкоманда: report
    report_parser = subparsers.add_parser(
        'report',
        help='Згенерувати звіт'
    )
    report_parser.add_argument('output_file')
    report_parser.add_argument('--format', choices=['text', 'json', 'csv'])

    # Підкоманда: kill
    kill_parser = subparsers.add_parser(
        'kill',
        help='Зупинити процес'
    )
    kill_parser.add_argument('pid', type=int, help='PID процесу')

    return parser

def main():
    parser = create_parser_with_subcommands()
    args = parser.parse_args()

    if args.command == 'monitor':
        print(f"Запуск моніторингу з інтервалом {args.interval}s")
        # monitor_system(args.interval, args.threshold)

    elif args.command == 'report':
        print(f"Генерація звіту у {args.output_file}")
        # generate_report(args.output_file, args.format)

    elif args.command == 'kill':
        print(f"Зупинка процесу {args.pid}")
        # kill_process(args.pid)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Приклади запуску:**
```bash
python monitor_tool.py monitor --interval 30 --threshold 75
python monitor_tool.py report output.json --format json
python monitor_tool.py kill 1234
python monitor_tool.py --help
python monitor_tool.py monitor --help
```

---

## 🔹 ЧАСТИНА 5. Інтеграція всього разом

---

### **Слайд 17. Повний приклад: Система моніторингу з усіма lifehacks**

```python
#!/usr/bin/env python3
"""
Система моніторингу з Single Instance та argparse
"""
import argparse
import psutil
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict

class SingleInstance:
    """Single Instance через PID файл"""
    def __init__(self, lockfile: str):
        self.lockfile = Path(lockfile)
        self.pid = os.getpid()

    def __enter__(self):
        if self.lockfile.exists():
            try:
                old_pid = int(self.lockfile.read_text().strip())
                if self._is_running(old_pid):
                    print(f"❌ Моніторинг вже запущений (PID: {old_pid})")
                    sys.exit(1)
                else:
                    self.lockfile.unlink()
            except (ValueError, FileNotFoundError):
                self.lockfile.unlink()

        self.lockfile.write_text(str(self.pid))
        print(f"✅ Моніторинг запущено (PID: {self.pid})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lockfile.exists():
            self.lockfile.unlink()

    @staticmethod
    def _is_running(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

class SystemMonitor:
    """Клас для моніторингу системи"""

    def __init__(self, cpu_threshold: float, memory_threshold: float):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold

    def collect_metrics(self) -> Dict:
        """Збір метрик системи"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'warning': cpu_percent > self.cpu_threshold
            },
            'memory': {
                'percent': memory.percent,
                'used_gb': memory.used / (1024**3),
                'warning': memory.percent > self.memory_threshold
            },
            'disk': {
                'percent': disk.percent,
                'free_gb': disk.free / (1024**3)
            }
        }

    def check_alerts(self, metrics: Dict) -> list:
        """Перевірка на попередження"""
        alerts = []

        if metrics['cpu']['warning']:
            alerts.append(
                f"⚠️  CPU: {metrics['cpu']['percent']:.1f}% "
                f"(поріг: {self.cpu_threshold}%)"
            )

        if metrics['memory']['warning']:
            alerts.append(
                f"⚠️  Пам'ять: {metrics['memory']['percent']:.1f}% "
                f"(поріг: {self.memory_threshold}%)"
            )

        return alerts

def create_parser():
    """Створення парсера аргументів"""
    parser = argparse.ArgumentParser(
        description='Система моніторингу системних ресурсів',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--cpu-threshold',
        type=float,
        default=80.0,
        help='Поріг CPU для попередження (%%)'
    )

    parser.add_argument(
        '--memory-threshold',
        type=float,
        default=90.0,
        help='Поріг пам\'яті для попередження (%%)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        default=Path('monitoring.json'),
        help='Файл для збереження звіту'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Детальний вивід'
    )

    parser.add_argument(
        '--lockfile',
        type=Path,
        default=Path('/tmp/system_monitor.lock'),
        help='Lock файл для Single Instance'
    )

    return parser

def main():
    """Головна функція"""
    parser = create_parser()
    args = parser.parse_args()

    # Використання Single Instance
    with SingleInstance(str(args.lockfile)):
        # Створення монітора
        monitor = SystemMonitor(
            cpu_threshold=args.cpu_threshold,
            memory_threshold=args.memory_threshold
        )

        # Збір метрик
        metrics = monitor.collect_metrics()

        # Перевірка попереджень
        alerts = monitor.check_alerts(metrics)

        # Вивід результатів
        if args.verbose or alerts:
            print(f"\n{'='*60}")
            print(f"Час: {metrics['timestamp']}")
            print(f"CPU: {metrics['cpu']['percent']:.1f}%")
            print(f"Пам'ять: {metrics['memory']['percent']:.1f}% "
                  f"({metrics['memory']['used_gb']:.2f} GB)")
            print(f"Диск: {metrics['disk']['percent']:.1f}% "
                  f"(вільно: {metrics['disk']['free_gb']:.2f} GB)")

            if alerts:
                print("\n🚨 ПОПЕРЕДЖЕННЯ:")
                for alert in alerts:
                    print(f"  {alert}")

            print(f"{'='*60}\n")

        # Збереження звіту
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(metrics, f, indent=2)

        if args.verbose:
            print(f"✅ Звіт збережено: {args.output}")

if __name__ == "__main__":
    main()
```

**Приклади використання:**
```bash
# Базовий запуск
python system_monitor.py

# З налаштованими порогами
python system_monitor.py --cpu-threshold 70 --memory-threshold 85

# З детальним виводом
python system_monitor.py --verbose --output /var/log/monitoring.json

# Спроба запуску другого екземпляра
python system_monitor.py  # ❌ Помилка: вже запущений

# Довідка
python system_monitor.py --help
```

---

### **Слайд 18. Інтеграція з cron для періодичного моніторингу**

**Створення скрипту для cron:**

```bash
#!/bin/bash
# monitor_cron.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON="/usr/bin/python3"
SCRIPT="${SCRIPT_DIR}/system_monitor.py"
LOG_DIR="/var/log/monitoring"

# Створення директорії для логів
mkdir -p "$LOG_DIR"

# Запуск моніторингу
$PYTHON $SCRIPT \
    --cpu-threshold 75 \
    --memory-threshold 85 \
    --output "${LOG_DIR}/report_$(date +%Y%m%d_%H%M%S).json" \
    --verbose >> "${LOG_DIR}/monitor.log" 2>&1
```

**Додавання до crontab:**
```bash
# Відкрити crontab для редагування
crontab -e

# Запуск кожні 5 хвилин
*/5 * * * * /path/to/monitor_cron.sh

# Запуск щогодини
0 * * * * /path/to/monitor_cron.sh

# Запуск щодня о 9:00
0 9 * * * /path/to/monitor_cron.sh
```

**Завдяки Single Instance:**
- Якщо попередній запуск не завершився — новий не запуститься
- Немає дублювання процесів
- Система залишається стабільною

---

## 📚 Підсумок заняття

### **Що ми вивчили:**

1. **Моніторинг з psutil:**
   - Збір інформації про CPU, пам'ять, диски, мережу
   - Робота з процесами
   - Фільтрація та пошук процесів

2. **Створення звітів:**
   - Структурування даних
   - Генерація текстових, JSON та CSV звітів
   - Збереження історії моніторингу

3. **Lifehack 1 - Single Instance:**
   - PID-файл метод
   - Використання psutil
   - Сокет-блокування
   - Запобігання дублюванню процесів

4. **Lifehack 2 - argparse:**
   - Створення гнучких скриптів
   - Валідація аргументів
   - Підкоманди
   - Інтеграція з системами автоматизації

### **Практичне застосування:**

✅ Моніторинг серверів та робочих станцій
✅ Створення систем попереджень про перевантаження
✅ Автоматизація системного адміністрування
✅ Збір метрик для аналізу продуктивності
✅ Інтеграція з системами логування

---

## 🏠 Самостійна робота (0.5 год)

### **Завдання:**

Створити повноцінну систему моніторингу з наступними можливостями:

1. **Моніторинг кількох параметрів:**
   - CPU, пам'ять, диски
   - Топ-5 процесів за CPU
   - Топ-5 процесів за пам'яттю

2. **Single Instance:**
   - Реалізувати з PID-файлом або psutil

3. **Конфігурація через argparse:**
   - Пороги для всіх параметрів
   - Формат виводу (text/json/csv)
   - Режим роботи (one-shot/continuous)

4. **Додаткові функції:**
   - Email-попередження при перевищенні порогів
   - Ротація старих звітів (зберігати лише останні N)
   - Веб-інтерфейс для перегляду метрик (опціонально)

5. **Автозапуск:**
   - Налаштувати запуск через cron/systemd
   - Створити скрипт встановлення

### **Критерії оцінювання:**

- ✅ Коректний збір метрик (2 бали)
- ✅ Реалізація Single Instance (2 бали)
- ✅ Повна конфігурація через argparse (2 бали)
- ✅ Генерація звітів у різних форматах (2 бали)
- ✅ Додаткові функції (2 бали)

**Максимум: 10 балів**

---

## 🔗 Корисні ресурси

1. **Документація psutil:**
   - https://psutil.readthedocs.io/

2. **Документація argparse:**
   - https://docs.python.org/3/library/argparse.html

3. **Системне програмування в Python:**
   - https://realpython.com/python-subprocess/
   - https://realpython.com/command-line-interfaces-python-argparse/

4. **Паттерн Single Instance:**
   - https://stackoverflow.com/questions/220525/ensure-a-single-instance-of-an-application-in-linux

---

**Успіхів у створенні систем моніторингу! 🚀**