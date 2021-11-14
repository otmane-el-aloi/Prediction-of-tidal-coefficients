# External
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit

# Internal
from models.RfModel import RFModel





def run():
    # Loading the model
    RF  = RFModel(params = {"n_estimators":100})

    """ First experience: Changing the params of the Random forest ameliorates the score?"""
    # # Performing crossValidation (TimeSeries like cross validation)
    # tscv = TimeSeriesSplit(n_splits=10)
    # param_grid = {"n_estimators":[100, 200, 300, 400, 500],
    #               "max_depth": [2, 5, 10, 15],
    #               "min_samples_split":[2, 5, 10, 15],
    #               "min_samples_leaf":[1, 5, 10, 15]}
    # clf = GridSearchCV(RF.model, param_grid = param_grid, cv = tscv, verbose=10, n_jobs=-1)
    # best_clf = clf.fit(X_train, y_train)

    # # Fit best classifier
    # RF = RFModel(params= clf.best_params_)
    # RF.mlflowRun(n_run = "RF: GridSearchCV Best")
    
    """ Second experience: Changing the past values number ameliorates the score?"""
    # Finding Best back_step 
    # back_step  = np.arange(14, 120) # up to 2 months a go 
    # for step in back_step:
    #     # Setting the step
    #     RF.setPast(step)
        
    #     # Loading data
    #     RF.loadData()

    #     # fitting the model and saving errors
    #     RF.mlflowRun("RF: Selecting best back step value")
    




if __name__ == "__main__":
    run()
