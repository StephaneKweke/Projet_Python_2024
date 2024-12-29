
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
    """
    Visualise les prédictions effectuées par un modèle ARIMA pour une variable donnée.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame contenant les données historiques avec au moins deux colonnes :
        - 'day' : Les dates correspondantes.
        - La variable cible spécifiée par `var`.
    var : str
        Nom de la variable cible (colonne dans `data`) à prédire.
    model_fit : statsmodels.tsa.arima.model.ARIMAResults
        Modèle ARIMA entraîné via statsmodels, utilisé pour générer les prédictions.

    Description:
    ------------
    1. Trace les valeurs réelles de la variable cible à partir des données historiques.
    2. Trace les prédictions générées par le modèle ARIMA entraîné.
    3. Ajoute une légende pour différencier les valeurs réelles et prédites, et un titre spécifique à la variable.

    Returns:
    --------
    None
        La fonction affiche uniquement un graphique montrant les prédictions ARIMA et les valeurs réelles.

    Notes:
    ------
    - La colonne 'day' dans `data` doit contenir des objets de type datetime ou équivalent pour un traçage correct.
    - Le modèle ARIMA doit être préalablement entraîné sur les données fournies.
    """
    #prediction
    plt.figure(figsize=(10, 6))
    plt.plot(data["day"],data[var], label="real",color="black")
    plt.plot(data["day"],model_fit.predict(), label="Predict", color='skyblue')
    plt.title("Prédictions ARIMA {}".format(var))
    plt.legend()
    plt.show()



    
def prevision_arima(data,var,model_fit):
    """
    Génère des prévisions à court terme à l'aide d'un modèle ARIMA et visualise les résultats.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame contenant les données historiques avec au moins deux colonnes :
        - 'day' : Les dates correspondantes.
        - La variable cible spécifiée par `var`.
    var : str
        Nom de la variable cible (colonne dans `data`) à prédire.
    model_fit : statsmodels.tsa.arima.model.ARIMAResults
        Modèle ARIMA entraîné via statsmodels, utilisé pour effectuer les prévisions.

    Description:
    ------------
    1. Utilise le modèle ARIMA entraîné pour effectuer des prévisions sur une période de 14 jours.
    2. Génère un graphique comparant l'historique des données avec les prévisions sur la période future.
    3. Affiche un graphique avec les prévisions et renvoie les résultats sous forme de série.

    Returns:
    --------
    pandas.Series
        Les prévisions générées par le modèle ARIMA pour la période spécifiée (par défaut 14 jours).

    Notes:
    ------
    - La colonne 'day' dans `data` doit contenir des objets de type datetime ou équivalent pour un traçage correct.
    - Le modèle ARIMA doit être préalablement ajusté (fit) aux données historiques.
    - Le nombre de jours pour les prévisions est fixé à 14 par défaut (2 semaines), mais peut être ajusté en modifiant `forecast_steps`.
    """
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
    """ 
    Génère des prévisions à court terme à l'aide d'un modèle VAR et visualise les résultats.

    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame contenant les données historiques utilisées pour entraîner le modèle VAR.
        Chaque colonne représente une variable incluse dans le modèle.
        L'index doit être de type datetime ou équivalent pour garantir un traçage correct.
    var : str
        Nom de la variable cible à prédire, correspondant à l'une des colonnes de `data`.
    model_fit : statsmodels.tsa.api.VARResultsWrapper
        Modèle VAR ajusté (fit) aux données historiques, utilisé pour effectuer les prévisions.

    Description:
    ------------
    1. Utilise le modèle VAR ajusté pour effectuer des prévisions sur une période de 14 jours.
    2. Les prévisions sont générées pour toutes les variables du modèle, mais seul le résultat
       de la variable cible spécifiée (`var`) est tracé.
    3. Affiche un graphique comparant les données historiques avec les prévisions pour la période future.

    Returns:
    --------
    pandas.DataFrame
        DataFrame contenant les prévisions pour toutes les variables du modèle VAR, indexées par les dates
        futures (par défaut, 14 jours).

    Notes:
    ------
    - Le nombre de jours pour les prévisions est fixé à 14 par défaut, mais peut être ajusté en modifiant `forecast_steps`.
    - La visualisation montre uniquement la variable cible spécifiée dans `var`.
    - Assurez-vous que `data` contient les mêmes variables que celles utilisées pour ajuster `model_fit`.
    """
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
    """
    Calcule un indice synthétique d'évaluation des erreurs de prévision pour plusieurs polluants, 
    en pondérant les erreurs par l'inverse des moyennes des polluants.

    Parameters:
    -----------
    polluants : list
        Liste des noms des colonnes représentant les polluants à évaluer.
    forecast : pandas.DataFrame
        DataFrame contenant les valeurs prédites pour chaque polluant, indexé par les mêmes dates que `test`.
    data : pandas.DataFrame
        DataFrame contenant les valeurs historiques utilisées pour le calcul des moyennes des polluants.
    test : pandas.DataFrame
        DataFrame contenant les valeurs réelles (observées) des polluants correspondant aux prévisions dans `forecast`.

    Returns:
    --------
    float
        Indice synthétique d'évaluation, pondérant les erreurs par l'inverse des moyennes des concentrations des polluants.

    Description:
    ------------
    1. Pour chaque polluant dans la liste `polluants`, la fonction calcule le rapport entre l'erreur quadratique moyenne
       (RMSE) des prévisions et la moyenne historique des concentrations.
    2. Les erreurs sont ensuite pondérées par l'inverse des moyennes historiques pour équilibrer les contributions des différents polluants.
    3. Le résultat est un indice synthétique unique qui reflète la qualité des prévisions sur l'ensemble des polluants.

    Notes:
    ------
    - Assurez-vous que les colonnes spécifiées dans `polluants` sont présentes dans les DataFrames `forecast`, `data`, et `test`.
    - La fonction `root_mean_squared_error` doit être définie dans l'environnement.
    - Ce type d'indice est particulièrement utile lorsque les concentrations des polluants ont des ordres de grandeur différents,
      ce qui pourrait biaiser une évaluation globale simple.

    Example:
    --------
    polluants = ['pm10', 'pm2_5', 'ozone', 'nitrogen_dioxide', 'sulphur_dioxide']
    forecast = pd.DataFrame({'pm10': [20, 25], 'pm2_5': [15, 18], ...})
    data = pd.DataFrame({'pm10': [50, 55, 60], 'pm2_5': [30, 35, 40], ...})
    test = pd.DataFrame({'pm10': [22, 27], 'pm2_5': [16, 20], ...})
    indice = indice_eval(polluants, forecast, data, test)
    print(indice)
    0.2451
    """
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

