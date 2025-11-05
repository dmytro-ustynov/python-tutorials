"""
Практичне заняття 4-4: Основи веб-скрапінгу
Приклад 1: Основи BeautifulSoup та CSS селектори

Автор: Курс Python для кібербезпеки
"""

from bs4 import BeautifulSoup
import requests
from typing import List, Dict


def example_1_basic_parsing():
    """Приклад 1: Базовий парсинг HTML"""
    print("\n" + "="*70)
    print("ПРИКЛАД 1: Базовий парсинг HTML")
    print("="*70)
    
    html_doc = """
    <html>
    <head><title>Новини кібербезпеки</title></head>
    <body>
        <header>
            <h1>Головні новини</h1>
            <nav>
                <ul>
                    <li><a href="/news">Новини</a></li>
                    <li><a href="/blog">Блог</a></li>
                </ul>
            </nav>
        </header>
        
        <main>
            <article class="news-article" id="article-1">
                <h2>Нова вразливість у Windows</h2>
                <p class="author">Автор: Іван Петренко</p>
                <p class="date">2025-11-04</p>
                <div class="content">
                    <p>Microsoft випустила патч для критичної вразливості...</p>
                </div>
                <div class="tags">
                    <span class="tag">Windows</span>
                    <span class="tag">Security</span>
                </div>
            </article>
            
            <article class="news-article" id="article-2">
                <h2>Ransomware атака на компанію</h2>
                <p class="author">Автор: Марія Коваленко</p>
                <p class="date">2025-11-03</p>
                <div class="content">
                    <p>Велика корпорація стала жертвою ransomware...</p>
                </div>
                <div class="tags">
                    <span class="tag">Ransomware</span>
                    <span class="tag">Incident</span>
                </div>
            </article>
        </main>
        
        <footer>
            <p>&copy; 2025 Новини безпеки</p>
        </footer>
    </body>
    </html>
    """
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    # 1. Пошук за тегом
    print("\n1️⃣  Пошук за тегом:")
    title = soup.find('title')
    print(f"   Заголовок сторінки: {title.text}")
    
    h1 = soup.find('h1')
    print(f"   Головний заголовок: {h1.text}")
    
    # 2. Пошук за класом
    print("\n2️⃣  Пошук за класом:")
    first_article = soup.find('article', class_='news-article')
    print(f"   Перша стаття: {first_article.find('h2').text}")
    
    # 3. Пошук всіх елементів
    print("\n3️⃣  Пошук всіх статей:")
    all_articles = soup.find_all('article', class_='news-article')
    for i, article in enumerate(all_articles, 1):
        h2 = article.find('h2')
        author = article.find('p', class_='author')
        print(f"   {i}. {h2.text}")
        print(f"      {author.text}")
    
    # 4. CSS селектори
    print("\n4️⃣  CSS селектори:")
    
    # Селектор за ID
    article_1 = soup.select_one('#article-1')
    print(f"   Стаття #article-1: {article_1.find('h2').text}")
    
    # Комбінований селектор
    tags = soup.select('article .tag')
    print(f"   Всі теги:")
    for tag in tags:
        print(f"      - {tag.text}")
    
    # Ієрархічний селектор
    nav_links = soup.select('nav ul li a')
    print(f"   Навігаційні посилання:")
    for link in nav_links:
        print(f"      - {link.text} ({link.get('href')})")


def example_2_css_selectors():
    """Приклад 2: Детальні CSS селектори"""
    print("\n" + "="*70)
    print("ПРИКЛАД 2: Детальні CSS селектори")
    print("="*70)
    
    html = """
    <div class="container">
        <ul id="security-list">
            <li class="critical">CVE-2025-0001: RCE у nginx</li>
            <li class="high">CVE-2025-0002: XSS у WordPress</li>
            <li class="medium">CVE-2025-0003: SQLi у Joomla</li>
            <li class="low">CVE-2025-0004: Info Disclosure</li>
        </ul>
        
        <table class="vulnerability-table">
            <tr>
                <th>ID</th>
                <th>Severity</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>CVE-2025-0001</td>
                <td class="severity critical">Critical</td>
                <td class="status patched">Patched</td>
            </tr>
            <tr>
                <td>CVE-2025-0002</td>
                <td class="severity high">High</td>
                <td class="status vulnerable">Vulnerable</td>
            </tr>
        </table>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    print("\n1️⃣  Селектор за атрибутом:")
    critical_items = soup.select('li.critical')
    print(f"   Критичні вразливості:")
    for item in critical_items:
        print(f"      - {item.text}")
    
    print("\n2️⃣  Комбінований селектор:")
    vuln_cells = soup.select('td.status.vulnerable')
    print(f"   Вразливі системи:")
    for cell in vuln_cells:
        # Знайти CVE ID в тому ж рядку
        row = cell.parent
        cve_id = row.find('td').text
        print(f"      - {cve_id}: {cell.text}")
    
    print("\n3️⃣  Ієрархічний селектор:")
    table_rows = soup.select('table.vulnerability-table tr')
    print(f"   Всі рядки таблиці: {len(table_rows)}")
    
    print("\n4️⃣  Селектор нащадків:")
    all_in_container = soup.select('div.container *')
    print(f"   Всіх елементів у контейнері: {len(all_in_container)}")


def example_3_navigation():
    """Приклад 3: Навігація по DOM дереву"""
    print("\n" + "="*70)
    print("ПРИКЛАД 3: Навігація по DOM дереву")
    print("="*70)
    
    html = """
    <div class="report">
        <h2>Звіт про інцидент безпеки</h2>
        <div class="metadata">
            <span class="id">INC-2025-001</span>
            <span class="date">2025-11-04</span>
            <span class="severity critical">Critical</span>
        </div>
        <div class="description">
            <p>Виявлено несанкціонований доступ до системи.</p>
            <p>Атака здійснена через вразливість веб-додатку.</p>
        </div>
        <div class="actions">
            <button>Закрити</button>
            <button>Ескалувати</button>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Знайти стартовий елемент
    report = soup.find('div', class_='report')
    
    print("\n1️⃣  Дочірні елементи (children):")
    for child in report.children:
        if child.name:  # Пропускаємо текстові вузли
            print(f"   - {child.name}: {child.get('class', ['no class'])}")
    
    print("\n2️⃣  Всі нащадки (descendants):")
    all_descendants = [d for d in report.descendants if d.name]
    print(f"   Всього нащадків: {len(all_descendants)}")
    
    print("\n3️⃣  Батьківський елемент (parent):")
    metadata = soup.find('div', class_='metadata')
    print(f"   Батько metadata: {metadata.parent.get('class')}")
    
    print("\n4️⃣  Сусідні елементи (siblings):")
    description = soup.find('div', class_='description')
    next_elem = description.find_next_sibling()
    print(f"   Наступний після description: {next_elem.get('class')}")
    
    prev_elem = description.find_previous_sibling()
    print(f"   Попередній перед description: {prev_elem.get('class')}")


def example_4_attributes():
    """Приклад 4: Робота з атрибутами"""
    print("\n" + "="*70)
    print("ПРИКЛАД 4: Робота з атрибутами")
    print("="*70)
    
    html = """
    <div class="links-section">
        <a href="https://nvd.nist.gov/" class="external" target="_blank">
            NVD Database
        </a>
        <a href="/internal/reports" class="internal">
            Внутрішні звіти
        </a>
        <img src="/images/logo.png" alt="Logo" width="100" height="50">
        <input type="text" name="search" placeholder="Пошук CVE..." required>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    print("\n1️⃣  Отримання атрибутів:")
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        text = link.text.strip()
        classes = link.get('class', [])
        print(f"   {text}:")
        print(f"      href: {href}")
        print(f"      classes: {classes}")
    
    print("\n2️⃣  Атрибути зображення:")
    img = soup.find('img')
    print(f"   src: {img.get('src')}")
    print(f"   alt: {img.get('alt')}")
    print(f"   width: {img.get('width')}px")
    
    print("\n3️⃣  Атрибути форми:")
    input_field = soup.find('input')
    print(f"   type: {input_field.get('type')}")
    print(f"   name: {input_field.get('name')}")
    print(f"   placeholder: {input_field.get('placeholder')}")
    print(f"   required: {input_field.has_attr('required')}")
    
    print("\n4️⃣  Словник всіх атрибутів:")
    print(f"   {img.attrs}")


def example_5_extracting_data():
    """Приклад 5: Витягування структурованих даних"""
    print("\n" + "="*70)
    print("ПРИКЛАД 5: Витягування структурованих даних")
    print("="*70)
    
    html = """
    <table class="vulnerability-list">
        <thead>
            <tr>
                <th>CVE ID</th>
                <th>Product</th>
                <th>Severity</th>
                <th>CVSS</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="/cve/2025-0001">CVE-2025-0001</a></td>
                <td>Apache HTTP Server</td>
                <td class="critical">Critical</td>
                <td>9.8</td>
            </tr>
            <tr>
                <td><a href="/cve/2025-0002">CVE-2025-0002</a></td>
                <td>WordPress</td>
                <td class="high">High</td>
                <td>7.5</td>
            </tr>
            <tr>
                <td><a href="/cve/2025-0003">CVE-2025-0003</a></td>
                <td>MySQL</td>
                <td class="medium">Medium</td>
                <td>5.3</td>
            </tr>
        </tbody>
    </table>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Парсинг таблиці
    vulnerabilities = []
    
    table = soup.find('table', class_='vulnerability-list')
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        
        vuln = {
            'cve_id': cols[0].find('a').text,
            'link': cols[0].find('a').get('href'),
            'product': cols[1].text,
            'severity': cols[2].text,
            'severity_class': cols[2].get('class')[0],
            'cvss': float(cols[3].text)
        }
        
        vulnerabilities.append(vuln)
    
    print("\n📊 Витягнуті дані:")
    for vuln in vulnerabilities:
        print(f"\n   {vuln['cve_id']} - {vuln['product']}")
        print(f"      Severity: {vuln['severity']} (CVSS: {vuln['cvss']})")
        print(f"      Link: {vuln['link']}")
    
    # Статистика
    print("\n📈 Статистика:")
    critical = [v for v in vulnerabilities if v['severity_class'] == 'critical']
    high = [v for v in vulnerabilities if v['severity_class'] == 'high']
    medium = [v for v in vulnerabilities if v['severity_class'] == 'medium']
    
    print(f"   Critical: {len(critical)}")
    print(f"   High: {len(high)}")
    print(f"   Medium: {len(medium)}")
    print(f"   Average CVSS: {sum(v['cvss'] for v in vulnerabilities) / len(vulnerabilities):.2f}")


def main():
    """Запуск всіх прикладів"""
    print("\n" + "="*70)
    print("🎓 ОСНОВИ BEAUTIFULSOUP ТА CSS СЕЛЕКТОРИ")
    print("="*70)
    
    try:
        example_1_basic_parsing()
        example_2_css_selectors()
        example_3_navigation()
        example_4_attributes()
        example_5_extracting_data()
        
        print("\n" + "="*70)
        print("✅ Всі приклади успішно виконані!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Перевірка наявності BeautifulSoup
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Помилка: Бібліотека BeautifulSoup не встановлена")
        print("Встановіть її командою: pip install beautifulsoup4")
        exit(1)
    
    main()
