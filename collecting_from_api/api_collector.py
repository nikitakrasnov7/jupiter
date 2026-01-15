# collecting_from_api/api_collector.py
import requests
import pandas as pd
import time
from typing import Dict, List
import os
import sys
import json

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import API_CONFIG

class APIDataCollector:
    def __init__(self, api_name: str):
        self.api_name = api_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'StudentDataCollector/1.0',
            'Accept': 'application/json'
        })

    def get_base_url(self) -> str:
        return API_CONFIG[self.api_name]['base_url']

    def get_api_key(self) -> str:
        return API_CONFIG[self.api_name]['api_key']

    def make_request(self, endpoint: str, params: Dict = None) -> Dict:
        url = f"{self.get_base_url()}{endpoint}"
        params = params or {}
        # У GNews параметр ключа называется 'apikey'
        params['apikey'] = self.get_api_key()
        
        print(f"  [DEBUG] Запрос: {url} | Params: {params.keys()}") # Не показываем сам ключ
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"  [ERROR] Статус: {response.status_code}")
                print(f"  [ERROR] Ответ: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] Ошибка сети: {e}")
            return {}

    def save_to_csv(self, data: List[Dict], filename: str):
        if not data:
            print("Нет данных для сохранения")
            return
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Данные сохранены в {filename}")
        print(f"Всего записей: {len(df)}")
        print("\nПример данных:")
        print(df[['title', 'published_at']].head().to_string())

class NewsDataCollector(APIDataCollector):
    def __init__(self):
        # Используем конфиг 'gnews'
        super().__init__('gnews')

    def collect_news_by_topics(self, topics: List[str]) -> List[Dict]:
        all_news = []
        print(f"Начинаем сбор через GNews API...")
        
        endpoint = API_CONFIG['gnews']['endpoints']['search']

        for topic in topics:
            print(f"\nТема: {topic}")
            
            params = {
                'q': topic,
                'lang': 'en',        # Ищем на английском
                'max': 5,            # Максимум 5 статей (у GNews лимит 100 всего)
                'sortby': 'publishedAt'
            }
            
            data = self.make_request(endpoint, params)
            
            # У GNews список статей лежит в 'articles'
            if 'articles' in data:
                articles = data['articles']
                parsed_articles = [self._parse_article(a, topic) for a in articles]
                all_news.extend(parsed_articles)
                print(f"  -> Найдено: {len(articles)}")
            else:
                print(f"  -> Странный ответ (нет ключа 'articles'): {data}")
            
            # Небольшая пауза (у GNews ограничение 1 запрос в секунду для free)
            time.sleep(1.1)

        return all_news
    
    def _parse_article(self, article: Dict, topic: str) -> Dict:
        # Парсим формат GNews
        source_data = article.get('source', {})
        return {
            'topic': topic,
            'title': article.get('title'),
            'description': article.get('description'),
            'url': article.get('url'),
            'published_at': article.get('publishedAt'),
            'source_name': source_data.get('name'),
            'source_url': source_data.get('url')
        }