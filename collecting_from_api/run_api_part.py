import sys
import os

# --- Настройка путей ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
# -----------------------

# ВАЖНО: При запуске через "python -m" нужно указывать полный путь
from collecting_from_api.api_collector import NewsDataCollector
from utils.config import TOPICS

def main():
    # 1. Создаем коллектор
    news_collector = NewsDataCollector()
    
    # 2. Собираем новости по темам из конфига
    news_data = news_collector.collect_news_by_topics(TOPICS)
    
    # 3. Сохраняем в CSV
    output_filename = os.path.join(current_dir, 'data', 'news_data.csv')
    
    news_collector.save_to_csv(
        news_data,
        output_filename
    )

if __name__ == "__main__":
    main()