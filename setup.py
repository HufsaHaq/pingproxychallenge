import requests
import sys
import json
from scraper import use_threading
from apiscraper import scraper

def create_team(team_name: str, team_email: str) -> str:
    r = requests.post(
        "https://api.scrapemequickly.com/register",
        data=json.dumps({"team_name": team_name, "team_email": team_email}),
        headers={"Content-Type": "application/json"}
    )

    if r.status_code != 200:
        print(r.json())
        print("Failed to create a team")
        sys.exit(1)

    return r.json()["data"]["team_id"]

def start_scraping_run(team_id: str) -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={team_id}")

    if r.status_code != 200:
        print(r.json())
        print("Failed to start scraping run")
        sys.exit(1)

    return r.json()["data"]["scraping_run_id"]

def submit(answers: dict, scraping_run_id: str) -> bool:
    r = requests.post(
        f"https://api.scrapemequickly.com/cars/solve?scraping_run_id={scraping_run_id}",
        data=json.dumps(answers),
        headers={"Content-Type": "application/json"}
    )

    if r.status_code != 200:
        print(r.json())
        print("Failed to submit answers")
        return False

    return True
run_ID = start_scraping_run('bace025d-120a-11f0-aaf0-0242ac120002')
#ans_dict = {'min_year': 1930, 'max_year': 2025, 'avg_price': int(24033.03512), 'mode_make': 'Chevrolet'}
#submit(use_threading(run_ID) ,run_ID)
submit(scraper(run_ID), run_ID)