import pandas as pd
import matplotlib.pyplot as plt
# Import necessary packages
import os 
import folium
from folium import plugins
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import earthpy as et
import webbrowser


from IPython.display import display
from folium import plugins
from folium.plugins import HeatMap

# Import data from EarthPy
data = et.data.get_data('colorado-flood')

# Set working directory to earth-analytics
os.chdir(os.path.join(et.io.HOME, 'earth-analytics'))

def plotplot(players):
    LDN_COORDINATES = (40.2, -4)
    myMap = folium.Map(location=LDN_COORDINATES, zoom_start=5)

  
    # Add marker for Boulder, CO
    for player in players:
        folium.Marker(
            location=[player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
            popup='Gameplay Moment', # pop-up label for the marker
            icon=folium.Icon()
        ).add_to(myMap)


    myMap.save("map.html")
    webbrowser.open("map.html")

def heatmap_plot(players):

    LDN_COORDINATES = (40.2, -4)
    myMap = folium.Map(location=LDN_COORDINATES, zoom_start=5)

    load_file = 'D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\CountryDistributionCSVs\PRT_population.csv'
    df_acc = pd.read_csv(load_file)
    # Add marker for Boulder, CO
    for player in players:
        folium.Marker(
            location=[player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
            popup='Gameplay Moment', # pop-up label for the marker
            icon=folium.Icon()
        ).add_to(myMap)


    df_acc['latitude'] = df_acc['latitude'].astype(float)
    df_acc['longitude'] = df_acc['longitude'].astype(float)

    # Filter the DF for rows, then columns, then remove NaNs
    heat_df = df_acc[df_acc['population']>3] # Reducing data size so it runs faster
    heat_df = heat_df[['latitude', 'longitude']]
    heat_df = heat_df.dropna(axis=0, subset=['latitude','longitude'])

    # List comprehension to make out list of lists
    heat_data = [[row['latitude'],row['longitude']] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(myMap)

    myMap.save("map.html")
    webbrowser.open("map.html")


         
def plot_players(players):
    print("PLAYERS LENGTH: {}".format(len(players)))
    lats = []
    longs = []
    for player in players:
        lats.append(player.PlayerLocationInfo.latitude)
        longs.append(player.PlayerLocationInfo.longitude)

    df = pd.DataFrame([lats, longs]).T
    df.columns=['Latitude', 'Longitude']
    ruh_m = plt.imread('Resources/map.png')
    BBox = (-10.371, 3.735, 35.443, 44.402)
    fig, ax = plt.subplots(figsize = (8,7))
    
    ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha= 1, c='b', s=10)
    ax.set_title('Iberian Peninsula Players')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()


def plot_player_moments(moments):
 
    lats = []
    longs = []
    for moment in moments:
        lats.append(moment.latitude)
        longs.append(moment.longitude)

    df = pd.DataFrame([lats, longs]).T
    df.columns=['Latitude', 'Longitude']
    ruh_m = plt.imread('Resources/map.png')
    BBox = (-10.371, 3.735, 35.443, 44.402)
    fig, ax = plt.subplots(figsize = (8,7))
    
    ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha= 1, c='b', s=10)
    ax.set_title('Iberian Peninsula Moments')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()
