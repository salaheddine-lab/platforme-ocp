import pandas as pd
import numpy as np
from catboost import CatBoostClassifier

class MoteurDiagnosticML:
    def __init__(self, chemin_modele="../data/traitees/modele_gta_catboost.cbm"):
        """
        Initialise le moteur IA avec le classificateur CatBoost.
        """
        self.chemin_modele = chemin_modele
        # Configuration du modèle (iterations = arbres, depth = profondeur de réflexion)
        self.modele = CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            loss_function='MultiClass',
            verbose=False # Pour ne pas inonder le terminal lors de l'entraînement
        )
        self.modele_entraine = False
        
        # Définition des variables que le modèle va observer (Features)
        self.features = [
            'Resistance_Thermique', 'Pertes_Turbine_kW', 'Pertes_Alternateur_kW', 
            'T_eau_mer_in', 'T_BP', 'P_HP'
        ]

    def preparer_donnees_entrainement(self, df_historique, df_scenarios_pannes):
        """
        Fusionne les données normales (Baseline) avec les données de défauts injectés
        pour créer le dataset d'apprentissage.
        """
        print("Préparation du dataset d'entraînement (Features & Labels)...")
        # Concaténation des données saines et des pannes simulées
        df_train = pd.concat([df_historique, df_scenarios_pannes], ignore_index=True)
        
        # Séparation des caractéristiques (X) et de la cible à prédire (y)
        X = df_train[self.features]
        y = df_train['Label_Diagnostic'] # Colonne contenant "Nominal", "Encrassement_Condenseur", etc.
        
        return X, y

    def entrainer_modele(self, X_train, y_train):
        """
        Entraîne l'algorithme CatBoost à reconnaître les signatures de pannes.
        """
        print("🚀 Début de l'entraînement de l'algorithme CatBoost...")
        self.modele.fit(X_train, y_train)
        self.modele_entraine = True
        
        # Sauvegarde du modèle sur le disque pour ne pas le ré-entraîner à chaque lancement
        self.modele.save_model(self.chemin_modele)
        print(f"✅ Modèle entraîné et sauvegardé sous : {self.chemin_modele}")

    def charger_modele(self):
        """Charge un modèle préalablement entraîné."""
        self.modele.load_model(self.chemin_modele)
        self.modele_entraine = True
        print("🧠 Modèle d'IA chargé avec succès.")

    def predire_etat(self, ligne_calculee):
        """
        Méthode utilisée en temps réel (toutes les 20 secondes) dans Streamlit.
        L'IA analyse la ligne et prédit le diagnostic avec un pourcentage de confiance.
        """
        if not self.modele_entraine:
            raise ValueError("Le modèle doit être entraîné ou chargé avant de faire des prédictions.")

        # Extraction des features de la ligne temps réel
        X_temps_reel = pd.DataFrame([ligne_calculee])[self.features]
        
        # L'IA fait sa prédiction
        prediction_classe = self.modele.predict(X_temps_reel)[0][0]
        
        # L'IA donne son niveau de certitude (probabilité)
        probabilites = self.modele.predict_proba(X_temps_reel)[0]
        confiance = max(probabilites) * 100
        
        # Déduction du code couleur pour le dashboard
        if prediction_classe == "Nominal":
            couleur = "VERT"
        elif confiance < 70: 
            couleur = "ORANGE" # L'IA suspecte quelque chose mais n'est pas certaine
        else:
            couleur = "ROUGE"

        return couleur, prediction_classe, confiance