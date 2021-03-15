import json
import csv
import names
import requests
from Model.player import Player, PlayerLocationInfo, Demographic, Personality
import random
import pandas as pd
import overpy
import country_converter as coco
import pathlib


def generateDemo(player):


    df = pd.read_csv('Resources/quality_of_life.csv')
    
   
    latitude = random.uniform(40,60)
    longitude = random.uniform(-10,15)
    querystring = """https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=14&accept-language=en
    """.format(latitude,longitude)
    response = requests.request("GET", querystring)

    r = json.loads(response.text)
    print(r)
    api = overpy.Overpass()
    
    if 'address' in r:
        
        country_df = df[df['Country']==r['address']['country']]
        print(r['address']['country'])

        querystring = """
        node["tourism"]
        ({},{},{},{}); 
        out;
            """.format(latitude-.01,longitude-.01,latitude+.01,longitude+.01)
        # fetch all ways and nodes
        result = api.query(querystring)
      
        print("AAAAAAAAAA")
        print(len(result.get_nodes()))
        print("CCCCCCCCCCC")
        for node in result.nodes:
            print("Name: %s" % node.tags.get("name", "n/a"))
           
  
       
        #worldpopapi

        if not pathlib.Path("Resources/Geotiff Files/"+r['address']['country']+".tif").exists():           

            country_code = coco.convert(names=r['address']['country'], to='ISO3')
            url= "https://www.worldpop.org/rest/data/pop/wpgp?iso3={}".format(country_code)
            response = requests.request("GET", url)
            data = json.loads(response.text)
            url_download = data['data'][len(data['data'])-1]['files'][0]
            tif = requests.get(url_download, allow_redirects=True)
            open("Resources/Geotiff Files/"+r['address']['country']+".tif", 'wb').write(tif.content)

        


    #player.Demographic = 

    

    
    

def generatePlayer():
    player = Player(names.get_full_name())
    print("Name: "+player.name)
    generateDemo(player)

