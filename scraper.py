import requests
from bs4 import BeautifulSoup
info = []
for num in range(100000):
    URL = f"https://scrapemequickly.com/cars/static/{num}?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    info.append(soup)

    print(soup)