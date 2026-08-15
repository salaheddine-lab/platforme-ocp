"""
Module de traitement des données de la GTA.
Gère l'ingestion, l'optimisation mémoire (Parquet) et les calculs thermodynamiques rigoureux.
"""

from .gestion_memoire import GestionnaireDonnees
from .bilan_isentropique import CalculateurThermodynamique

__all__ = ["GestionnaireDonnees", "CalculateurThermodynamique"]