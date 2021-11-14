# external 
import numpy as np

# plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns

# theme for plots
plt.style.use('seaborn-bright')


class Plots():
    """ This class contains utils plotting methods"""
    def __init__(self, figsize):
        self.figsize = figsize

    def plotRmse(self, errors):
        plt.figure(figsize=self.figsize)
        plt.plot(np.arange(14)+1, errors)
        plt.xlabel("Days of the prediction")
        plt.ylabel("RMSE")
        plt.title("Evolution of the RMSE over time")
        plt.grid()

    def plotForcast(self, X, y, y_pred, data_index):
        """ this methods plots the forcast result of a given dataPoint """

        plt.figure(figsize = self.figsize)
        past_values = len(X[0])
        step = len(y[0])
        # Input 
        plt.scatter(np.arange(past_values)+1, X[data_index], color = "red")
        plt.plot(np.arange(past_values)+1, X[data_index], color = "red")

        # Ouptut (actual)
        plt.scatter(np.arange(past_values)+step+1, y[data_index], color = "red")
        plt.plot(np.arange(past_values)+step+1, y[data_index], color = "red", label = "actual")

        # Ouput (predicted)
        plt.scatter(np.arange(past_values)+step+1, y_pred[data_index], color ="blue")
        plt.plot(np.arange(past_values)+step+1, y_pred[data_index], color = "blue",  label = "predicted")

        # Decoration
        plt.axvline(x=step, color = "black")
        plt.axvspan(step, step+past_values, alpha=0.5, color='silver')
        
        plt.ylabel("Tidal coef value")
        plt.title("Foracast of {} days ahead using values from {} past days".format(step, past_values))
        plt.legend()
        plt.grid()
    
