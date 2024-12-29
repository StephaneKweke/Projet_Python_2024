
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import root_mean_squared_error

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

def indice_eval (polluants,forecast,data,test) :
    
    indice = 0 
    sum_inv_mean = 0
    for col in polluants : 
        indice = indice + (root_mean_squared_error(forecast[col], test[col])/ data[col].mean())
        sum_inv_mean=sum_inv_mean + (1/(data[col].mean()))
    indice = indice/sum_inv_mean
    return indice







def train_predict_visualize(train_data, historical_data, features_columns, target_column, future_start, future_end):
    """
    Entraîne un modèle Random Forest, prédit les valeurs futures, visualise les résultats, 
    et calcule les importances des caractéristiques.

    Parameters:
    - train_data (DataFrame): Données d'entraînement contenant les features et la cible.
    - historical_data (DataFrame): Données historiques contenant les valeurs observées de la cible.
    - features_columns (list): Liste des colonnes des variables explicatives (features).
    - target_column (str): Nom de la colonne cible (target).
    - future_start (str): Date de début pour les données futures (format 'YYYY-MM-DD').
    - future_end (str): Date de fin pour les données futures (format 'YYYY-MM-DD').

    Returns:
    - predictions (DataFrame): DataFrame contenant les prédictions pour la période future.
    - coeff_importances (Series): Importances des caractéristiques du modèle Random Forest.
    """
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    import matplotlib.pyplot as plt
    np.random.seed(42)
    # Séparation des variables features et target
    features = train_data[features_columns]
    target = train_data[target_column]

    # Entraînement du modèle
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Évaluation sur l'ensemble de test
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error for {target_column}: {mse}')

    # Calcul des importances des caractéristiques
    pertinence = rf.feature_importances_
    coeff_importances = pd.Series(pertinence, index=X_train.columns)
    print("\nImportances des caractéristiques :")
    print(coeff_importances.sort_values(ascending=False))

    # Génération des données synthétiques futures
    future_features = pd.DataFrame({
        col: np.random.normal(features[col].mean(), features[col].std(), len(pd.date_range(start=future_start, end=future_end)))
        for col in features_columns
    }, index=pd.date_range(start=future_start, end=future_end))
    
    # Prédictions pour les données futures
    predictions = pd.DataFrame(index=future_features.index)
    predictions[target_column] = rf.predict(future_features)
    
    # Visualisation des prédictions futures
    plt.figure(figsize=(14, 4))
    plt.plot(predictions.index, predictions[target_column], label=f'Predicted {target_column}', linestyle='--', color='red')
    plt.title('Predicted Concentrations of Pollutants for December 2024')
    plt.xlabel('Date')
    plt.ylabel('Concentration')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Combinaison des données historiques et des prédictions
    new_data = future_features.copy()
    new_data[target_column] = predictions[target_column]
    combined_data = pd.concat([historical_data[['day', target_column]], new_data.reset_index()], ignore_index=True)
    
    # Visualisation historique vs prédictions
    plt.figure(figsize=(14, 4))
    plt.plot(historical_data['day'], historical_data[target_column], label='Valeurs Historiques', color='blue')
    plt.plot(predictions.index, predictions[target_column], label='Prédictions', linestyle='--', color='red')
    plt.title(f'Historique vs Prédiction {target_column}')
    plt.xlabel('Date')
    plt.ylabel('Concentration')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return predictions

