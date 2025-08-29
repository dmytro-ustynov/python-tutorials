# Лекція 2.3: Файлові операції в Python

---

## 1. Вступ

Усі дані, які ми зберігаємо у колекціях (списки, словники, множини), існують лише **поки програма виконується**.
Якщо ми закриємо Python, дані зникнуть.
Файли дозволяють зберігати результати назавжди.

**Приклад з життя:**

* Текстові файли — зберігання логів роботи програми.
* CSV/Excel — статистика продажів.
* JSON — конфігураційні файли.
* Бінарні файли — фото, відео, бази даних.

---

## 2. Основи файлової системи

### Абсолютний та відносний шлях

```python
# Абсолютний шлях
f = open("C:/Users/User/Desktop/data.txt", "r")

# Відносний шлях (файл у тій же папці, що і скрипт)
f = open("data.txt", "r")
```

### Текстові та бінарні файли

* `"r"` → читає як текст (з урахуванням кодування UTF-8).
* `"rb"` → читає як «сирі байти».

**Міні-завдання:**
Студенти створюють у папці з програмою файл `hello.txt` і перевіряють, чи відкриється він через відносний та абсолютний шлях.

---

## 3. Відкриття та закриття файлів

```python
# Варіант 1 — обов’язково закрити файл
f = open("hello.txt", "r")
print(f.read())
f.close()

# Варіант 2 — з контекстним менеджером (краще)
with open("hello.txt", "r") as f:
    print(f.read())
# файл закриється автоматично
```

**Міні-завдання:**
Відкрити файл і прочитати його двома способами. Переконатися, що після `with open` файл закритий.

---

## 4. Читання з файлів

```python
with open("hello.txt", "r", encoding="utf-8") as f:
    content = f.read()          # читає все одразу
    print(content)

with open("hello.txt", "r", encoding="utf-8") as f:
    first_line = f.readline()   # читає один рядок
    print(first_line)

with open("hello.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()       # список рядків
    print(lines)

with open("hello.txt", "r", encoding="utf-8") as f:
    for line in f:              # ітерація по рядках
        print(line.strip())
```

**Міні-завдання:**
Прочитати файл з віршем/текстом і порахувати кількість рядків.

---

## 5. Запис у файли

```python
# перезапис файлу
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, world!\n")

# додавання в кінець файлу
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Another line\n")
```

**Міні-завдання:**
Записати у файл результати таблиці множення від 1 до 10.

---

## 6. Робота з JSON та CSV

### JSON

```python
import json

data = {"name": "Ivan", "age": 20, "skills": ["Python", "SQL"]}

# збереження у файл
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# зчитування з файлу
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
```

### CSV

```python
import csv

rows = [
    ["Name", "Age"],
    ["Ivan", 20],
    ["Oksana", 22],
]

with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

with open("people.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

**Міні-завдання:**
Створити словник з 3–4 студентами і зберегти його у форматі JSON. Потім прочитати і вивести у консоль.

---

## 7. Робота з бінарними файлами

```python
# копіювання зображення
with open("cat.jpg", "rb") as f_in:
    data = f_in.read()

with open("cat_copy.jpg", "wb") as f_out:
    f_out.write(data)
```

**Міні-завдання:**
Скопіювати будь-який `.jpg` файл у новий.

---

### 🔹7.2 Серіалізація та десеріалізація

#### Що це таке

* **Серіалізація** — процес перетворення об’єкта Python у послідовність байтів (щоб зберегти у файл або передати по мережі).
* **Десеріалізація** — відновлення Python-об’єкта з байтів.

У Python для цього є кілька варіантів:

* `json` — для обміну з іншими мовами (тільки прості типи).
* `pickle` — для збереження **будь-яких Python-об’єктів** (списки, словники, навіть власні класи).

---

#### Приклад з `pickle`

```python
import pickle

# об'єкт для збереження
student = {
    "name": "Ivan",
    "age": 21,
    "grades": [90, 85, 100]
}

# серіалізація (запис у файл)
with open("student.pkl", "wb") as f:
    pickle.dump(student, f)

# десеріалізація (читання з файлу)
with open("student.pkl", "rb") as f:
    loaded_student = pickle.load(f)

print(loaded_student)
```

---

#### Серіалізація списку об’єктів

```python
class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades

    def __repr__(self):
        return f"Student({self.name}, {self.age}, {self.grades})"

students = [
    Student("Ivan", 20, [90, 100]),
    Student("Oksana", 22, [95, 87])
]

# збереження списку об'єктів
with open("students.pkl", "wb") as f:
    pickle.dump(students, f)

# відновлення
with open("students.pkl", "rb") as f:
    loaded_students = pickle.load(f)

print(loaded_students)
```

---

#### Зауваження 🚨

* `pickle` зберігає дані **тільки для Python** (не сумісно з іншими мовами).
* Pickle-файли **небезпечні** — не можна завантажувати їх із ненадійних джерел, бо під час `load()` може виконатися шкідливий код.

---

### Міні-завдання для студентів

1. Створити список словників зі студентами (ім’я, вік, середній бал).
2. Зберегти його у файл `students.pkl`.
3. Завантажити з файлу і вивести дані.
4. Змінити дані одного студента і знову зберегти.

---


## 8. Обробка помилок

```python
try:
    with open("nofile.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("Файл не знайдено!")
```

**Міні-завдання:**
Зробити програму, яка читає файл `input.txt`. Якщо файлу немає — створити його і записати в нього текст `"Файл був створений"`.

---

## 9. Міні-практикум (20 хв)

**Задача для студентів:**

1. Є файл `text.txt` з довільним текстом.
2. Порахувати частоту кожного слова.
3. Результат записати у `result.txt` у вигляді:

   ```
   слово1: кількість
   слово2: кількість
   ```
4. Той самий словник зберегти у форматі JSON (`result.json`).

---

## 10. Підсумки

* **Колекції** → зберігають дані в оперативній пам’яті.
* **Файли** → дозволяють зберігати дані назавжди.
* Основні операції: **читання, запис, додавання, робота з форматами (JSON, CSV, бінарні дані)**.
* Використання `with open` → безпечніше і правильніше.
* Обробка помилок важлива у реальних проєктах.

