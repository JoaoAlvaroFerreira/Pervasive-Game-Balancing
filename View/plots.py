import pandas as pd
import matplotlib.pyplot as plt

         
def plot_players(players):
    
    longs = [-6,-4,-2]
    lats = [38,40,43]
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
