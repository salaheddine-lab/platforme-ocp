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
# 3. GESTION DES IMAGES (Logo et Background)
# ================================================================

def get_base64_image(image_path):
    """Encode une image en base64 pour l'utiliser dans le CSS."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def trouver_fichier(noms_fichiers):
    """Cherche l'image dans plusieurs dossiers possibles pour éviter les erreurs de chemin."""
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
CHEMIN_FOND = trouver_fichier(["image_a99884.jpg", "OIP (1).jpg", "OIP.jpg"]) 

# ================================================================
# 4. PAGE DE CONNEXION 
# ================================================================

def page_login():
    bg_b64 = get_base64_image(CHEMIN_FOND) if CHEMIN_FOND else ""
    logo_b64 = get_base64_image(CHEMIN_LOGO) if CHEMIN_LOGO else ""
    
    # Application du fond directement sur le conteneur principal (.stApp)
    if bg_b64:
        bg_css = f"""
        .stApp {{
            background: linear-gradient(rgba(20, 30, 25, 0.4), rgba(10, 15, 10, 0.8)), 
                        url('data:image/jpg;base64,{bg_b64}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        """
    else:
        bg_css = """
        .stApp {{
            background: linear-gradient(135deg, rgba(58,58,58,0.97), rgba(16,16,16,0.99)) !important;
        }}
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        #MainMenu, header, footer {{ visibility: hidden; }}
        
        /* Masquer la barre latérale sur la page de connexion */
        [data-testid="stSidebar"] {{ display: none !important; }}
        [data-testid="collapsedControl"] {{ display: none !important; }}

        /* Injection de l'image de fond */
        {bg_css}

        /* --- MASQUER "Press Enter to submit form" --- */
        div[data-testid="stFormSubmitInstructions"], 
        div[data-testid="InputInstructions"] {{
            display: none !important;
        }}

        /* --- CENTRAGE ET RÉDUCTION DE LA CARTE --- */
        .block-container {{
            padding-top: 15vh !important;
            max-width: 750px !important;
        }}

        /* --- ANIMATION FLOTTANTE --- */
        @keyframes float {{
            0% {{ transform: translateY(0px); box-shadow: 0px 15px 50px rgba(0,0,0,0.7); }}
            50% {{ transform: translateY(-15px); box-shadow: 0px 25px 60px rgba(0,0,0,0.8); }}
            100% {{ transform: translateY(0px); box-shadow: 0px 15px 50px rgba(0,0,0,0.7); }}
        }}

        /* --- LA CARTE BLANCHE --- */
        div[data-testid="stHorizontalBlock"] {{
            background-color: rgba(255, 255, 255, 0.98) !important;
            border-radius: 20px !important;
            padding: 40px 30px !important;
            box-shadow: 0px 15px 50px rgba(0,0,0,0.7) !important;
            align-items: center !important;
            animation: float 6s ease-in-out infinite !important; /* Ajout de l'animation ici */
        }}

        /* --- STYLE DU FORMULAIRE ET DES CHAMPS --- */
        div[data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}

        div[data-testid="stTextInput"] label p {{
            color: #007A33 !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }}

        div[data-testid="stTextInput"] input {{
            background-color: #f4f6f9 !important;
            border: 1px solid #e1e8ed !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 14px !important;
            color: #333 !important;
        }}

        div[data-testid="stTextInput"] input:focus {{
            border-color: #007A33 !important;
            box-shadow: 0 0 0 1px #007A33 !important;
        }}

        /* --- BOUTON CONNECTER --- */
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #007A33 !important;
            color: white !important;
            border-radius: 30px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 8px 24px !important;
            width: 100% !important;
            border: none !important;
            margin-top: 15px !important;
            transition: 0.3s ease !important;
        }}
        div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: #005f27 !important;
            transform: translateY(-2px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    col_logo, col_form = st.columns([1, 1.3], gap="medium")

    with col_logo:
        if logo_b64:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 250px; width: 100%;">
                    <img src="data:image/jpg;base64,{logo_b64}" style="width: 90px; height: auto; display: block;" alt="Logo OCP" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 250px;">
                    <div style="text-align: center; color: #007A33;">
                        <h1 style="font-size: 30px; margin: 0;">OCP</h1>
                        <p style="font-weight: 600; letter-spacing: 1px; font-size: 10px;">GROUPE OCP</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_form:
        st.markdown("<h2 style='color: #202522; font-weight: 700; font-size: 24px; margin-bottom: 5px; line-height: 1.2;'>Bienvenue sur votre<br>Dashboard GTA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #7a817d; font-size: 13px; margin-bottom: 20px;'>Merci de rentrer votre identifiant et mot de passe</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Identifiant *", placeholder="Entrez votre identifiant")
            password = st.text_input("Mot de passe *", type="password", placeholder="Entrez votre mot de passe")
            
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