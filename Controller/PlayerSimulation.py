import json
import names
import requests
from Model.player import Player, PlayerLocationInfo, Demographic, Personality
import random
import sys
sys.path.append('../')




def generateDemo():
    latitude = random.uniform(40,60)
    longitude = random.uniform(-10,15)
    querystring = """https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=14
    """.format(latitude,longitude)
    response = requests.request("GET", querystring)

    r = json.loads(response.text)
    print(r['address']['country'])
    

def generatePlayer():
    player = Player(names.get_full_name())
    print("Name: "+player.name)
    generateDemo()

