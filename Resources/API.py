import requests
import overpy
import json

#weather
url = "https://community-open-weather-map.p.rapidapi.com/weather"

querystring = {"q":"Porto,pt","lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}

headers = {
    'x-rapidapi-key': "0badc3df95mshb93f3d3be3cdaefp19e17fjsn15d54d650e2b",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

#response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)

#overpass api

api = overpy.Overpass()

latitude = 41.2530891
longitude = -8.6695254
querystring = """
   node["public_transport"]
  ({},{},{},{}); 
out;
    """.format(latitude-.01,longitude-.01,latitude+.01,longitude+.01)
# fetch all ways and nodes
#result = api.query(querystring)

#for node in result.nodes:
 #   print("Name: %s" % node.tags.get("name", "n/a"))
  #  print("    Lat: %f, Lon: %f" % (node.lat, node.lon))

#worldpopapi

url= "https://www.worldpop.org/rest/data/pop/wpgp?iso3=PRT"
response = requests.request("GET", url)

r = json.loads(response.text)
print(r['data'][0]['title'])