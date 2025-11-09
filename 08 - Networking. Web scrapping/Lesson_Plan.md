# Практичне заняття 4-4: Основи веб-скрапінгу

## 📋 Інформація про заняття

**Тема:** Основи веб-скрапінгу  
**Підтеми:**
1. Структура HTML документів. CSS селектори
2. Бібліотека BeautifulSoup для парсингу HTML

**Тривалість:** 2 години (120 хвилин)  
**Тип заняття:** Практичне  
**Попередні знання:** 
- Робота з API через requests
- Обробка JSON/XML даних
- Основи ООП в Python

---

## 🎯 Цілі заняття

### Навчальні цілі:
1. Розуміти структуру HTML документів та DOM
2. Володіти CSS селекторами для пошуку елементів
3. Використовувати BeautifulSoup для парсингу HTML
4. Інтегрувати веб-скрапінг з попередніми проектами

### Практичні навички:
1. Парсинг HTML сторінок за допомогою BeautifulSoup
2. Використання CSS селекторів та методів пошуку
3. Витягування даних з таблиць, списків, форм
4. Обробка та структурування даних з веб-сторінок

---

## 📚 Матеріали та підготовка

### Необхідні бібліотеки:
```bash
pip install beautifulsoup4 lxml requests
```

### Файли для роботи:
- Попередні проекти: `task1_weather.py`, `task2_currency.py`, `task3_rss.py`
- Нові приклади з веб-скрапінгом (будуть створені)

---

## 📖 Теоретична частина (30 хвилин)

### 1. Структура HTML документів (15 хвилин)

#### Основи HTML
```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Приклад структури</title>
</head>
<body>
    <header>
        <h1>Заголовок сторінки</h1>
        <nav>
            <ul>
                <li><a href="/">Головна</a></li>
                <li><a href="/news">Новини</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article class="news-article" id="article-1">
            <h2>Заголовок статті</h2>
            <p class="author">Автор: Іван Петренко</p>
            <div class="content">
                <p>Текст статті...</p>
            </div>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2025 Сайт</p>
    </footer>
</body>
</html>
```

#### DOM (Document Object Model)
- Дерево елементів
- Батьківські та дочірні елементи
- Атрибути елементів (class, id, href, src)
- Навігація по DOM дереву

### 2. CSS Селектори (15 хвилин)

#### Типи селекторів:

**1. Селектори за тегом:**
```css
p              /* всі параграфи */
div            /* всі div елементи */
a              /* всі посилання */
```

**2. Селектори за класом:**
```css
.news-article  /* елементи з class="news-article" */
.author        /* елементи з class="author" */
```

**3. Селектори за ID:**
```css
#article-1     /* елемент з id="article-1" */
#header        /* елемент з id="header" */
```

**4. Комбіновані селектори:**
```css
div.news-article        /* div з класом news-article */
p.author                /* параграф з класом author */
a.external              /* посилання з класом external */
```

**5. Ієрархічні селектори:**
```css
div p                   /* всі p всередині div */
article > h2            /* безпосередні h2 в article */
li + li                 /* li після іншого li */
```

**6. Селектори атрибутів:**
```css
a[href]                 /* посилання з атрибутом href */
img[src*="logo"]        /* img де src містить "logo" */
input[type="text"]      /* input з type="text" */
```

---

## 💻 Практична частина (80 хвилин)

### Частина 1: Основи BeautifulSoup (25 хвилин)

#### Приклад 1: Парсинг простого HTML

```python
from bs4 import BeautifulSoup
import requests

# HTML для прикладу
html_doc = """
<html>
<head><title>Тестова сторінка</title></head>
<body>
    <h1>Привіт, світ!</h1>
    <p class="intro">Це перший параграф.</p>
    <p class="content">Це другий параграф з <a href="https://example.com">посиланням</a>.</p>
    <ul id="news-list">
        <li class="news-item">Новина 1</li>
        <li class="news-item">Новина 2</li>
        <li class="news-item">Новина 3</li>
    </ul>
</body>
</html>
"""

# Створення об'єкту BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

# Різні методи пошуку
print("1. Пошук за тегом:")
h1 = soup.find('h1')
print(f"   {h1.text}")

print("\n2. Пошук за класом:")
intro = soup.find('p', class_='intro')
print(f"   {intro.text}")

print("\n3. Пошук за ID:")
news_list = soup.find('ul', id='news-list')
print(f"   Знайдено: {news_list.name}")

print("\n4. Пошук всіх елементів:")
all_p = soup.find_all('p')
for p in all_p:
    print(f"   - {p.text}")

print("\n5. Пошук з CSS селектором:")
news_items = soup.select('li.news-item')
for item in news_items:
    print(f"   - {item.text}")

print("\n6. Отримання атрибутів:")
link = soup.find('a')
print(f"   Текст: {link.text}")
print(f"   URL: {link.get('href')}")
```

#### Приклад 2: Навігація по DOM дереву

```python
from bs4 import BeautifulSoup

html = """
<div class="container">
    <h2>Заголовок</h2>
    <div class="content">
        <p>Перший параграф</p>
        <p>Другий параграф</p>
        <ul>
            <li>Пункт 1</li>
            <li>Пункт 2</li>
        </ul>
    </div>
</div>
"""

soup = BeautifulSoup(html, 'html.parser')

# Знайти контейнер
container = soup.find('div', class_='container')

print("Дочірні елементи:")
for child in container.children:
    if child.name:  # Пропускаємо текстові вузли
        print(f"  - {child.name}")

print("\nВсі нащадки:")
for descendant in container.descendants:
    if descendant.name:
        print(f"  - {descendant.name}")

# Навігація
content_div = soup.find('div', class_='content')
print("\nБатьківський елемент:", content_div.parent.name)

first_p = content_div.find('p')
print("Наступний елемент:", first_p.find_next_sibling().text)
```

### Частина 2: Розширення проекту Currency Converter (30 хвилин)

#### Завдання: Додати веб-скрапінг курсів НБУ

**Мета:** Порівняти курси з API та офіційного сайту НБУ

```python
"""
Розширення task2_currency.py
Додавання веб-скрапінгу курсів НБУ
"""

from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional
from datetime import datetime


class NBUScraperMixin:
    """
    Міксін для додавання можливості скрапінгу з сайту НБУ
    """
    
    NBU_URL = 'https://bank.gov.ua/ua/markets/exchangerates'
    
    def scrape_nbu_rates(self) -> Optional[Dict[str, float]]:
        """
        Отримати курси валют з сайту НБУ методом веб-скрапінгу
        
        Returns:
            Dict з курсами валют або None
        """
        try:
            print("🌐 Завантаження сторінки НБУ...")
            response = requests.get(self.NBU_URL, timeout=10)
            response.raise_for_status()
            
            # Парсинг HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Знайти таблицю з курсами
            # Примітка: CSS селектор залежить від структури сайту
            table = soup.find('table', class_='currency-table')
            
            if not table:
                print("❌ Таблицю курсів не знайдено")
                return None
            
            rates = {}
            
            # Парсинг рядків таблиці
            rows = table.find_all('tr')[1:]  # Пропускаємо заголовок
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    currency_code = cols[0].text.strip()
                    rate_text = cols[2].text.strip()
                    
                    # Конвертація тексту в число
                    try:
                        rate = float(rate_text.replace(',', '.'))
                        rates[currency_code] = rate
                    except ValueError:
                        continue
            
            print(f"✅ Отримано {len(rates)} курсів з НБУ")
            return rates
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка завантаження: {e}")
            return None
        except Exception as e:
            print(f"❌ Помилка парсингу: {e}")
            return None
    
    def compare_with_nbu(self, currency: str = 'USD'):
        """
        Порівняти курси з API та НБУ
        
        Args:
            currency: Код валюти
        """
        # Курс з API
        api_rates = self.get_rates('UAH')
        
        if not api_rates or currency not in api_rates:
            print(f"❌ Не вдалося отримати курс {currency} з API")
            return
        
        api_rate = api_rates[currency]
        
        # Курс з НБУ
        nbu_rates = self.scrape_nbu_rates()
        
        if not nbu_rates or currency not in nbu_rates:
            print(f"❌ Не вдалося отримати курс {currency} з НБУ")
            return
        
        nbu_rate = nbu_rates[currency]
        
        # Порівняння
        difference = api_rate - nbu_rate
        difference_percent = (difference / nbu_rate) * 100
        
        print("\n" + "="*60)
        print(f"📊 ПОРІВНЯННЯ КУРСІВ {currency}/UAH")
        print("="*60)
        print(f"API курс:    {api_rate:.4f}")
        print(f"НБУ курс:    {nbu_rate:.4f}")
        print(f"Різниця:     {difference:.4f} ({difference_percent:+.2f}%)")
        
        if abs(difference_percent) > 5:
            print("⚠️  Значна різниця в курсах!")
        else:
            print("✅ Курси приблизно однакові")
        
        print("="*60)


# Інтеграція з існуючим класом
class EnhancedCurrencyConverter(NBUScraperMixin, CurrencyConverter):
    """
    Розширений конвертер валют з веб-скрапінгом
    """
    pass


def demo_nbu_scraping():
    """Демонстрація скрапінгу НБУ"""
    print("\n" + "="*70)
    print("ДЕМО: Веб-скрапінг курсів НБУ")
    print("="*70)
    
    converter = EnhancedCurrencyConverter()
    
    # Порівняння курсів
    for currency in ['USD', 'EUR', 'GBP']:
        converter.compare_with_nbu(currency)
        print()


if __name__ == '__main__':
    demo_nbu_scraping()
```

### Частина 3: Розширення RSS Aggregator (25 хвилин)

#### Завдання: Додати парсинг новинних сайтів

**Мета:** Доповнити RSS новини прямим парсингом веб-сторінок

```python
"""
Розширення task3_rss.py
Додавання веб-скрапінгу новинних сайтів
"""

from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Optional
from datetime import datetime
import re


class WebScraperMixin:
    """
    Міксін для веб-скрапінгу новинних сайтів
    """
    
    # Конфігурація для різних сайтів
    SCRAPING_CONFIGS = {
        'threatpost': {
            'url': 'https://threatpost.com/',
            'article_selector': 'article.c-card',
            'title_selector': 'h2.c-card__title',
            'link_selector': 'a.c-card__link',
            'date_selector': 'time.c-card__time'
        },
        'bleeping_computer': {
            'url': 'https://www.bleepingcomputer.com/news/security/',
            'article_selector': 'div.bc_latest_news_text',
            'title_selector': 'h4',
            'link_selector': 'a',
            'date_selector': 'div.bc_news_date'
        }
    }
    
    def scrape_website(self, site_name: str) -> List[Dict]:
        """
        Парсинг новинного сайту
        
        Args:
            site_name: Назва сайту з SCRAPING_CONFIGS
            
        Returns:
            List статей
        """
        if site_name not in self.SCRAPING_CONFIGS:
            print(f"❌ Конфігурація для '{site_name}' не знайдена")
            return []
        
        config = self.SCRAPING_CONFIGS[site_name]
        
        try:
            print(f"🌐 Парсинг {site_name}...")
            
            # Завантаження сторінки
            response = requests.get(
                config['url'], 
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            
            # Парсинг
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Знайти всі статті
            articles_html = soup.select(config['article_selector'])
            
            articles = []
            
            for article_html in articles_html[:10]:  # Обмежити 10 статтями
                try:
                    # Витягти дані
                    title_elem = article_html.select_one(config['title_selector'])
                    link_elem = article_html.select_one(config['link_selector'])
                    date_elem = article_html.select_one(config['date_selector'])
                    
                    if not title_elem or not link_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get('href', '')
                    
                    # Повний URL
                    if link and not link.startswith('http'):
                        base_url = config['url'].rstrip('/')
                        link = base_url + link
                    
                    date = date_elem.get_text(strip=True) if date_elem else 'Unknown'
                    
                    article = {
                        'source': site_name.replace('_', ' ').title(),
                        'title': title,
                        'link': link,
                        'published': date,
                        'description': '',  # Потребує окремого запиту
                        'scraped': True  # Мітка, що отримано скрапінгом
                    }
                    
                    articles.append(article)
                    
                except Exception as e:
                    print(f"  ⚠️  Помилка парсингу статті: {e}")
                    continue
            
            print(f"  ✅ Отримано {len(articles)} статей")
            return articles
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Помилка завантаження: {e}")
            return []
        except Exception as e:
            print(f"  ❌ Помилка парсингу: {e}")
            return []
    
    def fetch_article_content(self, url: str) -> Optional[str]:
        """
        Отримати повний вміст статті
        
        Args:
            url: URL статті
            
        Returns:
            Текст статті або None
        """
        try:
            response = requests.get(
                url, 
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Спроба знайти основний контент
            # (може потребувати налаштування для кожного сайту)
            content_selectors = [
                'article',
                'div.article-content',
                'div.post-content',
                'div.entry-content'
            ]
            
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    # Видалити скрипти та стилі
                    for tag in content(['script', 'style', 'nav', 'aside']):
                        tag.decompose()
                    
                    # Витягти текст
                    text = content.get_text(separator='\n', strip=True)
                    return text
            
            return None
            
        except Exception as e:
            print(f"❌ Помилка отримання контенту: {e}")
            return None
    
    def scrape_all_configured_sites(self):
        """
        Парсинг всіх налаштованих сайтів
        """
        print("\n🔄 Веб-скрапінг новинних сайтів...")
        
        for site_name in self.SCRAPING_CONFIGS.keys():
            articles = self.scrape_website(site_name)
            self.articles.extend(articles)
        
        print(f"✅ Додано {len(self.articles)} статей через скрапінг")


# Інтеграція з існуючим класом
class EnhancedRSSAggregator(WebScraperMixin, RSSAggregator):
    """
    Розширений агрегатор з веб-скрапінгом
    """
    
    def fetch_all_sources(self):
        """
        Отримати дані з RSS та веб-скрапінгу
        """
        # RSS
        self.fetch_all_feeds()
        
        # Веб-скрапінг
        self.scrape_all_configured_sites()


def demo_web_scraping():
    """Демонстрація веб-скрапінгу"""
    print("\n" + "="*70)
    print("ДЕМО: Веб-скрапінг новинних сайтів")
    print("="*70)
    
    aggregator = EnhancedRSSAggregator()
    
    # Комбінований збір даних
    aggregator.fetch_all_sources()
    
    # Показати результати
    print(f"\n📊 Статистика:")
    print(f"   Всього статей: {len(aggregator.articles)}")
    
    # Розділити за джерелами
    rss_articles = [a for a in aggregator.articles if not a.get('scraped')]
    scraped_articles = [a for a in aggregator.articles if a.get('scraped')]
    
    print(f"   З RSS: {len(rss_articles)}")
    print(f"   Зі скрапінгу: {len(scraped_articles)}")
    
    # Показати топ
    aggregator.print_articles(aggregator.articles[:15])


if __name__ == '__main__':
    demo_web_scraping()
```

---

## 🎓 Самостійна робота (10 хвилин на заняття + домашнє завдання)

### Завдання на занятті:

1. **Створити простий скрапер** (5 хв)
   - Обрати будь-який новинний сайт
   - Написати код для витягування заголовків статей
   - Використати CSS селектори

2. **Інтегрувати з попередніми проектами** (5 хв)
   - Додати веб-скрапінг до одного з проектів
   - Протестувати функціонал

### Домашнє завдання:

#### Завдання 1: Розширити Weather Monitor (складність: ★★☆)
Додати парсинг погоди з веб-сайтів (наприклад, sinoptik.ua):
- Парсити прогноз на тиждень
- Порівнювати дані з API
- Створити комплексний звіт

#### Завдання 2: Створити Price Monitor (складність: ★★★)
Створити моніторинг цін на товари:
- Парсити ціни з 2-3 інтернет-магазинів
- Зберігати історію цін
- Відправляти алерти при зниженні ціни
- Генерувати графіки порівняння

#### Завдання 3: Job Scraper (складність: ★★★)
Створити скрапер вакансій:
- Парсити вакансії з djinni.co або work.ua
- Фільтрувати за ключовими словами
- Витягувати вимоги до кандидатів
- Генерувати структурований звіт

---

## 📝 Важливі примітки та best practices

### Етичні аспекти веб-скрапінгу:

1. **Robots.txt**
   ```python
   import requests
   from urllib.parse import urljoin
   
   def check_robots_txt(base_url: str) -> str:
       """Перевірити robots.txt"""
       robots_url = urljoin(base_url, '/robots.txt')
       try:
           response = requests.get(robots_url)
           if response.status_code == 200:
               return response.text
       except:
           pass
       return ""
   ```

2. **Затримки між запитами**
   ```python
   import time
   
   # Додавати затримку між запитами
   time.sleep(1)  # 1 секунда між запитами
   ```

3. **User-Agent**
   ```python
   headers = {
       'User-Agent': 'Mozilla/5.0 (educational purpose)'
   }
   requests.get(url, headers=headers)
   ```

### Обробка помилок:

```python
from requests.exceptions import RequestException

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
except RequestException as e:
    print(f"Помилка мережі: {e}")
except Exception as e:
    print(f"Помилка парсингу: {e}")
```

---

## 🔍 Контрольні питання

1. Що таке DOM і як він пов'язаний з HTML?
2. У чому різниця між `.find()` та `.find_all()` в BeautifulSoup?
3. Як використовувати CSS селектори в BeautifulSoup?
4. Які етичні аспекти потрібно враховувати при веб-скрапінгу?
5. Як обробляти помилки при парсингу HTML?
6. У чому різниця між парсером 'html.parser' та 'lxml'?

---

## 📚 Додаткові ресурси

1. **Документація BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
2. **CSS Selectors Reference**: https://www.w3schools.com/cssref/css_selectors.asp
3. **Requests documentation**: https://requests.readthedocs.io/
4. **HTML структура**: https://developer.mozilla.org/en-US/docs/Web/HTML

---

## ✅ Чеклист для викладача

- [ ] Підготувати демонстраційні HTML файли
- [ ] Перевірити доступність веб-сайтів для демо
- [ ] Підготувати резервні приклади (на випадок змін на сайтах)
- [ ] Встановити BeautifulSoup та lxml
- [ ] Підготувати код з попередніх занять
- [ ] Створити приклади інтеграції
- [ ] Підготувати матеріали про етичний скрапінг

---

## 🎯 Критерії оцінювання

### Робота на занятті (60%):
- Розуміння CSS селекторів (20%)
- Використання BeautifulSoup (20%)
- Інтеграція з попередніми проектами (20%)

### Домашнє завдання (40%):
- Функціональність скрапера (15%)
- Обробка помилок (10%)
- Структура коду (10%)
- Документація та коментарі (5%)

---

**Успіхів у вивченні веб-скрапінгу! 🚀**
