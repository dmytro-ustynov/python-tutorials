"""
Практичне заняття 4-4: Основи веб-скрапінгу
Приклад 3: Інтеграція з RSS Aggregator

Розширення task3_rss.py з прямим парсингом новинних сайтів
"""

from bs4 import BeautifulSoup
import requests
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
import json
from pathlib import Path
import re


class RSSAggregator:
    """Базовий RSS агрегатор (з task3_rss.py)"""
    
    DEFAULT_FEEDS = {
        'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
        'Krebs on Security': 'https://krebsonsecurity.com/feed/',
    }
    
    def __init__(self, feeds_file: str = 'feeds.json'):
        self.feeds_file = Path(feeds_file)
        self.feeds = self._load_feeds()
        self.articles = []
    
    def _load_feeds(self) -> Dict[str, str]:
        if self.feeds_file.exists():
            with open(self.feeds_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.DEFAULT_FEEDS.copy()
    
    def fetch_feed(self, url: str) -> Optional[feedparser.FeedParserDict]:
        try:
            feed = feedparser.parse(url)
            return feed if not feed.bozo else None
        except:
            return None
    
    def fetch_all_feeds(self):
        self.articles = []
        print("\n🔄 Завантаження RSS каналів...")
        
        for name, url in self.feeds.items():
            print(f"  • {name}...", end=" ")
            feed = self.fetch_feed(url)
            
            if feed and feed.entries:
                for entry in feed.entries:
                    article = {
                        'source': name,
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', 'Unknown'),
                        'summary': entry.get('summary', ''),
                        'type': 'rss'
                    }
                    self.articles.append(article)
                print(f"✅ {len(feed.entries)} статей")
            else:
                print("❌")
    
    @staticmethod
    def _clean_html(text: str) -> str:
        clean = re.sub('<.*?>', '', text)
        clean = re.sub(r'\s+', ' ', clean)
        return clean.strip()


class WebScraperMixin:
    """Міксін для веб-скрапінгу новинних сайтів"""
    
    # Конфігурації для різних сайтів
    SCRAPING_CONFIGS = {
        'bleeping_computer': {
            'name': 'Bleeping Computer',
            'url': 'https://www.bleepingcomputer.com/news/security/',
            'article_selector': 'article.bc_latest_news',
            'title_selector': 'h4 a',
            'link_selector': 'h4 a',
            'summary_selector': 'p.bc_latest_news_text',
            'date_selector': 'li.bc_news_date'
        },
        'demo_site': {
            'name': 'Demo Security News',
            'url': 'demo',  # Буде використано демо HTML
            'article_selector': 'article.news-item',
            'title_selector': 'h2.title',
            'link_selector': 'a.read-more',
            'summary_selector': 'p.summary',
            'date_selector': 'time.published'
        }
    }
    
    def scrape_website(self, site_key: str) -> List[Dict]:
        """
        Парсинг новинного сайту
        
        Args:
            site_key: Ключ сайту з SCRAPING_CONFIGS
            
        Returns:
            List статей
        """
        if site_key not in self.SCRAPING_CONFIGS:
            print(f"❌ Конфігурація для '{site_key}' не знайдена")
            return []
        
        config = self.SCRAPING_CONFIGS[site_key]
        
        # Для демо використовуємо тестовий HTML
        if site_key == 'demo_site':
            return self._scrape_demo_site(config)
        
        try:
            print(f"🌐 Парсинг {config['name']}...")
            
            # Завантаження сторінки
            headers = {
                'User-Agent': 'Mozilla/5.0 (educational purpose)'
            }
            response = requests.get(
                config['url'],
                timeout=15,
                headers=headers
            )
            response.raise_for_status()
            
            # Парсинг
            return self._parse_articles(response.content, config)
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Помилка завантаження: {e}")
            print(f"  💡 Використовуємо демо дані для {config['name']}")
            return self._get_demo_articles(config['name'])
        except Exception as e:
            print(f"  ❌ Помилка парсингу: {e}")
            return []
    
    def _scrape_demo_site(self, config: Dict) -> List[Dict]:
        """Парсинг демонстраційного HTML"""
        demo_html = """
        <html>
        <body>
            <article class="news-item">
                <h2 class="title">Нова критична вразливість у Windows</h2>
                <time class="published">2025-11-04</time>
                <p class="summary">
                    Microsoft випустила екстрений патч для критичної вразливості,
                    яка дозволяє віддалене виконання коду.
                </p>
                <a class="read-more" href="https://example.com/news/1">Читати далі</a>
            </article>
            
            <article class="news-item">
                <h2 class="title">Масштабна DDoS атака на банки</h2>
                <time class="published">2025-11-03</time>
                <p class="summary">
                    Кілька великих банків зазнали DDoS атаки, що призвело до
                    тимчасового припинення онлайн-сервісів.
                </p>
                <a class="read-more" href="https://example.com/news/2">Читати далі</a>
            </article>
            
            <article class="news-item">
                <h2 class="title">Виявлено нову ransomware групу</h2>
                <time class="published">2025-11-02</time>
                <p class="summary">
                    Дослідники безпеки виявили нову групу кіберзлочинців,
                    що спеціалізується на ransomware атаках.
                </p>
                <a class="read-more" href="https://example.com/news/3">Читати далі</a>
            </article>
            
            <article class="news-item">
                <h2 class="title">Оновлення політики кібербезпеки ЄС</h2>
                <time class="published">2025-11-01</time>
                <p class="summary">
                    Європейський Союз оголосив про нові вимоги до кібербезпеки
                    для критичної інфраструктури.
                </p>
                <a class="read-more" href="https://example.com/news/4">Читати далі</a>
            </article>
            
            <article class="news-item">
                <h2 class="title">Підсумки року: головні кіберінциденти</h2>
                <time class="published">2025-10-31</time>
                <p class="summary">
                    Огляд найзначніших кіберінцидентів та атак за останній рік.
                </p>
                <a class="read-more" href="https://example.com/news/5">Читати далі</a>
            </article>
        </body>
        </html>
        """
        
        print(f"🧪 Парсинг {config['name']} (демо режим)...")
        return self._parse_articles(demo_html, config)
    
    def _parse_articles(self, html_content, config: Dict) -> List[Dict]:
        """Парсинг статей з HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Знайти всі статті
        articles_html = soup.select(config['article_selector'])
        
        if not articles_html:
            print(f"  ⚠️  Статті не знайдено за селектором: {config['article_selector']}")
            return []
        
        articles = []
        
        for article_html in articles_html[:10]:  # Максимум 10
            try:
                # Витягти дані
                title_elem = article_html.select_one(config['title_selector'])
                link_elem = article_html.select_one(config['link_selector'])
                summary_elem = article_html.select_one(config['summary_selector'])
                date_elem = article_html.select_one(config['date_selector'])
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = link_elem.get('href', '') if link_elem else ''
                summary = summary_elem.get_text(strip=True) if summary_elem else ''
                date = date_elem.get_text(strip=True) if date_elem else 'Unknown'
                
                # Повний URL
                if link and not link.startswith('http'):
                    base_url = config['url'].rstrip('/')
                    if base_url != 'demo':
                        # Витягти base URL
                        from urllib.parse import urlparse
                        parsed = urlparse(config['url'])
                        base_url = f"{parsed.scheme}://{parsed.netloc}"
                        link = base_url + link
                
                article = {
                    'source': config['name'],
                    'title': title,
                    'link': link,
                    'published': date,
                    'summary': summary,
                    'type': 'scraped'
                }
                
                articles.append(article)
                
            except Exception as e:
                print(f"  ⚠️  Помилка парсингу статті: {e}")
                continue
        
        print(f"  ✅ Отримано {len(articles)} статей")
        return articles
    
    def _get_demo_articles(self, source_name: str) -> List[Dict]:
        """Отримати демо статті (якщо справжній сайт недоступний)"""
        return [
            {
                'source': source_name,
                'title': 'Демо стаття 1: Вразливість нульового дня',
                'link': 'https://example.com/demo1',
                'published': '2025-11-04',
                'summary': 'Виявлено критичну вразливість нульового дня...',
                'type': 'scraped'
            },
            {
                'source': source_name,
                'title': 'Демо стаття 2: Кібератака на підприємство',
                'link': 'https://example.com/demo2',
                'published': '2025-11-03',
                'summary': 'Великомасштабна атака на критичну інфраструктуру...',
                'type': 'scraped'
            }
        ]
    
    def scrape_all_configured_sites(self):
        """Парсинг всіх налаштованих сайтів"""
        print("\n🔄 Веб-скрапінг новинних сайтів...")
        
        scraped_count = 0
        
        for site_key in self.SCRAPING_CONFIGS.keys():
            articles = self.scrape_website(site_key)
            self.articles.extend(articles)
            scraped_count += len(articles)
        
        print(f"✅ Додано {scraped_count} статей через скрапінг")
    
    def fetch_article_full_content(self, url: str) -> Optional[str]:
        """
        Отримати повний вміст статті
        
        Args:
            url: URL статті
            
        Returns:
            Текст статті
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Спроба знайти основний контент
            content_selectors = [
                'article',
                'div.article-content',
                'div.post-content',
                'div.entry-content',
                'main'
            ]
            
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    # Видалити зайве
                    for tag in content(['script', 'style', 'nav', 'aside', 'ad']):
                        tag.decompose()
                    
                    # Витягти текст
                    text = content.get_text(separator='\n', strip=True)
                    return text
            
            return None
            
        except Exception as e:
            print(f"❌ Помилка отримання контенту: {e}")
            return None


class EnhancedRSSAggregator(WebScraperMixin, RSSAggregator):
    """Розширений RSS агрегатор з веб-скрапінгом"""
    
    def fetch_all_sources(self):
        """Отримати дані з RSS та веб-скрапінгу"""
        # RSS канали
        self.fetch_all_feeds()
        
        # Веб-скрапінг
        self.scrape_all_configured_sites()
    
    def print_articles_summary(self):
        """Вивести статистику статей"""
        if not self.articles:
            print("📰 Статей не знайдено")
            return
        
        print("\n" + "="*70)
        print("📊 СТАТИСТИКА ЗІБРАНИХ СТАТЕЙ")
        print("="*70)
        
        # Загальна статистика
        total = len(self.articles)
        rss_articles = [a for a in self.articles if a.get('type') == 'rss']
        scraped_articles = [a for a in self.articles if a.get('type') == 'scraped']
        
        print(f"\nВсього статей: {total}")
        print(f"  • З RSS каналів: {len(rss_articles)}")
        print(f"  • Зі скрапінгу: {len(scraped_articles)}")
        
        # За джерелами
        print("\n📍 За джерелами:")
        sources = {}
        for article in self.articles:
            source = article['source']
            sources[source] = sources.get(source, 0) + 1
        
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {source}: {count} статей")
        
        print("="*70)
    
    def print_articles(self, articles: List[Dict] = None, limit: int = None):
        """Вивести список статей"""
        articles_to_print = articles if articles else self.articles
        
        if not articles_to_print:
            print("📰 Статей не знайдено")
            return
        
        display_articles = articles_to_print[:limit] if limit else articles_to_print
        
        print("\n" + "="*70)
        print(f"📰 СТАТТІ")
        print("="*70)
        
        for i, article in enumerate(display_articles, 1):
            type_icon = "📡" if article.get('type') == 'rss' else "🌐"
            
            print(f"\n{i}. {type_icon} [{article['source']}] {article['title']}")
            print(f"   📅 {article['published']}")
            if article['link']:
                print(f"   🔗 {article['link']}")
            
            # Скорочений summary
            summary = article.get('summary', '')
            if summary:
                if len(summary) > 200:
                    summary = summary[:200] + "..."
                print(f"   💬 {summary}")
        
        if limit and len(articles_to_print) > limit:
            print(f"\n... та ще {len(articles_to_print) - limit} статей")
        
        print("="*70)


def demo_basic_scraping():
    """Демо базового скрапінгу"""
    print("\n" + "="*70)
    print("ДЕМО 1: Базовий веб-скрапінг новинних сайтів")
    print("="*70)
    
    aggregator = EnhancedRSSAggregator()
    
    # Тільки скрапінг
    aggregator.scrape_all_configured_sites()
    
    # Статистика
    aggregator.print_articles_summary()
    
    # Показати статті
    aggregator.print_articles(limit=5)


def demo_combined_sources():
    """Демо комбінованого збору даних"""
    print("\n" + "="*70)
    print("ДЕМО 2: Комбінований збір (RSS + Скрапінг)")
    print("="*70)
    
    aggregator = EnhancedRSSAggregator()
    
    # RSS + Скрапінг
    aggregator.fetch_all_sources()
    
    # Статистика
    aggregator.print_articles_summary()
    
    # Топ статей
    print("\n🔝 ТОП-10 ОСТАННІХ СТАТЕЙ:")
    aggregator.print_articles(limit=10)


def demo_article_content():
    """Демо завантаження повного контенту"""
    print("\n" + "="*70)
    print("ДЕМО 3: Завантаження повного контенту статті")
    print("="*70)
    
    aggregator = EnhancedRSSAggregator()
    
    # Отримати статті
    aggregator.scrape_all_configured_sites()
    
    if aggregator.articles:
        # Взяти першу статтю
        article = aggregator.articles[0]
        
        print(f"\n📄 Стаття: {article['title']}")
        print(f"🔗 URL: {article['link']}")
        
        print("\n⏳ Завантаження повного контенту...")
        
        # Для демо використовуємо заглушку
        print("\n📝 Повний контент:")
        print("-" * 70)
        print("(Для демо показано короткий варіант)")
        print(article.get('summary', 'Контент недоступний'))
        print("-" * 70)
        
        print("\n💡 У реальному застосунку тут буде повний текст статті,")
        print("   витягнутий методом fetch_article_full_content()")


def main():
    """Головна функція"""
    print("\n" + "="*70)
    print("📰 РОЗШИРЕНИЙ RSS АГРЕГАТОР З ВЕБ-СКРАПІНГОМ")
    print("="*70)
    print("\nІнтеграція веб-скрапінгу з попереднім проектом RSS Aggregator")
    
    try:
        # Запустити демонстрації
        demo_basic_scraping()
        demo_combined_sources()
        demo_article_content()
        
        print("\n" + "="*70)
        print("✅ Демонстрація завершена!")
        print("="*70)
        print("\n💡 Що було продемонстровано:")
        print("   ✓ Парсинг статей з веб-сторінок")
        print("   ✓ Комбінування RSS та скрапінгу")
        print("   ✓ Структурування даних з різних джерел")
        print("   ✓ Витягування повного контенту статей")
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Демонстрацію перервано користувачем")
    except Exception as e:
        print(f"\n\n❌ Помилка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Перевірка бібліотек
    try:
        from bs4 import BeautifulSoup
        import requests
        import feedparser
    except ImportError:
        print("❌ Помилка: Необхідні бібліотеки не встановлені")
        print("Встановіть їх командою:")
        print("pip install beautifulsoup4 requests feedparser")
        exit(1)
    
    main()
