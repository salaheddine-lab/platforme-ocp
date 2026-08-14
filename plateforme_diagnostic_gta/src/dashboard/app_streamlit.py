# ================================================================
# DASHBOARD GTA - GROUPE OCP
# Monitoring industriel d'un Groupe Turbo-Alternateur
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import base64
from pathlib import Path

# ================================================================
# 1. CONFIGURATION GLOBALE
# ================================================================

st.set_page_config(
    page_title="Dashboard GTA | OCP",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# 2. GESTION DE L'ÉTAT DE SESSION
# ================================================================

if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "historique" not in st.session_state:
    st.session_state["historique"] = None

# ================================================================
# 3. GESTION DES IMAGES (Logo)
# ================================================================

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def trouver_fichier(noms_fichiers):
    dossiers_a_chercher = [
        Path(__file__).parent,
        Path(__file__).parent / "assets",
        Path(__file__).parent.parent / "assets",
        Path(__file__).parent.parent.parent / "assets",
        Path.cwd() / "assets",
        Path.cwd()
    ]
    for dossier in dossiers_a_chercher:
        for nom in noms_fichiers:
            chemin = dossier / nom
            if chemin.exists():
                return chemin
    return None

CHEMIN_LOGO = trouver_fichier(["image_aa7580.jpg", "ocp_logo.png", "Ocp-Logo-Vector.svg-.png"])

# ================================================================
# 4. PAGE DE CONNEXION (Design fidèle à la capture d'écran)
# ================================================================

def page_login():
    logo_b64 = get_base64_image(CHEMIN_LOGO) if CHEMIN_LOGO else ""

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        #MainMenu, header, footer {{ visibility: hidden; }}
        
        /* Masquer la barre latérale sur la page de connexion */
        [data-testid="stSidebar"] {{ display: none !important; }}
        [data-testid="collapsedControl"] {{ display: none !important; }}

        /* --- FOND ANTHRACITE COMME SUR L'IMAGE --- */
        .stApp {{
            background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%) !important;
            /* Permet le défilement haut/bas (scroll) si nécessaire */
            overflow-y: auto !important;
        }}

        /* --- MASQUER "Press Enter to submit form" --- */
        div[data-testid="stFormSubmitInstructions"], 
        div[data-testid="InputInstructions"] {{
            display: none !important;
        }}

        /* --- CENTRAGE ET ESPACEMENT --- */
        .block-container {{
            padding-top: 12vh !important;
            padding-bottom: 12vh !important;
            max-width: 800px !important;
        }}

        /* --- ANIMATION FLOTTANTE (Haut vers le bas) --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); box-shadow: 0px 10px 40px rgba(0,0,0,0.5); }}
            50% {{ transform: translateY(-15px); box-shadow: 0px 25px 50px rgba(0,0,0,0.6); }}
            100% {{ transform: translateY(0px); box-shadow: 0px 10px 40px rgba(0,0,0,0.5); }}
        }}

        /* --- LA CARTE BLANCHE --- */
        div[data-testid="stHorizontalBlock"] {{
            background-color: #ffffff !important;
            border-radius: 18px !important;
            padding: 50px 40px !important;
            align-items: center !important;
            animation: float 6s ease-in-out infinite; /* Application de l'animation */
        }}

        /* --- TITRE ET SOUS-TITRE --- */
        .login-title {{
            color: #6c757d;
            font-weight: 400;
            font-size: 26px;
            margin-bottom: 5px;
            line-height: 1.3;
        }}
        .login-title b {{ color: #495057; font-weight: 600; }}
        .login-subtitle {{
            color: #8c98a4;
            font-size: 13px;
            margin-bottom: 30px;
        }}

        /* --- STYLE DU FORMULAIRE ET DES CHAMPS --- */
        div[data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}

        /* Libellés en vert */
        div[data-testid="stTextInput"] label p {{
            color: #00a651 !important;
            font-weight: 500 !important;
            font-size: 12px !important;
            margin-bottom: 2px !important;
        }}

        /* Fond bleuté des champs et ajout des icônes SVG */
        div[data-testid="stTextInput"] input {{
            background-color: #eef2f9 !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 12px 15px 12px 40px !important; /* Espace pour l'icône */
            font-size: 14px !important;
            color: #333 !important;
        }}

        /* Icône Utilisateur pour le premier champ */
        div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(1) input {{
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="%236c757d" viewBox="0 0 16 16"><path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 12px center !important;
        }}

        /* Icône Cadenas pour le deuxième champ */
        div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(2) input {{
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="%236c757d" viewBox="0 0 16 16"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 12px center !important;
        }}

        /* --- BOUTON CONNECTER CENTRÉ --- */
        div[data-testid="stFormSubmitButton"] {{
            display: flex !important;
            justify-content: center !important;
            margin-top: 25px !important;
        }}
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #00b87c !important;
            color: white !important;
            border-radius: 30px !important;
            font-weight: 500 !important;
            font-size: 15px !important;
            padding: 8px 35px !important;
            width: auto !important; /* Largeur automatique pour ressembler à l'image */
            border: none !important;
            transition: 0.3s ease !important;
            box-shadow: 0 4px 10px rgba(0, 184, 124, 0.3) !important;
        }}
        div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: #00a651 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 166, 81, 0.4) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    col_logo, col_form = st.columns([1, 1.2], gap="large")

    with col_logo:
        if logo_b64:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 250px; width: 100%;">
                    <img src="data:image/jpg;base64,{logo_b64}" style="width: 140px; height: auto; display: block;" alt="Logo OCP" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 250px;">
                    <div style="text-align: center; color: #00a651;">
                        <h1 style="font-size: 40px; margin: 0;">OCP</h1>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_form:
        st.markdown("<h2 class='login-title'>Bienvenue sur votre<br>portail <b>Dashboard GTA</b></h2>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle'>Merci de rentrer votre identifiant et mot de passe</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Identifiant *", value="admin")
            password = st.text_input("Mot de passe *", type="password", value="1234567")
            
            submit = st.form_submit_button("Connecter")

            if submit:
                if username == "admin" and password == "1234567":
                    st.session_state["authentifie"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")

# ================================================================
# 5. CSS DU DASHBOARD ET TOP BAR
# ================================================================

def appliquer_css_dashboard():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .stApp { background: #f4f6f5 !important; }

        /* Sidebar étroite */
        section[data-testid="stSidebar"] {
            background-color: #007A33 !important;
            width: 85px !important;
            min-width: 85px !important;
            max-width: 85px !important;
        }
        section[data-testid="stSidebar"] * { color: white !important; }
        
        div[data-testid="stMetric"] {
            background: white;
            padding: 16px;
            border-radius: 14px;
            border: 1px solid #edf0ee;
            box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def afficher_topbar():
    col_nav_logo, col_nav_user = st.columns([2, 2])
    with col_nav_logo:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; padding-top: 5px;">
                <span style="font-size: 24px; font-weight: 700; color: #007A33;">🟢 OCP</span>
                <span style="font-size: 14px; font-weight: 600; color: #2c3e50;">| Dashboard GTA</span>
            </div>
            """, unsafe_allow_html=True
        )
    with col_nav_user:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown(f"<p style='margin-top: 10px; font-weight: bold; color: #2c3e50; text-align: right;'>👤 {st.session_state['username']}</p>", unsafe_allow_html=True)
        with c2:
            if st.button("🚪 Déconnexion", use_container_width=True):
                st.session_state["authentifie"] = False
                st.session_state["username"] = ""
                st.rerun()
    st.markdown("<hr style='margin: 0px 0px 20px 0px;'>", unsafe_allow_html=True)


def afficher_sidebar():
    st.sidebar.markdown("<h3 style='text-align: center; color: #ffffff; font-size: 15px;'>GTA</h3>", unsafe_allow_html=True)
    return st.sidebar.radio(
        "Navigation",
        ["🏠 Accueil", "📈 Rendement", "🌡️ Résistance d'encrassement", "⚡ Perte turbine", "🔌 Perte alternateur"],
        label_visibility="collapsed"
    )

# ================================================================
# 6. MOTEUR DE SIMULATION ET GRAPHIQUES
# ================================================================

def generer_donnees_gta(n=60):
    rng = np.random.default_rng()
    temps = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="min")
    
    rendement = np.clip(0.82 + 0.015 * np.sin(np.linspace(0, 4*np.pi, n)) + rng.normal(0, 0.004, n), 0.72, 0.90)
    resistance = np.clip(0.00042 + np.linspace(0, 0.00010, n) + 0.000015 * np.sin(np.linspace(0, 3*np.pi, n)) + rng.normal(0, 0.000006, n), 0.00030, 0.00070)
    perte_turb = np.clip(6.2 + 0.6 * np.sin(np.linspace(0, 3*np.pi, n)) + rng.normal(0, 0.20, n), 4.0, 10.0)
    perte_alt = np.clip(3.8 + 0.4 * np.sin(np.linspace(0, 4*np.pi, n)) + rng.normal(0, 0.15, n), 2.5, 7.0)

    return pd.DataFrame({
        "Temps": temps, "Rendement": rendement * 100, "Resistance": resistance,
        "Perte_Turbine": perte_turb, "Perte_Alternateur": perte_alt
    })

def graphique_ligne(df, x, y, titre, nom_axe_y, unite=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode="lines", name=y, line=dict(shape="spline", width=3, color="#007A33")))
    fig.update_layout(title=titre, template="plotly_white", height=390, margin=dict(l=20, r=20, t=55, b=20), hovermode="x unified", yaxis_title=nom_axe_y)
    return fig

def afficher_alertes(df):
    dernier = df.iloc[-1]
    alertes = []
    if dernier["Rendement"] < 80: alertes.append(("warning", "Rendement à surveiller", f"Rendement : {dernier['Rendement']:.2f} %"))
    if dernier["Resistance"] > 0.00050: alertes.append(("danger", "Risque d'encrassement", f"Rth : {dernier['Resistance']:.6f} K/W"))
    
    if not alertes:
        st.success("✓ Système stable - Fonctionnement nominal du GTA.")
    else:
        for niveau, titre, msg in alertes:
            if niveau == "danger": st.error(f"⚠️ {titre} : {msg}")
            else: st.warning(f"⚠️ {titre} : {msg}")

# ================================================================
# 7. ROUTEUR ET PAGES DU DASHBOARD
# ================================================================

def dashboard_realtime():
    appliquer_css_dashboard()
    
    @st.fragment(run_every="5s")
    def monitoring():
        if st.session_state["historique"] is None:
            st.session_state["historique"] = generer_donnees_gta(59)
            
        df = st.session_state["historique"]
        df = pd.concat([df, generer_donnees_gta(1)], ignore_index=True).tail(60).reset_index(drop=True)
        st.session_state["historique"] = df

        page = afficher_sidebar()
        afficher_topbar()

        if page == "🏠 Accueil":
            st.title("🏭 Tableau de Bord - Accueil")
            afficher_alertes(df)
            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Rendement", f"{df.iloc[-1]['Rendement']:.2f} %")
            c2.metric("Rth Condenseur", f"{df.iloc[-1]['Resistance']:.6f}")
            c3.metric("Perte Turbine", f"{df.iloc[-1]['Perte_Turbine']:.2f} %")
            c4.metric("Perte Alternateur", f"{df.iloc[-1]['Perte_Alternateur']:.2f} %")

        elif page == "📈 Rendement":
            st.title("📈 Évolution du Rendement")
            st.metric("Rendement actuel", f"{df.iloc[-1]['Rendement']:.2f} %")
            st.plotly_chart(graphique_ligne(df, "Temps", "Rendement", "Calcul du Rendement", "%", "%"), use_container_width=True)

        elif page == "🌡️ Résistance d'encrassement":
            st.title("🌡️ Résistance Thermique")
            st.metric("Rth Actuelle", f"{df.iloc[-1]['Resistance']:.6f} K/W")
            st.plotly_chart(graphique_ligne(df, "Temps", "Resistance", "Encrassement Condenseur", "K/W", "K/W"), use_container_width=True)

        elif page == "⚡ Perte turbine":
            st.title("⚡ Pertes Turbine")
            st.metric("Pertes actuelles", f"{df.iloc[-1]['Perte_Turbine']:.2f} %")
            st.plotly_chart(graphique_ligne(df, "Temps", "Perte_Turbine", "Pertes Mécaniques et Thermiques", "%", "%"), use_container_width=True)

        elif page == "🔌 Perte alternateur":
            st.title("🔌 Pertes Alternateur")
            st.metric("Pertes actuelles", f"{df.iloc[-1]['Perte_Alternateur']:.2f} %")
            st.plotly_chart(graphique_ligne(df, "Temps", "Perte_Alternateur", "Pertes Électriques", "%", "%"), use_container_width=True)

    monitoring()

# ================================================================
# LANCEMENT
# ================================================================
if not st.session_state["authentifie"]:
    page_login()
else:
    dashboard_realtime()