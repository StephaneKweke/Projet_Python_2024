    
def time_series_france(polluants: list, time_trends_2023, time_trends_2024):
    """
    Trace une comparaison des évolutions moyennes journalières de plusieurs
    polluants atmosphériques pour l’année 2023 et l’année 2024.

    Paramètres
    ----------
    polluants : list
        Liste des noms de polluants analysés (ex. ["pm10", "pm2_5", "no2"]).
    time_trends_2023 : pandas.DataFrame ou pandas.Series
        Données de concentrations moyennes journalières des polluants pour 2023.
        Doit avoir au moins autant de colonnes (ou un index) que la liste `polluants`.
    time_trends_2024 : pandas.DataFrame ou pandas.Series
        Données de concentrations moyennes journalières des polluants pour 2024.
        Doit avoir au moins autant de colonnes (ou un index) que la liste `polluants`.

    Le code génère un graphique unique avec :
      - Les courbes pour 2023 (ligne pleine),
      - Les courbes pour 2024 (ligne pointillée),
      - Un titre général, des étiquettes d’axes et une légende personnalisée.

    Le rendu final est automatiquement affiché à l’écran (plt.show).
    """

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    # Traçage des tendances pour 2023
    time_trends_2023.plot(
        ax=plt.gca(),
        linewidth=1,
        linestyle="-",  # Ligne pleine pour 2023
        alpha=0.7,
        color=sns.color_palette("tab10", n_colors=len(polluants)),
        label=[f"{pollutant} (2023)" for pollutant in polluants]
    )

    # Traçage des tendances pour 2024
    time_trends_2024.plot(
        ax=plt.gca(),
        linewidth=1.5,
        linestyle="--",  # Ligne pointillée pour 2024
        alpha=0.9,
        color=sns.color_palette("tab10", n_colors=len(polluants)),
        label=[f"{pollutant} (2024)" for pollutant in polluants]
    )

    plt.title("📈 Tendances temporelles des polluants atmosphériques (2023 vs 2024)", fontsize=16)
    plt.xlabel("Jour", fontsize=14)
    plt.ylabel("Concentration moyenne (µg/m³)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title="Polluants et Années", fontsize=12, title_fontsize=14, loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(visible=True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def time_series_regions(polluants, df_final):
    
    """
    Trace, pour chaque région, l'évolution moyenne journalière 
    d'une liste de polluants sur les années 2023 et 2024.
    
    Paramètres
    ----------
    polluants : list
        Liste des colonnes (polluants) à tracer (ex: ['PM10', 'PM2.5']).
    df_final : pandas.DataFrame
        DataFrame contenant au moins les colonnes :
          - 'day' (date ou chaîne de caractères représentant la date)
          - 'region' (nom de la région)
          - et pour chaque polluant de la liste `polluants`.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    df_final['day'] = pd.to_datetime(df_final['day'])
    time_trends_reg = df_final.groupby(['day', 'region'])[polluants].mean().reset_index()
    regions = time_trends_reg['region'].unique()
        # Configuration du style seaborn
    sns.set_theme(style="whitegrid")
        # Création de la grille de sous-graphiques (2 colonnes, et assez de lignes pour toutes les régions)
    fig, axes = plt.subplots(
            nrows=(len(regions) + 1) // 2,
            ncols=2,
            figsize=(20, len(regions) * 3)
        )
    axes = axes.flatten()
        # Boucle sur chaque région pour tracer les courbes
    for i, region in enumerate(regions):
            region_data = time_trends_reg[time_trends_reg['region'] == region]

            time_trends_2023 = region_data[
                (region_data['day'] >= pd.to_datetime('2023-01-01')) &
                (region_data['day'] <= pd.to_datetime('2023-12-31'))
            ]
            time_trends_2024 = region_data[
                (region_data['day'] >= pd.to_datetime('2024-01-01')) &
                (region_data['day'] <= pd.to_datetime('2024-12-31'))
            ]
            #Tendance pour 2023
            if not time_trends_2023.empty:
                time_trends_2023.set_index('day')[polluants].plot(
                    ax=axes[i],
                    linewidth=1,
                    linestyle="-",
                    alpha=0.7,
                    color=sns.color_palette("tab10", n_colors=len(polluants)),
                    label=[f"{pollutant} (2023)" for pollutant in polluants]
                )

            # Tendance pour 2024
            if not time_trends_2024.empty:
                time_trends_2024.set_index('day')[polluants].plot(
                    ax=axes[i],
                    linewidth=1.5,
                    linestyle="--",
                    alpha=0.9,
                    color=sns.color_palette("tab10", n_colors=len(polluants)),
                    label=[f"{pollutant} (2024)" for pollutant in polluants]
                )

            # Personnalisation des axes et de la légende
            axes[i].set_title(f"Tendances des polluants ({region})", fontsize=14)
            axes[i].set_xlabel("Jour", fontsize=12)
            axes[i].set_ylabel("Concentration moyenne (µg/m³)", fontsize=12)
            axes[i].tick_params(axis='x', labelsize=10, rotation=30)
            axes[i].tick_params(axis='y', labelsize=10)
            axes[i].legend(fontsize=10)

        # Supprimer les axes non utilisés si le nombre de régions est impair
    for j in range(len(regions), len(axes)):
            fig.delaxes(axes[j])

        # Ajustement global de l'affichage
    plt.tight_layout()
    plt.show()






def plot_monthly_averages(df, variables):
    """
    Affiche pour chaque variable (polluant) la moyenne mensuelle sous forme de graphiques,
    organisés dans une grille de 2 lignes et 3 colonnes.
    
    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant, au minimum :
          - une colonne 'month' (mois numériques 1 à 12)
          - les colonnes listées dans `variables`
    variables : list
        Liste des noms des colonnes à tracer (e.g. ["pm10", "pm2_5", ...]).
        Cette liste doit inclure "month".
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    # 1. Calcul de la moyenne par mois pour les colonnes dans `variables`
    df_air_month = df[variables].groupby("month").mean()

    # 2. Création de la figure et de la grille de sous-graphiques
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))
    axes = axes.flatten()  # Transformation de la matrice d'axes en liste

    # 3. Tracé des courbes pour chaque colonne du DataFrame groupé
    for i, column in enumerate(df_air_month.columns):
        ax = axes[i]
        
        sns.lineplot(
            x=df_air_month.index,
            y=df_air_month[column],
            ax=ax
        )
        
        # Personnalisation de l’axe X et de l’axe Y
        ax.set_xlabel('Mois')
        ax.set_ylabel(f'Moyenne de {column}')
        ax.tick_params(axis='x', rotation=90)
        
        # Définition des ticks et étiquettes de l’axe X
        ax.set_xticks(df_air_month.index)
        ax.set_xticklabels(df_air_month.index)

        # Titre optionnel du graphique
        ax.set_title(f'Moyenne de {column} par mois')

    # 4. Masquage des axes inutilisés (si le nombre de variables < 6)
    for j in range(len(df_air_month.columns), len(axes)):
        axes[j].set_visible(False)

    # 5. Ajustement de l’espacement et affichage
    plt.tight_layout()
    plt.show()



def plot_pollutants(
    gd,
    pollutants,
    region_label_col='LIBELLE_REGION',
    fig_size=(30, 30),
    cmap='viridis',
    title_prefix="Carte de chaleur",
    xlim=None,
    ylim=None
):
    """
    Affichage de plusieurs cartes choroplèthes (une par polluant) 
    sur une même figure, avec labels régionaux.

    Paramètres
    ----------
    gd : geopandas.GeoDataFrame
        GeoDataFrame contenant au moins la géométrie des régions 
        (colonne 'geometry') et les colonnes de polluants 
        dans la liste `pollutants`, ainsi que la colonne 
        du nom de la région (par défaut 'LIBELLE_REGION').
    pollutants : list
        Liste des colonnes (polluants) à tracer. Par exemple:
        ["pm10", "pm2_5", "nitrogen_dioxide", "sulphur_dioxide", "ozone"].
    region_label_col : str
        Nom de la colonne contenant le label de la région 
        (par défaut 'LIBELLE_REGION').
    fig_size : tuple
        Taille de la figure en pouces (largeur, hauteur).
    cmap : str
        Nom de la palette de couleurs Matplotlib (par défaut 'viridis').
    title_prefix : str
        Préfixe du titre pour chaque carte.
    xlim : tuple or None
        Limites de l'axe X sous la forme (xmin, xmax). 
        Si None, la limite est déduite des données.
    ylim : tuple or None
        Limites de l'axe Y sous la forme (ymin, ymax). 
        Si None, la limite est déduite des données.
    """
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    # Nombre total de polluants
    n_pollutants = len(pollutants)

    # Calcul dynamique du nombre de lignes et de colonnes 
    # pour nos sous-figures. (Ici, on part sur un maximum 
    # de 3 colonnes pour éviter que les graphiques soient 
    # trop serrés, mais vous pouvez l’adapter.)
    ncols = 3
    nrows = (n_pollutants + ncols - 1) // ncols  # Arrondi vers le haut

    # Création de la figure et d'une grille de sous-graphiques
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=fig_size,
        subplot_kw={'aspect': 'equal'}  # Pour respecter le ratio carte
    )
    
    # Flatten si on a plusieurs lignes/colonnes 
    # (si nrows=1 et ncols=1, axes n'est pas un array)
    if nrows * ncols > 1:
        axes = axes.flatten()
    else:
        axes = [axes]

    # Boucle sur chaque polluant et chaque axe
    for i, pollutant in enumerate(pollutants):
        ax = axes[i]

        # Calcul de min/max pour normaliser la palette
        vmin = gd[pollutant].min()
        vmax = gd[pollutant].max()
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

        # Tracé de la carte choroplèthe pour le polluant courant
        gd.plot(
            column=pollutant,
            cmap=cmap,
            linewidth=0.5,
            ax=ax,
            edgecolor='0.8',
            legend=True,
            norm=norm,
            legend_kwds={
                'label': f"Concentration de {pollutant}",
                'orientation': "horizontal"
            }
        )

        # Limites de l'axe (si spécifiées)
        if xlim is not None:
            ax.set_xlim(xlim[0], xlim[1])
        if ylim is not None:
            ax.set_ylim(ylim[0], ylim[1])

        # Titre (un pour chaque polluant)
        ax.set_title(f"{title_prefix} : {pollutant}", fontsize=18)

        # Ajout des labels de région au centroïde de chaque géométrie
        for idx, row in gd.iterrows():
            centroid = row['geometry'].centroid
            ax.text(
                centroid.x,
                centroid.y,
                row[region_label_col],
                fontsize=10,
                ha='center',
                color='black',
                weight='bold'
            )

        # Retrait de l'axe dans la mesure du possible pour 
        # centrer l'attention sur la carte
        ax.axis('off')

    # Si le nombre de polluants est inférieur au nombre 
    # total de sous-axes (nrows*ncols), masquer les axes restants
    for j in range(n_pollutants, nrows*ncols):
        axes[j].axis('off')

    # Ajustement global de l'affichage
    plt.tight_layout()
    plt.show()




def plot_climatic_histograms(df, var_climat, n_cols=3, width=20, height_per_row=5):
    """
    Trace un histogramme (avec kde) pour chaque variable indiquée dans var_climat.
    
    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les variables climatiques.
    var_climat : list
        Liste des noms de colonnes à tracer (par ex. ["temperature_2m", "precipitation", ...]).
    n_cols : int
        Nombre de colonnes de la grille (par défaut 3).
    width : int
        Largeur (en pouces) de la figure globale (par défaut 20).
    height_per_row : int
        Hauteur (en pouces) par ligne de sous-graphiques (par défaut 5).
    
    Retour
    ------
    None
        Affiche directement la figure des histogrammes.
    """

    import math
    import matplotlib.pyplot as plt
    import seaborn as sns
    # 1. Détermination du nombre de variables et calcul des dimensions de la grille
    n_vars = len(var_climat)
    n_rows = math.ceil(n_vars / n_cols)  # Arrondi pour couvrir tous les sous-graphiques nécessaires

    # 2. Création de la figure et de la grille de sous-graphiques
    fig, axes = plt.subplots(
        nrows=n_rows,
        ncols=n_cols,
        figsize=(width, height_per_row * n_rows)
    )

    # 3. Aplatir la grille d'axes pour itérer plus facilement
    if isinstance(axes, plt.Axes):
        # Cas particulier si n_rows=1 et n_cols=1
        axes = [axes]
    else:
        axes = axes.flatten()

    # 4. Boucle pour tracer un histogramme pour chaque variable
    for i, variable in enumerate(var_climat):
        sns.histplot(data=df, x=variable, kde=True, ax=axes[i])
        axes[i].set_title(f"Distribution de {variable}")
        axes[i].set_xlabel(variable)
        axes[i].set_ylabel("Fréquence")

    # 5. Masquer les sous-graphiques inutilisés
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    # 6. Ajustement des espacements et affichage
    plt.tight_layout()
    plt.show()
