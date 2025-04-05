import requests
from bs4 import BeautifulSoup
import threading

total = 0
make_dict = {}
max_year = 0
min_year = 100000000

def scraper(num):
    global total, make_dict, max_year, min_year
    URL = f"https://scrapemequickly.com/all_cars?scraping_run_id=d8559512-120b-11f0-b749-0242ac120003"
    page = requests.get(URL)
    if page.status_code == 429:
        scraper(num)
        return
    
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup = soup1.find("div", class_="flex flex-wrap gap-2 justify-center items-center justify-items-center bg-[#F2F3F8] p-4 px-50")
    # Find all cars
    print(soup)
    cars = soup.find_all("div", class_="car min-w-80")
    print(cars[0])
    for car in cars:
        year = car.find("p", class_="year")
        price = car.find("p", class_="price")
        make = car.find("h2", class_="title")

        print(car)
        print(year)
        print(price)
        print(make)
        
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
    count = 250  # Set the number of cars you're scraping
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

result =use_threading()
print(result)