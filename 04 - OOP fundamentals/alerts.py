from datetime import datetime


class SecurityAlert:  # Креслення для оповіщення
    def __init__(self, ip_address, severity, alert_type):
        self.ip_address = ip_address
        self.severity = severity
        self.alert_type = alert_type
        self.timestamp = datetime.now()

# Створення конкретних оповіщень
alert1 = SecurityAlert("192.168.1.100", "HIGH", "BRUTE_FORCE")
alert2 = SecurityAlert("10.0.0.50", "MEDIUM", "PORT_SCAN")


class SecurityAlert:
    def __init__(self, ip, severity):
        self.ip_address = ip
        self.severity_level = severity
        self.timestamp = "2025-01-01 10:30:45"

    def get_info(self):
        return f"Alert from {self.ip_address}: {self.severity_level}"


# Створюємо об'єкт
alert = SecurityAlert("192.168.1.100", "HIGH")

# Аналізуємо що відбувається з оператором точка
print("=== Доступ до атрибутів ===")
"""
 alert.ip_address
 ↑     ↑    ↑
 |     |    └── назва атрибута
 |     └── оператор точка (доступ)
 └── об'єкт
"""
print(f"IP адреса: {alert.ip_address}")  # Читаємо атрибут
print(f"Рівень: {alert.severity_level}")  # Читаємо атрибут
print(f"Час: {alert.timestamp}")  # Читаємо атрибут

print("\n=== Зміна атрибутів ===")
alert.severity_level = "CRITICAL"  # Змінюємо атрибут
print(f"Новий рівень: {alert.severity_level}")

print("\n=== Виклик методів ===")

"""
 alert.get_info()
 ↑     ↑        ↑
 |     |        └── круглі дужки = виклик методу
 |     └── оператор точка (доступ)
 └── об'єкт
"""

result = alert.get_info()  # Викликаємо метод
print(f"Інформація: {result}")

