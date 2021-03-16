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
import Resources.API as local_api


def generateDemo(player):


    df = pd.read_csv('Resources/quality_of_life.csv')
    
   ##iberian peninsula
    latitude = random.uniform(36,43.8)
    print("Latitude:")
    print(latitude)
    longitude = random.uniform(-9.6,3.2)
    print("Longitude:")
    print(longitude)
    querystring = """https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=14&accept-language=en
    """.format(latitude,longitude)
    response = requests.request("GET", querystring)

    r = json.loads(response.text)
    print(r)

    
    if 'address' in r and r['address']['country']!= "France":

        country_code = coco.convert(names=r['address']['country'], to='ISO3')
        country_df = df[df['Country']==r['address']['country']]

        print(country_df)
     
        #print(local_api.location_data_from_Overpass(latitude, longitude, 0.01, "tourism"))
    
    
        pop = local_api.location_data_from_CSVs(latitude, longitude, 0.01, "{}_population".format(country_code))
        men_p = local_api.location_data_from_CSVs(latitude, longitude, 0.01, "{}_men".format(country_code))
        
        gender_rng = random.uniform(0,pop)
        if(gender_rng < men_p):
            gender = "Male"
        else: gender = "Female"

        kid = local_api.location_data_from_CSVs(latitude, longitude, 0.01, "{}_children".format(country_code))
        youth = local_api.location_data_from_CSVs(latitude, longitude, 0.01, "{}_youth".format(country_code))
        elderly = local_api.location_data_from_CSVs(latitude, longitude, 0.01, "{}_elderly".format(country_code))

        age_rng = random.uniform(0,pop)
        
        if(age_rng < kid):
            age = "Kid"
        elif(age_rng < kid+youth and age_rng>kid):
            age = "Youth"
        elif(age_rng < kid+youth+elderly and age_rng>kid+youth):
            age = "Elderly"
        else: age = "Adult"

        wealth = country_df.iloc[0]['Purchasing Power Index']/country_df.iloc[0]['Cost of Living Index'] + random.uniform(-0.5,0.5)
        print("PLAYER DEMO: Age, Gender, Wealth")
        print(age)
        print(gender)
        print(wealth)
        player.demographic = Demographic(age, gender, wealth)
         
    
    

def generatePlayer():
    player = Player(names.get_full_name())
    print("Name: "+player.name)
    generateDemo(player)

