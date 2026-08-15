import pandas as pd
import numpy as np

class InjecteurDefauts:
    def __init__(self, df_simulation):
        self.df_base = df_simulation.copy()

    def simuler_encrassement_condenseur(self, index_debut, duree):
        """Injecte une dérive thermique sur la TBP et la résistance."""
        df_defaut = self.df_base.copy()
        index_fin = index_debut + duree
        
        # Création d'une dérive de température
        derive = np.linspace(0, 5, duree) 
        df_defaut.iloc[index_debut:index_fin, df_defaut.columns.get_loc('TBP')] += derive
        
        # Étiquetage pour le Machine Learning
        df_defaut['Label_Diagnostic'] = "Nominal"
        df_defaut.iloc[index_debut:index_fin, df_defaut.columns.get_loc('Label_Diagnostic')] = "Encrassement_Condenseur"
        
        return df_defaut

    def simuler_usure_turbine(self, index_debut, duree):
        """Simule une augmentation des pertes internes isentropiques."""
        # Logique similaire pour la turbine
        pass