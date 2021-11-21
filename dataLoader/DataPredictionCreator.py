import pandas as pd
import datetime as dt
from hijri_converter import Hijri, Gregorian
import ephem


class  DataPredictionCreator:
    def __init__(self):
        self.moon = ephem.Moon()
        self.sun = ephem.Sun()

    def getMoonPhase(self, date):
        """ This method gets """
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

    def addMoonSubSolarLatitude(self, date):
        self.data["date"] = self.data["dateTime"].dt.date.values
        self.data["subsolar_latitude"] = self.data["date"].apply(lambda x: self.getMoonSubSolarLatitude(x))
        self.data.drop(["date"], axis = 1, inplace= True)
        print("moon subsolar latitude added successfully")

    def getMoonElongation(self, date):
        self.moon.compute(date)
        return self.moon.elong

    def getSunEarthDistance(self, date):
        self.sun.compute(date)
        return self.sun.earth_distance

    def createData(self, from_year, from_month, from_day, to_year, to_month, to_day):
        # Generating dates betwwen the entered dates
        sdate = dt.date(from_year,from_month,from_day)   # start date
        edate = dt.date(to_year, to_month, to_day)   # end date
        dates = pd.date_range(sdate,edate,freq='d').to_list()
        dates = list(map(lambda x : x.date(), dates))
        
        # Creating data Frame conataining a column of dates
        df = pd.DataFrame(dates, columns= ["date"])
        
        # Creating custom moon sun related features and dateTime features
        df["moon_phase"] = df['date'].apply(lambda x :self.getMoonPhase(x))
        df["earth_moon_distance"] = df['date'].apply(lambda x: self.getMoonDistance(x))
        df["sun_moon_distance"] = df['date'].apply(lambda x: self.getMoonSunDistance(x))
        df["libration_lat"] = df['date'].apply(lambda x: self.getMoonLibrationLatitude(x))
        df["libration_long"] = df['date'].apply(lambda x: self.getMoonLibrationLongitude(x))
        df["subsolar_latitude"] = df['date'].apply(lambda x: self.getMoonSubSolarLatitude(x))
        df["elongation"] = df['date'].apply(lambda x: self.getMoonElongation(x))
        df["earth_sun_distance"] = df['date'].apply(lambda x: self.getSunEarthDistance(x))

        # Creating time related features and dateTime features
        df['hijri_day'] = df['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().day)
        df['hijri_month'] = df['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().month)
        df['hijri_year'] = df['date'].apply(lambda x: Gregorian(x.year, x.month, x.day).to_hijri().year)

        # Dropping date column
        dates = df["date"].values
        df.drop(["date"], axis=1, inplace=True)

        return df, dates
        
        
        
