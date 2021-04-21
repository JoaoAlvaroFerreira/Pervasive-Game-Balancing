import requests
import overpy
import json
import pandas as pd
import datetime
from dateutil.parser import parse

#weather

def holiday_getter():
  url = "https://date.nager.at/api/v2/publicholidays/2021/PT"

  response = requests.request("GET", url)

  r = json.loads(response.text)
  print(r)


holiday_data = [{'date': '2021-01-01', 'localName': 'Ano Novo', 'name': "New Year's Day", 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-02-16', 'localName': 'Carnaval', 'name': 'Carnival', 'countryCode': 'PT', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Optional'}, {'date': '2021-04-02', 'localName': 'Sexta-feira Santa', 'name': 'Good Friday', 'countryCode': 'PT', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-04-04', 'localName': 'Domingo de Páscoa', 'name': 'Easter Day', 'countryCode': 'PT', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-04-25', 'localName': 'Dia da Liberdade', 'name': 'Freedom Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-05-01', 'localName': 'Dia do Trabalhador', 'name': 'Labour Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-06-01', 'localName': 'Dia dos Açores', 'name': 'Azores Day', 'countryCode': 'PT', 'fixed': True, 'global': False, 'counties': ['PT-20'], 'launchYear': None, 'type': 'Public'}, {'date': '2021-06-03', 'localName': 'Corpo de Deus', 'name': 'Corpus Christi', 'countryCode': 'PT', 'fixed': False, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-06-10', 'localName': 'Dia de Portugal, de Camões e das Comunidades Portuguesas', 'name': 'National Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-07-01', 'localName': 'Dia da Madeira', 'name': 'Madeira Day', 'countryCode': 'PT', 'fixed': True, 'global': False, 'counties': ['PT-30'], 'launchYear': None, 'type': 'Public'}, {'date': '2021-08-15', 'localName': 'Assunção de Nossa Senhora', 'name': 'Assumption Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-10-05', 'localName': 'Implantação da República', 'name': 'Republic Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-11-01', 'localName': 'Dia de Todos-os-Santos', 'name': 'All Saints Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-12-01', 'localName': 'Restauração da Independência', 'name': 'Restoration of Independence', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-12-08', 'localName': 'Imaculada Conceição', 'name': 'Immaculate Conception', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-12-25', 'localName': 'Natal', 'name': 'Christmas Day', 'countryCode': 'PT', 'fixed': True, 'global': True, 'counties': None, 'launchYear': None, 'type': 'Public'}, {'date': '2021-12-26', 'localName': 'Primeira Oitava', 'name': "St. Stephen's Day", 'countryCode': 'PT', 'fixed': True, 'global': False, 'counties': ['PT-30'], 'launchYear': None, 'type': 'Public'}]

def is_holiday(dt):
  
  d_truncated = datetime.datetime(dt.year, dt.month, dt.day)

  for obj in holiday_data:
    dateh = parse(obj['date'])
    if dt == dateh:
      return True
    
  return False
    



def weather_getter():
  url = "https://community-open-weather-map.p.rapidapi.com/weather"

  querystring = {"q":"Porto,pt","lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}

  headers = {
      'x-rapidapi-key': "0badc3df95mshb93f3d3be3cdaefp19e17fjsn15d54d650e2b",
      'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  print(response.text)

#overpass api
# fetch all ways and nodes
#result = api.query(querystring)

#for node in result.nodes:
 #   print("Name: %s" % node.tags.get("name", "n/a"))
  #  print("    Lat: %f, Lon: %f" % (node.lat, node.lon))

def worldpopapi():

  url= "https://www.worldpop.org/rest/data/pop/wpgp?iso3=PRT"
  response = requests.request("GET", url)

  r = json.loads(response.text)
  print(r['data'][0]['title'])

def worldpopapi_geotiff_get(country):

  if not pathlib.Path("Resources/Geotiff Files/"+country+".tif").exists():           

    country_code = coco.convert(names=country, to='ISO3')
    url= "https://www.worldpop.org/rest/data/pop/wpgp?iso3={}".format(country_code)
    response = requests.request("GET", url)
    data = json.loads(response.text)
    url_download = data['data'][len(data['data'])-1]['files'][0]
    tif = requests.get(url_download, allow_redirects=True)
    open("Resources/Geotiff Files/"+country+".tif", 'wb').write(tif.content)


def location_data_from_CSVs(latitude, longitude, buffer, demo):

  load_file = 'D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\CountryDistributionCSVs\{}.csv'.format(demo)
  df = pd.read_csv(load_file)
  locations_df = df.loc[(df['latitude'] > latitude - buffer) & (df['latitude'] < latitude+buffer) & (df['longitude'] > longitude - buffer) & (df['longitude'] < longitude+buffer)]
  return locations_df['population'].mean()


def location_data_from_Overpass(minlat, maxlat, minlon, maxlon, query):
 ###buffer => 0.01° = 1.11 km
  api = overpy.Overpass()
  
  querystring = """
    node["{}"]
      ({},{},{},{}); 
      out;
      """.format(query,minlat,minlon,maxlat,maxlon)

  result = api.query(querystring)

  return result.get_nodes()