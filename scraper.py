import requests
from bs4 import BeautifulSoup
info = []
for num in range(100000):
    URL = f"https://scrapemequickly.com/cars/static/{num}?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    year = soup.find("p", class_ = "year")
    price = soup.find("p", class_ = "price")
    make = soup.find("h2", class_ = "title")
    start = year.text.find("<strong>") + 1
    end = year.text.find("</strong>")
    print(year[start:end])
    print(price.text)
    print(make.text)
    inputt = input()
    info.append(soup)
