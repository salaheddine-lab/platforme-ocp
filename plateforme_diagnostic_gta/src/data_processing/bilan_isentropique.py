import pandas as pd
from iapws import IAPWS97

class CalculateurThermodynamique:
    def __init__(self):
        """
        Initialise le module de calcul thermodynamique de la plateforme.
        Ce module rejette les approximations génériques et se base sur 
        le bilan d'enthalpie isentropique strict.
        """
        pass

    def calculer_enthalpie_eau_vapeur(self, pression_bar, temperature_celsius):
        """
        Calcule l'enthalpie réelle (kJ/kg) et l'entropie (kJ/kg.K) à partir de P et T.
        Utilise les tables de la vapeur IAPWS97.
        """
        # Conversion bar -> MPa et Celsius -> Kelvin pour la librairie IAPWS
        pression_mpa = pression_bar / 10
        temp_kelvin = temperature_celsius + 273.15
        
        etat = IAPWS97(P=pression_mpa, T=temp_kelvin)
        return etat.h, etat.s

    def calculer_enthalpie_isentropique(self, pression_sortie_bar, entropie_admission):
        """
        Calcule l'enthalpie isentropique idéale (h_is) à la pression de sortie,
        en conservant l'entropie de l'état d'admission.
        """
        pression_mpa = pression_sortie_bar / 10
        etat_isentropique = IAPWS97(P=pression_mpa, s=entropie_admission)
        return etat_isentropique.h

    def enrichir_donnees(self, df_ligne):
        """
        Prend une ligne de données (temps réel) et calcule tous les indicateurs 
        de performance et de pertes en kW.
        """
        ligne_enrichie = df_ligne.copy()
        
        # 1. Calcul des états d'admission (HP)
        h_admission, s_admission = self.calculer_enthalpie_eau_vapeur(
            ligne_enrichie['P_HP'], ligne_enrichie['T_HP']
        )
        
        # 2. Calcul des états d'échappement réels et isentropiques (BP)
        h_echappement_reel, _ = self.calculer_enthalpie_eau_vapeur(
            ligne_enrichie['P_BP'], ligne_enrichie['T_BP']
        )
        h_echappement_is = self.calculer_enthalpie_isentropique(
            ligne_enrichie['P_BP'], s_admission
        )
        
        # 3. Calcul des puissances et pertes (avec conversion t/h -> kg/s)
        debit_kg_s = ligne_enrichie['Debit_HP'] / 3.6
        
        # Puissance Isentropique (théorique maximale)
        puissance_is = debit_kg_s * (h_admission - h_echappement_is)
        
        # Puissance Mécanique réelle sur l'arbre
        puissance_meca = debit_kg_s * (h_admission - h_echappement_reel)
        
        # Bilan de pertes
        ligne_enrichie['Pertes_Turbine_kW'] = puissance_is - puissance_meca
        ligne_enrichie['Pertes_Alternateur_kW'] = puissance_meca - ligne_enrichie['Welec']
        
        # 4. Calcul de la Résistance Thermique du condenseur (Rth)
        enthalpie_liquide_sature = IAPWS97(P=ligne_enrichie['P_BP']/10, x=0).h
        Q_condenseur_kW = abs(debit_kg_s * (h_echappement_reel - enthalpie_liquide_sature))
        
        delta_T = ligne_enrichie['T_BP'] - ligne_enrichie['T_eau_mer_in']
        
        # Sécurité pour éviter la division par zéro
        if Q_condenseur_kW > 0:
            ligne_enrichie['Resistance_Thermique'] = delta_T / Q_condenseur_kW
        else:
            ligne_enrichie['Resistance_Thermique'] = 0
            
        return ligne_enrichie

# --- Test du module ---
if __name__ == "__main__":
    # Test avec une ligne fictive représentant un régime stabilisé
    donnees_test = pd.Series({
        'P_HP': 60.0, 'T_HP': 480.0, 'Debit_HP': 120.0, 
        'P_BP': 0.08, 'T_BP': 41.5, 'T_eau_mer_in': 18.0, 
        'Welec': 28500.0
    })
    
    calculateur = CalculateurThermodynamique()
    resultat = calculateur.enrichir_donnees(donnees_test)
    
    print(f"Pertes internes Turbine : {resultat['Pertes_Turbine_kW']:.2f} kW")
    print(f"Résistance Thermique Condenseur : {resultat['Resistance_Thermique']:.6f} K/kW")