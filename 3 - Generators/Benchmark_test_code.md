# 🧪 **Експеримент: Порівняння продуктивності**
>Це частина уроку "Генератори в Python" https://docs.google.com/presentation/d/179_81fbS1I99ZnBUzpUee7M642_kP7lNrMtQDiMDhCs/edit?slide=id.g378e665e5a2_0_25#slide=id.g378e665e5a2_0_25

Давайте перевіримо різницю на практиці:

### **Тест 1: Використання пам'яті**

Встановіть бібліотеку `psutil`:

```bash
pip install psutil
```

```python
import psutil
import os

def memory_test_traditional():
    """Традиційний підхід"""
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Завантажуємо всі файли
    all_lines = []
    for i in range(10):
        with open(f'./log_investigation/access_log_{i}.log', 'r') as f:
            all_lines.extend(f.readlines())
    
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    return end_memory - start_memory

def memory_test_generator():
    """З генератором"""
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    def file_generator():
        for i in range(10):
            with open(f'./log_investigation/access_log_{i}.log', 'r') as f:
                for line in f:
                    yield line
    
    # Обробляємо по одному рядку
    count = 0
    for line in file_generator():
        count += 1
    
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    return end_memory - start_memory
```

**Очікувані результати:**
- Traditional: **+50-70MB пам'яті**
- Generator: **<5MB пам'яті**

### **Тест 2: Швидкість обробки**
```python
import time

def speed_test_traditional():
    start_time = time.time()
    
    # Спочатку завантажуємо все
    all_lines = []
    for i in range(10):
        with open(f'./log_investigation/access_log_{i}.log', 'r') as f:
            all_lines.extend(f.readlines())
    
    load_time = time.time() - start_time
    
    # Тепер обробляємо
    ip_count = 0
    for line in all_lines:
        if line.strip():
            ip_count += 1
    
    total_time = time.time() - start_time
    return load_time, total_time, ip_count

def speed_test_generator():
    start_time = time.time()
    
    def file_generator():
        for i in range(10):
            with open(f'./log_investigation/access_log_{i}.log', 'r') as f:
                for line in f:
                    yield line.strip()
    
    # Обробляємо відразу
    ip_count = 0
    first_result_time = None
    
    for line in file_generator():
        if line:
            ip_count += 1
            if first_result_time is None:
                first_result_time = time.time() - start_time
    
    total_time = time.time() - start_time
    return first_result_time, total_time, ip_count
```

**Очікувані результати:**
- Traditional: завантаження 2.5с, загалом 3.2с
- Generator: перший результат 0.001с, загалом 2.8с



# Приклади функцій які необхідно реалізувати:

 ## Отримання IP з рядка логу

```python
def get_ip_from_log_line(line):
    parts = line.split()
    if len(parts) > 0:
        return parts[0]
    return None
```


## Отримання дати з рядка логу

```python
import datetime

def get_datetime_from_log_line(line):
    # Знаючи формат рядка логу, можна знайти дату і час між квадратними дужками
    parts = line.split()
    if len(parts) > 8:
        date_str = parts[3][1:]
        try:
            date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')
            return date
        except ValueError:
            return None
    return None
```

## Отримання URL з рядка логу

```python
def get_url_from_log_line(line):
    # Знаючи формат рядка логу, можна знайти URL між лапками після методу запиту (GET, POST і т.д.)
    parts = line.split()
    if len(parts) > 8:
        return parts[6]
    return None
```

## Отримання статусу відповіді з рядка логу

```python
def get_status_from_log_line(line):
    parts = line.split()
    if len(parts) > 8:
        return parts[8]
    return None
```


## Визначення країни по IP
```python
IP_RANGES = {
    'ukraine': [
        '91.203.', '176.36.', '178.137.', '185.65.', '188.163.',
        '31.43.', '46.98.', '80.91.', '109.87.', '195.138.',
        '212.90.', '217.12.', '37.75.', '93.183.', '178.215.'
    ],
    'usa': [
        '104.23.', '172.71.', '209.126.', '107.175.', '173.252.',
        '8.8.', '1.1.', '208.67.', '64.233.', '162.159.',
        '199.232.', '184.72.', '54.230.', '23.21.', '52.84.'
    ],
    'germany': [
        '78.47.', '157.90.', '49.13.', '138.201.', '176.9.',
        '5.9.', '88.198.', '213.239.', '217.160.', '62.75.',
        '85.10.', '195.201.', '144.76.', '136.243.', '148.251.'
    ],
    'uk': [
        '81.2.', '86.49.', '90.155.', '212.58.', '217.169.',
        '194.74.', '31.170.', '188.39.', '95.216.', '178.79.',
        '213.205.', '185.233.', '46.101.', '167.99.', '134.122.'
    ],
    'canada': [
        '142.250.', '172.217.', '74.125.', '173.194.', '216.58.',
        '198.54.', '192.206.', '24.156.', '99.79.', '206.108.',
        '47.74.', '13.107.', '23.96.', '40.76.', '52.228.'
    ],
    'netherlands': [
        '62.210.', '51.15.', '163.172.', '212.83.', '195.154.',
        '87.98.', '141.101.', '185.3.', '46.232.', '213.32.',
        '217.21.', '82.196.', '145.220.', '188.166.', '159.203.'
    ],
    'russia': [
        '185.220.', '77.88.', '5.255.', '94.142.', '213.180.',
        '95.163.', '178.248.', '46.29.', '62.109.', '87.250.',
        '93.158.', '178.22.', '188.113.', '217.118.', '31.31.',
        '176.59.', '212.192.', '85.143.', '109.195.', '195.211.'
    ],
    'china': [
        '117.50.', '223.5.', '39.156.', '175.6.', '101.226.',
        '61.135.', '220.181.', '180.149.', '14.215.', '203.208.',
        '119.75.', '183.60.', '124.232.', '202.108.', '211.151.',
        '58.83.', '125.39.', '112.80.', '140.207.', '103.235.'
    ],
    'iran': [
        '2.177.', '5.253.', '31.7.', '37.98.', '78.157.',
        '85.15.', '87.107.', '91.98.', '151.232.', '185.55.',
        '194.146.', '212.16.', '217.218.', '46.224.', '79.175.',
        '82.99.', '95.38.', '176.65.', '188.34.', '213.233.'
    ],
    'north_korea': [
        '175.45.', '210.52.', '202.131.', '175.45.'
    ],
    'brazil': [
        '200.147.', '201.86.', '189.46.', '191.252.', '177.67.',
        '45.162.', '181.213.', '179.108.', '177.154.', '201.48.'
    ],
    'india': [
        '103.21.', '117.239.', '182.19.', '59.144.', '14.139.',
        '203.192.', '106.51.', '27.109.', '49.44.', '122.175.'
    ],
    'japan': [
        '133.130.', '210.173.', '61.115.', '219.117.', '118.238.',
        '202.32.', '153.149.', '160.16.', '163.49.', '203.104.'
    ]
}


def get_country_by_ip(address: str) -> str:
    # ітеруємо по словарю IP_RANGES
    for country, ip_ranges in IP_RANGES.items(): 
        for ip in ip_ranges:
            # перевіряємо що рядок IP починається з одного з префіксів
            if address.startswith(ip):
                return country
    return 'unknown'
```

##  Визначення підозрілих запитів

Підозрілі запити - це спроби дізнатися про вразливості, доступ до адмінок, використання відомих експлойтів.

Наприклад спроби зайти на адмінку WordPress, або спроба отримати файл конфігурації, або використання відомих інструментів як sqlmap.

Такі запити можна визначити за ключовими словами в URL або User-Agent.

```python
suspicious_paths = [
    '/wp-admin/', '/admin/', '/login/', '/setup-config.php', 
    '/phpmyadmin/', '/pma/', '/xmlrpc.php', '/.env', 
    '/config.php', '/.git/', '/.svn/', '/cgi-bin/', 
    'sqlmap', 'nmap', 'nikto', 'acunetix'
]
def is_suspicious_request(url, user_agent):
    url = url.lower()
    user_agent = user_agent.lower()
    
    for path in suspicious_paths:
        if path in url or path in user_agent:
            return True
    return False
```




---
(c) 2025, Устинов Дмитро