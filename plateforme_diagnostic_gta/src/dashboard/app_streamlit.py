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

if "premiere_visite" not in st.session_state:
    st.session_state["premiere_visite"] = True

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
# 4. PAGE DE CONNEXION (Design Équilibré & Professionnel)
# ================================================================

def page_login():
    bg_b64 = get_base64_image(CHEMIN_FOND) if CHEMIN_FOND else ""
    logo_b64 = get_base64_image(CHEMIN_LOGO) if CHEMIN_LOGO else ""
    
    loader_html = ""
    animation_carte_css = ""

    if st.session_state["premiere_visite"]:
        loader_html = """
        <div id="loader-wrapper">
            <div class="flower-container">
                <svg class="flower-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <path class="stem" d="M50 100 Q 45 75 50 50" stroke="#007A33" stroke-width="5" fill="none" stroke-linecap="round" />
                    <path class="leaf petal1" fill="#00a651" d="M50 50 C 30 30 40 10 50 10 C 60 10 70 30 50 50 Z" />
                    <path class="leaf petal2" fill="#007A33" d="M50 50 C 20 40 10 60 10 80 C 30 90 40 70 50 50 Z" />
                    <path class="leaf petal3" fill="#00a651" d="M50 50 C 80 40 90 60 90 80 C 70 90 60 70 50 50 Z" />
                </svg>
            </div>
        </div>
        """
        animation_carte_css = """
        div[data-testid="stHorizontalBlock"] {
            opacity: 0;
            animation: revealCard 0.8s ease-in-out 4.2s forwards !important;
        }
        @keyframes revealCard { to { opacity: 1; } }
        """
        st.session_state["premiere_visite"] = False
    else:
        animation_carte_css = """
        div[data-testid="stHorizontalBlock"] {
            opacity: 1 !important;
        }
        """

    if bg_b64:
        bg_css = f"""
        .stApp {{
            background: linear-gradient(rgba(20, 30, 25, 0.4), rgba(10, 15, 10, 0.8)), 
                        url('data:image/jpg;base64,{bg_b64}') !important;
            background-size: 100% auto !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            cursor: grab;
        }}
        .stApp:active {{ cursor: grabbing; }}
        #loader-wrapper {{
            background: linear-gradient(rgba(10, 15, 12, 0.45), rgba(5, 10, 8, 0.65)), 
                        url('data:image/jpg;base64,{bg_b64}') !important;
            background-size: cover !important;
            background-position: center !important;
        }}
        """
    else:
        bg_css = """
        .stApp { background: linear-gradient(135deg, #3a3a3a, #101010) !important; }
        #loader-wrapper { background: linear-gradient(135deg, rgba(20,20,20,0.95), rgba(5,5,5,0.98)) !important; }
        """

    st.markdown(
        f"""
        {loader_html}
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        #MainMenu, header, footer {{ visibility: hidden; }}
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none !important; }}

        {bg_css}

        /* --- SÉQUENCE D'ANIMATION --- */
        #loader-wrapper {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 999999; display: flex; justify-content: center; align-items: center;
            pointer-events: none;
            animation: slideUpLoader 0.8s cubic-bezier(0.8, 0, 0.2, 1) 4.0s forwards;
        }}
        @keyframes slideUpLoader {{
            to {{ transform: translateY(-100%); opacity: 0; visibility: hidden; display: none; z-index: -1; }}
        }}
        
        .flower-container {{
            position: relative; z-index: 20;
            animation: flowerFade 4.0s forwards;
        }}
        @keyframes flowerFade {{
            0%, 85% {{ opacity: 1; transform: scale(1); }}
            100% {{ opacity: 0; transform: scale(1.1); }}
        }}
        .flower-svg {{ width: 90px; height: 90px; }}
        .stem {{ stroke-dasharray: 100; stroke-dashoffset: 100; animation: drawStem 1s ease-out 0.3s forwards; }}
        @keyframes drawStem {{ to {{ stroke-dashoffset: 0; }} }}
        .petal1 {{ opacity: 0; transform-origin: 50px 50px; animation: popPetal 0.8s ease-out 1.0s forwards; }}
        .petal2 {{ opacity: 0; transform-origin: 50px 50px; animation: popPetal 0.8s ease-out 1.8s forwards; }}
        .petal3 {{ opacity: 0; transform-origin: 50px 50px; animation: popPetal 0.8s ease-out 2.6s forwards; }}
        @keyframes popPetal {{
            0% {{ transform: scale(0) translateY(15px); opacity: 0; }}
            70% {{ transform: scale(1.1) translateY(0); opacity: 1; }}
            100% {{ transform: scale(1) translateY(0); opacity: 1; }}
        }}

        /* --- CARTE DE CONNEXION --- */
        {animation_carte_css}

        div[data-testid="stFormSubmitInstructions"], div[data-testid="InputInstructions"] {{ display: none !important; }}

        .block-container {{ padding-top: 15vh !important; padding-bottom: 15vh !important; max-width: 820px !important; }}

        div[data-testid="stHorizontalBlock"] {{
            background-color: rgba(255, 255, 255, 0.99) !important;
            border-radius: 24px !important;
            padding: 45px 35px !important;
            box-shadow: 0px 20px 60px rgba(0,0,0,0.6) !important;
            align-items: center !important;
        }}

        /* --- STYLE PROFESSIONNEL DE LA COLONNE LOGO --- */
        /* Cible la première colonne (Logo) pour lui donner un fond subtil et chic */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) {{
            background: linear-gradient(135deg, #f8f9fa 0%, #f1f3f5 100%);
            border-radius: 16px;
            padding: 30px 15px;
            border: 1px solid #edf0f2;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        div[data-testid="stForm"] {{ border: none !important; padding: 0 !important; background: transparent !important; }}
        div[data-testid="stTextInput"] label p {{ color: #007A33 !important; font-weight: 600 !important; font-size: 13px !important; }}

        /* --- ICÔNES (Personne & Cadenas) --- */
        div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(1) input {{
            background-color: #f4f6f9 !important; border: 1px solid #e1e8ed !important; border-radius: 8px !important;
            padding: 10px 14px 10px 40px !important; font-size: 14px !important; color: #333 !important;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="%23007A33" viewBox="0 0 16 16"><path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>') !important;
            background-repeat: no-repeat !important; background-position: 12px center !important;
        }}
        div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(2) input {{
            background-color: #f4f6f9 !important; border: 1px solid #e1e8ed !important; border-radius: 8px !important;
            padding: 10px 14px 10px 40px !important; font-size: 14px !important; color: #333 !important;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="%23007A33" viewBox="0 0 16 16"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/></svg>') !important;
            background-repeat: no-repeat !important; background-position: 12px center !important;
        }}
        div[data-testid="stTextInput"] input:focus {{ border-color: #007A33 !important; box-shadow: 0 0 0 1px #007A33 !important; }}

        /* --- BOUTON CONNECTER --- */
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #007A33 !important; color: white !important; border-radius: 30px !important;
            font-weight: 600 !important; font-size: 15px !important; padding: 10px 24px !important; width: 100% !important;
            border: none !important; margin-top: 15px !important; transition: 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(0, 122, 51, 0.3);
        }}
        div[data-testid="stFormSubmitButton"] button:hover {{ background-color: #005f27 !important; transform: translateY(-2px); }}
        </style>

        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const app = document.querySelector('.stApp');
            if (!app) return;
            let scale = 100, posX = 50, posY = 50, isDragging = false, startX, startY;
            app.addEventListener('mousedown', function(e) {{
                if (e.target.closest('[data-testid="stHorizontalBlock"]')) return;
                isDragging = true; startX = e.clientX; startY = e.clientY;
            }});
            window.addEventListener('mousemove', function(e) {{
                if (!isDragging) return;
                let dx = e.clientX - startX, dy = e.clientY - startY;
                startX = e.clientX; startY = e.clientY;
                posX = Math.max(0, Math.min(100, posX - dx * 0.05));
                posY = Math.max(0, Math.min(100, posY - dy * 0.05));
                app.style.backgroundPosition = `${{posX}}% ${{posY}}%`;
            }});
            window.addEventListener('mouseup', function() {{ isDragging = false; }});
            app.addEventListener('wheel', function(e) {{
                if (e.target.closest('[data-testid="stHorizontalBlock"]')) return;
                e.preventDefault();
                scale = e.deltaY < 0 ? Math.min(300, scale + 10) : Math.max(50, scale - 10);
                app.style.backgroundSize = `${{scale}}% auto`;
            }}, {{ passive: false }});
        }});
        </script>
        """,
        unsafe_allow_html=True
    )

    # Rééquilibrage des colonnes : [0.9, 1.2] pour structurer l'espace du logo
    col_logo, col_form = st.columns([0.9, 1.2], gap="large")

    with col_logo:
        if logo_b64:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
                    <img src="data:image/jpg;base64,{logo_b64}" style="width: 130px; height: auto; display: block;" alt="Logo OCP" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
                    <div style="text-align: center; color: #007A33;">
                        <h1 style="font-size: 30px; margin: 0;">OCP</h1>
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