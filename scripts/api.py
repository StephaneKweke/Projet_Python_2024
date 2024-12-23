import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from openmeteo_requests import Client

def recup_data(start_date, end_date, url, variables, region_centroides):
    
    """
    Fonction pour récupérer des données climatiques horaires pour plusieurs régions.
    
    Paramètres:
    - start_date (str): Date de début au format 'YYYY-MM-DD'.
    - end_date (str): Date de fin au format 'YYYY-MM-DD'.
    - url (str): Lien de l'API météo.
    - variables (list): Liste des variables météorologiques à récupérer.
    - region_centroides (list): Liste de tuples (région, longitude, latitude).
    
    Retourne:
    - pd.DataFrame: DataFrame combiné avec les données climatiques pour toutes les régions.
    """
    # Création de la session avec cache
    cache_session = requests_cache.CachedSession(backend="memory", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = Client(session=retry_session)

    # Dictionnaire pour stocker les DataFrames des régions
    region_dataframes = {}

    for region, longitude, latitude in region_centroides:
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": variables,
                "start_date": start_date,
                "end_date": end_date
            }

            # Appel à l'API
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]  # Première réponse, si plusieurs localisations

            # Récupération des données horaires
            hourly = response.Hourly()
            date_range = pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )

            hourly_data = {
                "date": date_range,
                "region": [region] * len(date_range),
                "longitude": longitude,
                "latitude": latitude
            }

            # Ajout des variables horaires au DataFrame
            for i, variable in enumerate(variables):
                hourly_data[variable] = hourly.Variables(i).ValuesAsNumpy()

            # Stockage du DataFrame dans le dictionnaire
            region_dataframes[region] = pd.DataFrame(data=hourly_data)

        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {region}: {e}")

    # Concaténation de tous les DataFrames
    combined_dataframe = pd.concat(region_dataframes.values(), ignore_index=True)
<<<<<<< HEAD
    combined_dataframe['date'] = pd.to_datetime(combined_dataframe['date'])
    # Création d'une nouvelle colonne 'day' contenant uniquement la date (sans l'heure)
    combined_dataframe.insert(1,"day",combined_dataframe["date"].dt.date) 
=======
>>>>>>> origin

    return combined_dataframe


