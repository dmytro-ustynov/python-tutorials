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

    def get_info(self):
        return f"Alert #{SecurityAlert.total_alerts_created}: {self.alert_type} from {self.ip}"


# Демонстрація
alert1 = SecurityAlert("192.168.1.100", "HIGH", "MALWARE")
alert2 = SecurityAlert("10.0.0.5", "LOW", "PORT_SCAN")

print(f"Total alerts created: {SecurityAlert.total_alerts_created}")  # 2
print(alert1.get_info())  # Alert #2: MALWARE from 192.168.1.100