#!/usr/bin/env python3
"""
Базовий багатопотоковий сканер портів
Використовує ThreadPoolExecutor для паралельного сканування портів

⚠️ ВАЖЛИВО: Використовуйте ТІЛЬКИ на власних системах або з дозволом!
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse


def scan_port(host, port, timeout=1):
    """
    Сканує один порт на хості

    Args:
        host: IP адреса або доменне ім'я
        port: номер порту для сканування
        timeout: таймаут підключення в секундах

    Returns:
        tuple: (port, is_open, service_name)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

            if result == 0:
                # Порт відкритий
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return (port, True, service)
            else:
                return (port, False, None)
    except socket.gaierror:
        return (port, False, None)
    except socket.error:
        return (port, False, None)


def scan_ports(host, ports, max_workers=100, timeout=1, verbose=False):
    """
    Сканує список портів на хості

    Args:
        host: IP адреса або доменне ім'я
        ports: список або діапазон портів
        max_workers: кількість потоків
        timeout: таймаут для кожного порту
        verbose: показувати закриті порти

    Returns:
        list: список відкритих портів
    """
    ports_list = list(ports)

    print(f"\n{'='*70}")
    print(f"🔍 Port Scanner")
    print(f"{'='*70}")
    print(f"🎯 Target: {host}")
    print(f"📊 Ports: {len(ports_list)}")
    print(f"🧵 Threads: {max_workers}")
    print(f"⏱️  Timeout: {timeout}s")
    print(f"{'='*70}\n")

    start_time = time.time()
    open_ports = []
    scanned = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Запускаємо сканування всіх портів
        futures = {
            executor.submit(scan_port, host, port, timeout): port
            for port in ports_list
        }

        # Обробляємо результати по мірі готовності
        for future in as_completed(futures):
            port = futures[future]
            scanned += 1

            try:
                port_num, is_open, service = future.result()

                if is_open:
                    open_ports.append(port_num)
                    print(f"✓ Port {port_num:5d} | OPEN     | Service: {service}")
                elif verbose:
                    print(f"✗ Port {port_num:5d} | CLOSED")

                # Прогрес кожні 10%
                if scanned % (len(ports_list) // 10 or 1) == 0:
                    progress = (scanned / len(ports_list)) * 100
                    print(f"⏳ Progress: {progress:.0f}% ({scanned}/{len(ports_list)})")

            except Exception as e:
                print(f"✗ Port {port} | ERROR: {e}")

    elapsed_time = time.time() - start_time

    # Підсумок
    print(f"\n{'='*70}")
    print(f"📈 Scan Summary")
    print(f"{'='*70}")
    print(f"  • Total ports scanned: {len(ports_list)}")
    print(f"  • Open ports found: {len(open_ports)}")
    print(f"  • Time elapsed: {elapsed_time:.2f} seconds")
    print(f"  • Speed: {len(ports_list) / elapsed_time:.2f} ports/sec")
    print(f"{'='*70}\n")

    if open_ports:
        print("🔓 Open ports:", ", ".join(map(str, sorted(open_ports))))
    else:
        print("🔒 No open ports found")

    return open_ports


def main():
    """Головна функція з CLI"""
    parser = argparse.ArgumentParser(
        description="Simple multi-threaded port scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t 127.0.0.1 -p 1-1000
  %(prog)s -t example.com -p 80,443,8080
  %(prog)s -t 192.168.1.1 -p 1-65535 -w 200

⚠️  WARNING: Only scan systems you own or have permission to test!
        """
    )

    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target host (IP or domain)'
    )

    parser.add_argument(
        '-p', '--ports',
        default='1-1000',
        help='Port range (e.g., 1-1000) or list (e.g., 80,443,8080)'
    )

    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=100,
        help='Number of worker threads (default: 100)'
    )

    parser.add_argument(
        '--timeout',
        type=float,
        default=1.0,
        help='Connection timeout in seconds (default: 1.0)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show closed ports'
    )

    parser.add_argument(
        '--common',
        action='store_true',
        help='Scan only common ports'
    )

    args = parser.parse_args()

    # Визначаємо порти для сканування
    if args.common:
        # Найпопулярніші порти
        ports = [
            20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139,
            143, 443, 445, 993, 995, 1723, 3306, 3389, 5432,
            5900, 8080, 8443
        ]
        print("📋 Scanning common ports...")
    elif '-' in args.ports:
        # Діапазон портів
        start, end = map(int, args.ports.split('-'))
        ports = range(start, end + 1)
    elif ',' in args.ports:
        # Список портів
        ports = [int(p.strip()) for p in args.ports.split(',')]
    else:
        # Один порт
        ports = [int(args.ports)]

    # Запускаємо сканування
    try:
        scan_ports(
            host=args.target,
            ports=ports,
            max_workers=args.workers,
            timeout=args.timeout,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Приклад використання без аргументів
    if True:  # Змініть на False для використання CLI
        # Сканування localhost
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080]
        scan_ports("127.0.0.1", common_ports, max_workers=20, verbose=False)
    else:
        main()