import threading
import requests
import sys
import json
import random
import time
from itertools import cycle

THREAD_COUNT = 20
TARGET = 25000
RUN_ID = ""
#run_ID = start_scraping_run('bace025d-120a-11f0-aaf0-0242ac120002')
min_year = 50000
max_year = 0
make_dict = {}
total = 0
mode = 0
store = []

proxy_pool = cycle([
    'http://pingproxies:scrapemequickly@194.87.135.1:9875',    
    'http://pingproxies:scrapemequickly@194.87.135.2:9875',
    'http://pingproxies:scrapemequickly@194.87.135.3:9875',
    'http://pingproxies:scrapemequickly@194.87.135.4:9875',
    'http://pingproxies:scrapemequickly@194.87.135.5:9875',
])


def start_scraping_run(team_id: str) -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={team_id}")

    if r.status_code != 200:
        print(r.json())
        print("Failed to start scraping run")
        sys.exit(1)

    return r.json()["data"]["scraping_run_id"]


def get_key(id):
    ENDPOINT = f"https://api.scrapemequickly.com/get-token?scraping_run_id={id}"
    response = requests.get(ENDPOINT).content.decode("utf-8")
    response = json.loads(response)
    return response["token"]
    
def scraper(run_id):
    global store
    token = get_key(run_id)
    ENDPOINT = f"https://api.scrapemequickly.com/cars/test?scraping_run_id={run_id}&per_page=25&start=" #CONCAT THING AT END PLS
    threads = []

    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 0 , token, False)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 1 , token, False)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 2 , token, False)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 3 , token, False)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 4 , token, False)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 5 , token, False)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 6 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 7 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 8 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 9 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 10 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 11, token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 12 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 13 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 14 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 15 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 16 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 17 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 19 , token, True)))
    threads.append(threading.Thread(target=lambda:get_data(ENDPOINT, 18 , token, True)))
    for thread in threads:
        thread.start()
    
    for t in threads:
        t.join()

    result = process_data(store)
    print(result)
    print(len(store))
    return (result)

    
        
store_lock = threading.Lock()
def get_data(endpoint, index , key, is_proxy):
    global store
    users =["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36","Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"]
    
    for i in range(int(TARGET/(THREAD_COUNT*25))):
        success = False
        while not success:
            number = random.randint(0,2)
            #print(str((index*6250)+(25*i)))
            print('i',i)
            print('index',index)
            proxy = next(proxy_pool)
            response = requests.get(endpoint + str((index*1250)+(25*i)), 
                headers={
                    "Authorization": f"Bearer {key}",
                    "User-Agent": users[number]
                },
                proxies = None if not is_proxy else {
                    'http' : proxy,    
                    'https' : proxy
                } 
            )
            
            status = response.status_code
            response = response.content
            response = response.decode("utf-8")
            response = json.loads(response)
            if status != 429:
                success = True
                with store_lock:
                    for j in range(25):
                        store.append(response["data"][j])
            else:
                print(status)

def process_data(store):
    global min_year, max_year, make_dict, total, mode
    for car in store:
        total += car["price"]
        if car["year"]> max_year:
            max_year = car["year"]
        if car["year"] < min_year:
            min_year = car["year"]
            
        if car["make"] not in make_dict:
            make_dict[car["make"]] = 0
    
        make_dict[car["make"]] += 1
    
    mode = max(make_dict, key=make_dict.get)
    return {
        "min_year": min_year,
        "max_year": max_year,
        "avg_price": int(total/TARGET),
        "mode_make": mode
    }
            
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
#run_ID ='d8559512-120b-11f0-b749-0242ac120003'
#print(scraper(run_ID))
#mode = max(make_dict, key=make_dict.get)
submit(scraper(run_ID), run_ID)