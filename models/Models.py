# standard
import os 
import pickle
from abc import abstractmethod

# internal
from configs import config



class MlModel():
    """ this class contains methods shareds by all models """
    def __init__(self, params):
        self.config = config.CFG
        self.model = None
        self.params = params

    @classmethod
    def newInstance(cls, params):
        """ creates new class instance """
        return cls(params)
    
    def params(self):
        """ returns the parameters of the created model"""
        return self.params
    
    @abstractmethod
    def loadData(self):
        """ loads data for the model"""

    @abstractmethod
    def fit(self):
        """ fits the model to the data from that original data folder"""

    @abstractmethod
    def evaluate(slef):
        """ evaluates the model using the defined metrics"""

    @abstractmethod
    def mlflowRun(self):
        """ trains, evalutes and logs all metrics, params and all the
        artifacts for the current run using the MLflow API
        """

    def model(self):
        """ Returns the created model """
        return self.model

    def save(self, filename):
        """ saves the model to a pickle format"""
        path = self.config["models"]["path"] + filename
        pickle.dump(self.model, open(path, 'wb'))
        print ("model successfully saved to: {}".format(path))

    def load(self, filename):
        """ laods a trained model """
        path = self.config["models"]["path"] + filename
        pickle.loaded_model = pickle.load(open(path, 'rb'))
        print("model successfully loaded to: {}".format(path))

