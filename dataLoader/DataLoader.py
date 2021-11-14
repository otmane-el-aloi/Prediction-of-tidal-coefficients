
# external 
import numpy as np
import pandas as pd
import datetime as dt
import ephem
from sklearn.model_selection import TimeSeriesSplit
from hijri_converter import Hijri, Gregorian

# internal 
from configs import config

class DataLoader():
    """ This class contains methods that help manipulating data: loading, preprocessing..."""
    def __init__(self):
        self.config = config.CFG
        self.data = None
        self.moon = ephem.Moon()
        self.sun = ephem.Sun()
    
    def createDataFrame(self):
        """ laods data from data directory 
        returns à dataFrame Object containing:
            dateTime: a datetime format column
            coef: the corresponding tidal coefficient 
        """
        self.data = pd.read_csv(self.config["data"]["path"] + "data.txt",
                                sep = "     ",
                                index_col = None)
        self.data = self.data.reset_index()
        self.data= self.data.rename(columns = {'index':'dateTime', 'COEF_MAREE   UT: 0.0':'coef'})
        self.data['dateTime'] = pd.to_datetime(self.data['dateTime'])
        print("data successfully loaded ")
    
    def getMoonPhase(self, date):
        self.moon.compute(date)
        return self.moon.moon_phase
    
    def getMoonDistance(self, date):
        self.moon.compute(date)
        return self.moon.earth_distance

    def getMoonSunDistance(self, date):
        self.moon.compute(date)
        return self.moon.sun_distance

    def getMoonLibrationLatitude(self, date):
        self.moon.compute(date)
        return self.moon.libration_lat

    def getMoonLibrationLongitude(self, date):
        self.moon.compute(date)
        return self.moon.libration_long

    def getMoonSubSolarLatitude(self, date):
        self.moon.compute(date)
        return self.moon.subsolar_lat

    def getMoonElongation(self, date):
        self.moon.compute(date)
        return self.moon.elong

    def getSunEarthDistance(self, date):
        self.sun.compute(date)
        return self.sun.earth_distance
        
    def addMoonSunFeatures(self):
        """ This method adds features related to moon and sun """
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["moon_phase"] = self.data['date'].apply(lambda x :self.getMoonPhase(x))
        self.data["earth_moon_distance"] = self.data['date'].apply(lambda x: self.getMoonDistance(x))
        self.data["sun_moon_distance"] = self.data['date'].apply(lambda x: self.getMoonSunDistance(x))
        self.data["libration_lat"] = self.data['date'].apply(lambda x: self.getMoonLibrationLatitude(x))
        self.data["libration_long"] = self.data['date'].apply(lambda x: self.getMoonLibrationLongitude(x))
        self.data["subsolar_latitude"] = self.data['date'].apply(lambda x: self.getMoonSubSolarLatitude(x))
        self.data["elongation"] = self.data['date'].apply(lambda x: self.getMoonElongation(x))
        self.data["earth_sun_distance"] = self.data['date'].apply(lambda x: self.getSunEarthDistance(x))
        self.data.drop(["date"], axis=1, inplace=True)
        print("Features added successfully!")
    
    def addTimRelatedFeatures(self):
        """ This method adds hijri calendar related date-time features"""
        self.data['date'] = self.data['dateTime'].dt.date.values
        self.data['hijri_day'] = df['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().day)
        self.data['hijri_month'] = df['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().month)
        self.data['hijri_year'] = df['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().year)
        self.data['hour'] = self.data['dateTime'].dt.hour.values
        print("Date-Time features added with sucess!")

    def splitDataSet(self, past_values = 14, step = 14):
        """ This method splits data into train and test
        :past_values: int indicating how many past values you want the model to see
        :step: int indicating how many future values you want the model to predict
        
        """
        self.data['year'] = self.data['dateTime'].dt.year.values

        # split train and test
        train = self.data[self.data['year']!=2021].coef.values
        test = self.data[self.data['year']==2021].coef.values

        # restructure into windows of data
        X_train, y_train = [], []
        X_test, y_test = [], []
        train_shape = train.shape
        test_shape = test.shape

        for row in range(0, train_shape[0]):
            if row+past_values+step <= train_shape[0]:
                X_train.append(train[row:row+past_values].reshape(past_values, 1))
                y_train.append(train[row+past_values:row+past_values+step])
        for row in range(0, test_shape[0]):
            if row+past_values+step <= test_shape[0]:
                X_test.append(test[row:row+past_values].reshape(past_values, 1))
                y_test.append(test[row+past_values:row+past_values+step])

        X_train = np.array(X_train)
        X_test = np.array(X_test)

        y_train = np.array(y_train)
        y_test = np.array(y_test)

        X_train_shape = X_train.shape
        X_test_shape = X_test.shape

        # Reshaping to 2 dim 
        X_train_reshaped = X_train.reshape(X_train_shape[0], X_train_shape[1])
        X_test_reshaped = X_test.reshape(X_test_shape[0],X_test_shape[1])
        return X_train_reshaped, X_test_reshaped, y_train, y_test

    def crossValidationData(self, X_train, y_train, n_splits = 10):
        tscv = TimeSeriesSplit(n_splits=n_splits)
        # Getting splits indexes
        train_index = tscv.split(X_train)
        X_train = X_train[train_index]
        y_train = y_train[train_index]
        return X_train, y_train


