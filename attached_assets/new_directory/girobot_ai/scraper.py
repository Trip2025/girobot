# attached_assets/girobot_ai/scraper.py

import requests
from bs4 import BeautifulSoup

def fetch_stage_html(stage_num):
    """
    Fetch the raw HTML of a given Giro d'Italia stage result page from CyclingNews.
    """
    url = f"https://www.cyclingnews.com/races/giro-d-italia-2025/stage-{stage_num}/results/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[Error] Failed to fetch Stage {stage_num}: HTTP {response.status_code}")
            return None

        return BeautifulSoup(response.text, 'html.parser')

    except requests.RequestException as e:
        print(f"[Error] Network problem: {e}")
        return None
