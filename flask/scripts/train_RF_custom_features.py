# External
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
            score= mean_squared_error(y_test, y_predicted, squared=False)
            mlflow.log_metric("rmse", score)

            # model saving
        model.save("RF_custom_features_best.pk")

def run():
    # TODO: load data after getting best features from feature engineering
    # Worst Features 
    worst_features = ["year", "hijri_month", "hijri_year", "dateTime"]

    # Loading data
    DL = DataLoader()
    DL.createDataFrame()
    DL.addMoonSunFeatures()
    DL.addTimRelatedFeatures()
    df = DL.data

    # Creating year column usefull for splitting 
    df['year'] = df["dateTime"].dt.year.values
    df_test = df[df["year"]==2021]
    df_train = df[df["year"]!=2021]

    X_train = df_train.loc[:,df.columns!="coef"]
    y_train = df_train.loc[:, "coef"]
    X_test = df_test.loc[:, df.columns!= "coef"]
    y_test = df_test.loc[:, "coef"]

    # Dropping non usefull features
    for feature in worst_features:
        if feature in X_train.columns:
            X_train.drop([feature], axis = 1, inplace = True)
            X_test.drop([feature], axis = 1, inplace = True)
    # model 
    RF = RFModel({"n_estimators":100})

    # Performing crossValidation (TimeSeries like cross validation)
    tscv = TimeSeriesSplit(n_splits=10)
    param_grid = {"n_estimators":[100]}
                #   "max_depth": [2, 5, 10, 15, 20, 25],
                #   "min_samples_split":[2, 5, 10],
                #   "min_samples_leaf":[1, 5, 10, 15]
    clf = GridSearchCV(RF.model, param_grid = param_grid, cv = tscv, verbose=10, scoring="neg_mean_squared_error", n_jobs=-1)
    best_clf = clf.fit(X_train, y_train)

    # Fit best classifier
    RF = RFModel(params= clf.best_params_)
    mlflowRun(RF, X_train, X_test, y_train, y_test, n_run = "RF on custom features: GridSearchCV Best ")
    

if __name__ == "__main__":
    run()
