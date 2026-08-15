# 🏭 Plateforme de Diagnostic Intelligent - GTA (OCP Jorf Lasfar)

## 📌 Contexte du Projet
Projet d'ingénierie réalisé dans le cadre de l'optimisation des performances d'un Groupe Turbo-Alternateur (GTA). L'objectif est de passer d'une maintenance préventive calendaire à une **maintenance prédictive (Industry 4.0)**.

## 🚀 Fonctionnalités
- **Calcul Thermodynamique Temps Réel** : Bilan d'enthalpie isentropique strict (via `iapws`).
- **Intelligence Artificielle** : Algorithme `CatBoost` pour la classification et l'identification des pannes (Encrassement Condenseur, Dérive Turbine).
- **Dashboard Interactif** : Développé avec `Streamlit` pour les opérateurs en salle de contrôle.

## 🛠️ Installation
1. Activer l'environnement virtuel : `source .venv/Scripts/activate`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer la plateforme : `python main.py`