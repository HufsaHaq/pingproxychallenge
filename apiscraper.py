import threading
import requests
import sys
import json
import random
import time

def start_scraping_run(team_id: str) -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={team_id}")

    if r.status_code != 200:
        print(r.json())
        print("Failed to start scraping run")
        sys.exit(1)

    return r.json()["data"]["scraping_run_id"]


THREAD_COUNT = 100
TARGET = 25000
RUN_ID = ""
#run_ID = start_scraping_run('bace025d-120a-11f0-aaf0-0242ac120002')
min_year = 50000
max_year = 0
make_dict = {}
total = 0
mode = 0
store = []

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
    for i in range(THREAD_COUNT):
        threads.append(threading.Thread(target=lambda:get_data(ENDPOINT + str(int(10*i*(TARGET/THREAD_COUNT))), token)))
    for thread in threads:
        thread.start()
    
    for t in threads:
        t.join()

    process_data(store)
    print({"min_year": min_year,"max_year": max_year,"avg_price": total/TARGET,"mode_make": mode})

    
        

def get_data(endpoint, key):
    users =["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36","Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"]
    
    for i in range(10):
        success = False
        while not success:
            number = random.randint(0,2)
            response = requests.get(endpoint, 
                headers={
                    "Authorization": f"Bearer {key}",
                    "User-Agent": users[number]
                })
            status = response.status_code
            response = response.content
            response = response.decode("utf-8")
            response = json.loads(response)
            print(response)
            if status != 429:
                success = True
                store.append(response["data"])
            else:
                print(response)
                time.sleep(2)
def process_data(store):
    global min_year, max_year, make_dict, total, mode
    for response in store:
        for car in response:
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
            
    
    

run_ID = start_scraping_run('bace025d-120a-11f0-aaf0-0242ac120002')
#run_ID ='d8559512-120b-11f0-b749-0242ac120003'
print(scraper(run_ID))
mode = max(make_dict, key=make_dict.get)