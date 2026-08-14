# ================================================================
# DASHBOARD GTA - GROUPE OCP
# Monitoring industriel d'un Groupe Turbo-Alternateur
# ================================================================
#
# Installation des dépendances :
# pip install streamlit pandas numpy plotly
#
# Lancement de l'application :
# streamlit run app_streamlit.py
#
# Identifiants de démonstration :
# Identifiant : admin
# Mot de passe : 1234567
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time


# ================================================================
# 1. CONFIGURATION GLOBALE DE LA PAGE
# ================================================================

st.set_page_config(
    page_title="Dashboard GTA | OCP",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================================================================
# 2. GESTION DE L'ÉTAT DE SESSION (SESSION STATE)
# ================================================================

if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "historique" not in st.session_state:
    st.session_state["historique"] = None


# ================================================================
# 3. CSS GLOBAL (Design UI/UX Professionnel & Police Poppins)
# ================================================================

st.markdown(
    """
    <style>

    /* ============================================================
       TYPOGRAPHIE
       ============================================================ */

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: #f4f6f5;
    }

    /* ============================================================
       SIDEBAR (Étroite ~85px, style vert OCP)
       ============================================================ */

    section[data-testid="stSidebar"] {
        width: 85px !important;
        min-width: 85px !important;
        max-width: 85px !important;

        background: linear-gradient(
            180deg,
            #006b2d 0%,
            #007A33 50%,
            #005b28 100%
        );

        border-right: none;
    }

    section[data-testid="stSidebar"] > div {
        padding: 0.5rem 0.35rem;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 8px;
    }

    section[data-testid="stSidebar"] label {
        background: transparent;
        border-radius: 12px;
        padding: 8px 4px;
        margin-bottom: 4px;
        transition: 0.2s ease;
        justify-content: center;
    }

    section[data-testid="stSidebar"] label:hover {
        background: rgba(255,255,255,0.12);
    }

    section[data-testid="stSidebar"] label[data-checked="true"] {
        background: rgba(255,255,255,0.20);
    }

    section[data-testid="stSidebar"] label p {
        font-size: 10px !important;
        line-height: 1.15;
        text-align: center;
    }

    section[data-testid="stSidebar"] input {
        display: none;
    }

    /* ============================================================
       TOP BAR
       ============================================================ */

    .topbar {
        height: 72px;
        background: white;
        border-radius: 0 0 16px 16px;
        padding: 0 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 3px 15px rgba(0,0,0,0.07);
        margin-bottom: 22px;
    }

    .top-logo {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .ocp-symbol {
        width: 39px;
        height: 39px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00a651, #007A33);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 19px;
        font-weight: 700;
        box-shadow: 0 3px 8px rgba(0,122,51,0.25);
    }

    .ocp-text {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #006b2d;
    }

    /* ============================================================
       TITRES & CARTES
       ============================================================ */

    .page-title {
        font-size: 28px;
        font-weight: 700;
        color: #202522;
        margin-bottom: 2px;
    }

    .page-subtitle {
        color: #7a817d;
        font-size: 13px;
        margin-bottom: 25px;
    }

    .dashboard-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        border: 1px solid #edf0ee;
    }

    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #303633;
        margin-bottom: 10px;
    }

    /* ============================================================
       ALERTES
       ============================================================ */

    .alert-normal {
        background: #eaf7ef;
        border-left: 5px solid #007A33;
        border-radius: 10px;
        padding: 13px 16px;
        color: #176b3c;
        margin-bottom: 10px;
    }

    .alert-warning {
        background: #fff7df;
        border-left: 5px solid #e4a900;
        border-radius: 10px;
        padding: 13px 16px;
        color: #8a6500;
        margin-bottom: 10px;
    }

    .alert-danger {
        background: #fff0f0;
        border-left: 5px solid #d93025;
        border-radius: 10px;
        padding: 13px 16px;
        color: #9b2119;
        margin-bottom: 10px;
    }

    /* ============================================================
       PAGE DE CONNEXION (Pixel-Perfect)
       ============================================================ */

    .login-page {
        position: fixed;
        inset: 0;
        background: linear-gradient(135deg, rgba(58,58,58,0.97), rgba(16,16,16,0.99));
        overflow: hidden;
    }

    .login-page::before {
        content: "";
        position: absolute;
        inset: -50%;
        background: repeating-linear-gradient(135deg, transparent 0px, transparent 80px, rgba(255,255,255,0.025) 81px, transparent 82px);
        transform: rotate(-5deg);
    }

    .login-container {
        position: relative;
        z-index: 2;
        min-height: 88vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .login-card {
        width: 850px;
        min-height: 450px;
        background: white;
        border-radius: 22px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.45);
        overflow: hidden;
        display: flex;
    }

    .login-left {
        width: 42%;
        background: linear-gradient(145deg, #f7faf8, #eef4f0);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    .login-logo {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .logo-big {
        display: flex;
        align-items: center;
        font-size: 52px;
        font-weight: 700;
        color: #075c2c;
    }

    .logo-big-o {
        width: 67px;
        height: 67px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00a651, #007A33);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 4px;
    }

    .logo-line {
        width: 130px;
        height: 4px;
        background: #007A33;
        border-radius: 5px;
        margin-top: 5px;
    }

    .logo-subtitle {
        color: #555;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 3px;
        margin-top: 8px;
    }

    .login-right {
        width: 58%;
        padding: 55px 55px;
    }

    .login-title {
        font-size: 26px;
        font-weight: 700;
        color: #202522;
        margin-bottom: 5px;
    }

    .login-description {
        color: #888;
        font-size: 13px;
        margin-bottom: 30px;
    }

    /* ============================================================
       BOUTONS & METRICS
       ============================================================ */

    div.stButton > button {
        border-radius: 30px;
        border: none;
        background: #007A33;
        color: white;
        font-weight: 600;
        padding: 9px 24px;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background: #005f27;
        color: white;
        transform: translateY(-1px);
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #edf0ee;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #747b77;
    }

    .footer {
        text-align: center;
        color: #9aa09c;
        font-size: 11px;
        margin-top: 30px;
        padding-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ================================================================
# 4. COMPOSANT LOGO OCP
# ================================================================

def ocp_logo():
    return """
    <div class="top-logo">
        <div class="ocp-symbol">O</div>
        <div class="ocp-text">CP</div>
    </div>
    """


# ================================================================
# 5. SIMULATION DES DONNÉES INDUSTRIELLES GTA
# ================================================================

def generer_donnees_gta(n=60):
    rng = np.random.default_rng()
    maintenant = pd.Timestamp.now()

    temps = pd.date_range(end=maintenant, periods=n, freq="min")

    # Rendement GTA (%)
    rendement = (
        0.82
        + 0.015 * np.sin(np.linspace(0, 4*np.pi, n))
        + rng.normal(0, 0.004, n)
    )
    rendement = np.clip(rendement, 0.72, 0.90)

    # Résistance thermique condenseur (K/W)
    resistance = (
        0.00042
        + np.linspace(0, 0.00010, n)
        + 0.000015 * np.sin(np.linspace(0, 3*np.pi, n))
        + rng.normal(0, 0.000006, n)
    )
    resistance = np.clip(resistance, 0.00030, 0.00070)

    # Perte turbine (%)
    perte_turbine = (
        6.2
        + 0.6 * np.sin(np.linspace(0, 3*np.pi, n))
        + rng.normal(0, 0.20, n)
    )
    perte_turbine = np.clip(perte_turbine, 4.0, 10.0)

    # Perte alternateur (%)
    perte_alternateur = (
        3.8
        + 0.4 * np.sin(np.linspace(0, 4*np.pi, n))
        + rng.normal(0, 0.15, n)
    )
    perte_alternateur = np.clip(perte_alternateur, 2.5, 7.0)

    temperature_vapeur = 515 + 5 * np.sin(np.linspace(0, 2*np.pi, n)) + rng.normal(0, 1.2, n)
    temperature_condenseur = 38 + 1.5 * np.sin(np.linspace(0, 3*np.pi, n)) + rng.normal(0, 0.5, n)
    pression_entree = 42 + 0.4 * np.sin(np.linspace(0, 2*np.pi, n)) + rng.normal(0, 0.08, n)
    pression_sortie = 0.09 + rng.normal(0, 0.002, n)
    puissance_turbine = 32 + 1.5 * np.sin(np.linspace(0, 2*np.pi, n)) + rng.normal(0, 0.3, n)
    puissance_alternateur = 29.5 + 1.3 * np.sin(np.linspace(0, 2*np.pi, n)) + rng.normal(0, 0.25, n)

    df = pd.DataFrame({
        "Temps": temps,
        "Rendement": rendement * 100,
        "Resistance": resistance,
        "Perte_Turbine": perte_turbine,
        "Perte_Alternateur": perte_alternateur,
        "Temperature_Vapeur": temperature_vapeur,
        "Temperature_Condenseur": temperature_condenseur,
        "Pression_Entree": pression_entree,
        "Pression_Sortie": pression_sortie,
        "Puissance_Turbine": puissance_turbine,
        "Puissance_Alternateur": puissance_alternateur
    })

    return df


# ================================================================
# 6. GESTION DES GRAPHIQUES PLOTLY
# ================================================================

def graphique_ligne(df, x, y, titre, nom_axe_y, unite=""):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines",
            name=y,
            line=dict(shape="spline", width=3, color="#007A33"),
            hovertemplate="%{y:.3f}" + f" {unite}<extra></extra>"
        )
    )

    fig.update_layout(
        title=titre,
        template="plotly_white",
        height=390,
        margin=dict(l=20, r=20, t=55, b=20),
        hovermode="x unified",
        xaxis_title="Temps",
        yaxis_title=nom_axe_y,
        font=dict(family="Poppins", size=12),
        legend=dict(orientation="h", y=1.1)
    )

    return fig


# ================================================================
# 7. SYSTÈME D'ALERTES ET DIAGNOSTICS
# ================================================================

def analyser_alertes(df):
    dernier = df.iloc[-1]
    alertes = []

    if dernier["Rendement"] < 78:
        alertes.append(("danger", "Rendement faible", f"Le rendement actuel est de {dernier['Rendement']:.2f} %."))
    elif dernier["Rendement"] < 80:
        alertes.append(("warning", "Rendement à surveiller", f"Le rendement actuel est de {dernier['Rendement']:.2f} %."))

    if dernier["Resistance"] > 0.00055:
        alertes.append(("danger", "Encrassement du condenseur", f"Résistance thermique élevée : {dernier['Resistance']:.6f} K/W."))
    elif dernier["Resistance"] > 0.00050:
        alertes.append(("warning", "Encrassement à surveiller", f"Résistance thermique : {dernier['Resistance']:.6f} K/W."))

    if dernier["Perte_Turbine"] > 8:
        alertes.append(("danger", "Pertes turbine élevées", f"Pertes estimées : {dernier['Perte_Turbine']:.2f} %."))

    if dernier["Perte_Alternateur"] > 5:
        alertes.append(("danger", "Pertes alternateur élevées", f"Pertes estimées : {dernier['Perte_Alternateur']:.2f} %."))

    return alertes


def afficher_alertes(df):
    alertes = analyser_alertes(df)

    if not alertes:
        st.markdown(
            """
            <div class="alert-normal">
                <b>✓ État normal</b><br>
                Aucun dépassement de seuil détecté sur le GTA.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    for niveau, titre, message in alertes:
        classe = "alert-danger" if niveau == "danger" else "alert-warning"
        symbole = "⚠" if niveau == "danger" else "!"
        st.markdown(
            f"""
            <div class="{classe}">
                <b>{symbole} {titre}</b><br>
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )


# ================================================================
# 8. PAGE DE CONNEXION (LOGIN)
# ================================================================

def page_login():
    st.markdown(
        """
        <div class="login-page">
            <div class="login-container">
                <div class="login-card">
                    <div class="login-left">
                        <div class="login-logo">
                            <div class="logo-big">
                                <div class="logo-big-o">O</div>
                                CP
                            </div>
                            <div class="logo-line"></div>
                            <div class="logo-subtitle">GROUPE OCP</div>
                        </div>
                    </div>
                    <div class="login-right">
                        <div class="login-title">Bienvenue sur votre Dashboard GTA</div>
                        <div class="login-description">Merci de rentrer votre identifiant et mot de passe</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, right = st.columns([1.2, 1.8])

    with right:
        st.markdown(
            """
            <style>
            div[data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 175px'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Identifiant *", placeholder="Entrez votre identifiant")
            password = st.text_input("Mot de passe *", type="password", placeholder="Entrez votre mot de passe")
            connexion = st.form_submit_button("Connecter", use_container_width=True)

            if connexion:
                if username == "admin" and password == "1234567":
                    st.session_state["authentifie"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")


# ================================================================
# 9. TOP BAR ET SIDEBAR NAVIGATION
# ================================================================

def afficher_topbar():
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(ocp_logo(), unsafe_allow_html=True)

    with col2:
        username = st.session_state["username"]
        c1, c2 = st.columns([1.2, 1])

        with c1:
            st.markdown(
                f"""
                <div style="text-align:right; padding-top:8px; color:#444; font-size:13px; font-weight:500;">
                    👤 {username}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            if st.button("Se déconnecter", key="logout"):
                st.session_state["authentifie"] = False
                st.session_state["username"] = ""
                st.rerun()


def afficher_sidebar():
    st.sidebar.markdown(
        """
        <div style="text-align:center; font-size:25px; margin-bottom:15px;">
            🏭
        </div>
        """,
        unsafe_allow_html=True
    )

    choix = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Accueil",
            "📈 Rendement",
            "🌡️ Résistance d'encrassement",
            "⚡ Perte turbine",
            "🔌 Perte alternateur"
        ],
        label_visibility="collapsed"
    )

    return choix


# ================================================================
# 10. PAGES FONCTIONNELLES DU DASHBOARD
# ================================================================

def page_accueil(df):
    st.markdown('<div class="page-title">Centre de monitoring GTA</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Vue globale du Groupe Turbo-Alternateur • Surveillance en temps réel</div>', unsafe_allow_html=True)

    afficher_alertes(df)
    st.markdown("<br>", unsafe_allow_html=True)

    dernier = df.iloc[-1]
    precedent = df.iloc[-2]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Rendement GTA", f"{dernier['Rendement']:.2f} %", f"{dernier['Rendement'] - precedent['Rendement']:.2f} %")
    with c2:
        st.metric("Résistance condenseur", f"{dernier['Resistance']:.6f}", f"{(dernier['Resistance'] - precedent['Resistance']):.6f}")
    with c3:
        st.metric("Perte turbine", f"{dernier['Perte_Turbine']:.2f} %", f"{dernier['Perte_Turbine'] - precedent['Perte_Turbine']:.2f} %")
    with c4:
        st.metric("Perte alternateur", f"{dernier['Perte_Alternateur']:.2f} %", f"{dernier['Perte_Alternateur'] - precedent['Perte_Alternateur']:.2f} %")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Puissance turbine</div>', unsafe_allow_html=True)
        fig = graphique_ligne(df, "Temps", "Puissance_Turbine", "Évolution de la puissance mécanique", "Puissance", "MW")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Puissance alternateur</div>', unsafe_allow_html=True)
        fig = graphique_ligne(df, "Temps", "Puissance_Alternateur", "Évolution de la puissance électrique", "Puissance", "MW")
        st.plotly_chart(fig, use_container_width=True)


def page_rendement(df):
    st.markdown('<div class="page-title">Rendement du GTA</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Suivi du rendement global du Groupe Turbo-Alternateur</div>', unsafe_allow_html=True)

    dernier = df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Rendement actuel", f"{dernier['Rendement']:.2f} %")
    c2.metric("Rendement moyen", f"{df['Rendement'].mean():.2f} %")
    c3.metric("Rendement maximal", f"{df['Rendement'].max():.2f} %")

    st.markdown("<br>", unsafe_allow_html=True)
    fig = graphique_ligne(df, "Temps", "Rendement", "Évolution du rendement global", "Rendement", "%")
    st.plotly_chart(fig, use_container_width=True)


def page_resistance(df):
    st.markdown('<div class="page-title">Résistance d\'encrassement</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Suivi de la résistance thermique du condenseur</div>', unsafe_allow_html=True)

    dernier = df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Résistance actuelle", f"{dernier['Resistance']:.6f} K/W")
    c2.metric("Valeur moyenne", f"{df['Resistance'].mean():.6f} K/W")
    c3.metric("Valeur maximale", f"{df['Resistance'].max():.6f} K/W")

    st.markdown("<br>", unsafe_allow_html=True)
    fig = graphique_ligne(df, "Temps", "Resistance", "Évolution de la résistance thermique", "Résistance thermique", "K/W")
    st.plotly_chart(fig, use_container_width=True)


def page_perte_turbine(df):
    st.markdown('<div class="page-title">Pertes turbine</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Analyse des pertes thermiques et mécaniques de la turbine</div>', unsafe_allow_html=True)

    dernier = df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Pertes actuelles", f"{dernier['Perte_Turbine']:.2f} %")
    c2.metric("Pertes moyennes", f"{df['Perte_Turbine'].mean():.2f} %")
    c3.metric("Pertes maximales", f"{df['Perte_Turbine'].max():.2f} %")

    st.markdown("<br>", unsafe_allow_html=True)
    fig = graphique_ligne(df, "Temps", "Perte_Turbine", "Évolution des pertes turbine", "Pertes", "%")
    st.plotly_chart(fig, use_container_width=True)


def page_perte_alternateur(df):
    st.markdown('<div class="page-title">Pertes alternateur</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Analyse des pertes électriques de l\'alternateur</div>', unsafe_allow_html=True)

    dernier = df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Pertes actuelles", f"{dernier['Perte_Alternateur']:.2f} %")
    c2.metric("Pertes moyennes", f"{df['Perte_Alternateur'].mean():.2f} %")
    c3.metric("Pertes maximales", f"{df['Perte_Alternateur'].max():.2f} %")

    st.markdown("<br>", unsafe_allow_html=True)
    fig = graphique_ligne(df, "Temps", "Perte_Alternateur", "Évolution des pertes alternateur", "Pertes", "%")
    st.plotly_chart(fig, use_container_width=True)


# ================================================================
# 11. MODE TEMPS RÉEL (FRAGMENTS STREAMLIT)
# ================================================================

def dashboard_realtime():
    @st.fragment(run_every="5s")
    def monitoring():
        nouvelles_donnees = generer_donnees_gta(1)

        if st.session_state["historique"] is None:
            st.session_state["historique"] = generer_donnees_gta(59)

        df = st.session_state["historique"]
        df = pd.concat([df, nouvelles_donnees], ignore_index=True)
        df = df.tail(60).reset_index(drop=True)
        st.session_state["historique"] = df

        page = afficher_sidebar()

        st.markdown('<div class="topbar">', unsafe_allow_html=True)
        afficher_topbar()
        st.markdown('</div>', unsafe_allow_html=True)

        if page == "🏠 Accueil":
            page_accueil(df)
        elif page == "📈 Rendement":
            page_rendement(df)
        elif page == "🌡️ Résistance d'encrassement":
            page_resistance(df)
        elif page == "⚡ Perte turbine":
            page_perte_turbine(df)
        elif page == "🔌 Perte alternateur":
            page_perte_alternateur(df)

        st.markdown(
            f"""
            <div class="footer">
                Dashboard GTA • Groupe OCP • Monitoring temps réel • Dernière mise à jour : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            </div>
            """,
            unsafe_allow_html=True
        )

    monitoring()


# ================================================================
# 12. POINT D'ENTRÉE PRINCIPAL DE L'APPLICATION
# ================================================================

if not st.session_state["authentifie"]:
    page_login()
else:
    dashboard_realtime()