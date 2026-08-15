"""
Module d'Intelligence Artificielle et de diagnostic.
Contient le modèle CatBoost et la logique de génération de scénarios de pannes.
"""

# Si vous aviez gardé la version sans ML, vous importeriez MoteurDiagnostic
from .moteur_diagnostic import MoteurDiagnosticML
from .injection_defauts import InjecteurDefauts

__all__ = ["MoteurDiagnosticML", "InjecteurDefauts"]