#!/usr/bin/env python3
"""
Порівняння продуктивності різних підходів до багатопоточності
Демонструє різницю між послідовним виконанням та різними методами паралелізації
"""

import time
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue
import statistics
import matplotlib.pyplot as plt
from tabulate import tabulate


class PerformanceTester:
    """Клас для тестування продуктивності різних підходів"""

    def __init__(self, host="127.0.0.1", port_range=(1, 500)):
        self.host = host
        self.port_range = port_range
        self.results = {}

    def scan_port(self, port):
        """Базова функція сканування порту"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                result = sock.connect_ex((self.host, port))
                return result == 0
        except:
            return False

    def sequential_scan(self):
        """Послідовне сканування (без багатопоточності)"""
        print("\n🔄 Running Sequential Scan...")
        start = time.time()

        open_ports = []
        ports_to_scan = list(range(*self.port_range))

        for i, port in enumerate(ports_to_scan):
            if self.scan_port(port):
                open_ports.append(port)

            if (i + 1) % 50 == 0:
                print(f"   Scanned: {i+1}/{len(ports_to_scan)}")

        elapsed = time.time() - start

        self.results['Sequential'] = {
            'time': elapsed,
            'open_ports': len(open_ports),
            'speed': len(ports_to_scan) / elapsed
        }

        print(f"✓ Completed in {elapsed:.2f}s | "
              f"Speed: {self.results['Sequential']['speed']:.2f} ports/s")

        return elapsed

    def threaded_scan(self, num_threads, label=None):
        """Сканування з ThreadPoolExecutor"""
        label = label or f"ThreadPool-{num_threads}"
        print(f"\n🧵 Running {label}...")

        start = time.time()
        open_ports = []
        ports_to_scan = list(range(*self.port_range))

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = executor.map(self.scan_port, ports_to_scan)
            open_ports = [
                port for port, is_open in zip(ports_to_scan, results)
                if is_open
            ]

        elapsed = time.time() - start

        self.results[label] = {
            'time': elapsed,
            'open_ports': len(open_ports),
            'speed': len(ports_to_scan) / elapsed
        }

        print(f"✓ Completed in {elapsed:.2f}s | "
              f"Speed: {self.results[label]['speed']:.2f} ports/s")

        return elapsed

    def queue_based_scan(self, num_workers):
        """Сканування з використанням Queue"""
        label = f"Queue-{num_workers}"
        print(f"\n📦 Running {label}...")

        start = time.time()
        port_queue = Queue()
        results_queue = Queue()
        ports_to_scan = list(range(*self.port_range))

        # Заповнюємо чергу
        for port in ports_to_scan:
            port_queue.put(port)

        def worker():
            while not port_queue.empty():
                try:
                    port = port_queue.get(timeout=0.1)
                    if self.scan_port(port):
                        results_queue.put(port)
                    port_queue.task_done()
                except:
                    break

        # Створюємо воркерів
        threads = []
        for _ in range(num_workers):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        # Чекаємо завершення
        port_queue.join()
        for t in threads:
            t.join()

        elapsed = time.time() - start
        open_ports = results_queue.qsize()

        self.results[label] = {
            'time': elapsed,
            'open_ports': open_ports,
            'speed': len(ports_to_scan) / elapsed
        }

        print(f"✓ Completed in {elapsed:.2f}s | "
              f"Speed: {self.results[label]['speed']:.2f} ports/s")

        return elapsed

    def find_optimal_threads(self):
        """Знаходить оптимальну кількість потоків"""
        print(f"\n{'='*70}")
        print("🔍 Finding Optimal Thread Count")
        print(f"{'='*70}")

        thread_counts = [5, 10, 25, 50, 100, 200, 500]
        times = []

        for count in thread_counts:
            elapsed = self.threaded_scan(count, f"Threads-{count}")
            times.append(elapsed)

        # Знаходимо оптимальну кількість
        optimal_idx = times.index(min(times))
        optimal_count = thread_counts[optimal_idx]
        best_time = times[optimal_idx]

        print(f"\n{'='*70}")
        print(f"🎯 Optimal thread count: {optimal_count}")
        print(f"⚡ Best time: {best_time:.2f}s")
        print(f"📊 Speed: {(self.port_range[1] - self.port_range[0]) / best_time:.2f} ports/s")
        print(f"{'='*70}")

        return optimal_count, times

    def run_all_tests(self):
        """Запускає всі тести"""
        print(f"\n{'='*80}")
        print(f"🧪 Performance Testing Suite")
        print(f"{'='*80}")
        print(f"🎯 Target: {self.host}")
        print(f"📊 Port range: {self.port_range[0]}-{self.port_range[1]} "
              f"({self.port_range[1] - self.port_range[0]} ports)")
        print(f"⏰ Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

        # 1. Послідовне сканування
        self.sequential_scan()

        # 2. Багатопотокове з різною кількістю потоків
        for num_threads in [10, 50, 100]:
            self.threaded_scan(num_threads)

        # 3. Queue-based
        self.queue_based_scan(50)

        # 4. Виводимо результати
        self.print_comparison()

        # 5. Візуалізація (якщо є matplotlib)
        try:
            self.plot_results()
        except:
            print("\n⚠️  Install matplotlib for visualization: pip install matplotlib")

    def print_comparison(self):
        """Виводить порівняльну таблицю"""
        print(f"\n{'='*80}")
        print(f"📊 Performance Comparison")
        print(f"{'='*80}\n")

        # Готуємо дані для таблиці
        table_data = []
        baseline = self.results.get('Sequential', {}).get('time', 1)

        sorted_results = sorted(
            self.results.items(),
            key=lambda x: x[1]['time']
        )

        for method, data in sorted_results:
            speedup = baseline / data['time']
            efficiency = (speedup / self._get_threads(method)) * 100 if self._get_threads(method) else 0

            table_data.append([
                method,
                f"{data['time']:.2f}s",
                f"{data['speed']:.2f}",
                f"{speedup:.2f}x",
                f"{efficiency:.1f}%" if efficiency else "N/A"
            ])

        headers = ["Method", "Time", "Speed (p/s)", "Speedup", "Efficiency"]

        try:
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except:
            # Fallback якщо tabulate не встановлено
            print(f"{'Method':<20} {'Time':<12} {'Speed':<15} {'Speedup':<12} {'Efficiency':<12}")
            print("-" * 80)
            for row in table_data:
                print(f"{row[0]:<20} {row[1]:<12} {row[2]:<15} {row[3]:<12} {row[4]:<12}")

        print(f"\n{'='*80}")

        # Статистика
        times = [data['time'] for data in self.results.values()]
        speedups = [baseline / t for t in times]

        print(f"\n📈 Statistics:")
        print(f"  • Average time: {statistics.mean(times):.2f}s")
        print(f"  • Best time: {min(times):.2f}s ({min(times)/max(times)*100:.1f}% of worst)")
        print(f"  • Worst time: {max(times):.2f}s")
        print(f"  • Max speedup: {max(speedups):.2f}x")
        print(f"  • Average speedup: {statistics.mean(speedups):.2f}x")

        print(f"\n{'='*80}\n")

    def _get_threads(self, method_name):
        """Витягує кількість потоків з назви методу"""
        if 'Sequential' in method_name:
            return 1
        try:
            return int(method_name.split('-')[1])
        except:
            return None

    def plot_results(self):
        """Візуалізує результати"""
        print("\n📊 Generating visualization...")

        # Готуємо дані
        methods = []
        times = []
        speedups = []

        baseline = self.results.get('Sequential', {}).get('time', 1)

        for method, data in sorted(self.results.items(), key=lambda x: x[1]['time']):
            methods.append(method)
            times.append(data['time'])
            speedups.append(baseline / data['time'])

        # Створюємо графіки
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # График 1: Час виконання
        colors = ['red' if 'Sequential' in m else 'green' for m in methods]
        ax1.barh(methods, times, color=colors, alpha=0.7)
        ax1.set_xlabel('Time (seconds)', fontsize=12)
        ax1.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)

        # Додаємо значення на графік
        for i, (method, time_val) in enumerate(zip(methods, times)):
            ax1.text(time_val, i, f' {time_val:.2f}s', va='center')

        # График 2: Прискорення (Speedup)
        colors2 = ['red' if 'Sequential' in m else 'blue' for m in methods]
        ax2.barh(methods, speedups, color=colors2, alpha=0.7)
        ax2.set_xlabel('Speedup (x times faster)', fontsize=12)
        ax2.set_title('Speedup Comparison', fontsize=14, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        ax2.axvline(x=1, color='red', linestyle='--', linewidth=2, label='Baseline')

        # Додаємо значення
        for i, (method, speedup) in enumerate(zip(methods, speedups)):
            ax2.text(speedup, i, f' {speedup:.2f}x', va='center')

        plt.tight_layout()

        # Зберігаємо графік
        filename = 'performance_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved to: {filename}")

        # Показуємо графік
        # plt.show()  # Розкоментуйте для показу

    def export_results(self, filename='results.json'):
        """Експортує результати у JSON"""
        import json

        data = {
            'test_info': {
                'host': self.host,
                'port_range': self.port_range,
                'total_ports': self.port_range[1] - self.port_range[0],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'results': self.results
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Results exported to: {filename}")


def demo_io_vs_cpu_bound():
    """Демонстрація різниці між I/O-bound та CPU-bound задачами"""
    print(f"\n{'='*80}")
    print("🎓 Demo: I/O-bound vs CPU-bound Tasks")
    print(f"{'='*80}\n")

    # I/O-bound задача (імітація мережевої операції)
    def io_bound_task():
        time.sleep(0.1)  # Імітація очікування I/O
        return "done"

    # CPU-bound задача (обчислення)
    def cpu_bound_task():
        total = 0
        for i in range(1000000):
            total += i ** 2
        return total

    print("1️⃣  Testing I/O-bound task...")

    # Послідовне виконання
    start = time.time()
    for _ in range(10):
        io_bound_task()
    sequential_io = time.time() - start

    # З потоками
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(lambda x: io_bound_task(), range(10)))
    threaded_io = time.time() - start

    print(f"   Sequential: {sequential_io:.2f}s")
    print(f"   Threaded:   {threaded_io:.2f}s")
    print(f"   Speedup:    {sequential_io/threaded_io:.2f}x ✅ Good speedup!\n")

    print("2️⃣  Testing CPU-bound task...")

    # Послідовне виконання
    start = time.time()
    for _ in range(4):
        cpu_bound_task()
    sequential_cpu = time.time() - start

    # З потоками (через GIL не буде прискорення)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(lambda x: cpu_bound_task(), range(4)))
    threaded_cpu = time.time() - start

    print(f"   Sequential: {sequential_cpu:.2f}s")
    print(f"   Threaded:   {threaded_cpu:.2f}s")
    print(f"   Speedup:    {sequential_cpu/threaded_cpu:.2f}x ❌ No speedup due to GIL!\n")

    print("💡 Conclusion:")
    print("   • Use threading for I/O-bound tasks (network, files, DB)")
    print("   • Use multiprocessing for CPU-bound tasks (calculations, processing)")
    print(f"{'='*80}\n")


def main():
    """Головна функція"""
    print("\n" + "="*80)
    print("🚀 Multi-threading Performance Testing Tool")
    print("="*80)

    # Демонстрація I/O vs CPU
    demo_io_vs_cpu_bound()

    # Основне тестування
    tester = PerformanceTester(
        host="127.0.0.1",
        port_range=(1, 500)
    )

    # Запускаємо всі тести
    tester.run_all_tests()

    # Знаходимо оптимальну кількість потоків
    # optimal, times = tester.find_optimal_threads()

    # Експорт результатів
    tester.export_results('performance_results.json')


if __name__ == "__main__":
    main()