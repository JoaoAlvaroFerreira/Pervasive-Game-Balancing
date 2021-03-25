import datetime
import calendar
import pandas as pd

date = datetime.datetime(2003, 8, 1,0,0)
    
for _ in range(1, 35):
    date = date + datetime.timedelta(hours = 1)
    load_file = 'Resources/weather.csv'
    df = pd.read_csv(load_file)
    today = df.loc[df['Day'] == date.timetuple().tm_yday]
    print("The weather is:"+today['Weather'])

    print(date)