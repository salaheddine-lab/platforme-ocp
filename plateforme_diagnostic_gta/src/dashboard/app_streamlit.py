import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import os

# --- Configuration globale de la page ---
st.set_page_config(page_title="Monitoring GTA | OCP", page_icon="🏭", layout="wide")

# --- Gestion robuste des chemins d'accès aux assets (indépendant du système d'exploitation) ---
dossier_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_fond = os.path.join(dossier_actuel, "../../assets/OIP (1).jpg")
chemin_logo = os.path.join(dossier_actuel, "../../assets/Ocp-Logo-Vector.svg-.png")

# --- 🎨 FONCTIONS DE DESIGN ET CSS ---
def get_base64_of_bin_file(bin_file):
    """Permet d'encoder l'image locale pour l'utiliser en CSS."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def appliquer_css_personnalise():
    """Applique la charte graphique OCP (Vert) et l'image de fond."""
    try:
        # Chargement de l'image de fond minière via le chemin absolu sécurisé
        img_base64 = get_base64_of_bin_file(chemin_fond)
        bg_css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
    except FileNotFoundError:
        bg_css = "<style>.stApp { background-color: #f0f2f6; }</style>"

    # CSS pour la barre latérale verte OCP et le style général
    custom_css = bg_css + """
    <style>
        /* Couleur verte OCP pour la barre latérale */
        [data-testid="stSidebar"] {
            background-color: #007A33 !important; 
        }
        /* Texte en blanc dans la barre latérale */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        /* Style du formulaire de connexion au centre */
        .login-box {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
            text-align: center;
        }
        .contact-link {
            text-align: right;
            padding: 10px;
            font-weight: bold;
            color: #007A33;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# --- 🔐 GESTION DE L'AUTHENTIFICATION ---
if 'authentifie' not in st.session_state:
    st.session_state['authentifie'] = False

def page_connexion():
    """Affiche la page de login avec l'image de fond."""
    appliquer_css_personnalise()
    
    # En-tête avec Contact
    st.markdown('<div class="contact-link"><a href="mailto:contact@ocpgroup.ma" style="color:white; text-decoration:none; text-shadow: 1px 1px 2px black;">📞 Contactez-nous</a></div>', unsafe_allow_html=True)
    
    # Espacement pour centrer la boîte
    st.write("<br><br><br>", unsafe_allow_html=True)
    
    # Création d'une boîte centrée pour le login
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Affichage du logo officiel OCP sécurisé
        try:
            st.image(chemin_logo, width=180)
        except:
            st.markdown("### 🟢 Groupe OCP")
            
        st.markdown("### Accès Plateforme GTA")
        st.markdown("---")
        
        # Formulaire Streamlit
        with st.form("login_form"):
            utilisateur = st.text_input("Nom d'utilisateur")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            bouton_login = st.form_submit_button("Se connecter", use_container_width=True)
            
            if bouton_login:
                if utilisateur == "admin" and mot_de_passe == "admin":
                    st.session_state['authentifie'] = True
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")
                    
        st.markdown('</div>', unsafe_allow_html=True)

# --- 📊 FONCTION DE SIMULATION (Bouchon) ---
def generer_ligne_simulee(iteration):
    rth_base = 0.00012 + (iteration * 0.000002)
    pertes_turb_base = 1200 + np.random.normal(0, 10)
    return {
        'Temps': pd.Timestamp.now().strftime('%H:%M:%S'),
        'Resistance_Thermique': rth_base,
        'Pertes_Turbine_kW': pertes_turb_base,
        'Welec_kW': 28500 - (pertes_turb_base - 1200),
        'Diagnostic': "Fonctionnement Nominal", 'Couleur': "green"
    }

# --- 📈 DASHBOARD PRINCIPAL ---
def page_dashboard():
    """Affiche le tableau de bord une fois connecté."""
    st.markdown("""
    <style>
        .stApp { background-image: none !important; background-color: #f4f6f9 !important; }
        [data-testid="stSidebar"] { background-color: #007A33 !important; }
        [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    # --- BARRE LATÉRALE (Navigation) ---
    try:
        st.sidebar.image(chemin_logo, width=150)
    except:
        st.sidebar.markdown("### 🟢 OCP")
        
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "📌 Menu de Navigation",
        ["📊 Monitoring Temps Réel", "🔍 Analyse Thermodynamique", "⚙️ Paramètres IA"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Déconnexion"):
        st.session_state['authentifie'] = False
        st.rerun()

    if menu == "📊 Monitoring Temps Réel":
        st.title("Monitoring Dynamique du Groupe Turbo-Alternateur")
        
        run_sim = st.checkbox("▶️ Démarrer l'acquisition des données (Simulation)")
        
        col1, col2, col3 = st.columns(3)
        kpi_rth = col1.empty()
        kpi_pertes = col2.empty()
        kpi_welec = col3.empty()
        chart_box = st.empty()
        
        if 'historique' not in st.session_state:
            st.session_state.historique = pd.DataFrame(columns=['Temps', 'Resistance_Thermique', 'Pertes_Turbine_kW', 'Welec_kW'])
            st.session_state.iter = 0

        if run_sim:
            while True:
                st.session_state.iter += 1
                nv_donnee = generer_ligne_simulee(st.session_state.iter)
                st.session_state.historique = pd.concat([st.session_state.historique, pd.DataFrame([nv_donnee])], ignore_index=True).tail(50)
                
                kpi_rth.metric("Résistance Thermique Condenseur", f"{nv_donnee['Resistance_Thermique']:.6f} K/kW")
                kpi_pertes.metric("Pertes Turbine", f"{nv_donnee['Pertes_Turbine_kW']:.0f} kW")
                kpi_welec.metric("Puissance Électrique", f"{nv_donnee['Welec_kW']:.0f} kW")
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Scatter(x=st.session_state.historique['Temps'], y=st.session_state.historique['Resistance_Thermique'], name="Rth", line=dict(color='red')), secondary_y=False)
                fig.add_trace(go.Scatter(x=st.session_state.historique['Temps'], y=st.session_state.historique['Pertes_Turbine_kW'], name="Pertes Turbine", line=dict(color='orange', dash='dot')), secondary_y=True)
                
                fig.update_layout(title="Évolution Thermodynamique", height=400)
                chart_box.plotly_chart(fig, use_container_width=True)
                time.sleep(2)

    elif menu == "🔍 Analyse Thermodynamique":
        st.title("Analyse des Bilan d'Enthalpie Isentropique")
        st.info("Cette page affichera les calculs détaillés issus des manuels de formation de l'usine, basés strictement sur l'enthalpie isentropique.")

    elif menu == "⚙️ Paramètres IA":
        st.title("Configuration du Modèle CatBoost")
        st.warning("L'entraînement du modèle nécessite un accès administrateur de niveau 2.")

# --- ROUTAGE PRINCIPAL ---
if not st.session_state['authentifie']:
    page_connexion()
else:
    page_dashboard()