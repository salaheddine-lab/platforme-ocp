# ================================================================
# DASHBOARD GTA - GROUPE OCP
# Monitoring industriel d'un Groupe Turbo-Alternateur
# ================================================================
#
# Installation :
# pip install streamlit pandas numpy plotly
#
# Lancement :
# streamlit run dashboard_gta.py
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
# 1. CONFIGURATION GLOBALE
# ================================================================

st.set_page_config(
    page_title="Dashboard GTA",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================================================================
# 2. SESSION STATE
# ================================================================

if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "historique" not in st.session_state:
    st.session_state["historique"] = None


# ================================================================
# 3. CSS GLOBAL
# ================================================================

st.markdown(
    """
    <style>

    /* ============================================================
       POLICE
       ============================================================ */

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* ============================================================
       BACKGROUND GENERAL
       ============================================================ */

    .stApp {
        background: #f4f6f5;
    }

    /* ============================================================
       SIDEBAR
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

    /* Radio buttons */

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

        background: linear-gradient(
            135deg,
            #00a651,
            #007A33
        );

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

    .top-user {
        color: #444;
        font-size: 14px;
        font-weight: 500;
    }

    /* ============================================================
       TITRES
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

    /* ============================================================
       CARTES
       ============================================================ */

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
       LOGIN
       ============================================================ */

    .login-page {
        position: fixed;
        inset: 0;

        background:
            linear-gradient(
                135deg,
                rgba(58,58,58,0.97),
                rgba(16,16,16,0.99)
            );

        overflow: hidden;
    }

    .login-page::before {
        content: "";
        position: absolute;
        inset: -50%;

        background:
            repeating-linear-gradient(
                135deg,
                transparent 0px,
                transparent 80px,
                rgba(255,255,255,0.025) 81px,
                transparent 82px
            );

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

        box-shadow:
            0 30px 80px rgba(0,0,0,0.45);

        overflow: hidden;

        display: flex;
    }

    .login-left {
        width: 42%;

        background:
            linear-gradient(
                145deg,
                #f7faf8,
                #eef4f0
            );

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

        background:
            linear-gradient(
                135deg,
                #00a651,
                #007A33
            );

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
       BOUTONS
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

    /* ============================================================
       METRICS
       ============================================================ */

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

    /* ============================================================
       FOOTER
       ============================================================ */

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
# 4. LOGO OCP
# ================================================================

def ocp_logo():

    return """
    <div class="top-logo">
        <div class="ocp-symbol">O</div>
        <div class="ocp-text">CP</div>
    </div>
    """


# ================================================================
# 5. SIMULATION DES DONNÉES GTA
# ================================================================

def generer_donnees_gta(n=60):

    # Générateur aléatoire reproductible par session
    rng = np.random.default_rng()

    # Temps
    maintenant = pd.Timestamp.now()

    temps = pd.date_range(
        end=maintenant,
        periods=n,
        freq="min"
    )

    # ------------------------------------------------------------
    # Rendement GTA
    # ------------------------------------------------------------

    rendement = (
        0.82
        + 0.015 * np.sin(np.linspace(0, 4*np.pi, n))
        + rng.normal(0, 0.004, n)
    )

    rendement = np.clip(rendement, 0.72, 0.90)

    # ------------------------------------------------------------
    # Résistance thermique condenseur
    # ------------------------------------------------------------

    resistance = (
        0.00042
        + np.linspace(0, 0.00010, n)
        + 0.000015 * np.sin(np.linspace(0, 3*np.pi, n))
        + rng.normal(0, 0.000006, n)
    )

    resistance = np.clip(resistance, 0.00030, 0.00070)

    # ------------------------------------------------------------
    # Perte turbine
    # ------------------------------------------------------------

    perte_turbine = (
        6.2
        + 0.6 * np.sin(np.linspace(0, 3*np.pi, n))
        + rng.normal(0, 0.20, n)
    )

    perte_turbine = np.clip(perte_turbine, 4.0, 10.0)

    # ------------------------------------------------------------
    # Perte alternateur
    # ------------------------------------------------------------

    perte_alternateur = (
        3.8
        + 0.4 * np.sin(np.linspace(0, 4*np.pi, n))
        + rng.normal(0, 0.15, n)
    )

    perte_alternateur = np.clip(
        perte_alternateur,
        2.5,
        7.0
    )

    # ------------------------------------------------------------
    # Températures
    # ------------------------------------------------------------

    temperature_vapeur = (
        515
        + 5 * np.sin(np.linspace(0, 2*np.pi, n))
        + rng.normal(0, 1.2, n)
    )

    temperature_condenseur = (
        38
        + 1.5 * np.sin(np.linspace(0, 3*np.pi, n))
        + rng.normal(0, 0.5, n)
    )

    # ------------------------------------------------------------
    # Pressions
    # ------------------------------------------------------------

    pression_entree = (
        42
        + 0.4 * np.sin(np.linspace(0, 2*np.pi, n))
        + rng.normal(0, 0.08, n)
    )

    pression_sortie = (
        0.09
        + rng.normal(0, 0.002, n)
    )

    # ------------------------------------------------------------
    # Puissances
    # ------------------------------------------------------------

    puissance_turbine = (
        32
        + 1.5 * np.sin(np.linspace(0, 2*np.pi, n))
        + rng.normal(0, 0.3, n)
    )

    puissance_alternateur = (
        29.5
        + 1.3 * np.sin(np.linspace(0, 2*np.pi, n))
        + rng.normal(0, 0.25, n)
    )

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
# 6. GRAPHIQUE PLOTLY
# ================================================================

def graphique_ligne(
    df,
    x,
    y,
    titre,
    nom_axe_y,
    unite=""
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines",
            name=y,
            line=dict(
                shape="spline",
                width=3
            ),
            hovertemplate=(
                "%{y:.3f}"
                + f" {unite}"
                + "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=titre,
        template="plotly_white",
        height=390,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),
        hovermode="x unified",
        xaxis_title="Temps",
        yaxis_title=nom_axe_y,
        font=dict(
            family="Poppins",
            size=12
        ),
        legend=dict(
            orientation="h",
            y=1.1
        )
    )

    return fig


# ================================================================
# 7. SYSTÈME D'ALERTES
# ================================================================

def analyser_alertes(df):

    dernier = df.iloc[-1]

    alertes = []

    # Rendement
    if dernier["Rendement"] < 78:
        alertes.append(
            (
                "danger",
                "Rendement faible",
                f"Le rendement actuel est de "
                f"{dernier['Rendement']:.2f} %."
            )
        )
    elif dernier["Rendement"] < 80:
        alertes.append(
            (
                "warning",
                "Rendement à surveiller",
                f"Le rendement actuel est de "
                f"{dernier['Rendement']:.2f} %."
            )
        )

    # Encrassement
    if dernier["Resistance"] > 0.00055:
        alertes.append(
            (
                "danger",
                "Encrassement du condenseur",
                f"Résistance thermique élevée : "
                f"{dernier['Resistance']:.6f} K/W."
            )
        )
    elif dernier["Resistance"] > 0.00050:
        alertes.append(
            (
                "warning",
                "Encrassement à surveiller",
                f"Résistance thermique : "
                f"{dernier['Resistance']:.6f} K/W."
            )
        )

    # Turbine
    if dernier["Perte_Turbine"] > 8:
        alertes.append(
            (
                "danger",
                "Pertes turbine élevées",
                f"Pertes estimées : "
                f"{dernier['Perte_Turbine']:.2f} %."
            )
        )

    # Alternateur
    if dernier["Perte_Alternateur"] > 5:
        alertes.append(
            (
                "danger",
                "Pertes alternateur élevées",
                f"Pertes estimées : "
                f"{dernier['Perte_Alternateur']:.2f} %."
            )
        )

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

        classe = (
            "alert-danger"
            if niveau == "danger"
            else "alert-warning"
        )

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
# 8. PAGE DE CONNEXION
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

                            <div class="logo-subtitle">
                                GROUPE OCP
                            </div>

                        </div>

                    </div>

                    <div class="login-right">

                        <div class="login-title">
                            Bienvenue sur votre Dashboard GTA
                        </div>

                        <div class="login-description">
                            Merci de rentrer votre identifiant et mot de passe
                        </div>

                    </div>

                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------
    # Formulaire positionné visuellement sur la partie droite
    # ------------------------------------------------------------

    # Les colonnes permettent de positionner le formulaire
    # par-dessus la carte blanche.
    left, right = st.columns([1.2, 1.8])

    with right:

        st.markdown(
            """
            <style>
            div[data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }

            .login-form-label {
                font-size: 13px;
                font-weight: 500;
                color: #333;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Petit décalage pour aligner le formulaire avec la carte
        st.markdown(
            "<div style='height: 175px'></div>",
            unsafe_allow_html=True
        )

        with st.form("login_form"):

            username = st.text_input(
                "Identifiant *",
                placeholder="Entrez votre identifiant"
            )

            password = st.text_input(
                "Mot de passe *",
                type="password",
                placeholder="Entrez votre mot de passe"
            )

            connexion = st.form_submit_button(
                "Connecter",
                use_container_width=True
            )

            if connexion:

                if username == "admin" and password == "1234567":

                    st.session_state["authentifie"] = True
                    st.session_state["username"] = username

                    st.rerun()

                else:

                    st.error(
                        "Identifiant ou mot de passe incorrect."
                    )


# ================================================================
# 9. TOP BAR
# ================================================================

def afficher_topbar():

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown(
            ocp_logo(),
            unsafe_allow_html=True
        )

    with col2:

        username = st.session_state["username"]

        c1, c2 = st.columns([1.2, 1])

        with c1:

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    padding-top:8px;
                    color:#444;
                    font-size:13px;
                    font-weight:500;
                ">
                    👤 {username}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            if st.button(
                "Se déconnecter",
                key="logout"
            ):

                st.session_state["authentifie"] = False
                st.session_state["username"] = ""

                st.rerun()


# ================================================================
# 10. SIDEBAR
# ================================================================

def afficher_sidebar():

    st.sidebar.markdown(
        """
        <div style="
            text-align:center;
            font-size:25px;
            margin-bottom:15px;
        ">
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
# 11. PAGE ACCUEIL
# ================================================================

def page_accueil(df):

    st.markdown(
        '<div class="page-title">Centre de monitoring GTA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Vue globale du Groupe Turbo-Alternateur
            • Surveillance en temps réel
            • Diagnostic industriel
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------
    # Informations temps réel
    # ------------------------------------------------------------

    afficher_alertes(df)

    st.markdown("<br>", unsafe_allow_html=True)

    dernier = df.iloc[-1]
    precedent = df.iloc[-2]

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Rendement GTA",
            f"{dernier['Rendement']:.2f} %",
            f"{dernier['Rendement'] - precedent['Rendement']:.2f} %"
        )

    with c2:

        st.metric(
            "Résistance condenseur",
            f"{dernier['Resistance']:.6f}",
            f"{(dernier['Resistance'] - precedent['Resistance']):.6f}"
        )

    with c3:

        st.metric(
            "Perte turbine",
            f"{dernier['Perte_Turbine']:.2f} %",
            f"{dernier['Perte_Turbine'] - precedent['Perte_Turbine']:.2f} %"
        )

    with c4:

        st.metric(
            "Perte alternateur",
            f"{dernier['Perte_Alternateur']:.2f} %",
            f"{dernier['Perte_Alternateur'] - precedent['Perte_Alternateur']:.2f} %"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # Puissances
    # ------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="section-title">Puissance turbine</div>',
            unsafe_allow_html=True
        )

        fig = graphique_ligne(
            df,
            "Temps",
            "Puissance_Turbine",
            "Évolution de la puissance mécanique",
            "Puissance",
            "MW"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown(
            '<div class="section-title">Puissance alternateur</div>',
            unsafe_allow_html=True
        )

        fig = graphique_ligne(
            df,
            "Temps",
            "Puissance_Alternateur",
            "Évolution de la puissance électrique",
            "Puissance",
            "MW"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ================================================================
# 12. PAGE RENDEMENT
# ================================================================

def page_rendement(df):

    st.markdown(
        '<div class="page-title">Rendement du GTA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Suivi du rendement global du Groupe Turbo-Alternateur
        </div>
        """,
        unsafe_allow_html=True
    )

    dernier = df.iloc[-1]

    rendement_moyen = df["Rendement"].mean()
    rendement_max = df["Rendement"].max()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Rendement actuel",
            f"{dernier['Rendement']:.2f} %"
        )

    with c2:

        st.metric(
            "Rendement moyen",
            f"{rendement_moyen:.2f} %"
        )

    with c3:

        st.metric(
            "Rendement maximal",
            f"{rendement_max:.2f} %"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    fig = graphique_ligne(
        df,
        "Temps",
        "Rendement",
        "Évolution du rendement global",
        "Rendement",
        "%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="dashboard-card">
            <b>Interprétation :</b><br>
            Le rendement global permet d'évaluer la performance
            énergétique du GTA. Une diminution durable peut indiquer
            une dégradation des performances de la turbine,
            du condenseur ou de l'alternateur.
        </div>
        """,
        unsafe_allow_html=True
    )


# ================================================================
# 13. PAGE RÉSISTANCE D'ENCRASSEMENT
# ================================================================

def page_resistance(df):

    st.markdown(
        '<div class="page-title">Résistance d\'encrassement</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Suivi de la résistance thermique du condenseur
        </div>
        """,
        unsafe_allow_html=True
    )

    dernier = df.iloc[-1]

    resistance_moyenne = df["Resistance"].mean()
    resistance_max = df["Resistance"].max()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Résistance actuelle",
            f"{dernier['Resistance']:.6f} K/W"
        )

    with c2:

        st.metric(
            "Valeur moyenne",
            f"{resistance_moyenne:.6f} K/W"
        )

    with c3:

        st.metric(
            "Valeur maximale",
            f"{resistance_max:.6f} K/W"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    fig = graphique_ligne(
        df,
        "Temps",
        "Resistance",
        "Évolution de la résistance thermique",
        "Résistance thermique",
        "K/W"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Diagnostic
    if dernier["Resistance"] > 0.00055:

        st.error(
            "⚠️ Encrassement important détecté : "
            "une inspection du condenseur est recommandée."
        )

    elif dernier["Resistance"] > 0.00050:

        st.warning(
            "⚠️ Niveau d'encrassement à surveiller."
        )

    else:

        st.success(
            "✓ Résistance thermique dans une plage normale."
        )


# ================================================================
# 14. PAGE PERTES TURBINE
# ================================================================

def page_perte_turbine(df):

    st.markdown(
        '<div class="page-title">Pertes turbine</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Analyse des pertes thermiques et mécaniques de la turbine
        </div>
        """,
        unsafe_allow_html=True
    )

    dernier = df.iloc[-1]

    moyenne = df["Perte_Turbine"].mean()
    maximum = df["Perte_Turbine"].max()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Pertes actuelles",
            f"{dernier['Perte_Turbine']:.2f} %"
        )

    with c2:

        st.metric(
            "Pertes moyennes",
            f"{moyenne:.2f} %"
        )

    with c3:

        st.metric(
            "Pertes maximales",
            f"{maximum:.2f} %"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    fig = graphique_ligne(
        df,
        "Temps",
        "Perte_Turbine",
        "Évolution des pertes turbine",
        "Pertes",
        "%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if dernier["Perte_Turbine"] > 8:

        st.error(
            "⚠️ Pertes turbine élevées. "
            "Une analyse des conditions de fonctionnement est recommandée."
        )

    else:

        st.success(
            "✓ Pertes turbine dans la plage de fonctionnement normale."
        )


# ================================================================
# 15. PAGE PERTES ALTERNATEUR
# ================================================================

def page_perte_alternateur(df):

    st.markdown(
        '<div class="page-title">Pertes alternateur</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Analyse des pertes électriques de l'alternateur
        </div>
        """,
        unsafe_allow_html=True
    )

    dernier = df.iloc[-1]

    moyenne = df["Perte_Alternateur"].mean()
    maximum = df["Perte_Alternateur"].max()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Pertes actuelles",
            f"{dernier['Perte_Alternateur']:.2f} %"
        )

    with c2:

        st.metric(
            "Pertes moyennes",
            f"{moyenne:.2f} %"
        )

    with c3:

        st.metric(
            "Pertes maximales",
            f"{maximum:.2f} %"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    fig = graphique_ligne(
        df,
        "Temps",
        "Perte_Alternateur",
        "Évolution des pertes alternateur",
        "Pertes",
        "%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if dernier["Perte_Alternateur"] > 5:

        st.error(
            "⚠️ Pertes alternateur élevées. "
            "Vérifier les conditions électriques et thermiques."
        )

    else:

        st.success(
            "✓ Pertes alternateur dans la plage normale."
        )


# ================================================================
# 16. APPLICATION PRINCIPALE
# ================================================================

def application_principale():

    # ------------------------------------------------------------
    # Génération des données
    # ------------------------------------------------------------

    if st.session_state["historique"] is None:

        st.session_state["historique"] = generer_donnees_gta(60)

    # ------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------

    page = afficher_sidebar()

    # ------------------------------------------------------------
    # Top bar
    # ------------------------------------------------------------

    st.markdown(
        '<div class="topbar">',
        unsafe_allow_html=True
    )

    afficher_topbar()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------
    # Données
    # ------------------------------------------------------------

    df = st.session_state["historique"]

    # ------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # Actualisation automatique
    # ------------------------------------------------------------

    # Streamlit >= 1.37
    # Le fragment permet de relancer automatiquement l'application.
    #
    # Pour une véritable connexion industrielle, cette simulation
    # devra être remplacée par une source de données réelle :
    # OPC-UA, Modbus, API, SQL, Historian, etc.

    st.markdown(
        f"""
        <div class="footer">
            Dashboard GTA • Groupe OCP •
            Dernière mise à jour :
            {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        </div>
        """,
        unsafe_allow_html=True
    )


# ================================================================
# 17. MODE TEMPS RÉEL
# ================================================================

# Pour éviter de dépendre d'une librairie externe comme
# streamlit-autorefresh, on utilise le mécanisme de fragments
# disponible dans les versions récentes de Streamlit.

def dashboard_realtime():

    @st.fragment(run_every="5s")
    def monitoring():

        # --------------------------------------------------------
        # Génération d'une nouvelle mesure
        # --------------------------------------------------------

        nouvelles_donnees = generer_donnees_gta(1)

        # --------------------------------------------------------
        # Historique existant
        # --------------------------------------------------------

        if st.session_state["historique"] is None:

            st.session_state["historique"] = generer_donnees_gta(59)

        df = st.session_state["historique"]

        # --------------------------------------------------------
        # Ajout de la nouvelle mesure
        # --------------------------------------------------------

        df = pd.concat(
            [
                df,
                nouvelles_donnees
            ],
            ignore_index=True
        )

        # Conservation des 60 derniers points
        df = df.tail(60).reset_index(drop=True)

        st.session_state["historique"] = df

        # --------------------------------------------------------
        # Navigation
        # --------------------------------------------------------

        page = afficher_sidebar()

        # --------------------------------------------------------
        # Top bar
        # --------------------------------------------------------

        st.markdown(
            '<div class="topbar">',
            unsafe_allow_html=True
        )

        afficher_topbar()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # --------------------------------------------------------
        # Affichage
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # Footer
        # --------------------------------------------------------

        st.markdown(
            f"""
            <div class="footer">
                Dashboard GTA • Groupe OCP •
                Monitoring temps réel •
                Dernière mise à jour :
                {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            </div>
            """,
            unsafe_allow_html=True
        )

    monitoring()


# ================================================================
# 18. POINT D'ENTRÉE
# ================================================================

if not st.session_state["authentifie"]:

    page_login()

else:

    dashboard_realtime()