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

# --- Gestion robuste des chemins d'accès aux assets ---
dossier_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_fond = os.path.join(dossier_actuel, "../../assets/OIP (1).jpg")
chemin_logo = os.path.join(dossier_actuel, "../../assets/Ocp-Logo-Vector.svg-.png")

# --- FONCTIONS DE DESIGN ET CSS ---
def get_base64_of_bin_file(bin_file):
    """Permet d'encoder l'image locale pour l'utiliser en CSS."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- GESTION DE L'AUTHENTIFICATION ---
if 'authentifie' not in st.session_state:
    st.session_state['authentifie'] = False

def page_connexion():
    """Affiche la page de login avec le design en deux colonnes (carte blanche centrale)."""
    img_b64 = get_base64_of_bin_file(chemin_fond)
    
    custom_css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        [data-testid="stSidebar"] {{
            background-color: #007A33 !important; 
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        .login-box-container {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.write("<br><br><br>", unsafe_allow_html=True)
    
    col_ext1, col_centre, col_ext2 = st.columns([1, 2.2, 1])
    
    with col_centre:
        st.markdown('<div class="login-box-container">', unsafe_allow_html=True)
        col_logo, col_form = st.columns([1, 1.2], gap="medium")
        
        with col_logo:
            st.write("<br><br>", unsafe_allow_html=True)
            if os.path.exists(chemin_logo):
                st.image(chemin_logo, width=180)
            else:
                st.markdown("### 🟢 Groupe OCP")
                
        with col_form:
            st.markdown("<h3 style='color: #2c3e50; font-size: 20px; margin-bottom: 0px;'>Bienvenue sur votre portail GTA</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 13px;'>Merci de rentrer votre identifiant et mot de passe</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                utilisateur = st.text_input("Identifiant *")
                mot_de_passe = st.text_input("Mot de passe *", type="password")
                st.write("")
                bouton_login = st.form_submit_button("Se connecter", use_container_width=True)
                
                if bouton_login:
                    if utilisateur == "admin" and mot_de_passe == "admin":
                        st.session_state['authentifie'] = True
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- FONCTION DE SIMULATION ---
def generer_ligne_simulee(iteration):
    rth_base = 0.00012 + (iteration * 0.000001)
    pertes_turb = 1200 + np.random.normal(0, 15)
    pertes_alt = 350 + np.random.normal(0, 5)
    rendement = 88.5 - (iteration * 0.01)
    
    if rth_base > 0.00013:
        alerte = "⚠️ Attention : Encrassement détecté sur le condenseur !"
    elif pertes_turb > 1250:
        alerte = "⚠️ Alerte : Pertes thermiques élevées sur la turbine !"
    else:
        alerte = "✅ Système stable - Fonctionnement nominal optimal."

    return {
        'Temps': pd.Timestamp.now().strftime('%H:%M:%S'),
        'Rendement': max(70.0, min(95.0, rendement)),
        'Resistance_Thermique': rth_base,
        'Pertes_Turbine_kW': max(1000, pertes_turb),
        'Pertes_Alternateur_kW': max(200, pertes_alt),
        'Alerte': alerte
    }

# --- DASHBOARD PRINCIPAL ---
def page_dashboard():
    """Affiche le tableau de bord avec la barre supérieure et l'espace Accueil."""
    st.markdown("""
    <style>
        .stApp { background-image: none !important; background-color: #f4f6f9 !important; }
        [data-testid="stSidebar"] { background-color: #007A33 !important; }
        [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    # --- BARRE SUPÉRIEURE (Top Header Navbar) ---
    header_col1, header_col2, header_col3 = st.columns([2, 5, 2.5])
    
    with header_col1:
        if os.path.exists(chemin_logo):
            st.image(chemin_logo, width=130)
        else:
            st.markdown("### 🟢 OCP Jorf Lasfar")
            
    with header_col3:
        user_col1, user_col2 = st.columns([3, 2])
        with user_col1:
            st.markdown("<p style='margin-top: 10px; font-weight: bold; color: #2c3e50; text-align: right;'>👤 Salah Eddine AKI</p>", unsafe_allow_html=True)
        with user_col2:
            if st.button("🚪 Déconnexion", use_container_width=True):
                st.session_state['authentifie'] = False
                st.rerun()

    st.markdown("<hr style='margin: 0px 0px 20px 0px;'>", unsafe_allow_html=True)

    # --- BARRE LATÉRALE ---
    st.sidebar.markdown("### 🧭 Menu Principal")
    menu = st.sidebar.radio(
        "Navigation",
        ["🏠 Accueil", "🔍 Analyse Thermodynamique", "⚙️ Paramètres IA"],
        label_visibility="collapsed"
    )

    # --- INITIALISATION DE L'HISTORIQUE ---
    if 'historique' not in st.session_state:
        st.session_state.historique = pd.DataFrame(columns=[
            'Temps', 'Rendement', 'Resistance_Thermique', 'Pertes_Turbine_kW', 'Pertes_Alternateur_kW', 'Alerte'
        ])
        st.session_state.iter = 0

    # ================= PAGE ACCUEIL =================
    if menu == "🏠 Accueil":
        st.title("🏭 Tableau de Bord - Groupe Turbo-Alternateur (GTA)")
        st.markdown("Suivi en temps réel des performances énergétiques et thermodynamiques.")
        
        col_ctrl1, col_ctrl2 = st.columns([1, 4])
        with col_ctrl1:
            run_sim = st.toggle("▶️ Activer le flux live", value=True)
            
        st.markdown("---")
        
        # 1. SECTION ALERTES EN TEMPS REEL
        st.subheader("🚨 Centre d'Alertes et Diagnostics")
        alerte_placeholder = st.empty()
        
        # 2. SECTION 4 BLOCS DE CALCULS CLÉS
        st.markdown("### 📊 Indicateurs de Performance en Temps Réel")
        col1, col2, col3, col4 = st.columns(4)
        
        kpi_rend = col1.empty()
        kpi_rth = col2.empty()
        kpi_turb = col3.empty()
        kpi_alt = col4.empty()
        
        st.markdown("---")
        
        # 3. GRAPHIQUE D'EVOLUTION ESTHÉTIQUE
        chart_box = st.empty()

        if run_sim:
            st.session_state.iter += 1
            nv_donnee = generer_ligne_simulee(st.session_state.iter)
            st.session_state.historique = pd.concat(
                [st.session_state.historique, pd.DataFrame([nv_donnee])], 
                ignore_index=True
            ).tail(30)
            
            if "Attention" in nv_donnee['Alerte'] or "Alerte" in nv_donnee['Alerte']:
                alerte_placeholder.error(nv_donnee['Alerte'])
            else:
                alerte_placeholder.success(nv_donnee['Alerte'])
                
            kpi_rend.metric("Rendement Global", f"{nv_donnee['Rendement']:.2f} %", delta="+0.1%")
            kpi_rth.metric("Résistance d'Encrassement", f"{nv_donnee['Resistance_Thermique']:.6f} K/kW")
            kpi_turb.metric("Pertes Turbine", f"{nv_donnee['Pertes_Turbine_kW']:.1f} kW", delta="-5 kW", delta_color="inverse")
            kpi_alt.metric("Pertes Alternateur", f"{nv_donnee['Pertes_Alternateur_kW']:.1f} kW")
            
            # --- CREATION DU GRAPHIQUE DESIGN ET PROFESSIONNEL ---
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Courbe de rendement stylisée (Vert OCP, lissée, avec points)
            fig.add_trace(go.Scatter(
                x=st.session_state.historique['Temps'], 
                y=st.session_state.historique['Rendement'], 
                name="Rendement (%)", 
                mode='lines+markers',
                line=dict(color='#007A33', width=3, shape='spline'),
                marker=dict(size=6, color='#007A33')
            ), secondary_y=False)
            
            # Courbe d'encrassement stylisée (Rouge élégant, pointillée)
            fig.add_trace(go.Scatter(
                x=st.session_state.historique['Temps'], 
                y=st.session_state.historique['Resistance_Thermique'], 
                name="Rth (K/kW)", 
                mode='lines+markers',
                line=dict(color='#E74C3C', width=2.5, dash='dot', shape='spline'),
                marker=dict(size=5, color='#E74C3C')
            ), secondary_y=True)
            
            # Mise en page moderne et soignée
            fig.update_layout(
                template='plotly_white',
                title=dict(
                    text="<b>Évolution Dynamique : Rendement Global & Résistance d'Encrassement</b>",
                    font=dict(size=15, color='#2c3e50')
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=20, t=50, b=20),
                hovermode="x unified",
                height=400
            )
            
            # Grilles et axes propres
            fig.update_xaxes(showgrid=True, gridcolor='#f0f2f6', linecolor='#dcdcdc')
            fig.update_yaxes(title_text="<b>Rendement (%)</b>", secondary_y=False, showgrid=True, gridcolor='#f0f2f6', linecolor='#dcdcdc')
            fig.update_yaxes(title_text="<b>Résistance Thermique (K/kW)</b>", secondary_y=True, showgrid=False, linecolor='#dcdcdc')
            
            chart_box.plotly_chart(fig, use_container_width=True)
            
            time.sleep(2)
            st.rerun()

    # ================= PAGE ANALYSE =================
    elif menu == "🔍 Analyse Thermodynamique":
        st.title("🔍 Analyse Détaillée - Bilan d'Enthalpie")
        st.info("Module dédié aux calculs thermodynamiques stricts issus des manuels de formation de l'usine.")

    # ================= PAGE PARAMETRES =================
    elif menu == "⚙️ Paramètres IA":
        st.title("⚙️ Paramètres & Modèle CatBoost")
        st.warning("Espace réservé à la configuration des hyperparamètres du modèle prédictif.")

# --- ROUTAGE PRINCIPAL ---
if not st.session_state['authentifie']:
    page_connexion()
else:
    page_dashboard()