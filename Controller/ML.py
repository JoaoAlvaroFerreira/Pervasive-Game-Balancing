from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from math import sqrt
import numpy as np
import random
import pandas as pd




def forest_train(X_train, y_train):
    rfregressor = RandomForestRegressor()

    rfregressor.fit(X_train, y_train)

    return rfregressor

def forest_classifier_train(X_train, z_train):
    rfclassifier = RandomForestClassifier()

    rfclassifier.fit(X_train, z_train)

    return rfclassifier
    
def forest_predict(X_pred, model):
    y_pred = model.predict(X_pred)

    return y_pred





def encoding(dataset):
    oe_style = OneHotEncoder()
    oe_results = oe_style.fit_transform(dataset[["Age"]])
    pd.DataFrame(oe_results.toarray(), columns=oe_style.categories_).head()
    dataset = pd.DataFrame(oe_results.toarray(), columns=oe_style.categories_).join(dataset)
    dataset = dataset.drop(columns=['Age'])
    dataset = dataset.dropna()

    print(dataset)
    return dataset

def random_forest(dataset, max):
    dataset = dataset.copy()
    avg = dataset['Economic Status'].mean()
    print("AVERAGE IS:",avg)
    
    dataset = encoding(dataset)

    y = dataset.iloc[:, 4:8].values
    z = dataset.iloc[:, 0:4]
    X = dataset.iloc[:, 7:11].values

    X_train1, X_test1, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    X_train2, X_test2, z_train, z_test = train_test_split(X, z, test_size=0.25, random_state=0)

    #sc = StandardScaler()
    #X_train = sc.fit_transform(X_train)
    #X_test = sc.transform(X_test)

   
    
    rfregressor = forest_train(X_train1, y_train)
    rfclassifier = forest_classifier_train(X_train2, z_train)
   # y_pred = forest_predict(X_test, rfregressor)

    
    #stringa = 'Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred)
    #stringb = 'Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred)
    #stringc = 'Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))

    #X_predict = create_test_data_kpis(300, max)
    y_predict = forest_predict(X_test1, rfregressor)
    z_predict = forest_predict(X_test2, rfclassifier)
    predict = np.append(z_predict, y_predict, axis=1)
    return predict

def filter_data(dataset, variable, value, max):
    
    print("Variable:{} Value: {} Max:{}".format(variable,value,max))
    
    if max == "Max":
        dataset = dataset[dataset[variable]>int(value)] # Reducing data size so it runs faster
    else:
        dataset = dataset[dataset[variable]<int(value)] # Reducing data size so it runs faster

    return dataset
