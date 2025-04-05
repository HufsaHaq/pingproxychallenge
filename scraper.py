import requests
from bs4 import BeautifulSoup
import threading

total = 0
make_dict = {}
max_year = 0
min_year = 100000000

def scraper(num):
    global total, make_dict, max_year, min_year
    URL = f"https://scrapemequickly.com/cars/static/{num}?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6"
    page = requests.get(URL)
    if page.status_code == 429:
        scraper(num)
        return
    soup = BeautifulSoup(page.content, "html.parser")
    year = soup.find("p", class_ = "mt-4 text-2xl year")
    price = soup.find("p", class_ = "mt-4 text-2xl price")
    make = soup.find("h2", class_ = "title")
    year_lst = year.text.split()
    price_lst = price.text.split()
    make_lst = make.text.split()
    if max_year < int(year_lst[1]):
        max_year = int(year_lst[1])
    total += int(price_lst[1].replace('$',''))
    
    make = make_lst[0].replace(',','')
    if min_year > int(year_lst[1]):
        min_year = int(year_lst[1])
    
    if make not in make_dict:
        make_dict[make] = 0
    
    make_dict[make] += 1

def use_threading():
    global total, make_dict, max_year, min_year
    threads = []
    count = 25000
    for i in range(0, count):
        thread = threading.Thread(target=scraper, args=(i,))
        threads.append(thread)
        thread.start()

        if len(threads) >= 3:
            for t in threads:
                t.join()
            threads = []
        
    for t in threads:
        t.join()

    mode = max(make_dict, key=make_dict.get)

    print({"min_year": min_year,"max_year": max_year,"avg_price": total/count,"mode_make": mode})

    return {
        "min_year": min_year,
        "max_year": max_year,
        "avg_price": total/count,
        "mode_make": mode
    }

use_threading()

scraper(0)