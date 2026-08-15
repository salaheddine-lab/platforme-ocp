import os
import subprocess

def lancer_plateforme():
    print("==================================================")
    print("🏭 Démarrage de la Plateforme Diagnostic GTA - OCP")
    print("==================================================")
    
    # Étape 1 : On pourrait rajouter ici l'appel à gestion_memoire.py 
    # pour s'assurer que le Parquet est généré avant de lancer l'UI.
    
    # Étape 2 : Lancement automatique du Dashboard Streamlit
    print("🚀 Lancement de l'interface Streamlit...")
    
    # Utilisation de subprocess pour exécuter la commande terminal depuis Python
    chemin_app = os.path.join("src", "dashboard", "app_streamlit.py")
    subprocess.run(["python", "-m", "streamlit", "run", chemin_app])

if __name__ == "__main__":
    lancer_plateforme()