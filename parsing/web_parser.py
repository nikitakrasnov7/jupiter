# parsing/web_parser.py
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

class GitHubParser:
    def __init__(self):
        self.base_url = "https://github.com/trending"
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Настройка Google Chrome"""
        chrome_options = Options()
        # --headless означает, что браузер запустится без окна (фоновый режим)
        # Если хотите видеть браузер, закомментируйте строку ниже
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Маскируемся под обычного пользователя
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        print("Запуск браузера Chrome...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse_trending(self):
        """Сбор данных о трендовых репозиториях"""
        print(f"Переходим на сайт: {self.base_url}")
        repos_data = []
        
        try:
            self.driver.get(self.base_url)
            
            # Ждем, пока загрузится список репозиториев (блок article)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            
            # Получаем HTML страницы и парсим через BeautifulSoup (это быстрее и надежнее)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Находим все блоки с репозиториями
            repo_list = soup.find_all('article', class_='Box-row')
            print(f"Найдено репозиториев на странице: {len(repo_list)}")

            for repo in repo_list:
                try:
                    # 1. Название и ссылка
                    h2_tag = repo.find('h2')
                    link_tag = h2_tag.find('a')
                    relative_link = link_tag['href'] # /author/repo
                    full_link = f"https://github.com{relative_link}"
                    # Удаляем лишние пробелы и переносы строк
                    name = link_tag.text.strip().replace('\n', '').replace(' ', '')
                    
                    # 2. Описание (может не быть)
                    desc_tag = repo.find('p', class_='col-9')
                    description = desc_tag.text.strip() if desc_tag else "Нет описания"
                    
                    # 3. Язык программирования (может не быть)
                    lang_tag = repo.find('span', itemprop='programmingLanguage')
                    language = lang_tag.text.strip() if lang_tag else "Unknown"
                    
                    # 4. Звезды (Всего)
                    # Ищем ссылку, которая ведет на /stargazers
                    stars_tag = repo.find('a', href=f"{relative_link}/stargazers")
                    stars = stars_tag.text.strip() if stars_tag else "0"

                    repos_data.append({
                        'name': name,
                        'language': language,
                        'stars': stars,
                        'description': description,
                        'url': full_link
                    })
                    
                except Exception as e:
                    print(f"Ошибка при парсинге элемента: {e}")
                    continue

        except Exception as e:
            print(f"Глобальная ошибка парсинга: {e}")
        finally:
            self.close()
            
        return repos_data

    def save_to_csv(self, data, filename):
        if not data:
            print("Нет данных для сохранения")
            return
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nДанные успешно сохранены в: {filename}")
        print("-" * 30)
        print(df.head().to_string())

    def close(self):
        if self.driver:
            self.driver.quit()
            print("Браузер закрыт.")