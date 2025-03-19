#LIBRARIES
import requests
import json
import os 
import tkinter
import numpy as np
import pandas as pd

#API
apikey = "aOe1emfgmlMK8SebzLaVeQcNjHX3LuOYHuoptRLC"

#try
base_url = f"https://api.nasa.gov/planetary/apod?api_key={apikey}"
response = requests.get(base_url)
print(response.text)

