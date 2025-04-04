#LIBRARIES
import requests
import json
import os 
import numpy as np
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import base64
import subprocess


#OS
base_dir = os.path.dirname(os.path.abspath(__file__))
path_file = os.path.join(base_dir,'spacemoives.pdf')

#API
apikey = "aOe1emfgmlMK8SebzLaVeQcNjHX3LuOYHuoptRLC"

def nasa_opod():
    base_url = f"https://api.nasa.gov/planetary/apod?api_key={apikey}"
    response = requests.get(base_url)
    data = response.json()
    print(data)

def nasa_asteroid():
    base_url2 = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-08-07&end_date=2024-08-08&api_key={apikey}"
    response = requests.get(base_url2)
    data = response.json()
    asteroids = []

    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            asteroids.append({
                'name': asteroid['name'],
                'id': asteroid['id'],
                'approach_date': date,
                'velocity_km_h': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                'miss_distance_km': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
                'diameter_min': asteroid['estimated_diameter']['meters']['estimated_diameter_min'],
                'diameter_max': asteroid['estimated_diameter']['meters']['estimated_diameter_max'],
                'is_hazardous': asteroid['is_potentially_hazardous_asteroid']
            })

    df = pd.DataFrame(asteroids)
    print(df)

def nasa_natifications():
    base_url3 = f"https://api.nasa.gov/DONKI/notifications?startDate=2024-05-01&endDate=2024-05-08&type=all&api_key={apikey}"
    response = requests.get(base_url3) 
    print(json.dumps(response.json(), indent = 4))


def nasa_ssc():
    command = (
        'cd %USERPROFILE%\\Downloads && '
        'if exist sscws rmdir /S /Q sscws && '
        'mkdir sscws && '
        'cd sscws && '
        'python -m venv sscws && '
        'sscws\\Scripts\\activate.bat && '
        'pip install sscws matplotlib && '
        'curl -sOJ "https://sscweb.gsfc.nasa.gov/WS/sscr/2/observatories/iss/clientLibraryExample/sscwspy" && '
        'python sscws_iss_example.py'
    )
    subprocess.run(command, shell=True)

    #Selenium
def letterboxd():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,3000')

    driver = webdriver.Chrome(options=options)
    driver.get("https://letterboxd.com/tarokhnstuff/list/space/by/rating/")
    time.sleep(2)

    scroll_pause = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(2)

    #pdf save
    pdf = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True,
        "landscape": False,
        "paperWidth": 8.27,
        "paperHeight": 11.69,
        "marginTop": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "marginRight": 0,
    })

    with open(path_file, "wb") as f:
        f.write(base64.b64decode(pdf['data']))

    driver.quit()

nasa_asteroid()