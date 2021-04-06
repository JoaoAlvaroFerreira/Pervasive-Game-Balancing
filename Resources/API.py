import requests
import overpy
import json
import pandas as pd

#weather

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


def location_data_from_Overpass(latitude, longitude, buffer, query):
 ###buffer => 0.01° = 1.11 km
  api = overpy.Overpass()
  
  querystring = """
    node["{}"]
      ({},{},{},{}); 
      out;
      """.format(query,latitude-buffer,longitude-buffer,latitude+buffer,longitude+buffer)

  result = api.query(querystring)

  return len(result.get_nodes())/111