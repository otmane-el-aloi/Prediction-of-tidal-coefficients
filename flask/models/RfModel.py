
# external
from sklearn.ensemble import RandomForestRegressor


# internal 
from evaluations.Evaluations import metrics
from models.Models import MlModel
from dataLoader.DataLoader import DataLoader


# Class for the random forest model
class RFModel(MlModel):
    def __init__(self, params):
        super().__init__(params)
        self.model = RandomForestRegressor(**params)

        # data
        self.past = 14
        self.future = 14
        self.dataLoader = DataLoader()
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def setPast(self, value):
        self.past = value

    def loadData(self):
        self.df = self.dataLoader.createDataFrame()
        self.X_train, self.X_test, self.y_train, self.y_test = self.dataLoader.splitDataSet(self.past,
                                                                                            self.future)
    def loadCustomData(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
                                                                                           
    def fit(self, X, y):
        self.model.fit(X,y)

    def predict(self, X):
        y_predicted = self.model.predict(X)
        return y_predicted

    def evaluate(self, X, y):
        y_predicted = self.model.predict(X)
        scores, score = metrics.rmsErrors(y, y_predicted)
        return scores, score




