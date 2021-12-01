# External
from pickle import FALSE
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import mlflow.sklearn

# Internal
from dataLoader.DataLoader import DataLoader
from models.RfModel import RFModel


def mlflowRun(model, X_train, X_test, y_train, y_test, n_run = "RF: tidal coefficients forcasting"):
        """ this method executes an Mlflow run and logs important metrics, artifacts..."""
        
        # Mlflow run
        with mlflow.start_run(run_name = n_run) as run:
            # get run id and experiment id
            run_id = run.info.run_uuid
            experiment_id = run.info.experiment_id

            # train model  and predict
            model.fit(X_train, y_train)
            
            # log model and params using MLflow API
            mlflow.sklearn.log_model(model.model, "random-forest-reg-model")
            mlflow.log_params(model.params)

            # log metrics 
            y_predicted = model.predict(X_test)

            # compute overall error
            error= mean_squared_error(y_test, y_predicted, squared=False)
            mlflow.log_metric("rmse", error)

            # compute min coef error
            min_error = mean_squared_error(y_test.values[:,0], y_predicted[:,0], squared=False)
            mlflow.log_metric("min coef rmse", min_error)

            # compute max coef error
            max_error = mean_squared_error(y_test.values[:,1], y_predicted[:,1], squared=False)
            mlflow.log_metric("max coef rmse", max_error)
            
            # model saving
        model.save("RF_custom_features_two_target_best.pk")

def run():
    # TODO: load data after getting best features from feature engineering

    # Loading data
    DL = DataLoader()
    DL.createDataFrameSeperateCoef()
    DL.addMoonSunFeatures(two_target=True)
    DL.addTimRelatedFeatures(two_target=True)
    df = DL.data

    df_train, df_test = df[df.year!=2021], df[df.year==2021]
    # Dropping year column 
    df_train.drop(["year"], axis = 1, inplace=True)
    df_test.drop(["year"], axis = 1, inplace=True)

    # Getting X, y
    X_train = df_train.iloc[:,2:]
    X_test = df_test.iloc[:,2:]
    y_train = df_train.iloc[:, 0:2]
    y_test = df_test.iloc[:, 0:2]

    # model 
    RF = RFModel({"n_estimators":100})

    # Performing crossValidation (TimeSeries like cross validation)
    tscv = TimeSeriesSplit(n_splits=10)
    param_grid = {"n_estimators":[100, 200, 300, 400, 500],
                  "max_depth": [2, 5, 10, 15, 20, 25],
                  "min_samples_split":[2, 5, 10],
                  "min_samples_leaf":[1, 5, 10, 15]}
    clf = GridSearchCV(RF.model, param_grid = param_grid, cv = tscv, verbose=10, scoring="neg_mean_squared_error", n_jobs=-1)
    best_clf = clf.fit(X_train, y_train)

    # Fit best classifier
    RF = RFModel(params= clf.best_params_)
    mlflowRun(RF, X_train, X_test, y_train, y_test, n_run = "RF on custom features: GridSearchCV Best ")
    

if __name__ == "__main__":
    run()
