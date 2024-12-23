    
def time_series_france(polluants: list, time_trends_2023, time_trends_2024):
    import pandas as pd
    import seaborn as sns
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


def time_series_regions(polluants: list, df_final):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Créer le DataFrame groupé
    time_trends_reg = df_final.groupby(['day', 'region'])[polluants].mean()

    # Réinitialiser l'index pour faciliter la manipulation
    time_trends_reg = time_trends_reg.reset_index()

    # Liste unique des régions
    regions = time_trends_reg['region'].unique()

    sns.set_theme(style="whitegrid")

    # Dimensions des sous-graphiques
    fig, axes = plt.subplots(
        nrows=(len(regions) + 1) // 2,  # Calculer le nombre de lignes
        ncols=2,
        figsize=(20, len(regions) * 3)
    )
    axes = axes.flatten()
    for i, region in enumerate(regions):
        # Filtrer les données par région
        region_data = time_trends_reg[time_trends_reg['region'] == region]

        # Filtrer les données par année
        time_trends_2023 = region_data[(region_data['day'] >= '2023-01-01') & (region_data['day'] <= '2023-12-31')]
        time_trends_2024 = region_data[(region_data['day'] >= '2024-01-01') & (region_data['day'] <= '2024-12-31')]

        # Traçage des tendances pour 2023
        time_trends_2023.set_index('day')[polluants].plot(
            ax=axes[i],
            linewidth=1,
            linestyle="-",
            alpha=0.7,
            color=sns.color_palette("tab10", n_colors=len(polluants)),
            label=[f"{pollutant} (2023)" for pollutant in polluants]
        )

        # Traçage des tendances pour 2024
        time_trends_2024.set_index('day')[polluants].plot(
            ax=axes[i],
            linewidth=1.5,
            linestyle="--",
            alpha=0.9,
            color=sns.color_palette("tab10", n_colors=len(polluants)),
            label=[f"{pollutant} (2024)" for pollutant in polluants]
        )

        # Ajuster le titre, les axes et la légende
        axes[i].set_title(f"Tendances des polluants ({region})", fontsize=14)
        axes[i].set_xlabel("Jour", fontsize=12)
        axes[i].set_ylabel("Concentration moyenne (µg/m³)", fontsize=12)
        axes[i].tick_params(axis='x', labelsize=10)
        axes[i].tick_params(axis='y', labelsize=10)
        axes[i].legend(fontsize=10)

    # Supprimer les axes inutilisés
    for j in range(len(regions), len(axes)):
        fig.delaxes(axes[j])

    # Ajustement global
    plt.tight_layout()
    plt.show()

    
  