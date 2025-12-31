#!/usr/bin/env python3
"""
Розширений багатопотоковий сканер портів з Banner Grabbing
Використовує ThreadPoolExecutor та підтримує ідентифікацію сервісів

⚠️ ВАЖЛИВО: Використовуйте ТІЛЬКИ на власних системах або з дозволом!
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import json
from datetime import datetime


def grab_banner(host, port, timeout=2):
    """
    Отримує banner від сервісу для ідентифікації версії

    Args:
        host: IP адреса
        port: порт
        timeout: таймаут

    Returns:
        str: banner сервісу або None
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))

            # Деякі сервіси одразу надсилають banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

            if not banner:
                # Спробуємо надіслати HTTP запит
                sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

            return banner[:200] if banner else None
    except:
        return None


class AdvancedPortScanner:
    """Розширений сканер портів з додатковими можливостями"""

    def __init__(self, host, timeout=1, grab_banners=True):
        self.host = host
        self.timeout = timeout
        self.grab_banners = grab_banners
        self.results = []
        self.start_time = None

    def scan_port(self, port):
        """
        Сканує один порт з отриманням інформації про сервіс

        Args:
            port: номер порту

        Returns:
            dict: інформація про порт
        """
        result = {
            'port': port,
            'is_open': False,
            'service': None,
            'banner': None,
            'response_time': None
        }

        try:
            start = time.time()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                connection_result = sock.connect_ex((self.host, port))

                if connection_result == 0:
                    result['is_open'] = True
                    result['response_time'] = time.time() - start

                    # Отримуємо назву сервісу
                    try:
                        result['service'] = socket.getservbyport(port)
                    except:
                        result['service'] = 'unknown'

                    # Отримуємо banner якщо потрібно
                    if self.grab_banners:
                        result['banner'] = grab_banner(
                            self.host, port, self.timeout
                        )

        except Exception as e:
            result['error'] = str(e)

        return result

    def scan_range(self, start_port, end_port, max_workers=50):
        """
        Сканує діапазон портів

        Args:
            start_port: початковий порт
            end_port: кінцевий порт
            max_workers: кількість потоків

        Returns:
            list: список результатів для відкритих портів
        """
        self.start_time = time.time()
        total_ports = end_port - start_port + 1

        print(f"\n{'='*80}")
        print(f"🔍 Advanced Port Scanner")
        print(f"{'='*80}")
        print(f"🎯 Target: {self.host}")
        print(f"📊 Port Range: {start_port}-{end_port} ({total_ports} ports)")
        print(f"🧵 Threads: {max_workers}")
        print(f"⏱️  Timeout: {self.timeout}s")
        print(f"🏷️  Banner Grabbing: {'Enabled' if self.grab_banners else 'Disabled'}")
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.scan_port, port): port
                for port in range(start_port, end_port + 1)
            }

            completed = 0

            for future in as_completed(futures):
                completed += 1
                result = future.result()

                if result['is_open']:
                    self.results.append(result)
                    self._print_result(result)

                # Прогрес кожні 5%
                if completed % (total_ports // 20 or 1) == 0:
                    progress = (completed / total_ports) * 100
                    elapsed = time.time() - self.start_time
                    speed = completed / elapsed
                    eta = (total_ports - completed) / speed if speed > 0 else 0

                    print(f"⏳ Progress: {progress:5.1f}% | "
                          f"Scanned: {completed:5d}/{total_ports} | "
                          f"Speed: {speed:6.1f} p/s | "
                          f"ETA: {eta:5.0f}s")

        self._print_summary(total_ports)
        return self.results

    def _print_result(self, result):
        """Виводить інформацію про відкритий порт"""
        response_time_ms = result['response_time'] * 1000 if result['response_time'] else 0

        print(f"\n✓ Port {result['port']:5d} | {result['service']:15s} | "
              f"Response: {response_time_ms:6.2f}ms")

        if result['banner']:
            # Виводимо перший рядок banner
            banner_line = result['banner'].split('\n')[0][:70]
            print(f"  └─ Banner: {banner_line}")

    def _print_summary(self, total_ports):
        """Виводить підсумкову статистику"""
        elapsed = time.time() - self.start_time

        print(f"\n{'='*80}")
        print(f"📈 Scan Summary")
        print(f"{'='*80}")
        print(f"  • Total ports scanned: {total_ports}")
        print(f"  • Open ports found: {len(self.results)}")
        print(f"  • Closed ports: {total_ports - len(self.results)}")
        print(f"  • Time elapsed: {elapsed:.2f} seconds")
        print(f"  • Average speed: {total_ports / elapsed:.2f} ports/sec")

        if self.results:
            avg_response = sum(
                r['response_time'] for r in self.results if r['response_time']
            ) / len(self.results)
            print(f"  • Average response time: {avg_response * 1000:.2f}ms")

        print(f"{'='*80}\n")

        if self.results:
            print("🔓 Open Ports Summary:")
            for result in sorted(self.results, key=lambda x: x['port']):
                print(f"   • {result['port']:5d} - {result['service']}")

    def save_results(self, filename, format='txt'):
        """
        Зберігає результати у файл

        Args:
            filename: ім'я файлу
            format: формат ('txt', 'json', 'csv')
        """
        if format == 'json':
            self._save_json(filename)
        elif format == 'csv':
            self._save_csv(filename)
        else:
            self._save_txt(filename)

        print(f"💾 Results saved to: {filename}")

    def _save_txt(self, filename):
        """Зберігає у текстовому форматі"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Port Scan Results\n")
            f.write(f"{'='*60}\n")
            f.write(f"Target: {self.host}\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Open Ports: {len(self.results)}\n")
            f.write(f"\n{'='*60}\n\n")

            for result in sorted(self.results, key=lambda x: x['port']):
                f.write(f"Port: {result['port']}\n")
                f.write(f"Service: {result['service']}\n")
                if result['response_time']:
                    f.write(f"Response Time: {result['response_time']*1000:.2f}ms\n")
                if result['banner']:
                    f.write(f"Banner:\n{result['banner']}\n")
                f.write(f"{'-'*60}\n")

    def _save_json(self, filename):
        """Зберігає у JSON форматі"""
        data = {
            'scan_info': {
                'target': self.host,
                'scan_date': datetime.now().isoformat(),
                'total_open_ports': len(self.results)
            },
            'results': self.results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _save_csv(self, filename):
        """Зберігає у CSV форматі"""
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['port', 'service', 'response_time_ms', 'banner']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'port': result['port'],
                    'service': result['service'],
                    'response_time_ms': f"{result['response_time']*1000:.2f}" if result['response_time'] else '',
                    'banner': result['banner'][:100] if result['banner'] else ''
                })


def main():
    """Головна функція з CLI"""
    parser = argparse.ArgumentParser(
        description="Advanced multi-threaded port scanner with banner grabbing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t 127.0.0.1 -s 1 -e 1000
  %(prog)s -t example.com -s 1 -e 65535 -w 200 --no-banner
  %(prog)s -t 192.168.1.1 --common -o results.json

⚠️  WARNING: Only scan systems you own or have permission to test!
        """
    )

    parser.add_argument('-t', '--target', required=True, help='Target host')
    parser.add_argument('-s', '--start', type=int, default=1, help='Start port (default: 1)')
    parser.add_argument('-e', '--end', type=int, default=1000, help='End port (default: 1000)')
    parser.add_argument('-w', '--workers', type=int, default=50, help='Worker threads (default: 50)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Timeout (default: 1.0s)')
    parser.add_argument('--no-banner', action='store_true', help='Disable banner grabbing')
    parser.add_argument('-o', '--output', help='Output file (supports .txt, .json, .csv)')
    parser.add_argument('--common', action='store_true', help='Scan common ports only')

    args = parser.parse_args()

    # Створюємо сканер
    scanner = AdvancedPortScanner(
        host=args.target,
        timeout=args.timeout,
        grab_banners=not args.no_banner
    )

    # Визначаємо діапазон портів
    if args.common:
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
            443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443
        ]
        # Сканування списку портів
        for port in common_ports:
            result = scanner.scan_port(port)
            if result['is_open']:
                scanner.results.append(result)
                scanner._print_result(result)
        scanner._print_summary(len(common_ports))
    else:
        # Сканування діапазону
        scanner.scan_range(args.start, args.end, args.workers)

    # Збереження результатів
    if args.output:
        if args.output.endswith('.json'):
            scanner.save_results(args.output, 'json')
        elif args.output.endswith('.csv'):
            scanner.save_results(args.output, 'csv')
        else:
            scanner.save_results(args.output, 'txt')


if __name__ == "__main__":
    # Приклад використання без CLI
    if True:  # Змініть на False для використання CLI
        scanner = AdvancedPortScanner("127.0.0.1", timeout=1, grab_banners=True)
        scanner.scan_range(1, 1000, max_workers=100)

        # Збереження результатів
        if scanner.results:
            scanner.save_results("scan_results.json", "json")
    else:
        main()