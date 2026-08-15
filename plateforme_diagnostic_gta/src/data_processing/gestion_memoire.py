import pandas as pd
import numpy as np
import os

class GestionnaireDonnees:
    def __init__(self, chemin_excel, chemin_parquet="../data/brutes/donnees_gta.parquet"):
        """
        Initialise le gestionnaire avec les chemins de fichiers.
        """
        self.chemin_excel = chemin_excel
        self.chemin_parquet = chemin_parquet
        self.donnees_completes = None
        self.donnees_entrainement = None
        self.donnees_simulation = None

    def preparer_et_charger_donnees(self):
        """
        Convertit l'Excel en Parquet s'il n'existe pas encore, pour accélérer les futurs chargements.
        Charge ensuite les données en mémoire.
        """
        if not os.path.exists(self.chemin_parquet):
            print(f"🔄 Première exécution : Conversion de {self.chemin_excel} en Parquet...")
            df_temp = pd.read_excel(self.chemin_excel)
            
            # Optimisation mémoire : float64 -> float32
            cols_float = df_temp.select_dtypes(include=['float64']).columns
            df_temp[cols_float] = df_temp[cols_float].astype('float32')
            
            # Sauvegarde dans le format ultra-rapide Parquet
            df_temp.to_parquet(self.chemin_parquet, engine='pyarrow', index=False)
            print("✅ Conversion terminée.")
        
        # Chargement instantané depuis le Parquet
        print("⚡ Chargement ultra-rapide des données depuis le format Parquet...")
        self.donnees_completes = pd.read_parquet(self.chemin_parquet)
        print(f"📊 Données chargées : {len(self.donnees_completes)} lignes.")

    def diviser_donnees(self, ratio_entrainement=0.7):
        """
        Divise les données pour l'apprentissage et le flux temps réel.
        """
        index_coupure = int(len(self.donnees_completes) * ratio_entrainement)
        
        self.donnees_entrainement = self.donnees_completes.iloc[:index_coupure].copy()
        self.donnees_simulation = self.donnees_completes.iloc[index_coupure:].copy()
        
        print(f"🎓 Base d'entraînement : {len(self.donnees_entrainement)} lignes.")
        print(f"🚀 Base de simulation (Temps réel) : {len(self.donnees_simulation)} lignes.")

    def generer_scenario_condenseur(self, index_debut, duree):
        """
        Injecte un défaut artificiel (hausse de la résistance thermique) dans la base de simulation.
        """
        df_scenario = self.donnees_simulation.copy()
        index_fin = index_debut + duree
        
        # Création d'une dérive progressive de +5°C sur la température d'échappement
        derive = np.linspace(0, 5, duree) 
        df_scenario.iloc[index_debut:index_fin, df_scenario.columns.get_loc('TBP')] += derive
        
        # Sauvegarde du scénario de test
        os.makedirs("../data/traitees", exist_ok=True)
        chemin_sortie = "../data/traitees/scenario_condenseur_encrasse.parquet"
        df_scenario.to_parquet(chemin_sortie, engine='pyarrow', index=False)
        print(f"⚠️ Scénario de panne généré et sauvegardé dans {chemin_sortie}")
        
        return df_scenario

# --- Bloc de test (s'exécute uniquement si vous lancez ce script directement) ---
if __name__ == "__main__":
    gestionnaire = GestionnaireDonnees(chemin_excel="../data/brutes/donnees_gta.xlsx")
    gestionnaire.preparer_et_charger_donnees()
    gestionnaire.diviser_donnees()
    gestionnaire.generer_scenario_condenseur(index_debut=100, duree=300)