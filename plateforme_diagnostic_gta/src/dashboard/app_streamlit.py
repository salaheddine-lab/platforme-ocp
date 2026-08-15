import streamlit as st
import base64
from PIL import Image
from pathlib import Path

# ================================================================
# 1. CONFIGURATION GLOBALE
# ================================================================

st.set_page_config(
    page_title="Dashboard GTA | OCP Groupe",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================================================
# 2. GESTION DES ASSETS ET ASYNCHRONE
# ================================================================

# Pour le développement, vous pouvez utiliser des liens d'images de démonstration.
# Pour la production, remplacez-les par les chemins locaux exacts.

LOGO_OCP_DEMO = "https://iconlogovector.com/logo/ocp-group/seeklogo.com-ocp-group-vector-logo.png"
FOND_MINIER_DEMO = "https://images.unsplash.com/photo-1549416878-b998782a2099"

# Fonction pour encoder une image locale en base64 pour l'utiliser dans le CSS
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.warning(f"Impossible de charger l'image {image_path}. Vérifiez le chemin. {e}")
        return ""

# Définit les fichiers locaux exacts (images fournies dans votre exemple)
chemin_logo_local = Path(__file__).parent / "central_logo.png"
chemin_fond_local = Path(__file__).parent / "fond_gta.jpg"

# ================================================================
# 3. CSS COMPACT (L'INGÉNIERIE CLÉ)
# ================================================================

# Nous ciblons les classes internes de Streamlit '[data-testid="stHorizontalBlock"]'
# pour transformer les colonnes standard en blocs de formulaire chic.

# Encode les images locales pour le CSS
bg_base64 = get_base64_image(chemin_fond_local) if chemin_fond_local.exists() else get_base64_image(Path(__file__).parent.parent / "fond_gta.jpg")
logo_base64 = get_base64_image(chemin_logo_local) if chemin_logo_local.exists() else get_base64_image(Path(__file__).parent.parent / "central_logo.png")

# Si les images locales n'existent pas, on utilise les URL de démonstration
bg_url_css = f"url('data:image/jpg;base64,{bg_base64}')" if bg_base64 else f"url('{FOND_MINIER_DEMO}')"
logo_url_css = f"url('data:image/jpg;base64,{logo_base64}')" if logo_base64 else f"url('{LOGO_OCP_DEMO}')"

css_formulaire = f"""
<style>
/* 1. Masquer les éléments Streamlit standard */
#MainMenu, header, footer {{
    visibility: hidden;
}}

/* 2. Style de l'arrière-plan de l'application (l'image minière) */
.stApp {{
    background-image: {bg_url_css} !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    height: 100vh !important;
    width: 100vw !important;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden !important;
}}

/* 3. Masquer les instructions de formulaire standard pour un look minimaliste */
div[data-testid="stFormSubmitInstructions"], div[data-testid="InputInstructions"] {{
    display: none !important;
}}

/* 4. LA CARTE BLANCHE COMPACTE ET CHIC (Targeting internal Streamlit classes) */
/* Nous ciblons un bloc horizontal (stHorizontalBlock) et lui donnons l'apparence de la carte */
div[data-testid="stHorizontalBlock"] {{
    background-color: white !important;
    border-radius: 20px !important;
    padding: 30px !important;
    max-width: 750px !important;
    width: 100%;
    margin: 0 auto !important;
    display: flex;
    justify-content: space-between;
    align-items: center !important;
    gap: 15px !important;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4) !important;
    min-height: 250px;
}}

/* 5. CIBLAGE DES COLONNES INDIVIDUELLES (The balanced look) */
/* Streamlit utilise une grille 12. Nous devons équilibrer les colonnes pour les formulaires. */

/* La colonne de gauche (logo OCP) */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) {{
    flex: 1 1 35% !important; /* Donne 35% de largeur au logo */
    max-width: 35% !important;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* La colonne de droite (formulaire de connexion) */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) {{
    flex: 1 1 65% !important; /* Donne 65% de largeur au formulaire */
    max-width: 65% !important;
    padding-left: 20px !important;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

/* 6. STYLE DES WIDGETS ET DU BOUTON LARGE */
/* Supprime les bordures Streamlit standard des conteneurs de formulaire */
div[data-testid="stForm"] {{
    border: none !important;
    padding: 0 !important;
    background-color: transparent !important;
}}

/* Style des champs de texte pour plus de clarté */
div[data-testid="stTextInput"] {{
    margin-bottom: 0px !important; /* Supprime l'espace pour un look ultra-compact */
}}
div[data-testid="stTextInput"] > div > div > input {{
    background-color: #f7f9f8 !important;
    border: 1px solid #e1e8ed !important;
    border-radius: 8px !important;
    color: #333 !important;
}}

/* Style des labels pour les rapprocher de l'exemple */
div[data-testid="stTextInput"] > label > div > p {{
    font-weight: 500 !important;
    font-size: 14px !important;
}}

/* LE BOUTON LARGE ET PLEINE LARGEUR */
div[data-testid="stFormSubmitButton"] > button {{
    background-color: #007A33 !important;
    color: white !important;
    border-radius: 20px !important;
    padding: 8px 30px !important;
    width: 100% !important; /* Étend le bouton sur toute la largeur */
    border: none !important;
    margin-top: 20px !important;
    font-weight: bold;
    font-size: 15px;
}}
div[data-testid="stFormSubmitButton"] > button:hover {{
    background-color: #005f27 !important;
    color: white !important;
    border: none !important;
}}

</style>
"""

# Injection du CSS
st.markdown(css_formulaire, unsafe_allow_html=True)

# ================================================================
# 4. LE LAYOUT PYTHON EXACT
# ================================================================

# Pour recréer la structure de la carte, nous utilisons une seule ligne de colonnes Streamlit.
# Le CSS s'occupera de transformer cette structure en carte.

# Création de la structure de colonnes (1:1.3 pour équilibrer logo et formulaire)
col_logo, col_form = st.columns([1, 1.3])

# SECTION DE GAUCHE : LOGO OCP
with col_logo:
    if chemin_logo_local.exists():
        img_logo = Image.open(chemin_logo_local)
        st.image(img_logo, width=110)
    else:
        # Utilise l'image de démonstration en ligne si le fichier local n'existe pas
        st.image(LOGO_OCP_DEMO, width=110)

# SECTION DE DROITE : LE FORMULAIRE DE RE-AUTHENTIFICATION
with col_form:
    # 1. Le Titre Principal avec le style exact
    st.markdown("""
        <h2 style='font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 0px;'>
            Bienvenue sur votre
        </h2>
        <h2 style='font-size: 24px; font-weight: bold; color: #2c3e50; margin-top: -5px; margin-bottom: 10px;'>
            Dashboard GTA
        </h2>
        <p style='font-size: 13px; color: #7a817d; margin-bottom: 20px;'>
            Merci de rentrer votre identifiant et mot de passe
        </p>
    """, unsafe_allow_html=True)

    # 2. Le Formulaire et les Champs Compacts
    with st.form("login_form"):
        # Labels exacts et placeholders de votre exemple
        st.text_input("Identifiant *", placeholder="salaheddine.aki")
        st.text_input("Mot de passe *", type="password", placeholder="••••••••")
        
        # Le bouton large (le CSS s'occupe de la largeur)
        st.form_submit_button("Se connecter")