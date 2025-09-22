from datetime import datetime


class NetworkConnection:
    # Відомі порти сервісів
    WELL_KNOWN_PORTS = {
        22: "SSH", 80: "HTTP", 443: "HTTPS", 25: "SMTP",
        53: "DNS", 3389: "RDP", 3306: "MySQL"
    }

    # Підозрілі порти
    SUSPICIOUS_PORTS = {4444, 31337, 12345, 54321}

    def __init__(self, source_ip, dest_ip, dest_port, protocol="TCP"):
        self._source_ip = source_ip
        self._dest_ip = dest_ip
        self._dest_port = None
        self._protocol = protocol.upper()
        self._start_time = datetime.now()
        self._bytes_transferred = 0
        self._status = "ACTIVE"

        # Використовуємо setter для валідації
        self.dest_port = dest_port

    @property
    def dest_port(self):
        """Порт призначення"""
        return self._dest_port

    @dest_port.setter
    def dest_port(self, value):
        """Встановлення порту з валідацією"""
        try:
            port = int(value)
            if not 1 <= port <= 65535:
                raise ValueError("Port must be between 1 and 65535")
            self._dest_port = port
        except (ValueError, TypeError):
            raise ValueError("Port must be a valid integer")

    @property
    def connection_string(self):
        """Рядкове представлення з'єднання (тільки читання)"""
        return f"{self._source_ip} -> {self._dest_ip}:{self._dest_port}"

    @property
    def service_name(self):
        """Назва сервісу на основі порту (тільки читання)"""
        return self.WELL_KNOWN_PORTS.get(self._dest_port, "Unknown")

    @property
    def is_suspicious(self):
        """Перевірка підозрілості з'єднання (тільки читання)"""
        return (self._dest_port in self.SUSPICIOUS_PORTS or
                self._is_external_connection())

    @property
    def duration_seconds(self):
        """Тривалість з'єднання в секундах (тільки читання)"""
        return (datetime.now() - self._start_time).total_seconds()

    @property
    def bytes_transferred(self):
        """Кількість переданих байтів"""
        return self._bytes_transferred

    @bytes_transferred.setter
    def bytes_transferred(self, value):
        """Встановлення кількості байтів з валідацією"""
        if value < 0:
            raise ValueError("Bytes transferred cannot be negative")
        self._bytes_transferred = value

    @staticmethod
    def is_private_ip(ip):
        """Перевірка приватної IP адреси"""
        try:
            parts = list(map(int, ip.split('.')))
            return (parts[0] == 10 or
                    (parts[0] == 172 and 16 <= parts[1] <= 31) or
                    (parts[0] == 192 and parts[1] == 168))
        except:
            return False

    def _is_external_connection(self):
        """Приватний метод - перевірка зовнішнього з'єднання"""
        return (self.is_private_ip(self._source_ip) and
                not self.is_private_ip(self._dest_ip))

    def close_connection(self):
        """Закриття з'єднання"""
        self._status = "CLOSED"

    def __str__(self):
        return f"{self.connection_string} [{self.service_name}] {'⚠️SUSPICIOUS' if self.is_suspicious else '✅OK'}"


# Приклад використання
conn1 = NetworkConnection("192.168.1.100", "8.8.8.8", 80)
print("Connection 1:", conn1)
print(f"Duration: {conn1.duration_seconds:.1f} seconds")

conn2 = NetworkConnection("10.0.0.5", "192.168.1.200", 4444)
print("Connection 2:", conn2)
print(f"Is suspicious: {conn2.is_suspicious}")

# Тестування валідації
try:
    conn3 = NetworkConnection("192.168.1.1", "8.8.8.8", 99999)  # Неправильний порт
except ValueError as e:
    print(f"Validation error: {e}")

# Робота з properties
conn1.bytes_transferred = 1024
print(f"Bytes transferred: {conn1.bytes_transferred}")

# Спроба змінити read-only property викличе помилку
# conn1.service_name = "CUSTOM"  # AttributeError!