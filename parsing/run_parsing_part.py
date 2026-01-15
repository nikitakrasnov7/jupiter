import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsing.web_parser import GitHubParser

def main():
    parser = GitHubParser()
    
    data = parser.parse_trending()
    
    output_path = os.path.join('parsing', 'data', 'github_trending.csv')
    
    parser.save_to_csv(data, output_path)

if __name__ == "__main__":
    main()