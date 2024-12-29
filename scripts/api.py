import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from openmeteo_requests import Client

def recup_data(start_date, end_date, url, variables, region_centroides):
    
    """
    Récupère des données climatiques horaires pour plusieurs régions via une API météorologique.

    Parameters:
    -----------
    start_date : str
        Date de début au format 'YYYY-MM-DD'.
    end_date : str
        Date de fin au format 'YYYY-MM-DD'.
    url : str
        Lien de l'API météo utilisée pour les requêtes.
    variables : list
        Liste des variables météorologiques à récupérer (e.g., ['temperature_2m', 'precipitation']).
    region_centroides : list
        Liste de tuples contenant :
        - Nom de la région (str),
        - Longitude (float),
        - Latitude (float).

    Returns:
    --------
    pandas.DataFrame
        DataFrame combiné contenant les données climatiques horaires pour toutes les régions spécifiées, avec les colonnes :
        - 'date' : Date et heure de l'observation.
        - 'day' : Date sans heure (YYYY-MM-DD).
        - 'region' : Nom de la région.
        - 'longitude' : Longitude de la région.
        - 'latitude' : Latitude de la région.
        - Variables météorologiques récupérées (une colonne par variable spécifiée).

    Description:
    ------------
    1. Initialise une session avec cache pour optimiser les appels à l'API et réduire les temps de réponse.
    2. Effectue des appels API pour chaque région en utilisant les coordonnées fournies.
    3. Récupère les données horaires pour chaque variable spécifiée, créant un DataFrame individuel pour chaque région.
    4. Concatène tous les DataFrames en un seul, avec une colonne indiquant la région.
    5. Crée une colonne 'day' pour faciliter les analyses agrégées au niveau journalier.

    Notes:
    ------
    - La fonction utilise un système de gestion des erreurs pour afficher les régions ayant échoué à récupérer les données.
    - Les données sont alignées sur une base horaire, et l'intervalle est déduit automatiquement via l'API.
    - Assurez-vous que le module `openmeteo_requests` est installé et configuré pour fonctionner avec l'API utilisée.
    """
    import openmeteo_requests
    import requests_cache
    import pandas as pd
    from retry_requests import retry
    from openmeteo_requests import Client
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
    combined_dataframe['date'] = pd.to_datetime(combined_dataframe['date'])
    # Création d'une nouvelle colonne 'day' contenant uniquement la date (sans l'heure)
    combined_dataframe.insert(1,"day",combined_dataframe["date"].dt.date) 


    return combined_dataframe