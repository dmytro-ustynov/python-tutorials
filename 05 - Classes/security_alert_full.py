from datetime import datetime


class SecurityAlert:
    # Атрибути класу - спільні для всіх об'єктів
    total_alerts_created = 0
    severity_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

    def __init__(self, ip, severity, alert_type):
        # Атрибути екземпляра - унікальні для кожного об'єкта
        self.ip = ip
        self.severity = severity
        self.alert_type = alert_type
        self.created_at = datetime.now()

        # Збільшуємо лічильник класу
        SecurityAlert.total_alerts_created += 1

    @classmethod
    def get_statistics(cls):
        """Метод класу - повертає статистику"""
        return {
            'total_alerts': cls.total_alerts_created,
            'available_severities': cls.severity_levels
        }

    @classmethod
    def create_from_log_line(cls, log_line):
        """Альтернативний конструктор - створює об'єкт з рядка логу"""
        # Приклад: "192.168.1.1 HIGH MALWARE_DETECTED"
        parts = log_line.strip().split()
        if len(parts) >= 3:
            ip, severity, alert_type = parts[0], parts[1], ' '.join(parts[2:])
            return cls(ip, severity, alert_type)
        else:
            raise ValueError("Invalid log line format")

    @staticmethod
    def is_private_ip(ip):
        """Статичний метод - перевірка приватної IP"""
        try:
            parts = list(map(int, ip.split('.')))
            return (parts[0] == 10 or
                    (parts[0] == 172 and 16 <= parts[1] <= 31) or
                    (parts[0] == 192 and parts[1] == 168))
        except:
            return False

    @staticmethod
    def calculate_risk_score(severity, is_internal=True):
        """Статичний метод - розрахунок ризику"""
        base_scores = {'LOW': 25, 'MEDIUM': 50, 'HIGH': 75, 'CRITICAL': 100}
        score = base_scores.get(severity, 0)
        # Зовнішні IP більш ризикові
        if not is_internal:
            score *= 1.5
        return min(100, score)

    def get_info(self):
        return f"Alert #{SecurityAlert.total_alerts_created}: {self.alert_type} from {self.ip}"

    def _validate_ip(self, ip):
        """Приватний метод для валідації IP"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

    def mark_as_processed(self):
        """Метод екземпляра - працює з конкретним об'єктом"""
        self.processed = True
        print(f"Alert for {self.ip} marked as processed")

    def get_age_minutes(self):
        """Розрахунок віку сповіщення в хвилинах"""
        return (datetime.now() - self.created_at).total_seconds() / 60


# Демонстрація
alert1 = SecurityAlert("192.168.1.100", "HIGH", "MALWARE")
alert2 = SecurityAlert("10.0.0.5", "LOW", "PORT_SCAN")

print(f"Total alerts created: {SecurityAlert.total_alerts_created}")  # 2
print(alert1.get_info())  # Alert #2: MALWARE from 192.168.1.100

# Тестування
try:
    alert = SecurityAlert("192.168.1.100", "HIGH", "MALWARE")
    alert.mark_as_processed()
    print(f"Alert age: {alert.get_age_minutes():.1f} minutes")

    # Це викличе помилку
    bad_alert = SecurityAlert("999.999.999.999", "HIGH", "MALWARE")
except ValueError as e:
    print(f"Error: {e}")


# Використання різних типів методів
print("Statistics:", SecurityAlert.get_statistics())

# Створення з логу
alert = SecurityAlert.create_from_log_line("10.0.0.5 HIGH MALWARE_DETECTED")
print(f"Created alert: {alert.ip}, {alert.severity}")

# Статичні методи
print(f"Is 192.168.1.1 private? {SecurityAlert.is_private_ip('192.168.1.1')}")
print(f"Risk score: {SecurityAlert.calculate_risk_score('HIGH', False)}")