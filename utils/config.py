

import os


API_CONFIG = {
    'gnews': {
        'base_url': 'https://gnews.io/api/v4',
        'api_key': os.getenv('GNEWS_API_KEY'),
        'endpoints': {
            'search': '/search',
            'top': '/top-headlines'
        }
    }
}

TOPICS = [
    'Data Science',
    'Python',
    'Artificial Intelligence',
    'Machine Learning',
    'SpaceX'
]