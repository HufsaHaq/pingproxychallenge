import requests
from bs4 import BeautifulSoup

def solution():
    price_total = 0
    max_year = 0
    min_year = 10000000
    make_list = []

    for num in range(99999):
        URL = f"https://scrapemequickly.com/cars/static/{num}?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        year = soup.find("p", class_ = "year")
        price = soup.find("p", class_ = "price")
        make = soup.find("h2", class_ = "title")
        year_lst = year.text.split()
        price_lst = price.text.split()
        make_lst = make.text.split()
        if max_year < int(year_lst[1]):
            max_year = int(year_lst[1])
        price_total += int(price_lst[1].replace('$',''))
        
        make = make_lst[0].replace(',','')
        if min_year > int(year_lst[1]):
            min_year = int(year_lst[1])

        for i in make_list:
            if make == i[0]:
                i[1] += 1
                break
            else:
                notfound = True
        if notfound:
            make_list.append([make, 1])

    temp = 0
    mode = ''
    for i in make_list:
        if i[1] > temp:
            temp = i[1]
            mode = i[0]

    return {
        "min_year": min_year,
        "max_year": max_year,
        "avg_price": price_total/99999,
        "mode_make": mode
    }


