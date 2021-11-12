
# external
from typing import AbstractSet
from sklearn.ensemble import RandomForestRegressor
import mlflow.sklearn

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
                                                                                           
    def fit(self, X, y):
        self.model.fit(X,y)

    def evaluate(self, X, y):
        y_predicted = self.model.predict(X)
        scores, score = metrics.rmsErrors(y, y_predicted)
        return scores, score

    def mlflowRun(self, n_run = "RF: tidal coefficients forcasting"):
        """ this method execute an Mlflow run and logs important metrics, artifacts..."""
        # load data 
        self.loadData()
        
        # Mlflow run
        with mlflow.start_run(run_name = n_run) as run:
            # get run id and experiment id
            run_id = run.info.run_uuid
            experiment_id = run.info.experiment_id

            # train model  and predict
            self.fit(self.X_train, self.y_train)
            
            # log model and params using MLflow API
            mlflow.sklearn.log_model(self.model, "random-forest-reg-model")
            mlflow.log_params(self.params)
            mlflow.log_param("past_step", self.past)

            # log metrics 
            score, scores= self.evaluate(self.X_test, self.y_test)

            mlflow.log_metric("rmse", score)

            idx = 0
            for idx in range(len(scores)):
                mlflow.log_metric(key = 'rmse_day',value = scores[idx], step = idx)
                idx+=1

            # model saving
            self.save("RF_model")




