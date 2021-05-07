from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import numpy as np

def features_selector(dataset):
    dataset_features = dataset[["playerAPM", "playerReactionTime",
                                "playerPaddleSafety", "type of personality"]]

    return dataset_features


def labels_selector(dataset):
    labels_features = dataset[[
        "brick height", "paddle speed", "ball speed", "paddle length", "ball size"]]

    return labels_features


def data_preparation_train(dataset):
    X_train = features_selector(dataset)
    y_train = labels_selector(dataset)

    return X_train, y_train


def data_preparation_predict(dataset):
    X_pred = features_selector(dataset)

    return X_pred


def random_forest(dataset):
    X = dataset.iloc[:, 1:5].values
    y = dataset.iloc[:, 5:7].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    regressor = RandomForestRegressor(n_estimators=20, random_state=0)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)

    
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))