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
    year_lst = year.text.split()
    price_lst = price.text.split()
    make_lst = make.text.split()
    #print((int(year_lst[1]),int(price_lst[1].replace('$','')),make_lst[1],make_lst[0].replace(',','')))
    info.append((int(year_lst[1]),int(price_lst[1].replace('$','')),make_lst[1],make_lst[0].replace(',','')))
