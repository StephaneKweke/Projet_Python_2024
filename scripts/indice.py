# Define functions to compute sub-indices for each pollutant
def get_subindex_pm10(value):
    if value <= 6: return 1
    elif value <= 13: return 2
    elif value <= 20: return 3
    elif value <= 27: return 4
    elif value <= 34: return 5
    elif value <= 41: return 6
    elif value <= 49: return 7
    elif value <= 64: return 8
    elif value <= 79: return 9
    else: return 10

def get_subindex_pm2_5(value):
    if value <= 5: return 1
    elif value <= 10: return 2
    elif value <= 15: return 3
    elif value <= 20: return 4
    elif value <= 25: return 5
    elif value <= 30: return 6
    elif value <= 40: return 7
    elif value <= 50: return 8
    elif value <= 75: return 9
    else: return 10

def get_subindex_no2(value):
    if value <= 29: return 1
    elif value <= 54: return 2
    elif value <= 84: return 3
    elif value <= 109: return 4
    elif value <= 134: return 5
    elif value <= 164: return 6
    elif value <= 199: return 7
    elif value <= 274: return 8
    elif value <= 399: return 9
    else: return 10

def get_subindex_o3(value):
    if value <= 29: return 1
    elif value <= 54: return 2
    elif value <= 79: return 3
    elif value <= 104: return 4
    elif value <= 129: return 5
    elif value <= 149: return 6
    elif value <= 179: return 7
    elif value <= 209: return 8
    elif value <= 239: return 9
    else: return 10

def get_subindex_so2(value):
    if value <= 39: return 1
    elif value <= 79: return 2
    elif value <= 119: return 3
    elif value <= 159: return 4
    elif value <= 199: return 5
    elif value <= 249: return 6
    elif value <= 299: return 7
    elif value <= 399: return 8
    elif value <= 499: return 9
    else: return 10
    

def atmo(df_hourly, regions):

    """
    Calcule l'indice Atmo quotidien pour différentes régions à partir de données horaires, 
    en suivant les critères de sous-indices pour les principaux polluants atmosphériques.

    Parameters:
    -----------
    df_hourly : pandas.DataFrame
        DataFrame contenant des données horaires avec les colonnes suivantes :
        - 'day' : Date correspondant au jour des données.
        - 'region' : Région associée aux données.
        - 'pm10', 'pm2_5', 'nitrogen_dioxide', 'ozone', 'sulphur_dioxide' : Concentrations horaires des polluants.
        - 'temperature_2m', 'relative_humidity_2m', 'precipitation', 'surface_pressure', 'wind_speed_10m' : Variables climatiques.
    regions : list
        Liste des régions à inclure dans le calcul de l'indice Atmo.

    Returns:
    --------
    pandas.DataFrame
        DataFrame contenant les moyennes journalières des variables, les sous-indices calculés 
        pour chaque polluant, et l'indice Atmo final. Les colonnes incluent :
        - 'day' : Date correspondant au jour.
        - 'region' : Région associée aux données.
        - Moyennes des variables (e.g., 'pm10', 'pm2_5', etc.).
        - Sous-indices calculés pour chaque polluant (e.g., 'subindex_pm10', 'subindex_pm2_5', etc.).
        - 'indice_atmo' : Indice Atmo final calculé comme le maximum des sous-indices.
    
    Description:
    ------------
    1. Calcule les moyennes journalières des variables à partir des données horaires.
    2. Calcule les sous-indices pour chaque polluant selon les règles définies par les fonctions associées (e.g., `get_subindex_pm10`).
    3. Calcule l'indice Atmo final comme le maximum des sous-indices pour chaque jour et chaque région.
    4. Filtre les données pour inclure uniquement les régions spécifiées dans la liste `regions`.

    Notes:
    ------
    - L'indice pour l'ozone est calculé à partir de la moyenne glissante maximale sur 8 heures.
    - Assurez-vous que les fonctions `get_subindex_pm10`, `get_subindex_pm2_5`, `get_subindex_no2`, 
      `get_subindex_o3` et `get_subindex_so2` sont disponibles dans l'environnement.
    """
    
        # Calcul des moyennes journalières pour toutes les variables
    daily_data = df_hourly.groupby(['day', 'region']).agg({
        'pm10': 'mean',
        'pm2_5': 'mean',
        'nitrogen_dioxide': 'mean',
        'ozone': lambda x: x.rolling(8, min_periods=1).mean().max(),  # Max sur 8h glissantes
        'sulphur_dioxide': 'mean',
        'temperature_2m'  : 'mean',        
        'relative_humidity_2m' : 'mean' , 
        'precipitation'   : 'mean'  ,      
        'surface_pressure'  : 'mean' ,    
        'wind_speed_10m': 'mean'
    }).reset_index()

    # Calcul des sous-indices
    daily_data['subindex_pm10'] = daily_data['pm10'].apply(get_subindex_pm10)
    daily_data['subindex_pm2_5'] = daily_data['pm2_5'].apply(get_subindex_pm2_5)
    daily_data['subindex_no2'] = daily_data['nitrogen_dioxide'].apply(get_subindex_no2)
    daily_data['subindex_o3'] = daily_data['ozone'].apply(get_subindex_o3)
    daily_data['subindex_so2'] = daily_data['sulphur_dioxide'].apply(get_subindex_so2)

    # Calcul de l'indice Atmo final
    daily_data['indice_atmo'] = daily_data[[
        'subindex_pm10', 'subindex_pm2_5', 'subindex_no2', 'subindex_o3', 'subindex_so2'
    ]].max(axis=1)

    # Fusion avec le DataFrame original pour conserver uniquement les colonnes de df
    df_final = df_hourly[['day', 'region']].drop_duplicates().merge(daily_data, on=['day', 'region'], how='left')
    # Filtrage des régions européennes
    df_final = df_final[df_final['region'].isin(regions)]
    return df_final