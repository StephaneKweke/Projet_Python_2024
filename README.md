# 🌤️ Prédiction de la qualité de l'air en France  
## 🌡️ Les variables climatiques comme la température, les précipitations, etc. nous aident-elles pour une meilleure prédiction? 
**Par [], 2024**

---

## 📋 Table des matières  
1. [🌟 INTRODUCTION](#INTRODUCTION)  
2. [🎯 Objectifs](#objectifs)  
3. [📚 Sources des données](#sources-des-données)  
4. [🗂️ Présentation du dépôt](#présentation-du-dépôt)  
5. [⚖️ Licence](#licence)  

---

## 1. 🌟 Introduction  

🌍 La pollution de l'air constitue l'un des enjeux environnementaux les plus préoccupants au monde entier, et en France plus particulièrement. Avec l'urbanisation croissante, l'industrialisation et la densité du trafic routier 🚗, la qualité de l'air est devenue un facteur nuisible à la santé publique 🏥, à l’environnement 🌱 et à la qualité de vie 🌬️. En France, les polluants atmosphériques tels que les particules fines (PM10, PM2.5), le dioxyde d'azote (NO₂), le dioxyde de soufre (SO₂) et l’ozone (O₃) sont étroitement mesurés en raison de leur contribution majeure aux maladies respiratoires, cardiovasculaires et à d'autres impacts environnementaux négatifs. Ces mesures demeurent une nécessité pour atténuer ces effets négatifs.

🛠️ Pour répondre à ces enjeux, notre projet repose, dans une première partie, sur l'analyse de la qualité de l'air en France à partir de l’indice ATMO. Cet indice est un indicateur synthétique utilisé en France pour évaluer la qualité de l’air 🌡️ sur une échelle standardisée, selon des seuils établis pour différents polluants (PM10, PM2.5, NO₂, O₃, SO₂). Il est calculé quotidiennement comme le maximum des sous-indices des polluants.

📈 Dans une deuxième partie, notre projet se concentre sur la prévision des concentrations des gaz polluants ci-dessus, en Île-de-France, la région la plus urbanisée et industrialisée en France 🏙️, pour la période entre le 01-12-2024 et le 14-12-2024, en se basant sur plusieurs variables climatiques (température 🌡️, pression 📉, précipitations 🌧️, …), à partir de modèles :

VAR (**Vector Auto-Regressive**) 📊 : un modèle statistique utilisé pour traiter les relations linéaires entre plusieurs variables, en considérant la dépendance de chaque variable par rapport à ses propres valeurs passées et aux valeurs passées des autres variables.
ARIMA (**AutoRegressive Integrated Moving Average**) 📈 : un modèle de séries temporelles utilisé pour comprendre et prédire les valeurs futures en tenant compte des dépendances et des valeurs passées.
RF (**Random Forest**) 🌳 : un modèle d’apprentissage utilisant les prédictions agrégées de plusieurs arbres de décision, capturant ainsi avec précision les multiples relations non linéaires entre les variables explicatives et la variable cible.
✨ Ce projet vise à fournir des outils prédictifs et des indicateurs synthétiques pour mieux comprendre et anticiper les variations de la qualité de l’air en France, contribuant à des actions concrètes pour réduire l’impact de la pollution atmosphérique.
 

---

## 2. 🎯 Objectifs  

Notre projet a donc pour objectif:
1. **Analyser la qualité de l’air.**
2. **Prédire les concentrations de polluants à travers différentes approches.**
3. **Comparer la performance de ces approches.**

# L’objectif ultime de cette démarche est donc d’essayer d’atténuer les effets néfastes de la pollution d’air sur la qualité de vie des individus et sur l’environnement dans lequel ils vivent.
 

---

## 3. 📚 Sources des données  

Les données utilisées dans ce projet proviennent des sources suivantes :  
- **🌐 Open-Meteo API** : Récupération des données climatiques horaires (température, précipitations, pression, etc.).  
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
