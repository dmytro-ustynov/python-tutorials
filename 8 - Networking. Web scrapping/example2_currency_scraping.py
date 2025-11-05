"""
Практичне заняття 4-4: Основи веб-скрапінгу
Приклад 2: Інтеграція з Currency Converter

Розширення task2_currency.py з веб-скрапінгом курсів НБУ
"""

from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path


class CurrencyConverter:
    """Базовий конвертер валют (з task2_currency.py)"""
    
    def __init__(self, cache_ttl: int = 3600):
        self.base_url = 'https://api.exchangerate-api.com/v4/latest'
        self.cache_file = Path('currency_cache.json')
        self.cache_ttl = cache_ttl
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _is_cache_valid(self, currency: str) -> bool:
        if currency not in self.cache:
            return False
        cached_time = datetime.fromisoformat(self.cache[currency]['timestamp'])
        return (datetime.now() - cached_time).seconds < self.cache_ttl
    
    def get_rates(self, base_currency: str = 'USD', 
                  use_cache: bool = True) -> Optional[Dict]:
        """Отримати курси валют з API"""
        if use_cache and self._is_cache_valid(base_currency):
            print(f"💾 Використано кеш для {base_currency}")
            return self.cache[base_currency]['rates']
        
        url = f'{self.base_url}/{base_currency}'
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data['rates']
            
            self.cache[base_currency] = {
                'rates': rates,
                'timestamp': datetime.now().isoformat(),
                'base': base_currency
            }
            self._save_cache()
            
            print(f"🌐 Отримано актуальні курси для {base_currency}")
            return rates
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка запиту: {e}")
            return None


class NBUScraperMixin:
    """Міксін для веб-скрапінгу курсів НБУ"""
    
    NBU_URL = 'https://bank.gov.ua/ua/markets/exchangerates'
    
    def scrape_nbu_rates(self) -> Optional[Dict[str, float]]:
        """
        Парсинг курсів валют з сайту НБУ
        
        Returns:
            Dict з курсами валют {код_валюти: курс_до_UAH}
        """
        try:
            print("\n🌐 Завантаження сторінки НБУ...")
            
            # Завантаження сторінки
            headers = {
                'User-Agent': 'Mozilla/5.0 (educational purpose)'
            }
            response = requests.get(self.NBU_URL, timeout=15, headers=headers)
            response.raise_for_status()
            
            # Парсинг HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print("🔍 Пошук таблиці з курсами...")
            
            # Знайти таблицю (структура може змінюватись)
            # Спробуємо різні варіанти селекторів
            table = None
            
            # Варіант 1: Таблиця з класом
            table = soup.find('table', class_='table')
            
            # Варіант 2: Таблиця без класу
            if not table:
                table = soup.find('table')
            
            # Варіант 3: Шукаємо по структурі
            if not table:
                # Можливо таблиця в div з певним класом
                container = soup.find('div', class_='exchange-rates')
                if container:
                    table = container.find('table')
            
            if not table:
                print("❌ Таблицю курсів не знайдено")
                print("💡 Можлива причина: структура сайту змінилась")
                return self._get_demo_nbu_rates()
            
            print("✅ Таблиця знайдена, парсинг даних...")
            
            rates = {}
            
            # Парсинг рядків таблиці
            rows = table.find_all('tr')
            
            for row in rows[1:]:  # Пропускаємо заголовок
                cols = row.find_all('td')
                
                if len(cols) >= 2:
                    # Код валюти зазвичай в першій колонці
                    currency_cell = cols[0]
                    rate_cell = cols[-1]  # Курс зазвичай в останній
                    
                    # Витягти текст
                    currency_text = currency_cell.get_text(strip=True)
                    rate_text = rate_cell.get_text(strip=True)
                    
                    # Спробувати витягти 3-літерний код валюти
                    import re
                    currency_match = re.search(r'([A-Z]{3})', currency_text)
                    
                    if currency_match:
                        currency_code = currency_match.group(1)
                        
                        # Конвертувати курс в число
                        try:
                            # Очистити від непотрібних символів
                            rate_text = rate_text.replace(',', '.').replace(' ', '')
                            rate = float(rate_text)
                            rates[currency_code] = rate
                        except ValueError:
                            continue
            
            if rates:
                print(f"✅ Отримано {len(rates)} курсів з НБУ")
                return rates
            else:
                print("⚠️  Курси не знайдено, використовуємо демо дані")
                return self._get_demo_nbu_rates()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка завантаження: {e}")
            print("💡 Використовуємо демо дані")
            return self._get_demo_nbu_rates()
        except Exception as e:
            print(f"❌ Помилка парсингу: {e}")
            import traceback
            traceback.print_exc()
            print("💡 Використовуємо демо дані")
            return self._get_demo_nbu_rates()
    
    def _get_demo_nbu_rates(self) -> Dict[str, float]:
        """Демонстраційні курси НБУ (для тестування)"""
        return {
            'USD': 41.25,
            'EUR': 44.80,
            'GBP': 52.30,
            'PLN': 10.15,
            'CHF': 47.20
        }
    
    def compare_with_nbu(self, currency: str = 'USD'):
        """
        Порівняти курси з API та НБУ
        
        Args:
            currency: Код валюти для порівняння
        """
        print("\n" + "="*70)
        print(f"📊 ПОРІВНЯННЯ КУРСІВ {currency}")
        print("="*70)
        
        # Отримати курс з API (до UAH)
        print("\n1️⃣  Отримання курсу з API...")
        api_rates = self.get_rates('UAH')
        
        if not api_rates:
            print("❌ Не вдалося отримати курс з API")
            return
        
        # API дає курс UAH до інших валют, нам потрібно навпаки
        if currency in api_rates:
            api_rate = 1 / api_rates[currency]  # Конвертуємо
        else:
            print(f"❌ Валюта {currency} не знайдена в API")
            return
        
        # Отримати курс з НБУ
        print("\n2️⃣  Парсинг курсу з сайту НБУ...")
        nbu_rates = self.scrape_nbu_rates()
        
        if not nbu_rates or currency not in nbu_rates:
            print(f"❌ Не вдалося отримати курс {currency} з НБУ")
            return
        
        nbu_rate = nbu_rates[currency]
        
        # Порівняння
        difference = api_rate - nbu_rate
        difference_percent = (difference / nbu_rate) * 100
        
        print("\n" + "="*70)
        print(f"💱 РЕЗУЛЬТАТ ПОРІВНЯННЯ {currency}/UAH")
        print("="*70)
        print(f"{'Джерело':<20} {'Курс':<15} {'Різниця':<15}")
        print("-"*70)
        print(f"{'API курс:':<20} {api_rate:<15.4f}")
        print(f"{'НБУ курс:':<20} {nbu_rate:<15.4f}")
        print(f"{'Різниця:':<20} {difference:<15.4f} ({difference_percent:+.2f}%)")
        print("="*70)
        
        # Висновок
        if abs(difference_percent) > 5:
            print("⚠️  Значна різниця в курсах (>5%)")
            print("💡 Можливі причини:")
            print("   - Різний час оновлення даних")
            print("   - Різні джерела даних")
            print("   - Комісії та спреди")
        elif abs(difference_percent) > 1:
            print("ℹ️  Помірна різниця в курсах (1-5%)")
        else:
            print("✅ Курси практично однакові (<1%)")
    
    def get_all_nbu_rates_table(self):
        """Вивести всі курси НБУ у вигляді таблиці"""
        print("\n" + "="*70)
        print("📋 ОФІЦІЙНІ КУРСИ НБУ")
        print("="*70)
        
        nbu_rates = self.scrape_nbu_rates()
        
        if not nbu_rates:
            print("❌ Не вдалося отримати дані")
            return
        
        print(f"\n{'Валюта':<10} {'Курс до UAH':<15} {'100 UAH у валюті':<20}")
        print("-"*70)
        
        for currency, rate in sorted(nbu_rates.items()):
            uah_to_currency = 100 / rate
            print(f"{currency:<10} {rate:<15.4f} {uah_to_currency:<20.2f}")
        
        print("="*70)
        print(f"Всього валют: {len(nbu_rates)}")
        print(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")


class EnhancedCurrencyConverter(NBUScraperMixin, CurrencyConverter):
    """
    Розширений конвертер валют з веб-скрапінгом НБУ
    """
    pass


def demo_basic_scraping():
    """Демо базового скрапінгу"""
    print("\n" + "="*70)
    print("ДЕМО 1: Базовий веб-скрапінг НБУ")
    print("="*70)
    
    converter = EnhancedCurrencyConverter()
    
    # Показати всі курси НБУ
    converter.get_all_nbu_rates_table()


def demo_comparison():
    """Демо порівняння курсів"""
    print("\n" + "="*70)
    print("ДЕМО 2: Порівняння курсів з API та НБУ")
    print("="*70)
    
    converter = EnhancedCurrencyConverter()
    
    # Порівняти різні валюти
    currencies = ['USD', 'EUR', 'GBP']
    
    for currency in currencies:
        converter.compare_with_nbu(currency)
        print()


def demo_full_analysis():
    """Демо повного аналізу"""
    print("\n" + "="*70)
    print("ДЕМО 3: Повний аналіз валют")
    print("="*70)
    
    converter = EnhancedCurrencyConverter()
    
    print("\n📊 Аналіз валютного ринку\n")
    
    # 1. Курси НБУ
    print("1️⃣  Офіційні курси НБУ")
    nbu_rates = converter.scrape_nbu_rates()
    
    # 2. Курси API
    print("\n2️⃣  Ринкові курси (API)")
    api_rates = converter.get_rates('UAH')
    
    # 3. Порівняльна таблиця
    if nbu_rates and api_rates:
        print("\n" + "="*80)
        print("📈 ПОРІВНЯЛЬНА ТАБЛИЦЯ")
        print("="*80)
        print(f"{'Валюта':<10} {'НБУ':<12} {'API':<12} {'Різниця':<12} {'%':<10}")
        print("-"*80)
        
        for currency in ['USD', 'EUR', 'GBP']:
            if currency in nbu_rates and currency in api_rates:
                nbu = nbu_rates[currency]
                api = 1 / api_rates[currency]
                diff = api - nbu
                diff_pct = (diff / nbu) * 100
                
                indicator = "⚠️ " if abs(diff_pct) > 5 else "✅"
                print(f"{currency:<10} {nbu:<12.4f} {api:<12.4f} {diff:<12.4f} {diff_pct:>+9.2f}% {indicator}")
        
        print("="*80)


def main():
    """Головна функція"""
    print("\n" + "="*70)
    print("💱 РОЗШИРЕНИЙ КОНВЕРТЕР ВАЛЮТ З ВЕБ-СКРАПІНГОМ")
    print("="*70)
    print("\nІнтеграція веб-скрапінгу з попереднім проектом Currency Converter")
    
    try:
        # Запустити демонстрації
        demo_basic_scraping()
        demo_comparison()
        demo_full_analysis()
        
        print("\n" + "="*70)
        print("✅ Демонстрація завершена!")
        print("="*70)
        print("\n💡 Що було продемонстровано:")
        print("   ✓ Парсинг таблиць з веб-сторінок")
        print("   ✓ Обробка структурованих даних")
        print("   ✓ Порівняння даних з різних джерел")
        print("   ✓ Інтеграція скрапінгу з існуючим кодом")
        
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
    except ImportError as e:
        print("❌ Помилка: Необхідні бібліотеки не встановлені")
        print("Встановіть їх командою:")
        print("pip install beautifulsoup4 requests")
        exit(1)
    
    main()
