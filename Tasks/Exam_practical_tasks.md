# **Практичні Завдання для Екзамену**

## **Курс "Крос-платформне програмування"**

**Час виконання:** кожне завдання розраховане на 30-40 хвилин **Інструкції:** Вам випаде одне з цих завдань. Напишіть код, який вирішує задачу, з належною обробкою помилок.

---

## **Завдання 1: Аналізатор лог-файлів**

Створіть програму для аналізу лог-файлу веб_сервера. Програма повинна:

* Читати текстовий файл з логами у форматі: \[2024-01-15 14:23:45\] ERROR: Database connection failed  
* Підраховувати кількість записів кожного типу (INFO, WARNING, ERROR, CRITICAL)  
* Знаходити всі записи за певну дату  
* Зберігати статистику у JSON файл

**Приклад вхідних даних (server.log):**

```
[2024-01-15 10:30:21] INFO: Server started
[2024-01-15 10:30:22] ERROR: Connection timeout
[2024-01-15 10:31:05] WARNING: High memory usage
[2024-01-15 10:32:11] INFO: Request processed
[2024-01-16 09:15:33] ERROR: File not found
```

**Очікуваний результат (log_statistics.json):**

```json
{
  "total_logs": 5,
  "by_level": {
    "INFO": 2,
    "WARNING": 1,
    "ERROR": 2,
    "CRITICAL": 0
  },
  "by_date": {
    "2024-01-15": 4,
    "2024-01-16": 1
  }
}
```  
---

## **Завдання 2: Система управління студентами (OOP)**

Створіть систему управління студентами з використанням ООП:

**Вимоги:**

* Клас Student з атрибутами: ім'я, прізвище, номер студентського, список оцінок  
* Властивість average_grade (обчислюється автоматично)  
* Метод add_grade(grade) з валідацією (оцінка від 0 до 100\)  
* Метод get_status() що повертає "Відмінник" (\>=90), "Хорошист" (\>=75), "Задовільно" (\>=60), "Незадовільно" (\<60)  
* Клас Group для управління списком студентів  
* Метод top_students(n) що повертає n найкращих студентів  
* Збереження та завантаження даних групи з JSON файлу

**Приклад використання:**

```python
student1 = Student("Іван", "Петренко", "CS-2024-001")
student1.add_grade(95)
student1.add_grade(88)
student1.add_grade(92)
print(student1.average_grade)  # 91.67
print(student1.get_status())    # "Відмінник"

group = Group("КБ-21")
group.add_student(student1)
group.save_to_file("group_kb21.json")
```  
---

## **Завдання 3: Аналізатор системи входу/виходу**

Створіть програму для аналізу логів системи контролю доступу (вхід/вихід співробітників):

**Вимоги:**

* Читати лог-файл з записами входу/виходу у форматі: timestamp,employee_id,action  
* Підраховувати загальний час присутності кожного співробітника за день  
* Виявляти аномалії: вхід без виходу, вихід без входу, робота понад 12 годин  
* Генерувати звіт з часом роботи кожного співробітника  
* Зберігати результати у CSV файл  
* Обробляти помилки: некоректні дані, дублікати, невалідний формат

**Приклад вхідного файлу (access_log.csv):**

```csv
timestamp,employee_id,action
2024-01-15 08:30:00,EMP001,ENTRY
2024-01-15 12:15:00,EMP001,EXIT
2024-01-15 13:00:00,EMP001,ENTRY
2024-01-15 17:30:00,EMP001,EXIT
2024-01-15 09:00:00,EMP002,ENTRY
2024-01-15 18:00:00,EMP002,EXIT
2024-01-15 08:45:00,EMP003,ENTRY
```

**Очікуваний результат (work_time_report.csv):**

```csv
employee_id,total_hours,entries,exits,anomalies
EMP001,8.25,2,2,none
EMP002,9.00,1,1,none
EMP003,0.00,1,0,missing_exit
```

**Консольний звіт:**

```
=== Work Time Report for 2024-01-15 ===
EMP001: 8h 15m (08:30-12:15, 13:00-17:30)
EMP002: 9h 00m (09:00-18:00)
EMP003: ANOMALY - Entry without exit

Total employees: 3
Anomalies detected: 1
```  
---

## **Завдання 4: CSV обробник даних про продажі**

Створіть програму для аналізу даних про продажі з CSV файлу:

**Вхідний файл (sales.csv):**

```csv
date,product,category,quantity,price
2024-01-10,Laptop,Electronics,2,25000
2024-01-10,Mouse,Electronics,5,350
2024-01-11,Keyboard,Electronics,3,890
2024-01-11,Chair,Furniture,4,2500
2024-01-12,Laptop,Electronics,1,25000
```

**Вимоги:**

* Прочитати CSV файл
* Підрахувати загальну виручку за кожен день
* Знайти найпопулярніший товар (за кількістю проданих одиниць)
* Підрахувати виручку по категоріях
* Експортувати результати у новий CSV файл sales_report.csv

**Очікуваний звіт:**

```csv
metric,value
total_revenue,89950
most_popular_product,Mouse
electronics_revenue,80950
furniture_revenue,10000
```  
---

## **Завдання 5: Клас для роботи з файловою системою**

Створіть клас FileManager з наступними можливостями:

**Вимоги:**

* Метод search_files(directory, pattern) _ пошук файлів за шаблоном (наприклад, \*.txt, \*.py)  
* Метод get_file_info(filepath) _ повертає словник з інформацією: розмір, дата створення, дата модифікації  
* Метод organize_by_extension(source_dir, target_dir) _ сортує файли по папкам за розширеннями  
* Метод find_duplicates(directory) _ знаходить файли-дублікати за вмістом (використовуючи MD5 хеш)  
* Обробка помилок (файл не існує, немає прав доступу)

**Приклад використання:**

```python
fm = FileManager()

# Пошук всіх Python файлів
files = fm.search_files("/path/to/project", "*.py")

# Інформація про файл
info = fm.get_file_info("script.py")
print(f"Розмір: {info['size']} байт")
print(f"Модифіковано: {info['modified']}")

# Організація файлів
fm.organize_by_extension("Downloads", "Organized")
# Створить: Organized/pdf/, Organized/jpg/, Organized/docx/ і т.д.

# Пошук дублікатів
duplicates = fm.find_duplicates("/path/to/check")
```  
---

## **Завдання 6: Збереження рецептів з API**

Створіть програму для завантаження рецептів з API [https://dummyjson.com/recipes/](https://dummyjson.com/recipes/):

**Вимоги:**

* Використовувати бібліотеку requests для роботи з API  
* За вибором користувача _ Отримати випадковий рецепт або рецепт за ID.  
* Зберегти рецепт у текстовий файл з форматованим текстом  
* Завантажити та зберегти зображення рецепту (якщо є)  
* Нормалізувати текст: очистити від зайвих пробілів, форматувати інгредієнти списком  
* Створити структуру директорій: recipes/recipe_name/  
* Обробка помилок: мережеві помилки, відсутність зображення

**Приклад структури файлів:**

```
recipes/
  └── Classic Margherita Pizza/
      ├── recipe.txt
      └── image.jpg
```

**Приклад використання:**

```python
# Завантаження конкретного рецепту  
recipe_saver = RecipeSaver()  
recipe_saver.save_recipe(recipe_id=1, output_dir="recipes")

# Завантаження випадкового рецепту  
recipe_saver.save_random_recipe(output_dir="recipes")

# Завантаження декількох рецептів  
recipe_saver.save_multiple_recipes(count=5, output_dir="recipes")
```  
---

## **Завдання 7: Система шифрування файлів**

Створіть програму для шифрування та дешифрування файлів:

**Вимоги:**

* Використовувати бібліотеку cryptography (Fernet для симетричного шифрування)  
* Функція generate_key() _ генерує та зберігає ключ у файл  
* Функція encrypt_file(input_file, output_file, key_file) _ шифрує файл  
* Функція decrypt_file(input_file, output_file, key_file) _ дешифрує файл  
* Обробка помилок (неправильний ключ, файл не існує)  
* Можливість шифрування/дешифрування текстових та бінарних файлів

**Приклад використання:**

```python
# Генерація ключа  
generate_key("secret.key")

# Шифрування  
encrypt_file("document.txt", "document.encrypted", "secret.key")

# Дешифрування  
decrypt_file("document.encrypted", "document_decrypted.txt", "secret.key")
```  
---

## **Завдання 8: Монітор системних ресурсів**

Створіть програму для моніторингу системних ресурсів:

**Вимоги:**

* Використовувати бібліотеку psutil  
* Збирати інформацію: CPU usage, Memory usage, Disk usage, Network activity  
* Зберігати історію моніторингу у CSV файл з timestamp  
* Функція get_current_stats() _ повертає поточний стан  
* Функція monitor(duration, interval) _ збирає дані протягом певного часу з інтервалом  
* Функція generate_report() _ створює текстовий звіт з середніми значеннями

**Приклад виведення:**

```
=== System Monitor Report ===  
Time: 2024-01-15 14:30:00  
CPU Usage: 45.2%  
Memory Usage: 62.8% (5.2 GB / 8 GB)  
Disk Usage: 78.4% (235 GB / 300 GB)  
Network Sent: 1.5 MB  
Network Received: 3.2 MB
```

**CSV файл (monitor_log.csv):**

```csv
timestamp,cpu_percent,memory_percent,disk_percent,net_sent_mb,net_recv_mb
2024-01-15 14:30:00,45.2,62.8,78.4,1.5,3.2
2024-01-15 14:30:05,43.1,62.9,78.4,1.6,3.3
```  
---

## **Завдання 9: Генератор Rainbow Table для паролів**

Створіть програму для генерації rainbow table з паролів:

**Вимоги:**

* Читати список паролів з текстового файлу (один пароль на рядок)  
* Генерувати хеші для кожного паролю, використовуючи 5 найпопулярніших алгоритмів:  
  * MD5  
  * SHA1  
  * SHA256  
  * SHA512  
  * bcrypt (опціонально, якщо є час)  
* Зберігати результати у CSV файл з колонками: password,md5,sha1,sha256,sha512  
* Обробка помилок: порожній файл, некоректні дані  
* Підрахунок статистики: скільки паролів оброблено, час генерації  
* Додати можливість пошуку оригінального паролю за хешем

**Приклад вхідного файлу (passwords.txt):**

```
password123
admin
qwerty
letmein
welcome
123456
password
```

**Очікуваний результат (rainbow_table.csv):**

```csv
password,md5,sha1,sha256,sha512
password123,482c811da5d5b4bc6d497ffa98491e38,c83db8d2bed82e02ca1bfc1c524e6a9cb4b02df3,...,...
admin,21232f297a57a5a743894a0e4a801fc3,d033e22ae348aeb5660fc2140aec35850c4da997,...,...
qwerty,d8578edf8458ce06fbc5bb76a58c5ca4,b1b3773a05c0ed0176787a4f1574ff0075f7521e,...,...
```

**Приклад виведення під час генерації:**

```
=== Rainbow Table Generator ===
Loading passwords from passwords.txt...
Loaded: 7 passwords

Results:
  Total passwords: 7
  MD5 hashes generated: 7
  SHA1 hashes generated: 7
  SHA256 hashes generated: 7
  SHA512 hashes generated: 7
  Time elapsed: 0.03 seconds
  Output saved to: rainbow_table.csv

Rainbow table created successfully!
```  
---

## **Завдання 10: Парсер конфігураційних файлів**

Створіть програму для роботи з конфігураційними файлами різних форматів:

**Вимоги:**

* Читання конфігурації з JSON, CSV, та звичайного текстового формату KEY=VALUE  
* Конвертація між форматами  
* Валідація обов'язкових полів  
* Merge (об'єднання) конфігурацій з різних джерел  
* Підтримка вкладених структур у JSON

**Приклад:**

**config.txt:**

```
HOST=localhost
PORT=8080
DEBUG=true
MAX_CONNECTIONS=100
```

**config.json:**

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "mydb"
  },
  "cache": {
    "enabled": true,
    "ttl": 3600
  }
}
```

**Вимоги до функціоналу:**

```python
config = ConfigParser()
config.load_from_file("config.txt")
config.load_from_file("config.json")
config.validate_required(["HOST", "PORT", "database.host"])
config.save_to_file("merged_config.json", format="json")
```  
---

## **Завдання 11: Автоматичне створення резервних копій**

Створіть програму для автоматичного створення резервних копій файлів:

**Вимоги:**

* Функція backup_directory(source, destination) _ створює архів ZIP з усіма файлами  
* Додавання timestamp до імені архіву (backup_2024-01-15_14-30-00.zip)  
* Ротація бекапів _ зберігати тільки останні N бекапів, старі видаляти  
* Функція restore_backup(archive, destination) _ відновлення з архіву  
* Створення звіту про бекап (які файли включені, розмір, час створення)  
* Можливість виключення файлів за патерном (наприклад, \*.tmp, __pycache__)

**Приклад використання:**

```python
# Створення бекапу
backup_info = backup_directory(  
    source="./my_project",  
    destination="./backups",  
    exclude_patterns=["*.pyc", "__pycache__", ".git"],  
    keep_last=5  
)

print(f"Backup created: {backup_info['filename']}")  
print(f"Files backed up: {backup_info['file_count']}")  
print(f"Total size: {backup_info['size_mb']:.2f} MB")

# Відновлення  
restore_backup("backups/backup_2024-01-15_14-30-00.zip", "./restored") 
```
---

## **Завдання 12: Валідатор послідовності дужок**

Створіть програму для перевірки правильності послідовності дужок у виразі:

**Вимоги:**

* Функція is_valid(expression) - перевіряє чи правильна послідовність дужок  
* Підтримка різних типів дужок: (), [], {}  
* Перевірка що кожна відкриваюча дужка має відповідну закриваючу  
* Перевірка правильного порядку (вкладеності)  
* Функція повертає True якщо послідовність валідна, False - якщо ні  
* Опционально: Додаткова функція find_error_position(expression) - знаходить позицію помилки  
* Опционально: Функція get_details(expression) - повертає детальний звіт про дужки

**Приклад використання:**

```python
validator = ParenthesesValidator()

# Прості випадки  
assert validator.is_valid("()")  == True  
assert validator.is_valid("()\[\]{}")  == True  
assert validator.is_valid("(\]")  == False  
assert validator.is_valid("(\[)\]")  == False  
assert validator.is_valid("{\[\]}")  == True

# Складніші випадки  
assert validator.is_valid("((()))")  == True  
assert validator.is_valid("((())")  == False  
assert validator.is_valid("())(")  == False  
assert validator.is_valid("")  == True  # порожній рядо- валідний

# З кодом  
assert validator.is_valid("if (x \> 0\) { print(\[1, 2, 3\]); }") == True  
assert validator.is_valid("def foo(): return \[1, 2, 3") == False
```

---

## **Завдання 13: Аналізатор коду Python**

Створіть програму для аналізу файлів Python коду:

**Вимоги:**

* Підрахунок рядків коду (загальна кількість, порожні рядки, коментарі, код)  
* Пошук всіх функцій та класів у файлі (використовуючи регулярні вирази або AST модуль)  
* Підрахунок складності (кількість if, for, while)  
* Пошук потенційних проблем (занадто довгі рядки \>80 символів, функції \>50 рядків)  
* Генерація звіту у текстовому або JSON форматі

**Приклад виведення:**

```
=== Code Analysis Report ===  
File: my_script.py  
Total Lines: 150  
  Code Lines: 95  
  Comment Lines: 30  
  Blank Lines: 25

Functions Found: 8  
  - calculate_total (10 lines)  
  - process_data (45 lines) [WARNING: Too long]  
  - validate_input (5 lines)  
  ...

Classes Found: 2  
  - User (25 lines)  
  - Database (60 lines)

Complexity Metrics:  
  If statements: 15  
  Loops: 8  
  Try-except blocks: 3

Warnings:  
  - Line 45: Line too long (95 characters)  
  - Line 78: Function 'process_data' is too long (45 lines)
```

---

## **Завдання 14: Генератор паролів з перевіркою надійності**

Створіть програму для генерації та перевірки надійності паролів:

**Вимоги:**

* Функція generate_password(length, include_special=True, include_numbers=True) - генерує випадковий пароль  
* Функція check_password_strength(password) - перевіряє надійність (Weak, Medium, Strong, Very Strong)  
* Критерії надійності:  
  * Довжина >= 8 символів  
  * Містить великі та малі літери  
  * Містить цифри  
  * Містить спеціальні символи  
  * Не містить послідовних символів (123, abc)  
  * Не містить повторюваних символів (aaa, 111)  
* Функція save_password(service, username, password, filename) - зберігає паролі у зашифрованому файлі  
* Функція get_password(service, filename) - отримує пароль для сервісу

**Приклад використання:**

```python
# Генерація
password = generate_password(length=16, include_special=True)  
print(f"Generated: {password}")

# Перевірка надійності  
strength = check_password_strength(password)  
print(f"Strength: {strength}")  # Very Strong

# Збереження паролів (використовуючи шифрування)  
save_password("gmail", "user@gmail.com", password, "passwords.enc")  
retrieved = get_password("gmail", "passwords.enc")
```
---

## **Завдання 15: Парсер HTML таблиць**

Створіть програму для парсингу даних з HTML файлу, що містить таблиці:

**Вимоги:**

* Використовувати BeautifulSoup для парсингу HTML  
* Знайти всі таблиці у файлі та ідентифікувати їх за заголовками  
* Витягнути дані з таблиць у структуровані словники/списки  
* Експортувати дані з кожної таблиці у окремий CSV файл  
* Обробка помилок: невалідний HTML, відсутні таблиці, порожні комірки  
* Генерація звіту про знайдені таблиці

**Приклад вхідного HTML файлу (data.html):**

```html
<!DOCTYPE html>  
<html>  
<head><title>Company Data</title></head>  
<body>  
    <h2>Employees</h2>  
    <table border="1">  
        <tr>  
            <th>ID</th>  
            <th>Name</th>  
            <th>Department</th>  
            <th>Salary</th>  
        </tr>  
        <tr>  
            <td>001</td>  
            <td>John Doe</td>  
            <td>IT</td>  
            <td>50000</td>  
        </tr>  
        <tr>  
            <td>002</td>  
            <td>Jane Smith</td>  
            <td>HR</td>  
            <td>45000</td>  
        </tr>  
    </table>

    <h2>Projects</h2>  
    <table border="1">  
        <tr>  
            <th>Project ID</th>  
            <th>Name</th>  
            <th>Budget</th>  
            <th>Status</th>  
        </tr>  
        <tr>  
            <td>P001</td>  
            <td>Website Redesign</td>  
            <td>100000</td>  
            <td>Active</td>  
        </tr>  
    </table>  
</body>  
</html>
```

**Очікувані результати:**

**employees.csv:**

```csv
ID,Name,Department,Salary  
001,John Doe,IT,50000  
002,Jane Smith,HR,45000
```

**projects.csv:**

```csv
Project ID,Name,Budget,Status  
P001,Website Redesign,100000,Active
```

**Приклад використання:**

```python
parser = HTMLTableParser("data.html")

# Знайти всі таблиці  
tables = parser.find_all_tables()  
print(f"Found {len(tables)} tables")

# Витягнути дані  
for i, table_data in enumerate(parser.extract_tables()):  
    print(f"Table {i+1}: {table_data['title']}")  
    print(f"  Rows: {table_data['row_count']}")  
    print(f"  Columns: {table_data['columns']}")

# Експортувати у CSV  
parser.export_to_csv(output_dir="extracted_tables")

# Звіт  
parser.generate_report("parsing_report.txt")
```

**Консольний звіт:**

```
=== HTML Table Parser Report ===  
File: data.html  
Tables found: 2

Table 1: Employees  
  Location: Line 8  
  Columns: ['ID', 'Name', 'Department', 'Salary']  
  Rows: 2  
  Exported to: employees.csv

Table 2: Projects  
  Location: Line 25  
  Columns: ['Project ID', 'Name', 'Budget', 'Status']  
  Rows: 1  
  Exported to: projects.csv

Total rows extracted: 3  
Processing time: 0.05 seconds
```  
---

## **Завдання 16: Система логування з ротацією**

Створіть власну систему логування з ротацією файлів:

**Вимоги:**

* Клас Logger з методами: info(), warning(), error(), critical()  
* Логи записуються у файл з timestamp  
* Різні рівні логування (можна вмикати/вимикати)  
* Ротація файлів: коли файл досягає певного розміру, створюється новий файл  
* Збереження останніх N лог-файлів  
* Форматування: `[2024-01-15 14:30:00] [ERROR] [module.py:45] Error message ` 
* Можливість логування у файл та консоль одночасно

**Приклад використання:**

```python
logger = Logger(  
    filename="app.log",  
    max_size_mb=5,  
    backup_count=3,  
    level="INFO",  
    log_to_console=True  
)

logger.info("Application started")  
logger.warning("High memory usage detected")  
logger.error("Database connection failed", extra={"db": "postgres"})  
logger.critical("System shutdown initiated")
```

# Файли: app.log, app.log.1, app.log.2, app.log.3  
---

## **Завдання 17: Пошук дублікатів файлів**

Створіть програму для пошуку дублікатів файлів у директорії:

**Вимоги:**

* Функція find_duplicates(directory, recursive=True) - шукає дублікати  
* Порівняння файлів за хешем MD5 або SHA256  
* Групування дублікатів разом  
* Підрахунок потенційно вивільненого місця  
* Опція автоматичного видалення дублікатів (залишати найновіший файл)  
* Створення звіту з дублікатами

**Приклад виведення:**

```
=== Duplicate Files Report ===  
Scan Directory: /home/user/Documents  
Total Files Scanned: 1,523  
Total Duplicates Found: 45 files in 18 groups  
Potential Space to Free: 234.5 MB

Duplicate Group 1:  
  - /home/user/Documents/photo1.jpg (2.5 MB, 2024-01-10)  
  - /home/user/Documents/backup/photo1.jpg (2.5 MB, 2024-01-09)  
  - /home/user/Downloads/photo1.jpg (2.5 MB, 2024-01-08)  
  Hash: a3f5b21c9d8e7f6a...

Duplicate Group 2:  
  - /home/user/Documents/report.pdf (1.2 MB, 2024-01-15)  
  - /home/user/Documents/old/report.pdf (1.2 MB, 2024-01-10)  
  Hash: 7e9f8d6c5b4a3e2d...

Actions:  
  [1] Delete all duplicates (keep newest)  
  [2] Delete all duplicates (keep oldest)  
  [3] Manual selection  
  [4] Generate report only  
```

---

## **Завдання 18: Аналізатор логів веб-сервера**

Створіть програму для аналізу логів веб-сервера (Apache/Nginx формат):

**Вимоги:**

* Парсити лог-файл у стандартному форматі Apache Combined Log  
* Витягувати: IP адресу, дату/час, метод HTTP, URL, статус-код, розмір відповіді, user agent  
* Статистика за IP адресами (топ відвідувачів)  
* Статистика за URL (найбільш відвідувані сторінки)  
* Статистика за статус-кодами (200, 404, 500 тощо)  
* Виявлення підозрілої активності (багато 404, спроби SQL ін'єкцій у URL)  
* Експорт результатів у JSON та CSV

**Приклад вхідного файлу (access.log):**
```
192.168.1.10 - - [15/Jan/2024:10:30:45 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"  
192.168.1.11 - - [15/Jan/2024:10:31:12 +0000] "GET /about.html HTTP/1.1" 200 5678 "-" "Mozilla/5.0"  
192.168.1.10 - - [15/Jan/2024:10:32:03 +0000] "GET /admin.php HTTP/1.1" 404 162 "-" "Python-requests/2.28"  
192.168.1.12 - - [15/Jan/2024:10:33:15 +0000] "POST /login HTTP/1.1" 200 890 "-" "Mozilla/5.0"  
192.168.1.10 - - [15/Jan/2024:10:34:22 +0000] "GET /index.php?id=1' OR '1'='1 HTTP/1.1" 403 0 "-" "curl/7.68"  
10.0.0.5 - - [15/Jan/2024:10:35:01 +0000] "GET /api/users HTTP/1.1" 500 234 "-" "PostmanRuntime/7.26"
```

**Очікувані результати:**

**Статистика (statistics.json):**

```json
{  
  "total_requests": 6,  
  "unique_ips": 3,  
  "date_range": {  
    "start": "2024-01-15 10:30:45",  
    "end": "2024-01-15 10:35:01"  
  },  
  "status_codes": {  
    "200": 3, ...  },  
  "top_ips": [ ... ],  
  "top_urls": [ ... ],

}
```

**Приклад використання:**

```python
analyzer = WebLogAnalyzer("access.log")

# Парсинг логів  
analyzer.parse_logs()

# Статистика  
stats = analyzer.get_statistics()  
print(f"Total requests: {stats['total_requests']}")  
print(f"Unique visitors: {stats['unique_ips']}")

# Топ IP  
top_ips = analyzer.get_top_ips(limit=5)  
for ip_data in top_ips:  
    print(f"{ip_data['ip']}: {ip_data['requests']} requests")

# Підозріла активність  
suspicious = analyzer.detect_suspicious_activity()  
print(f"Suspicious activities detected: {len(suspicious)}")

# Експорт  
analyzer.export_to_json("statistics.json")  
analyzer.export_to_csv("requests.csv")
```
---

## **Завдання 19: Менеджер завдань (To-Do List)**

Створіть консольний менеджер завдань (To-Do List) з збереженням у файл:

**Вимоги:**

* Додавання завдання з назвою, описом, пріоритетом (Low, Medium, High), дедлайном  
* Відображення всіх завдань  
* Фільтрація за пріоритетом або статусом (Pending, In Progress, Completed)  
* Відмітка завдання як виконаного  
* Видалення завдання  
* Пошук завдань за ключовим словом  
* Сортування за пріоритетом або дедлайном  
* Збереження у JSON файл  
* Повідомлення про прострочені завдання

**Приклад інтерфейсу:**

```
=== To-Do List Manager ===  
1. Add task  
2. View all tasks  
3. View by priority  
4. Mark as completed  
5. Delete task  
6. Search tasks  
7. Save and exit

Choice: 1  
Title: Finish Python exam  
Description: Complete all 25 tasks  
Priority (Low/Medium/High): High  
Deadline (YYYY-MM-DD): 2024-01-20  
Task added successfully\!

Choice: 2  
=== All Tasks ===  
[1] [PENDING] [HIGH] Finish Python exam (Due: 2024-01-20)  
    Complete all 25 tasks  
[2] [IN PROGRESS] [MEDIUM] Read chapter 5 (Due: 2024-01-18)  
    OOP concepts  
[3] [COMPLETED] [LOW] Buy groceries (Completed: 2024-01-15)

OVERDUE TASKS: 0
```  
---

## **Завдання 20: Обробка великих файлів по частинах**

Створіть програму для ефективної обробки великих файлів:

**Вимоги:**

* Функція process_large_file(filename, chunk_size=1024\*1024) _ читає файл частинами  
* Функція count_words(filename) _ підраховує слова у великому файлі без завантаження всього в пам'ять  
* Функція find_in_file(filename, search_term) _ шукає рядок у файлі, повертає номери рядків  
* Функція split_file(filename, parts) _ розділяє файл на N частин  
* Функція merge_files(file_list, output) _ об'єднує декілька файлів в один  
* Прогрес-бар для відображення процесу обробки

**Приклад використання:**

```python
# Підрахунок слів у великому файлі (1GB)  
word_count = count_words("large_file.txt")  
print(f"Total words: {word_count:,}")

# Пошук у файлі  
lines = find_in_file("large_file.txt", "error")  
print(f"Found 'error' on lines: {lines}")

# Розділення файлу  
split_file("large_file.txt", parts=4)  
# Створює: large_file_part1.txt, large_file_part2.txt, ...

# Об'єднання файлів  
merge_files(["part1.txt", "part2.txt", "part3.txt"], "merged.txt")

# З прогрес-баром  
Processing: [████████████████████] 100% (1024 MB / 1024 MB)
```
---

## **Завдання 21: Система управління інвентарем (OOP + Files)**

Створіть систему управління інвентарем для магазину:

**Вимоги:**

* Клас Product з атрибутами: назва, категорія, ціна, кількість, артикул  
* Клас Inventory для управління продуктами  
* Методи:  
  * add_product(product) - додати товар  
  * remove_product(article) - видалити товар за артикулом  
  * update_quantity(article, quantity) - оновити кількість  
  * update_price(article, new_price) - оновити ціну  
  * search_by_name(name) - пошук за назвою  
  * search_by_category(category) - пошук за категорією  
  * get_low_stock(threshold=10) - товари з кількістю нижче порогу  
  * get_total_value() - загальна вартість інвентаря  
  * generate_report() - звіт про інвентар  
* Збереження та завантаження з JSON або CSV  
* Експорт звіту у текстовий файл

**Приклад використання:**

```python
inventory = Inventory()

# Додавання товарів  
inventory.add_product(Product("Laptop", "Electronics", 25000, 15, "ELEC-001"))  
inventory.add_product(Product("Mouse", "Electronics", 350, 50, "ELEC-002"))  
inventory.add_product(Product("Desk", "Furniture", 5000, 8, "FURN-001"))

# Пошук  
electronics \= inventory.search_by_category("Electronics")

# Товари з низьким запасом  
low_stock \= inventory.get_low_stock(threshold=10)  
for product in low_stock:  
    print(f"Low stock: {product.name} _ {product.quantity} units")

# Загальна вартість  
total \= inventory.get_total_value()  
print(f"Total inventory value: {total:,} UAH")

# Збереження  
inventory.save_to_file("inventory.json")

# Звіт  
inventory.generate_report("inventory_report.txt")  
```
---

**Рекомендації для студентів:**

* Використовуйте обробку винятків у всіх завданнях  
* Пишіть зрозумілий код з коментарями  
* Тестуйте програми з різними вхідними даними  
* Звертайте увагу на крайні випадки – edge cases  (порожні файли, невалідні дані тощо)

Успіхів на екзамені\! 🎓