# Теоретичні матеріали: Веб-скрапінг

## Зміст

1. [Структура HTML](#структура-html)
2. [DOM (Document Object Model)](#dom-document-object-model)
3. [CSS Селектори](#css-селектори)
4. [BeautifulSoup API](#beautifulsoup-api)
5. [Етичні аспекти](#етичні-аспекти)
6. [Best Practices](#best-practices)
7. [FAQ](#faq)

---

## Структура HTML

### Основи HTML

HTML (HyperText Markup Language) - мова розмітки для створення веб-сторінок.

#### Базова структура документу

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Заголовок сторінки</title>
</head>
<body>
    <!-- Вміст сторінки -->
</body>
</html>
```

### Основні HTML елементи

#### Текстові елементи

```html
<h1>Заголовок 1 рівня</h1>
<h2>Заголовок 2 рівня</h2>
<p>Параграф тексту</p>
<span>Інлайн текст</span>
<strong>Жирний текст</strong>
<em>Курсив</em>
```

#### Структурні елементи

```html
<div>Блоковий елемент</div>
<header>Шапка сторінки</header>
<nav>Навігація</nav>
<main>Основний контент</main>
<section>Секція</section>
<article>Стаття</article>
<aside>Бічна панель</aside>
<footer>Підвал</footer>
```

#### Списки

```html
<!-- Нумерований список -->
<ol>
    <li>Перший пункт</li>
    <li>Другий пункт</li>
</ol>

<!-- Маркований список -->
<ul>
    <li>Пункт A</li>
    <li>Пункт B</li>
</ul>
```

#### Таблиці

```html
<table>
    <thead>
        <tr>
            <th>Заголовок 1</th>
            <th>Заголовок 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Дані 1</td>
            <td>Дані 2</td>
        </tr>
    </tbody>
</table>
```

#### Посилання та зображення

```html
<a href="https://example.com">Посилання</a>
<img src="image.jpg" alt="Опис зображення">
```

### HTML Атрибути

Атрибути надають додаткову інформацію про елементи:

```html
<!-- class - для стилізації та ідентифікації -->
<div class="container main-content">...</div>

<!-- id - унікальний ідентифікатор -->
<div id="header">...</div>

<!-- href - посилання -->
<a href="https://example.com">...</a>

<!-- src - джерело ресурсу -->
<img src="image.jpg">

<!-- title - підказка -->
<button title="Натисніть для збереження">Зберегти</button>

<!-- data-* - кастомні атрибути -->
<div data-user-id="123" data-role="admin">...</div>
```

---

## DOM (Document Object Model)

### Що таке DOM?

DOM - це програмний інтерфейс для HTML документів. Він представляє сторінку у вигляді дерева об'єктів.

### Приклад DOM дерева

**HTML:**
```html
<html>
    <head>
        <title>Приклад</title>
    </head>
    <body>
        <div class="container">
            <h1>Заголовок</h1>
            <p class="text">Параграф</p>
            <ul>
                <li>Пункт 1</li>
                <li>Пункт 2</li>
            </ul>
        </div>
    </body>
</html>
```

**DOM дерево:**
```
html
├── head
│   └── title
│       └── "Приклад"
└── body
    └── div (class="container")
        ├── h1
        │   └── "Заголовок"
        ├── p (class="text")
        │   └── "Параграф"
        └── ul
            ├── li
            │   └── "Пункт 1"
            └── li
                └── "Пункт 2"
```

### Термінологія DOM

- **Вузол (Node)** - кожен елемент в дереві
- **Батьківський вузол (Parent)** - вузол на рівень вище
- **Дочірній вузол (Child)** - вузол на рівень нижче
- **Сусідній вузол (Sibling)** - вузол на тому ж рівні
- **Нащадок (Descendant)** - будь-який вузол нижче (не обов'язково прямий)
- **Предок (Ancestor)** - будь-який вузол вище

### Навігація по DOM

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# Знайти елемент
div = soup.find('div', class_='container')

# Батьківський елемент
parent = div.parent  # <body>

# Дочірні елементи
children = list(div.children)  # [<h1>, <p>, <ul>]

# Наступний сусід
next_elem = div.h1.next_sibling

# Попередній сусід
prev_elem = div.p.previous_sibling

# Всі нащадки
descendants = list(div.descendants)
```

---

## CSS Селектори

CSS селектори - це патерни для вибору HTML елементів.

### Базові селектори

#### 1. Селектор за тегом

Вибирає всі елементи певного типу:

```css
p       /* Всі параграфи */
div     /* Всі div елементи */
h1      /* Всі заголовки h1 */
```

**Python:**
```python
soup.find_all('p')        # Всі <p>
soup.select('div')        # Всі <div>
```

#### 2. Селектор за класом

Вибирає елементи з певним класом:

```css
.container      /* class="container" */
.news-item      /* class="news-item" */
```

**Python:**
```python
soup.find_all(class_='container')
soup.select('.news-item')
```

#### 3. Селектор за ID

Вибирає елемент з унікальним ID:

```css
#header         /* id="header" */
#main-content   /* id="main-content" */
```

**Python:**
```python
soup.find(id='header')
soup.select('#main-content')
```

### Комбіновані селектори

#### 4. Тег + Клас

Вибирає елементи певного типу з певним класом:

```css
div.container       /* <div class="container"> */
p.intro             /* <p class="intro"> */
```

**Python:**
```python
soup.select('div.container')
soup.find('p', class_='intro')
```

#### 5. Множинні класи

Елемент з кількома класами:

```css
.class1.class2      /* class="class1 class2" */
```

**Python:**
```python
soup.select('.class1.class2')
```

### Ієрархічні селектори

#### 6. Нащадки (пробіл)

Вибирає всі нащадки (на будь-якому рівні):

```css
div p           /* Всі <p> всередині <div> */
ul li           /* Всі <li> всередині <ul> */
```

**Python:**
```python
soup.select('div p')
soup.select('ul li')
```

#### 7. Прямі нащадки (>)

Вибирає тільки безпосередні дочірні елементи:

```css
div > p         /* Тільки прямі <p> в <div> */
ul > li         /* Тільки прямі <li> в <ul> */
```

**Python:**
```python
soup.select('div > p')
soup.select('ul > li')
```

#### 8. Сусідні елементи (+)

Вибирає елемент, що йде одразу після:

```css
h1 + p          /* <p> одразу після <h1> */
```

**Python:**
```python
soup.select('h1 + p')
```

#### 9. Всі наступні сусіди (~)

Вибирає всі наступні елементи того ж рівня:

```css
h1 ~ p          /* Всі <p> після <h1> */
```

**Python:**
```python
soup.select('h1 ~ p')
```

### Селектори атрибутів

#### 10. Наявність атрибута

```css
[href]          /* Елементи з атрибутом href */
[data-id]       /* Елементи з data-id */
```

**Python:**
```python
soup.select('[href]')
soup.find_all(attrs={'data-id': True})
```

#### 11. Точне значення

```css
[type="text"]           /* type="text" */
[class="container"]     /* class="container" */
```

**Python:**
```python
soup.select('[type="text"]')
soup.find_all(attrs={'class': 'container'})
```

#### 12. Містить підрядок

```css
[href*="example"]       /* href містить "example" */
[class*="btn"]          /* class містить "btn" */
```

**Python:**
```python
soup.select('[href*="example"]')
```

#### 13. Починається з

```css
[href^="https"]         /* href починається з "https" */
[id^="item-"]           /* id починається з "item-" */
```

**Python:**
```python
soup.select('[href^="https"]')
```

#### 14. Закінчується на

```css
[href$=".pdf"]          /* href закінчується на ".pdf" */
[src$=".jpg"]           /* src закінчується на ".jpg" */
```

**Python:**
```python
soup.select('[href$=".pdf"]')
```

### Псевдокласи

```css
:first-child        /* Перший дочірній елемент */
:last-child         /* Останній дочірній елемент */
:nth-child(n)       /* N-ий дочірній елемент */
```

**Python:**
```python
soup.select('li:first-child')
soup.select('tr:nth-child(2)')
```

### Таблиця всіх селекторів

| Селектор | Синтаксис | Приклад | Опис |
|----------|-----------|---------|------|
| Універсальний | `*` | `*` | Всі елементи |
| Тег | `tag` | `div`, `p` | За типом елемента |
| Клас | `.class` | `.container` | За класом |
| ID | `#id` | `#header` | За ідентифікатором |
| Тег+Клас | `tag.class` | `div.box` | Комбінація |
| Нащадки | `A B` | `div p` | B всередині A |
| Діти | `A > B` | `div > p` | Прямі нащадки |
| Сусід | `A + B` | `h1 + p` | B одразу після A |
| Всі сусіди | `A ~ B` | `h1 ~ p` | Всі B після A |
| Атрибут | `[attr]` | `[href]` | З атрибутом |
| Атрибут=значення | `[attr=val]` | `[type=text]` | Точне значення |
| Атрибут містить | `[attr*=val]` | `[href*=example]` | Містить підрядок |
| Атрібут починається | `[attr^=val]` | `[href^=https]` | Починається з |
| Атрібут закінчується | `[attr$=val]` | `[src$=.jpg]` | Закінчується на |

---

## BeautifulSoup API

### Створення об'єкта

```python
from bs4 import BeautifulSoup

# З рядка
html = "<html><body><p>Text</p></body></html>"
soup = BeautifulSoup(html, 'html.parser')

# З файлу
with open('page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# З requests
import requests
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
```

### Парсери

| Парсер | Команда встановлення | Швидкість | Точність |
|--------|---------------------|-----------|-----------|
| `html.parser` | Вбудований | Середня | Висока |
| `lxml` | `pip install lxml` | Висока | Висока |
| `html5lib` | `pip install html5lib` | Низька | Найвища |
| `lxml-xml` | `pip install lxml` | Висока | Висока (XML) |

**Рекомендація:** Використовуйте `lxml` для продакшну.

### Методи пошуку

#### find()

Знаходить **перший** елемент:

```python
# За тегом
tag = soup.find('div')

# За класом
elem = soup.find('div', class_='container')

# За ID
elem = soup.find('div', id='main')

# За атрибутами
elem = soup.find('a', href='https://example.com')
elem = soup.find('div', attrs={'data-id': '123'})

# Комбінація
elem = soup.find('div', class_='box', id='first')
```

#### find_all()

Знаходить **всі** елементи:

```python
# Всі теги
tags = soup.find_all('p')              # Список всіх <p>

# За класом
elems = soup.find_all('div', class_='item')

# Кілька тегів
tags = soup.find_all(['h1', 'h2', 'h3'])

# Обмеження кількості
tags = soup.find_all('p', limit=5)    # Перші 5

# За функцією
def has_class(tag):
    return tag.has_attr('class')
tags = soup.find_all(has_class)
```

#### select() та select_one()

Використовують CSS селектори:

```python
# select_one() - перший елемент
elem = soup.select_one('div.container')
elem = soup.select_one('#header')

# select() - всі елементи
elems = soup.select('div.item')
elems = soup.select('.news-article h2')
elems = soup.select('ul > li')
```

### Навігація

```python
# Батьківський елемент
parent = elem.parent

# Всі батьки (аж до кореня)
parents = list(elem.parents)

# Дочірні елементи (генератор)
for child in elem.children:
    print(child)

# Всі нащадки (генератор)
for descendant in elem.descendants:
    print(descendant)

# Наступний сусід
next_elem = elem.next_sibling

# Попередній сусід
prev_elem = elem.previous_sibling

# Всі наступні сусіди
next_siblings = list(elem.next_siblings)

# Всі попередні сусіди
prev_siblings = list(elem.previous_siblings)

# Наступний елемент (не текстовий вузол)
next_elem = elem.find_next_sibling()

# Попередній елемент
prev_elem = elem.find_previous_sibling()
```

### Отримання даних

```python
# Текстовий вміст
text = elem.text                    # Весь текст
text = elem.get_text()              # Те саме
text = elem.get_text(strip=True)    # Без пробілів
text = elem.get_text(separator=' ') # З роздільником

# Один атрибут
href = elem.get('href')
href = elem['href']                 # Те саме

# Всі атрибути
attrs = elem.attrs                  # Dict всіх атрибутів

# Перевірка наявності
has_class = elem.has_attr('class')

# Ім'я тега
tag_name = elem.name               # 'div', 'p', etc.
```

### Модифікація

```python
# Змінити текст
elem.string = "Новий текст"

# Додати клас
elem['class'] = elem.get('class', []) + ['new-class']

# Видалити атрибут
del elem['id']

# Видалити елемент
elem.decompose()

# Замінити елемент
elem.replace_with(new_elem)
```

---

## Етичні аспекти

### Robots.txt

Файл `robots.txt` містить правила для веб-краулерів.

#### Перевірка robots.txt

```python
import requests

def check_robots_txt(base_url):
    """Перевірити robots.txt"""
    robots_url = base_url.rstrip('/') + '/robots.txt'
    
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            print(response.text)
            return response.text
    except:
        pass
    
    return None

# Використання
check_robots_txt('https://example.com')
```

#### Приклад robots.txt

```
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /public/

Crawl-delay: 10
```

### Правила етичного скрапінгу

#### ✅ Що ПОТРІБНО робити:

1. **Читати robots.txt**
   ```python
   # Поважати правила сайту
   if '/api/' in robots_disallowed:
       print("Скрапінг заборонено")
       return
   ```

2. **Додавати затримки**
   ```python
   import time
   
   for url in urls:
       scrape(url)
       time.sleep(1)  # 1 секунда між запитами
   ```

3. **Використовувати User-Agent**
   ```python
   headers = {
       'User-Agent': 'MyBot/1.0 (contact@example.com)'
   }
   requests.get(url, headers=headers)
   ```

4. **Обмежувати навантаження**
   ```python
   # Не більше N запитів на хвилину
   from time import time, sleep
   
   requests_per_minute = 10
   interval = 60 / requests_per_minute
   
   last_request = 0
   for url in urls:
       elapsed = time() - last_request
       if elapsed < interval:
           sleep(interval - elapsed)
       
       response = requests.get(url)
       last_request = time()
   ```

5. **Кешувати результати**
   ```python
   import json
   from pathlib import Path
   
   cache_file = Path('cache.json')
   
   if cache_file.exists():
       with open(cache_file) as f:
           data = json.load(f)
   else:
       data = scrape_website(url)
       with open(cache_file, 'w') as f:
           json.dump(data, f)
   ```

#### ❌ Що НЕ ПОТРІБНО робити:

- ❌ Ігнорувати robots.txt
- ❌ Робити тисячі запитів за секунду
- ❌ Підробляти User-Agent під браузер для обходу захисту
- ❌ Копіювати весь контент сайту
- ❌ Створювати конкуруючі сервіси на основі скрапленого контенту
- ❌ Порушувати Terms of Service

### Юридичні аспекти

- **Авторське право:** Не копіюйте контент без дозволу
- **Terms of Service:** Дотримуйтесь правил сайту
- **GDPR:** Не збирайте персональні дані без згоди
- **Комерційне використання:** Можуть бути обмеження

---

## Best Practices

### 1. Обробка помилок

```python
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

def scrape_safe(url):
    """Безпечний скрапінг з обробкою помилок"""
    try:
        # Запит з timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Парсинг
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Витягування даних з перевіркою
        title = soup.find('h1')
        if title:
            return title.text.strip()
        else:
            return None
            
    except Timeout:
        print(f"⏱️ Timeout для {url}")
    except HTTPError as e:
        print(f"❌ HTTP помилка {e.response.status_code}: {url}")
    except RequestException as e:
        print(f"❌ Помилка запиту: {e}")
    except Exception as e:
        print(f"❌ Помилка парсингу: {e}")
    
    return None
```

### 2. Використання сесій

```python
import requests

# Створити сесію для переvикористання з'єднань
session = requests.Session()
session.headers.update({
    'User-Agent': 'MyBot/1.0'
})

# Використовувати для всіх запитів
for url in urls:
    response = session.get(url)
    # ...
```

### 3. Функція з fallback

```python
def get_text(elem, default=''):
    """Отримати текст з fallback"""
    if elem:
        return elem.text.strip()
    return default

# Використання
title = get_text(soup.find('h1'), 'Без заголовка')
```

### 4. Логування

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def scrape_with_logging(url):
    logger.info(f"Початок скрапінгу: {url}")
    
    try:
        # Скрапінг...
        logger.info("Успішно завершено")
    except Exception as e:
        logger.error(f"Помилка: {e}")
```

### 5. Структурування даних

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Article:
    """Структура для статті"""
    title: str
    url: str
    author: Optional[str] = None
    date: Optional[str] = None
    content: Optional[str] = None

def parse_article(soup) -> Article:
    """Парсити статтю зі структурою"""
    return Article(
        title=get_text(soup.find('h1')),
        url=soup.find('link', rel='canonical')['href'],
        author=get_text(soup.find('span', class_='author')),
        date=get_text(soup.find('time')),
        content=get_text(soup.find('article'))
    )
```

---

## FAQ

### Q: Чому мій код не знаходить елемент?

**A:** Можливі причини:

1. **Невірний селектор**
   ```python
   # Перевірте структуру
   print(soup.prettify())
   ```

2. **JavaScript контент**
   ```python
   # BeautifulSoup не виконує JS
   # Використовуйте Selenium
   ```

3. **Елемент завантажується пізніше**
   ```python
   # Додайте затримку або використайте Selenium
   ```

### Q: Як обійти блокування?

**A:** Етичні методи:

1. Додайте правильний User-Agent
2. Поважайте robots.txt
3. Додайте затримки
4. Звернітся до власників за API

**Неетичні методи (не рекомендуються):**
- ❌ Proxies
- ❌ VPN
- ❌ Підробка headers

### Q: API чи скрапінг?

**A:** 

**Використовуйте API коли:**
- ✅ API доступний
- ✅ API безкоштовний або прийнятна ціна
- ✅ Потрібна висока надійність
- ✅ Потрібні структуровані дані

**Використовуйте скрапінг коли:**
- ✅ API недоступний
- ✅ API занадто дорогий
- ✅ Потрібні дані недоступні через API
- ✅ Це дозволено правилами сайту

### Q: Як парсити JavaScript сайти?

**A:** Використайте Selenium або Playwright:

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)

# Почекати завантаження
import time
time.sleep(3)

# Отримати HTML після JS
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

driver.quit()
```

### Q: Як зберігати дані?

**A:** Варіанти:

1. **JSON** - прості структури
   ```python
   import json
   with open('data.json', 'w') as f:
       json.dump(data, f, indent=2)
   ```

2. **CSV** - таблична data
   ```python
   import csv
   with open('data.csv', 'w') as f:
       writer = csv.writer(f)
       writer.writerows(data)
   ```

3. **База даних** - великі обсяги
   ```python
   import sqlite3
   conn = sqlite3.connect('data.db')
   cursor = conn.cursor()
   cursor.execute('INSERT INTO ...')
   ```

---

**Успіхів у вивченні веб-скрапінгу! 🚀**

*Останнє оновлення: Листопад 2025*
