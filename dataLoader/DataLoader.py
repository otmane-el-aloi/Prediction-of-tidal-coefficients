
# external 
import numpy as np
import pandas as pd
import datetime as dt
import ephem
from sklearn.model_selection import TimeSeriesSplit
from hijri_converter import Hijri, Gregorian

# internal 
from configs import config

# TODO :add documentation
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
    
    def createDataFrameSeperateCoef(self):
        """ laods data from data directory 
        returns à dataFrame Object containing:
            date: a datetime format column
            min_coef: the corresponding min tidal coefficient 
            max_coef: the corresponding max tidal coefficient
        """
        self.data = pd.read_csv(self.config["data"]["path"] + "data.txt",
                                sep = "     ",
                                index_col = None)
        self.data = self.data.reset_index()
        self.data= self.data.rename(columns = {'index':'dateTime', 'COEF_MAREE   UT: 0.0':'coef'})
        self.data['dateTime'] = pd.to_datetime(self.data['dateTime'])
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["min_ceof"] = self.data.groupby("date")["coef"].transform("min")
        self.data["max_ceof"] = self.data.groupby("date")["coef"].transform("max")
        self.data.drop(["coef", "dateTime"], axis = 1, inplace = True)
        self.data = self.data.drop_duplicates()
        print("data successfully loaded  with two target features")
    
    def getMoonPhase(self, date):
        """ This method gets """
        self.moon.compute(date)
        return self.moon.moon_phase
    
    def addMonnPhase(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["moon_phase"] = self.data["date"].apply(lambda x: self.getMoonPhase(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("Moon phase added successfully")

    def getMoonDistance(self, date):
        self.moon.compute(date)
        return self.moon.earth_distance
    
    def addMoonDistance(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["earth_moon_distance"] = self.data["date"].apply(lambda x: self.getMoonDistance(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("earth moon distance added successfully")

    def getMoonSunDistance(self, date):
        self.moon.compute(date)
        return self.moon.sun_distance

    def addMoonDistance(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["sun_moon_distance"] = self.data["date"].apply(lambda x: self.getMoonSunDistance(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("sun moon distance added successfully")

    def getMoonLibrationLatitude(self, date):
        self.moon.compute(date)
        return self.moon.libration_lat
    
    def addMoonLibrationLatitude(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["liberation_lat"] = self.data["date"].apply(lambda x: self.getMoonLibrationLatitude(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("moon liberation latitude added successfully")

    def getMoonLibrationLongitude(self, date):
        self.moon.compute(date)
        return self.moon.libration_long

    def addMoonLibrationLongitude(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["liberation_long"] = self.data["date"].apply(lambda x: self.getMoonLibrationLongitude(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("moon liberation latitude added successfully")

    def getMoonSubSolarLatitude(self, date):
        self.moon.compute(date)
        return self.moon.subsolar_lat

    def addMoonSubSolarLatitude(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["subsolar_latitude"] = self.data["date"].apply(lambda x: self.getMoonSubSolarLatitude(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("moon subsolar latitude added successfully")

    def getMoonElongation(self, date):
        self.moon.compute(date)
        return self.moon.elong

    def addMoonElongation(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["elongation"] = self.data["date"].apply(lambda x: self.getMoonElongation(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("moon elongation added successfully") 

    def getSunEarthDistance(self, date):
        self.sun.compute(date)
        return self.sun.earth_distance

    def addSunEarthDistance(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["earth_sun_distance"] = self.data["date"].apply(lambda x: self.getSunEarthDistance(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("earth sun distance added successfully") 
        
    def addMoonSunFeatures(self, two_target=False):
        """ This method adds features related to moon and sun """   
        if two_target == False: 
            self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["moon_phase"] = self.data['date'].apply(lambda x :self.getMoonPhase(x))
        self.data["earth_moon_distance"] = self.data['date'].apply(lambda x: self.getMoonDistance(x))
        self.data["sun_moon_distance"] = self.data['date'].apply(lambda x: self.getMoonSunDistance(x))
        self.data["libration_lat"] = self.data['date'].apply(lambda x: self.getMoonLibrationLatitude(x))
        self.data["libration_long"] = self.data['date'].apply(lambda x: self.getMoonLibrationLongitude(x))
        self.data["subsolar_latitude"] = self.data['date'].apply(lambda x: self.getMoonSubSolarLatitude(x))
        self.data["elongation"] = self.data['date'].apply(lambda x: self.getMoonElongation(x))
        self.data["earth_sun_distance"] = self.data['date'].apply(lambda x: self.getSunEarthDistance(x))
        print("Features added successfully!")
    
    def addTimRelatedFeatures(self, two_target = False):
        """ This method adds hijri calendar related date-time features"""
        if two_target == False:
            self.data['date'] = self.data['dateTime'].dt.date.values
            self.data['hour'] = self.data['dateTime'].dt.hour.values
        self.data['hijri_day'] = self.data['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().day)
        self.data['hijri_month'] = self.data['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().month)
        self.data['hijri_year'] = self.data['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().year)
        self.data['year']= self.data["date"].apply(lambda x: x.year)
        self.data.drop(["date"], axis=1, inplace=True)
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


