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
import Resources.utils as utils


def generateDemo(player, latitude, longitude, r ):


    df = pd.read_csv('D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\quality_of_life.csv')
    


    
    if 'address' in r and r['address']['country']!= "France" and r['address']['country']!= "Czechia":

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
        
        
        return Demographic(age, gender, wealth) 
         
def generatePersonality(demo):
    #balanced, competitive, relaxed

    #Concentration,Competitiveness,PlayerSkills,UserControl,ClearGoals,Feedback,Immersion,SocialInteraction,Free2Play, PersonalityType
    rand_var = random.randint(0,3)
    if rand_var == 0:
        PersonalityType = "Balanced"
    elif rand_var == 1:
        PersonalityType = "Competitive"
    elif rand_var == 2:
        PersonalityType = "Relaxed"
    elif rand_var == 3:
        if demo.Age == "Youth" or demo.Age == "Kid":
            PersonalityType = "Competitive"
        elif demo.Age == "Elderly":
            PersonalityType = "Relaxed"
        else: PersonalityType = "Balanced"

    if PersonalityType == "Balanced":
     return Personality(random.randint(2,4),random.randint(2,4),random.randint(2,4),random.randint(2,4),random.randint(2,4),random.randint(2,4),random.randint(2,4),random.randint(2,4),random.randint(2,4),"Balanced")
    
    if PersonalityType == "Competitive":
     return Personality(random.randint(3,5), random.randint(4,5), random.randint(3,5), random.randint(3,5), random.randint(1,4), random.randint(1,5), random.randint(1,3), random.randint(1,3), random.randint(3,5), "Competitive")

    if PersonalityType == "Relaxed":
     return Personality(random.randint(1,3), random.randint(1,3), random.randint(1,4), random.randint(2,4), random.randint(3,5), random.randint(3,5), random.randint(4,5), random.randint(4,5), random.randint(1,3), "Relaxed")






def generatePlayer():

    #minLat, maxLat, minLon, maxLon
    #41.1042, 41.2788,-8.6627, -8.4361
    player_batch = []
     ##iberian peninsula
    latitude = random.uniform(41.1042, 41.2788)
    print("Latitude:")
    print(latitude)
    longitude = random.uniform(-8.6627, -8.4361)
    print("Longitude:")
    print(longitude)
    querystring = """https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=14&accept-language=en
    """.format(latitude,longitude)
    response = requests.request("GET", querystring)
    
    r = json.loads(response.text)

    
    if 'address' in r and r['address']['country']!= "France" and r['address']['country']!= "Czechia":
        for _ in range(0,10):
        
            player = Player(names.get_full_name())

            rand_mod_a = random.uniform(-0.2,0.2)
            rand_mod_b  = random.uniform(-0.2,0.2)
            player.PlayerLocationInfo = PlayerLocationInfo(latitude+rand_mod_a, longitude+rand_mod_b, r['address']['country'])
            player.Demographic = generateDemo(player, latitude+rand_mod_a, longitude+rand_mod_b, r)
            
            player.Personality = generatePersonality(player.Demographic)
            player_batch.append(player)
    

    return player_batch
    
