# 🌤️ Prédiction de la qualité de l'air en France  
## 🌡️ Les variables climatiques comme la température, les précipitations, etc. nous aident-elles pour une meilleure prédiction  
**Par [], 2024**

---

## 📋 Table des matières  
1. [🌟 INTRODUCTION](#INTRODUCTION)  
2. [🎯 Objectifs](#objectifs)  
3. [📚 Sources des données](#sources-des-données)  
4. [🗂️ Présentation du dépôt](#présentation-du-dépôt)  
5. [⚖️ Licence](#licence)  

---

## 1. 🌟 Définitions  

### Indice Atmo 🌫️ :  
L’**indice Atmo** est un indicateur qui mesure la qualité de l'air selon des seuils établis pour différents polluants (PM10, PM2.5, NO2, O3, SO2). Il est calculé quotidiennement comme le maximum des sous-indices des polluants.  

### Modèles de prévision 🤖 :  
Des modèles tels que **ARIMA**, **VAR**, et **Random Forest** sont utilisés pour analyser les séries temporelles des polluants et des variables climatiques. Ces modèles permettent de prévoir les concentrations futures en tenant compte des dépendances temporelles et des interactions entre variables.  

---

## 2. 🎯 Objectifs  

Ce projet vise à :  
1. **Analyser la qualité de l'air** en utilisant des données de polluants (PM10, PM2.5, NO2, O3, SO2).  
2. **Prédire les concentrations des polluants** sur une période future à l'aide de modèles comme **ARIMA**, **VAR**, et **Random Forest**.  
3. **Évaluer la performance des modèles** à l’aide d’un indice synthétique basé sur le RMSE des prévisions.  
4. **Intégrer les variables climatiques** (température, humidité, précipitations, etc.) pour affiner les prévisions et mieux comprendre leurs interactions avec les polluants.  

---

## 3. 📚 Sources des données  

Les données utilisées dans ce projet proviennent des sources suivantes :  
- **🌐 Open-Meteo API** : Récupération des données climatiques horaires (température, précipitations, vent, etc.).  
- **🗂️ Bases de données locales** : Données historiques des concentrations des polluants issues de mesures locales ou simulées.  
- **🔢 Scripts générés** : Synthèse des variables issues des calculs internes pour enrichir les analyses.  

---

## 4. 🗂️ Présentation du dépôt  

### Structure principale du dépôt :  
1. **Fichiers principaux :**  
   - `📓 notebook_final.ipynb` : Contient l’intégralité du projet avec les analyses et commentaires.  
   - `📓 main_executed.ipynb` : Version exécutée incluant les résultats obtenus pour chaque étape de l’analyse, même en cas d’inaccessibilité des données externes.  

2. **Dossier `scripts` :**  
   Contient des fonctions utiles, notamment :  
   - `📂 fetch_data.py` : Récupération des données climatiques.  
   - `📂 train_models.py` : Entraînement des modèles ARIMA, VAR, et Random Forest.  
   - `📂 predict.py` : Génération des prévisions futures.  
   - `📂 evaluate_models.py` : Calcul des métriques et des indices d’évaluation.  

---

## 5. ⚖️ Licence  

Ce projet est distribué sous la licence **On ne sait pas encore**. Vous êtes libre de le partager, modifier et distribuer, à condition que vos contributions respectent les mêmes termes.  
Consultez le fichier `LICENSE` pour plus de détails.  
