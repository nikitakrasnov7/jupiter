import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from collecting_from_api.api_collector import NewsDataCollector
from utils.config import TOPICS

def main():
    news_collector = NewsDataCollector()
    
    news_data = news_collector.collect_news_by_topics(TOPICS)
    output_filename = os.path.join(current_dir, 'data', 'news_data.csv')
    
    news_collector.save_to_csv(
        news_data,
        output_filename
    )

if __name__ == "__main__":
    main()