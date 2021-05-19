from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import random




def forest_train(X_train, y_train):
    rfregressor = RandomForestRegressor()

    rfregressor.fit(X_train, y_train)

    return rfregressor


def forest_predict(X_pred, model):
    y_pred = model.predict(X_pred)

    return y_pred

def create_test_data_kpis(rows, max):

    data = []

    if max:
        for _ in range(rows): # "Challenges Done", "Lifetime Value", "Sessions"
            ch_d = random.randint(0, 90)
            lifetime = random.randint(0,9)
            sessions = random.randint(0,24)
            datarow = [ch_d,lifetime, sessions]
            data.append(datarow)
    else: 
        for _ in range(rows): # "Challenges Done", "Lifetime Value", "Sessions"
            ch_d = 0
            lifetime = 0
            sessions = random.randint(0,3)
            datarow = [ch_d,lifetime, sessions]
            data.append(datarow)

    return data

def random_forest(dataset, max):
    y = dataset.iloc[:, 0:5].values
    X = dataset.iloc[:, 5:8].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    #sc = StandardScaler()
    #X_train = sc.fit_transform(X_train)
    #X_test = sc.transform(X_test)

   
    
    rfregressor = forest_train(X_train, y_train)
    y_pred = forest_predict(X_test, rfregressor)

    
    stringa = 'Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred)
    stringb = 'Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred)
    stringc = 'Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))

    X_predict = create_test_data_kpis(200, max)
    y_predict = forest_predict(X_predict, rfregressor)

    return y_predict 

def filter_data(dataset, variable, value, max):
    
    print("Variable:{} Value: {} Max:{}".format(variable,value,max))
    
    if max == "Max":
        dataset = dataset[dataset[variable]>int(value)] # Reducing data size so it runs faster
    else:
        dataset = dataset[dataset[variable]<int(value)] # Reducing data size so it runs faster

    return dataset
