#!/usr/bin/env python3
"""
Приклади коду для заняття 5.4: Моніторинг системних процесів
"""

import psutil
import os
import sys
import socket
import argparse
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List


# ============================================================================
# ЧАСТИНА 1: Моніторинг процесів з psutil
# ============================================================================

def example_1_basic_system_info():
    """Приклад 1: Базова інформація про систему"""
    print("=" * 60)
    print("ПРИКЛАД 1: Базова інформація про систему")
    print("=" * 60)

    # CPU
    print(f"\nCPU:")
    print(f"  Фізичних ядер: {psutil.cpu_count(logical=False)}")
    print(f"  Логічних ядер: {psutil.cpu_count(logical=True)}")
    print(f"  Завантаження CPU: {psutil.cpu_percent(interval=1)}%")

    # Використання по ядрах
    per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    for i, percent in enumerate(per_cpu):
        print(f"    Ядро {i}: {percent}%")

    # Пам'ять
    memory = psutil.virtual_memory()
    print(f"\nПам'ять:")
    print(f"  Всього: {memory.total / (1024**3):.2f} GB")
    print(f"  Доступно: {memory.available / (1024**3):.2f} GB")
    print(f"  Використано: {memory.used / (1024**3):.2f} GB ({memory.percent}%)")

    # Час роботи системи
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    print(f"\nСистема запущена: {boot_time}")
    print(f"Час роботи: {datetime.now() - boot_time}")


def example_2_disk_and_network():
    """Приклад 2: Інформація про диски та мережу"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 2: Диски та мережа")
    print("=" * 60)

    # Диски
    print("\nДиски:")
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

    # Мережа
    net_io = psutil.net_io_counters()
    print(f"\nМережа:")
    print(f"  Відправлено: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"  Отримано: {net_io.bytes_recv / (1024**2):.2f} MB")
    print(f"  Пакетів відправлено: {net_io.packets_sent}")
    print(f"  Пакетів отримано: {net_io.packets_recv}")


def example_3_process_info():
    """Приклад 3: Робота з процесами"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 3: Робота з процесами")
    print("=" * 60)

    # Поточний процес
    current = psutil.Process()
    print(f"\nПоточний процес:")
    print(f"  PID: {current.pid}")
    print(f"  Ім'я: {current.name()}")
    print(f"  Статус: {current.status()}")
    print(f"  Створений: {datetime.fromtimestamp(current.create_time())}")
    print(f"  CPU: {current.cpu_percent(interval=0.1)}%")
    print(f"  Пам'ять: {current.memory_info().rss / (1024**2):.2f} MB")
    print(f"  Потоків: {current.num_threads()}")

    # Список всіх процесів (перші 10)
    print(f"\nПерші 10 процесів:")
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            print(f"  PID: {proc.info['pid']:6d} | "
                  f"Ім'я: {proc.info['name']:30s} | "
                  f"Користувач: {proc.info['username']}")
            count += 1
            if count >= 10:
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def find_processes_by_name(name: str) -> List[psutil.Process]:
    """Знайти всі процеси за іменем"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if name.lower() in proc.info['name'].lower():
                processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes


def get_top_memory_processes(n: int = 5) -> List[Dict]:
    """Отримати топ N процесів за використанням пам'яті"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory': proc.info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes.sort(key=lambda x: x['memory'], reverse=True)
    return processes[:n]


def example_4_search_processes():
    """Приклад 4: Пошук процесів"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 4: Пошук процесів")
    print("=" * 60)

    # Пошук Python процесів
    python_procs = find_processes_by_name('python')
    print(f"\nЗнайдено {len(python_procs)} Python процесів:")
    for proc in python_procs[:5]:  # Показати перші 5
        try:
            print(f"  PID: {proc.pid}, Ім'я: {proc.name()}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Топ-5 процесів за пам'яттю
    print(f"\nТоп-5 процесів за використанням пам'яті:")
    for i, proc in enumerate(get_top_memory_processes(5), 1):
        print(f"  {i}. {proc['name']} (PID: {proc['pid']}): {proc['memory']:.2f}%")


# ============================================================================
# ЧАСТИНА 2: Створення звітів
# ============================================================================

def collect_system_info() -> Dict:
    """Збір всієї системної інформації"""
    # CPU
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

    return {
        'timestamp': datetime.now().isoformat(),
        'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        'cpu': cpu_info,
        'memory': memory_info,
        'disks': disk_info,
        'network': network_info
    }


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


def example_5_generate_reports():
    """Приклад 5: Генерація звітів"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 5: Генерація звітів")
    print("=" * 60)

    # Текстовий звіт
    print("\n" + generate_text_report())

    # JSON звіт
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    info = collect_system_info()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_file = output_dir / f"system_report_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    print(f"\n✅ JSON звіт збережено: {json_file}")

    # CSV звіт
    csv_file = output_dir / "monitoring.csv"
    row = {
        'timestamp': info['timestamp'],
        'cpu_percent': info['cpu']['total_usage'],
        'memory_percent': info['memory']['percent'],
        'memory_used_gb': info['memory']['used_gb'],
    }

    file_exists = csv_file.exists()
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"✅ CSV дані додано: {csv_file}")


# ============================================================================
# ЧАСТИНА 3: LIFEHACK 1 - Single Instance (PID файл)
# ============================================================================

class SingleInstance:
    """Гарантує, що запущений лише один екземпляр програми"""

    def __init__(self, lockfile: str = "/tmp/my_app.lock"):
        self.lockfile = Path(lockfile)
        self.pid = os.getpid()

    def __enter__(self):
        if self.lockfile.exists():
            try:
                old_pid = int(self.lockfile.read_text().strip())

                if self._is_process_running(old_pid):
                    print(f"❌ Програма вже запущена (PID: {old_pid})")
                    sys.exit(1)
                else:
                    print(f"⚠️  Знайдено старий lock файл (PID: {old_pid} не існує), видаляю...")
                    self.lockfile.unlink()
            except (ValueError, FileNotFoundError):
                self.lockfile.unlink()

        self.lockfile.write_text(str(self.pid))
        print(f"✅ Lock файл створено: {self.lockfile} (PID: {self.pid})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lockfile.exists():
            self.lockfile.unlink()
            print(f"✅ Lock файл видалено")

    @staticmethod
    def _is_process_running(pid: int) -> bool:
        """Перевірка чи процес з таким PID запущений"""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def example_6_single_instance_pid():
    """Приклад 6: Single Instance через PID файл"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 6: Single Instance через PID файл")
    print("=" * 60)

    with SingleInstance("/tmp/example_app.lock"):
        print("\n🚀 Програма запущена!")
        print("💡 Спробуйте запустити цей скрипт ще раз в іншому терміналі")
        print("⏳ Чекаємо 10 секунд...")

        import time
        for i in range(10, 0, -1):
            print(f"   {i}...", end='\r')
            time.sleep(1)

        print("\n✅ Робота завершена")


# ============================================================================
# ЧАСТИНА 4: LIFEHACK 1 - Single Instance (psutil)
# ============================================================================

class SingleInstancePsutil:
    """Single Instance з використанням psutil"""

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.current_pid = os.getpid()

    def __enter__(self):
        current_process = psutil.Process(self.current_pid)
        current_cmdline = current_process.cmdline()

        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                if proc.info['pid'] == self.current_pid:
                    continue

                if proc.info['cmdline'] == current_cmdline:
                    print(f"❌ Програма вже запущена (PID: {proc.info['pid']})")
                    print(f"   Командний рядок: {' '.join(current_cmdline)}")
                    sys.exit(1)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print(f"✅ Програма запущена (PID: {self.current_pid})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("✅ Програма завершена")


def example_7_single_instance_psutil():
    """Приклад 7: Single Instance через psutil"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 7: Single Instance через psutil")
    print("=" * 60)

    with SingleInstancePsutil("example_monitoring_app"):
        print("\n🚀 Програма запущена через psutil!")
        print("⏳ Чекаємо 5 секунд...")

        import time
        time.sleep(5)


# ============================================================================
# ЧАСТИНА 5: LIFEHACK 1 - Single Instance (Socket)
# ============================================================================

class SingleInstanceSocket:
    """Single Instance через мережевий сокет"""

    def __init__(self, port: int = 9999):
        self.port = port
        self.socket = None

    def __enter__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('127.0.0.1', self.port))
            print(f"✅ Програма запущена (порт {self.port} зайнято)")
            return self
        except socket.error:
            print(f"❌ Програма вже запущена (порт {self.port} зайнято)")
            sys.exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()
            print("✅ Сокет закрито")


def example_8_single_instance_socket():
    """Приклад 8: Single Instance через сокет"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 8: Single Instance через сокет")
    print("=" * 60)

    with SingleInstanceSocket(port=19999):
        print("\n🚀 Програма запущена через сокет!")
        print("⏳ Чекаємо 5 секунд...")

        import time
        time.sleep(5)


# ============================================================================
# ЧАСТИНА 6: LIFEHACK 2 - argparse
# ============================================================================

def create_basic_parser():
    """Створення базового парсера аргументів"""
    parser = argparse.ArgumentParser(
        description='Моніторинг системних ресурсів',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'output_file',
        help='Файл для збереження звіту'
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
        '--interval',
        type=int,
        default=60,
        help='Інтервал між перевірками (секунди)'
    )

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


def example_9_argparse_basic():
    """Приклад 9: Базове використання argparse"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 9: Базове використання argparse")
    print("=" * 60)

    print("\n💡 Приклад парсера аргументів створено!")
    print("   Використання:")
    print("   python script.py report.txt")
    print("   python script.py report.txt --cpu-threshold 70 --interval 30")
    print("   python script.py report.txt --verbose --format json")
    print("   python script.py --help")


# ============================================================================
# ЧАСТИНА 7: Повний приклад інтеграції
# ============================================================================

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

    def check_alerts(self, metrics: Dict) -> List[str]:
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


def example_10_full_integration():
    """Приклад 10: Повна інтеграція всіх компонентів"""
    print("\n" + "=" * 60)
    print("ПРИКЛАД 10: Повна інтеграція")
    print("=" * 60)

    # Single Instance
    with SingleInstance("/tmp/full_monitor.lock"):
        # Створення монітора
        monitor = SystemMonitor(cpu_threshold=80.0, memory_threshold=90.0)

        # Збір метрик
        metrics = monitor.collect_metrics()

        # Перевірка попереджень
        alerts = monitor.check_alerts(metrics)

        # Вивід результатів
        print(f"\n📊 Метрики системи:")
        print(f"  Час: {metrics['timestamp']}")
        print(f"  CPU: {metrics['cpu']['percent']:.1f}%")
        print(f"  Пам'ять: {metrics['memory']['percent']:.1f}% "
              f"({metrics['memory']['used_gb']:.2f} GB)")
        print(f"  Диск: {metrics['disk']['percent']:.1f}% "
              f"(вільно: {metrics['disk']['free_gb']:.2f} GB)")

        if alerts:
            print(f"\n🚨 ПОПЕРЕДЖЕННЯ:")
            for alert in alerts:
                print(f"  {alert}")
        else:
            print(f"\n✅ Всі параметри в нормі")

        # Збереження звіту
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "integrated_report.json"

        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2)

        print(f"\n💾 Звіт збережено: {output_file}")


# ============================================================================
# ГОЛОВНА ФУНКЦІЯ
# ============================================================================

def main():
    """Головна функція для запуску всіх прикладів"""
    examples = [
        ("Базова інформація про систему", example_1_basic_system_info),
        ("Диски та мережа", example_2_disk_and_network),
        ("Робота з процесами", example_3_process_info),
        ("Пошук процесів", example_4_search_processes),
        ("Генерація звітів", example_5_generate_reports),
        ("Single Instance (PID файл)", example_6_single_instance_pid),
        ("Single Instance (psutil)", example_7_single_instance_psutil),
        ("Single Instance (Socket)", example_8_single_instance_socket),
        ("Argparse базове", example_9_argparse_basic),
        ("Повна інтеграція", example_10_full_integration),
    ]

    print("🎓 ПРИКЛАДИ КОДУ ДЛЯ ЗАНЯТТЯ 5.4")
    print("Моніторинг системних процесів\n")

    while True:
        print("\n" + "=" * 60)
        print("Оберіть приклад для запуску:")
        print("=" * 60)

        for i, (name, _) in enumerate(examples, 1):
            print(f"{i:2d}. {name}")
        print(" 0. Вихід")

        try:
            choice = input("\nВаш вибір: ").strip()

            if choice == '0':
                print("\n👋 До побачення!")
                break

            choice_num = int(choice)
            if 1 <= choice_num <= len(examples):
                name, func = examples[choice_num - 1]
                func()
                input("\n⏸  Натисніть Enter для продовження...")
            else:
                print("❌ Невірний вибір!")

        except ValueError:
            print("❌ Будь ласка, введіть число!")
        except KeyboardInterrupt:
            print("\n\n👋 До побачення!")
            break
        except Exception as e:
            print(f"\n❌ Помилка: {e}")


if __name__ == "__main__":
    main()