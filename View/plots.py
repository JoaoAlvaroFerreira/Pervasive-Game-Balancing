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




###disregard this one
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

def heatmap_moments(moments):
    print("hello")
    print(len(moments))

    LDN_COORDINATES = (41.15,-8.6)
    myMap = folium.Map(location=LDN_COORDINATES, zoom_start=10)

    d = {'latitude': [], 'longitude': []}
    df_acc = pd.DataFrame(data=d)
    
   
    # Add marker for Boulder, CO
    for moment in moments:
        
        df2 = pd.DataFrame({'latitude': [moment.latitude], 'longitude': [moment.longitude]})
        df_acc = df_acc.append(df2)
        
    df_acc['latitude'] = df_acc['latitude'].astype(float)
    df_acc['longitude'] = df_acc['longitude'].astype(float)


    heat_df = df_acc[['latitude', 'longitude']]
    heat_df = heat_df.dropna(axis=0, subset=['latitude','longitude'])

    print(heat_df, "\n")

    # List comprehension to make out list of lists
    heat_data = [[row['latitude'],row['longitude']] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(myMap)

    myMap.save("map.html")
    webbrowser.open("map.html")

    
def plot_moments(moments):
    LDN_COORDINATES = (40.2, -4)
    myMap = folium.Map(location=LDN_COORDINATES, zoom_start=5)

  
    # Add marker for Boulder, CO
    for moment in moments:
        folium.Marker(
            location=[moment.latitude, moment.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
            popup='Gameplay Moment', # pop-up label for the marker
            icon=folium.Icon()
        ).add_to(myMap)


    myMap.save("map.html")
    webbrowser.open("map.html")


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


def plot_challenges(challenges):

 
    LDN_COORDINATES = (40,-8.7187)
    myMap = folium.Map(location=LDN_COORDINATES, zoom_start=15)

    print("b")
    print(len(challenges))
    print("c")
    # Add marker for Boulder, CO
    for challenge in challenges:
        
        if challenge.latitude > 41.2 and challenge.longitude > -8.4:
            folium.Marker(
                location=[challenge.latitude, challenge.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
                popup='Challenge', # pop-up label for the marker
                icon=folium.Icon()
            ).add_to(myMap)


    myMap.save("map.html")
    webbrowser.open("map.html")

def combined_plot(challenges, moments):

    
    LDN_COORDINATES = (41.15,-8.6)
    myMap = folium.Map(location=LDN_COORDINATES, zoom_start=10)

    d = {'latitude': [], 'longitude': []}
    df_acc = pd.DataFrame(data=d)
    
   
    # Add marker for Boulder, CO
    for moment in moments:
        
        df2 = pd.DataFrame({'latitude': [moment.latitude], 'longitude': [moment.longitude]})
        df_acc = df_acc.append(df2)
        
    df_acc['latitude'] = df_acc['latitude'].astype(float)
    df_acc['longitude'] = df_acc['longitude'].astype(float)


    heat_df = df_acc[['latitude', 'longitude']]
    heat_df = heat_df.dropna(axis=0, subset=['latitude','longitude'])

    print(heat_df, "\n")

    # List comprehension to make out list of lists
    heat_data = [[row['latitude'],row['longitude']] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(myMap)

    for challenge in challenges:

        if(challenge.success):
            folium.Marker(
                location=[challenge.Challenge.latitude, challenge.Challenge.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
                popup='Challenge Completed with Success', # pop-up label for the marker
                icon=folium.Icon(color="blue", icon="check-circle")
            ).add_to(myMap)
        else:
                folium.Marker(
                location=[challenge.Challenge.latitude, challenge.Challenge.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
                popup='Challenge Failure', # pop-up label for the marker
                icon=folium.Icon(color="gray", icon="times-circle")
            ).add_to(myMap)

    myMap.save("map.html")
    webbrowser.open("map.html")

