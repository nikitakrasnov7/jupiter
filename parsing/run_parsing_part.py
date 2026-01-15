# parsing/run_parsing_part.py
import sys
import os

# Трюк с путями, чтобы всё работало
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsing.web_parser import GitHubParser

def main():
    # 1. Создаем парсер
    parser = GitHubParser()
    
    # 2. Запускаем сбор
    data = parser.parse_trending()
    
    # 3. Сохраняем (путь относительно корня проекта)
    # Сохраним в ту же папку data, где и новости, но с другим именем
    output_path = os.path.join('parsing', 'data', 'github_trending.csv')
    
    parser.save_to_csv(data, output_path)

if __name__ == "__main__":
    main()