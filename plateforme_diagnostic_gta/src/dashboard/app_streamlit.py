import base64
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Dashboard GTA",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Gestion de l'état d'authentification et du nom d'utilisateur
# ---------------------------------------------------------------------------
if 'authentifie' not in st.session_state:
    st.session_state['authentifie'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = "admin"

# ---------------------------------------------------------------------------
# Logo OCP pour la barre supérieure (en PNG s'il existe)
# ---------------------------------------------------------------------------
dossier_actuel = Path(__file__).parent
LOGO_PATH = dossier_actuel / "../../assets/ocp_logo.png"
if not LOGO_PATH.exists():
    LOGO_PATH = dossier_actuel / "../../assets/Ocp-Logo-Vector.svg-.png"

# ---------------------------------------------------------------------------
# Page de Connexion (Fidèle à votre code HTML d'origine)
# ---------------------------------------------------------------------------
def page_connexion():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', Arial, sans-serif;
        }

        #MainMenu, header, footer {visibility: hidden;}

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.03), transparent 40%),
                linear-gradient(135deg, #3a3a3a 0%, #1c1c1c 45%, #101010 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
            max-width: 760px;
        }

        /* ---- Carte de connexion ---- */
        .login-card {
            background: #ffffff;
            border-radius: 22px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.45);
            padding: 46px 52px 46px 44px;
            display: flex;
            width: 720px;
            max-width: 90vw;
            margin: auto;
        }

        .card-left {
            flex: 0 0 40%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        /* ---- Logo OCP vectoriel natif ---- */
        .ocp-logo {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }

        .ocp-mark {
            display: flex;
            align-items: center;
            gap: 2px;
        }

        .ocp-mark .letter {
            font-size: 64px;
            font-weight: 700;
            color: #1a5632;
            letter-spacing: 2px;
            line-height: 1;
        }

        .ocp-mark .accent-o {
            position: relative;
            display: inline-block;
            width: 62px;
            height: 62px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2e7d46 0%, #1a5632 100%);
            margin-right: 4px;
        }

        .ocp-underline {
            width: 100%;
            height: 3px;
            background: #2e7d46;
            margin-top: 6px;
        }

        .ocp-subtitle {
            font-size: 13px;
            letter-spacing: 6px;
            color: #6b6b6b;
            font-weight: 600;
            margin-top: 10px;
        }

        .card-right {
            flex: 1;
            padding-left: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .welcome-title {
            font-size: 26px;
            font-weight: 500;
            color: #6b7280;
            line-height: 1.3;
        }

        .welcome-title b {
            color: #374151;
            font-weight: 700;
        }

        .welcome-sub {
            margin-top: 14px;
            margin-bottom: 6px;
            font-size: 14px;
            color: #6b7280;
            line-height: 1.5;
        }

        /* ---- Champs de saisie (Streamlit widgets) ---- */
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] p {
            font-size: 13px !important;
            color: #14b391 !important;
            font-weight: 500 !important;
            margin-bottom: 2px !important;
        }

        div[data-testid="stTextInput"] input {
            font-family: 'Poppins', Arial, sans-serif;
            font-size: 15px;
            color: #374151;
        }

        div[data-testid="stTextInput"]:nth-of-type(1) > div > div {
            border: none;
            border-bottom: 1px solid #e5e7eb;
            border-radius: 0;
            background: transparent;
            padding-left: 0;
        }

        div[data-testid="stTextInput"]:nth-of-type(2) > div > div {
            background: #eef0fb;
            border-radius: 6px;
            border: none;
        }

        /* Bouton Connecter */
        div.stButton > button {
            background: #14b391;
            color: #ffffff;
            border: none;
            padding: 12px 34px;
            border-radius: 24px;
            font-size: 15px;
            font-weight: 600;
            font-family: 'Poppins', Arial, sans-serif;
            margin-top: 18px;
            transition: background 0.2s ease;
            width: auto !important;
        }

        div.stButton > button:hover {
            background: #109c7f;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="login-card">
            <div class="card-left">
                <div class="ocp-logo">
                    <div class="ocp-mark">
                        <span class="accent-o"></span>
                        <span class="letter">CP</span>
                    </div>
                    <div class="ocp-underline"></div>
                    <div class="ocp-subtitle">GROUPE OCP</div>
                </div>
            </div>
            <div class="card-right" id="form-container">
                <div class="welcome-title">Bienvenue sur votre<br><b>Dashboard GTA</b></div>
                <div class="welcome-sub">Merci de rentrer votre identifiant et mot de passe</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        identifiant = st.text_input("Identifiant *", value="admin", placeholder="ex: admin")
        mot_de_passe = st.text_input("Mot de passe *", type="password", value="1234567", placeholder="••••••••")
        submit = st.form_submit_button("Connecter")

        if submit:
            if identifiant and mot_de_passe:
                st.session_state['authentifie'] = True
                st.session_state['username'] = identifiant
                st.rerun()
            else:
                st.error("Merci de renseigner votre identifiant et votre mot de passe.")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Fonction de Simulation en temps réel
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Tableau de Bord Principal (Post-Connexion)
# ---------------------------------------------------------------------------
def page_dashboard():
    st.markdown("""
    <style>
        .stApp { background-image: none !important; background-color: #f4f6f9 !important; }
        
        /* Sidebar étroite (~2cm / 85px) avec fond vert OCP */
        section[data-testid="stSidebar"] {
            background-color: #007A33 !important;
            width: 85px !important;
            min-width: 85px !important;
        }
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Barre supérieure compacte (~2 cm de hauteur) avec Logo OCP, username et déconnexion ---
    col_nav_logo, col_nav_user = st.columns([2, 2])
    
    with col_nav_logo:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=110)
        else:
            st.markdown("### 🟢 OCP")
            
    with col_nav_user:
        cols_right = st.columns([3, 2])
        with cols_right[0]:
            st.markdown(f"<p style='margin-top: 10px; font-weight: bold; color: #2c3e50; text-align: right;'>👤 {st.session_state['username']}</p>", unsafe_allow_html=True)
        with cols_right[1]:
            if st.button("🚪 Se déconnecter", use_container_width=True):
                st.session_state['authentifie'] = False
                st.rerun()

    st.markdown("<hr style='margin: 0px 0px 20px 0px;'>", unsafe_allow_html=True)

    # --- Sidebar étroite avec les rubriques demandées ---
    with st.sidebar:
        st.markdown("<h3 style='text-align: center; color: #ffffff; font-size: 16px;'>GTA</h3>", unsafe_allow_html=True)
        menu = st.sidebar.radio(
            "Menu",
            [
                "🏠 Accueil", 
                "📈 Rendement", 
                "🌡️ Résistance d'encrassement", 
                "⚡ Perte turbine", 
                "🔌 Perte alternateur"
            ],
            label_visibility="collapsed"
        )

    if 'historique' not in st.session_state:
        st.session_state.historique = pd.DataFrame(columns=[
            'Temps', 'Rendement', 'Resistance_Thermique', 'Pertes_Turbine_kW', 'Pertes_Alternateur_kW', 'Alerte'
        ])
        st.session_state.iter = 0

    st.session_state.iter += 1
    nv_donnee = generer_ligne_simulee(st.session_state.iter)
    st.session_state.historique = pd.concat(
        [st.session_state.historique, pd.DataFrame([nv_donnee])], 
        ignore_index=True
    ).tail(30)

    # ================= 1. ACCUEIL =================
    if menu == "🏠 Accueil":
        st.title("🏭 Tableau de Bord - Accueil & Alertes")
        st.markdown("Centre de supervision et messages d'alerte en temps réel du Groupe Turbo-Alternateur.")
        st.markdown("---")
        
        st.subheader("🚨 Centre d'Alertes et Diagnostics")
        if "Attention" in nv_donnee['Alerte'] or "Alerte" in nv_donnee['Alerte']:
            st.error(nv_donnee['Alerte'])
        else:
            st.success(nv_donnee['Alerte'])
            
        st.info("ℹ️ Utilisez la barre latérale étroite de gauche pour naviguer entre les différentes sections de calcul et d'analyse.")

    # ================= 2. RENDEMENT =================
    elif menu == "📈 Rendement":
        st.title("📈 Analyse & Calcul du Rendement")
        st.markdown("Suivi de la courbe d'évolution du rendement global du système en temps réel.")
        st.markdown("---")
        
        st.metric("Rendement Actuel", f"{nv_donnee['Rendement']:.2f} %", delta="+0.1%")
        
        fig_rend = go.Figure()
        fig_rend.add_trace(go.Scatter(
            x=st.session_state.historique['Temps'], 
            y=st.session_state.historique['Rendement'], 
            name="Rendement (%)", 
            mode='lines+markers',
            line=dict(color='#007A33', width=3, shape='spline'),
            marker=dict(size=6, color='#007A33')
        ))
        fig_rend.update_layout(
            template='plotly_white',
            title="<b>Courbe du Calcul du Rendement en Temps Réel</b>",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig_rend, use_container_width=True)

    # ================= 3. RESISTANCE D'ENCRASSEMENT =================
    elif menu == "🌡️ Résistance d'encrassement":
        st.title("🌡️ Résistance d'Encrassement")
        st.markdown("Suivi thermique de l'encrassement du condenseur.")
        st.markdown("---")
        
        st.metric("Résistance Thermique (Rth)", f"{nv_donnee['Resistance_Thermique']:.6f} K/kW")
        
        fig_rth = go.Figure()
        fig_rth.add_trace(go.Scatter(
            x=st.session_state.historique['Temps'], 
            y=st.session_state.historique['Resistance_Thermique'], 
            name="Rth (K/kW)", 
            mode='lines+markers',
            line=dict(color='#E74C3C', width=2.5, shape='spline'),
            marker=dict(size=6, color='#E74C3C')
        ))
        fig_rth.update_layout(
            template='plotly_white',
            title="<b>Évolution de la Résistance Thermique d'Encrassement</b>",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig_rth, use_container_width=True)

    # ================= 4. PERTE TURBINE =================
    elif menu == "⚡ Perte turbine":
        st.title("⚡ Calcul des Pertes Turbine")
        st.markdown("Analyse des pertes thermiques et mécaniques au niveau de la turbine.")
        st.markdown("---")
        
        st.metric("Pertes Turbine", f"{nv_donnee['Pertes_Turbine_kW']:.1f} kW", delta="-5 kW", delta_color="inverse")
        
        fig_turb = go.Figure()
        fig_turb.add_trace(go.Scatter(
            x=st.session_state.historique['Temps'], 
            y=st.session_state.historique['Pertes_Turbine_kW'], 
            name="Pertes Turbine (kW)", 
            mode='lines+markers',
            line=dict(color='#F39C12', width=3, shape='spline'),
            marker=dict(size=6, color='#F39C12')
        ))
        fig_turb.update_layout(
            template='plotly_white',
            title="<b>Évolution des Pertes de la Turbine</b>",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig_turb, use_container_width=True)

    # ================= 5. PERTE ALTERNATEUR =================
    elif menu == "🔌 Perte alternateur":
        st.title("🔌 Calcul des Pertes Alternateur")
        st.markdown("Analyse des pertes énergétiques et électriques au niveau de l'alternateur.")
        st.markdown("---")
        
        st.metric("Pertes Alternateur", f"{nv_donnee['Pertes_Alternateur_kW']:.1f} kW")
        
        fig_alt = go.Figure()
        fig_alt.add_trace(go.Scatter(
            x=st.session_state.historique['Temps'], 
            y=st.session_state.historique['Pertes_Alternateur_kW'], 
            name="Pertes Alternateur (kW)", 
            mode='lines+markers',
            line=dict(color='#8E44AD', width=3, shape='spline'),
            marker=dict(size=6, color='#8E44AD')
        ))
        fig_alt.update_layout(
            template='plotly_white',
            title="<b>Évolution des Pertes de l'Alternateur</b>",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig_alt, use_container_width=True)

    time.sleep(2)
    st.rerun()

# ---------------------------------------------------------------------------
# Routeur principal de l'application
# ---------------------------------------------------------------------------
if not st.session_state['authentifie']:
    page_connexion()
else:
    page_dashboard()