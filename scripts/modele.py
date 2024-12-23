from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd

def stationarity_acf(data,var):
    """
    Fonction pour tester la stationnarité et tracer les graphiques ACF et PACF associé à la série
    
    Paramètres:
    - data : base de données utilisée.
    - var : variable d'interêt.

    Retourne:
    - Affiche si la variable est stationnaire ou pas. Ainsi que les graphes des autocorrelations.
    """
    result = adfuller(data[var])
    #print(f"ADF Statistic: {result[0]}")
    #print(f"p-value: {result[1]}")
    if result[1] < 0.05:
        print("La série est stationnaire.")
    else:
        print("La série n'est pas stationnaire.")
        
    plot_acf(data[var])
    plot_pacf(data[var])
    plt.show()
    
def fit_arima(data,var,p,d,q):
    """
    Fonction pour entrainer le modele ARiMA sur notre série
    
    Paramètres:
    - data : base de données utilisée.
    - var : variable d'interêt.
    - p,d,q :  spécification dans la modelisation ARIMA

    Retourne:
    - le modele entrainé
    """
    model = ARIMA(data[var], order=(p,d,q)) 
    model_fit = model.fit() 
    return model_fit

def prediction_arima(data,var,model_fit):

    #prediction
    plt.figure(figsize=(10, 6))
    plt.plot(data["day"],data[var], label="real",color="black")
    plt.plot(data["day"],model_fit.predict(), label="Predict", color='skyblue')
    plt.title("Prédictions ARIMA {}".format(var))
    plt.legend()
    plt.show()
    
def prevision_arima(data,var,model_fit):
    forecast_steps = 14 #2semaines
    forecast = model_fit.forecast(steps=forecast_steps)
    # Visualisation des prévisions
    plt.figure(figsize=(10, 6))
    plt.plot(data["day"],data[var], label="Historique")
    plt.plot(pd.date_range(max(data["day"]), periods=forecast_steps+1, freq='D')[1:], 
            forecast, label="Prévisions", color='red')
    plt.title("Prévisions ARIMA {}".format(var))
    plt.legend()
    plt.show()
    
    return forecast
    
def residus(data,var,model_fit):
    residuals = model_fit.resid
    plt.figure(figsize=(10, 6))
    plt.plot(residuals, label="Résidus")
    plt.axhline(y=0, color='r', linestyle='--', linewidth=1)
    plt.title("Résidus du modèle ARIMA {}".format(var))
    plt.legend()
    plt.show()
    

def prevision_var(data,var,model_fit):
    forecast_steps = 14 #2semaines
    forecast = model_fit.forecast(y=data.values, steps=forecast_steps)
    forecast_df = pd.DataFrame(forecast, index=pd.date_range(max(data.index), periods=forecast_steps+1, freq='D')[1:], columns=data.columns)
    # Visualisation des prévisions
    plt.figure(figsize=(10, 6))
    plt.plot(data.index,data[var], label="Historique")
    plt.plot(pd.date_range(max(data.index), periods=forecast_steps+1, freq='D')[1:], 
            forecast_df[var], label="Prévisions", color='red')
    plt.title("Prévisions VAR {}".format(var))
    plt.legend()
    plt.show()
    
    return forecast_df