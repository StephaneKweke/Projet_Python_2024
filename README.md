# 🌤️ Prédiction de la qualité de l'air en France  
**Par [NOUTSOUGAN Komla Dominique, KWEKE NGAHANE Stéphane Evrad, RIAD Yahia], 2024**

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

* ARIMA (**AutoRegressive Integrated Moving Average**) 📈 : un modèle de séries temporelles utilisé pour comprendre et prédire les valeurs futures en tenant compte des dépendances et des valeurs passées.

* VAR (**Vector Auto-Regressive**) 📊 : un modèle statistique utilisé pour traiter les relations linéaires entre plusieurs variables, en considérant la dépendance de chaque variable par rapport à ses propres valeurs passées et aux valeurs passées des autres variables.

* RF (**Random Forest**) 🌳 : un modèle d’apprentissage utilisant les prédictions agrégées de plusieurs arbres de décision, capturant ainsi avec précision les multiples relations non linéaires entre les variables explicatives et la variable cible.

  
✨ Ce projet vise à fournir des outils prédictifs et des indicateurs synthétiques pour mieux comprendre et anticiper les variations de la qualité de l’air en France, contribuant à des actions concrètes pour réduire l’impact de la pollution atmosphérique.
 

---

## 2. 🎯 Objectifs  

Notre projet a donc pour objectif:
1. **Analyser la qualité de l’air en France.**
2. **Prédire les concentrations de polluants à travers différentes approches.**
3. **Comparer la performance de ces approches.**
4. **Evaluer si les variables climatiques permettent d'améliorer les prévisions de la qualité de l'air**

### L’objectif ultime de cette démarche est donc d’essayer d’atténuer les effets néfastes de la pollution d’air sur la qualité de vie des individus et sur l’environnement dans lequel ils vivent.
 

---

## 3. 📚 Sources des données  

Les données utilisées dans ce projet proviennent des sources suivantes :  
- **🌐 Open-Meteo API** : Récupération des données de qualité de l'air et des données climatiques horaires (température, précipitations, pression, etc.). https://open-meteo.com/en/docs/air-quality-api
- **🗂️ Bases de données de l'INSEE** : Données cartographiques sur les régions.  

---

## 4. 🗂️ Présentation du dépôt  

### Structure principale du dépôt :  
1. **Fichiers principaux :**  
   - `📓 notebook_final.ipynb` : Contient l’intégralité du projet avec les analyses et commentaires.  
   - `📓 Infos_géographiques_france.ipynb` : Contient les données géographiques de la France ainsi que les centroïdes des régions
   - `📓 Base_de_données_final.ipynb` : Contient le code necessaire pour construire la base de données finale par API
   - `📓 Statdesc.ipynb` : Contient le code necessaire à la constitution des statistiques descriptives du projet ( notes : il a servi de base pour la constitution du notebook, car il a servi à la création de fonctions de visualisation pour améliorer la lisibilité du projet)
     
2. **Dossier `scripts` :**  
   Contient des fichiers de fonctions, notamment :  
   - `api.py` : contient les fonctions de récupération des données par API.  
   - `dataviz.py` : contient toutes les fonctions de visualisation des des données (graphiques,...)
   - `modele.py ` : contient des fonctions utiles à la modélisation, en l'occurence les tests de stationnarité, les prévisions...  
   - `indice.py` : Contient les fonctions necessaires au calcul des sous-indices ainsi que de l'indice ATMO 

---

## 5. ⚖️ Licence  

Ce projet est distribué sous la licence **GNU General Public License (GPL)**. Vous êtes libre de le partager, modifier et distribuer, à condition que vos contributions respectent les mêmes termes.  
Consultez le fichier `LICENSE` pour plus de détails.  
