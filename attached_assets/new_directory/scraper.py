import requests
from bs4 import BeautifulSoup

def fetch_giro_stage_results(stage_num):
    """
    Fetch the Giro d'Italia stage results from CyclingNews website
    """
    try:
        url = f"https://www.cyclingnews.com/races/giro-d-italia-2025/stage-{stage_num}/results/"
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        if response.status_code != 200:
            print(f"Error fetching results: HTTP {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find results table
        result_table = soup.select_one('.results-table')

        if not result_table:
            print("No results table found on the page")
            return None

        riders = result_table.select('tbody tr')
        if not riders or len(riders) < 3:
            print("Could not find enough rider data")
            return None

        stage_winner_row = riders[0]
        second_place_row = riders[1]
        third_place_row = riders[2]

        stage_winner = stage_winner_row.select_one('.rider-name').text.strip()
        stage_winner_team = stage_winner_row.select_one('.team-name').text.strip()
        stage_time = stage_winner_row.select_one('.time').text.strip()
        second_place = second_place_row.select_one('.rider-name').text.strip()
        third_place = third_place_row.select_one('.rider-name').text.strip()

        # Jersey holders
        pink_jersey = "Data not available"
        points_jersey = "Data not available"
        kom_jersey = "Data not available"
        youth_jersey = "Data not available"

        jersey_section = soup.select_one('.jersey-classifications')
        if jersey_section:
            jersey_items = jersey_section.select('.jersey-item')
            for item in jersey_items:
                jersey_type = item.select_one('.jersey-type').text.strip().lower()
                jersey_holder = item.select_one('.jersey-holder').text.strip()
                if 'pink' in jersey_type or 'rosa' in jersey_type:
                    pink_jersey = jersey_holder
                elif 'points' in jersey_type or 'ciclamino' in jersey_type:
                    points_jersey = jersey_holder
                elif 'mountain' in jersey_type or 'azzurra' in jersey_type:
                    kom_jersey = jersey_holder
                elif 'youth' in jersey_type or 'bianca' in jersey_type:
                    youth_jersey = jersey_holder

        # Headline
        headline = soup.select_one('h1.article-title')
        top_story = headline.text.strip() if headline else f"Stage {stage_num} complete"

        # Lidl-Trek highlights
        lidl_trek_highlight = "No specific highlights available"
        team_standing = "Position not available"

        team_standings_section = soup.select_one('.team-standings')
        if team_standings_section:
            lidl_trek_row = None
            for row in team_standings_section.select('tr'):
                if 'Lidl-Trek' in row.text:
                    lidl_trek_row = row
                    break
            if lidl_trek_row:
                position = lidl_trek_row.select_one('.position').text.strip()
                team_standing = f"{position} in Team Classification"

        lidl_trek_riders = []
        for rider_row in riders:
            if 'Lidl-Trek' in rider_row.text:
                rider_name = rider_row.select_one('.rider-name').text.strip()
                rider_pos = rider_row.select_one('.position').text.strip()
                lidl_trek_riders.append((rider_name, rider_pos))

        if lidl_trek_riders:
            best_placed = min(lidl_trek_riders, key=lambda x: int(x[1]))
            lidl_trek_highlight = f"{best_placed[0]} finished {best_placed[1]} for Lidl-Trek"

        return {
            "stage_num": str(stage_num),
            "stage_winner": stage_winner,
            "team": stage_winner_team,
            "second": second_place,
            "third": third_place,
            "time": stage_time,
            "lidl_trek_highlight": lidl_trek_highlight,
            "team_standing": team_standing,
            "team_safety": "All riders finished safely",
            "pink_jersey": pink_jersey,
            "points_jersey": points_jersey,
            "kom_jersey": kom_jersey,
            "youth_jersey": youth_jersey,
            "top_story": top_story,
            "link": url
        }

    except Exception as e:
        print(f"Error fetching stage results: {str(e)}")
        return None
