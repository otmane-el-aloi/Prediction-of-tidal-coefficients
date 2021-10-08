
# external 
import numypy as np
import pandas as pd
import datetime as dt

# internal 
from configs import config

class DataLoader():
    """ This class contains methods that help manipulating data: loading, spliting..."""
    def __init__(self):
        self.config = config.CFG
        self.data = None
    
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
            return np.array(X_train), np.array(X_test), np.array(y_train), np.array(y_test)
