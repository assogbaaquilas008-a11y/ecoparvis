import streamlit as st
import urllib.parse
import base64
import sqlite3
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ─── Configuration de la page ───────────────────────────────────────────────
st.set_page_config(page_title="ST-Ecoparvis - Pavés Écologiques", page_icon="♻️", layout="wide")

# ─── Base de données historique ──────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("ecoparvis_historique.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS devis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT, nom TEXT, contact TEXT, type_pave TEXT,
        surface REAL, zone TEXT, couleur TEXT, forme TEXT,
        motif TEXT, montant_total REAL, plastique_kg REAL
    )""")
    conn.commit()
    conn.close()

# ─── Envoi email notification ─────────────────────────────────────────────────
def envoyer_email_notification(nom, contact, type_pave, surface, montant_total, zone):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'eloisemable17@gmail.com'
        msg['To'] = 'eloisemable17@gmail.com'
        msg['Subject'] = f'🌱 Nouvelle commande ST-Ecoparvis — {nom}'
        body = f'''
Nouvelle commande reçue !

👤 Client : {nom}
📞 Contact : {contact}
🧱 Type pavé : {type_pave}
📐 Surface : {surface} m²
📍 Zone : {zone}
💰 Montant total : {montant_total:,.0f} FCFA

Connectez-vous au tableau de bord admin pour plus de détails.
— ST-Ecoparvis
        '''
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Remplacez 'VOTRE_MOT_DE_PASSE_APP' par un mot de passe d'application Gmail
        server.login('eloisemable17@gmail.com', 'VOTRE_MOT_DE_PASSE_APP')
        server.sendmail('eloisemable17@gmail.com', 'eloisemable17@gmail.com', msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

def sauvegarder_devis(nom, contact, type_pave, surface, zone, couleur, forme, motif, montant_total, plastique_kg):
    conn = sqlite3.connect("ecoparvis_historique.db")
    c = conn.cursor()
    c.execute("""INSERT INTO devis (date,nom,contact,type_pave,surface,zone,couleur,forme,motif,montant_total,plastique_kg)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
              (datetime.now().strftime("%d/%m/%Y %H:%M"), nom, contact, type_pave,
               surface, zone, couleur, forme, motif, montant_total, plastique_kg))
    conn.commit()
    conn.close()

def get_historique(contact):
    conn = sqlite3.connect("ecoparvis_historique.db")
    c = conn.cursor()
    c.execute("SELECT * FROM devis WHERE contact=? ORDER BY id DESC LIMIT 10", (contact,))
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ─── Envoi email notification ─────────────────────────────────────────────────
def envoyer_email_notification(nom, contact, type_pave, surface, montant_total, zone):
    try:
        msg = MIMEMultipart()
        msg['From'] = 'eloisemable17@gmail.com'
        msg['To'] = 'eloisemable17@gmail.com'
        msg['Subject'] = f'🌱 Nouvelle commande ST-Ecoparvis — {nom}'
        body = f'''
Nouvelle commande reçue !

👤 Client : {nom}
📞 Contact : {contact}
🧱 Type pavé : {type_pave}
📐 Surface : {surface} m²
📍 Zone : {zone}
💰 Montant total : {montant_total:,.0f} FCFA

Connectez-vous au tableau de bord admin pour plus de détails.
— ST-Ecoparvis
        '''
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Remplacez 'VOTRE_MOT_DE_PASSE_APP' par un mot de passe d'application Gmail
        server.login('eloisemable17@gmail.com', 'VOTRE_MOT_DE_PASSE_APP')
        server.sendmail('eloisemable17@gmail.com', 'eloisemable17@gmail.com', msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

# ─── Traductions ─────────────────────────────────────────────────────────────
TRADUCTIONS = {
    "Français": {
        "titre": "ST-ECOPARVIS", "slogan": "Chaque déchet est une brique d'avenir",
        "sous_titre": "Conception de pavés recyclés, zéro résidu et haute performance.",
        "nav": ["Accueil & Concept", "Calculateur Technique & Devis", "Galerie Réalisations", "Contact", "Mon Historique", "Témoignages", "Admin 🔐"],
        "vision": "Notre Vision", "pourquoi": "Pourquoi choisir ST-Ecoparvis ?",
        "surface": "Surface à couvrir (en m²)", "type_pave": "Type de pavé",
        "zone": "Zone de livraison", "pluie": "Intensité de pluie simulée",
        "couleur_titre": "Personnalisation de la couleur",
        "couleur_q": "Souhaitez-vous une couleur ?",
        "naturel": "Naturel (sans supplément)",
        "couleur_unie": "Couleur unie (+500 FCFA/m²)",
        "melange": "Mélange de couleurs (prix variable)",
        "nb_couleurs": "Nombre de couleurs",
        "couleurs_dispo": "Choisissez vos couleurs",
        "forme_titre": "Forme du pavé",
        "motif_titre": "Motif sur le pavé",
        "motif_std": "Motif standard",
        "motif_perso": "Motif personnalisé (photo via WhatsApp)",
        "superficie_titre": "Comment saisir votre superficie ?",
        "manuelle": "Saisie manuelle",
        "carte": "Via carte (OpenStreetMap)",
        "carte_info": "Dessinez votre terrain sur la carte pour calculer la superficie automatiquement.",
        "montant": "Montant Total Estimé",
        "commander": "Passer la commande",
        "nom": "Votre Nom / Entreprise",
        "contact_label": "Numéro WhatsApp",
        "btn_wa": "Générer et envoyer la commande sur WhatsApp",
        "historique": "Mon Historique de Devis",
        "contact_page": "Contactez-nous",
        "plastique": "kg de déchets plastiques retirés de la nature !",
        "resistance": "Résistance mécanique",
        "simulation": "Simulation pluie",
        "specs": "Spécifications & Simulation",
        "galerie": "Galerie ST-Ecoparvis",
        "galerie_sous": "Aperçu de nos pavés et réalisations",
    },
    "English": {
        "titre": "ST-ECOPARVIS", "slogan": "Every waste is a brick for the future",
        "sous_titre": "Recycled paving stones — zero waste, high performance.",
        "nav": ["Home & Concept", "Technical Calculator & Quote", "Gallery", "Contact", "My History", "Testimonials", "Admin 🔐"],
        "vision": "Our Vision", "pourquoi": "Why choose ST-Ecoparvis?",
        "surface": "Area to cover (m²)", "type_pave": "Paving type",
        "zone": "Delivery zone", "pluie": "Simulated rain intensity",
        "couleur_titre": "Color customization",
        "couleur_q": "Do you want a color?",
        "naturel": "Natural (no extra cost)",
        "couleur_unie": "Single color (+500 FCFA/m²)",
        "melange": "Color mix (variable price)",
        "nb_couleurs": "Number of colors",
        "couleurs_dispo": "Choose your colors",
        "forme_titre": "Paving shape",
        "motif_titre": "Pattern on the paving",
        "motif_std": "Standard pattern",
        "motif_perso": "Custom pattern (photo via WhatsApp)",
        "superficie_titre": "How to enter your area?",
        "manuelle": "Manual entry",
        "carte": "Via map (OpenStreetMap)",
        "carte_info": "Draw your land on the map to auto-calculate the area.",
        "montant": "Estimated Total Amount",
        "commander": "Place your order",
        "nom": "Your Name / Company",
        "contact_label": "WhatsApp Number",
        "btn_wa": "Generate and send order via WhatsApp",
        "historique": "My Quote History",
        "contact_page": "Contact Us",
        "plastique": "kg of plastic waste removed from nature!",
        "resistance": "Mechanical resistance",
        "simulation": "Rain simulation",
        "specs": "Specifications & Simulation",
        "galerie": "ST-Ecoparvis Gallery",
        "galerie_sous": "Preview of our paving stones and achievements",
    },
    "Español": {
        "titre": "ST-ECOPARVIS", "slogan": "Cada residuo es un ladrillo para el futuro",
        "sous_titre": "Adoquines reciclados — cero residuos, alto rendimiento.",
        "nav": ["Inicio & Concepto", "Calculadora & Presupuesto", "Galería", "Contacto", "Mi Historial", "Testimonios", "Admin 🔐"],
        "vision": "Nuestra Visión", "pourquoi": "¿Por qué elegir ST-Ecoparvis?",
        "surface": "Superficie a cubrir (m²)", "type_pave": "Tipo de adoquín",
        "zone": "Zona de entrega", "pluie": "Intensidad de lluvia simulada",
        "couleur_titre": "Personalización de color",
        "couleur_q": "¿Desea un color?",
        "naturel": "Natural (sin recargo)",
        "couleur_unie": "Color sólido (+500 FCFA/m²)",
        "melange": "Mezcla de colores (precio variable)",
        "nb_couleurs": "Número de colores",
        "couleurs_dispo": "Elija sus colores",
        "forme_titre": "Forma del adoquín",
        "motif_titre": "Motivo en el adoquín",
        "motif_std": "Motivo estándar",
        "motif_perso": "Motivo personalizado (foto vía WhatsApp)",
        "superficie_titre": "¿Cómo ingresar su superficie?",
        "manuelle": "Entrada manual",
        "carte": "Via mapa (OpenStreetMap)",
        "carte_info": "Dibuje su terreno en el mapa para calcular el área automáticamente.",
        "montant": "Monto Total Estimado",
        "commander": "Realizar pedido",
        "nom": "Su Nombre / Empresa",
        "contact_label": "Número WhatsApp",
        "btn_wa": "Generar y enviar pedido por WhatsApp",
        "historique": "Mi Historial de Presupuestos",
        "contact_page": "Contáctenos",
        "plastique": "kg de residuos plásticos retirados de la naturaleza!",
        "resistance": "Resistencia mecánica",
        "simulation": "Simulación de lluvia",
        "specs": "Especificaciones & Simulación",
        "galerie": "Galería ST-Ecoparvis",
        "galerie_sous": "Vista previa de nuestros adoquines y realizaciones",
    },
    "Fon": {
        "titre": "ST-ECOPARVIS", "slogan": "Bɔbɔ bǐ nyí agbǎ ɖokpo",
        "sous_titre": "Mǐ wà pavé lɛ sín fánní jɔ, bo ma ɖó fánní ɖokpo.",
        "nav": ["Hwɛ & Nǔ", "Tɛnmɛ & Azɔ̌", "Mɛtɛnmɛ", "Wá mǐ kpɔ́n", "Azɔ̌ Taji", "Nǔ Yɔyɔ̌", "Admin 🔐"],
        "vision": "Mǐɖé nǔ wà", "pourquoi": "Etɛ wu è na xɔ ST-Ecoparvis?",
        "surface": "Fí e a jló na kpé (m²)", "type_pave": "Pavé xɔ́ntɔn",
        "zone": "Fí e è na zán", "pluie": "Jɔhɔn sixu kpé",
        "couleur_titre": "Rɔ̌ xɔ́ntɔn",
        "couleur_q": "A jló rɔ̌ ɖé à?",
        "naturel": "Sín ayǐ (ɖě sín)",
        "couleur_unie": "Rɔ̌ ɖokpo (+500 FCFA/m²)",
        "melange": "Rɔ̌ lɛ bǐ (nǔɖé)",
        "nb_couleurs": "Rɔ̌ mɛ",
        "couleurs_dispo": "Xɔ rɔ̌ lɛ",
        "forme_titre": "Pavé ta",
        "motif_titre": "Motif ɖò pavé",
        "motif_std": "Motif ɖé",
        "motif_perso": "Motif towe (foto WhatsApp)",
        "superficie_titre": "Alǒ tɛ nu a na zán?",
        "manuelle": "A wlan bǐ",
        "carte": "Carte jí",
        "carte_info": "Wlan fí towe ɖò carte jí.",
        "montant": "Gbɛ̌ bǐ mlɛ́mlɛ́",
        "commander": "Sɛ̀n azɔ̌",
        "nom": "Nyǐkɔ towe",
        "contact_label": "WhatsApp",
        "btn_wa": "Sɛ̀n azɔ̌ WhatsApp jí",
        "historique": "Azɔ̌ taji towe",
        "contact_page": "Wá mǐ kpɔ́n",
        "plastique": "kg fánní e è sɔ́ sín ayǐkúngban!",
        "resistance": "Pavé gbɔ̌n",
        "simulation": "Jɔhɔn tɛnmɛ",
        "specs": "Nǔ & Tɛnmɛ",
        "galerie": "Mɛtɛnmɛ ST-Ecoparvis",
        "galerie_sous": "Pavé lɛ kpɔ́n",
    },
    "Yoruba": {
        "titre": "ST-ECOPARVIS", "slogan": "Ẹ̀tàn kọọkan jẹ́ gẹ̀lẹ̀ kan fún ọjọ́ iwájú",
        "sous_titre": "Pavé tí a tún ṣe — kò sí ègbin, agbára gíga.",
        "nav": ["Ilé & Èrò", "Iṣirò & Iye Owó", "Àwòrán", "Kan Sí Wa", "Ìtàn Mi", "Ẹ̀rí Àwọn Oníbàárà", "Admin 🔐"],
        "vision": "Ìríran Wa", "pourquoi": "Kí ló dára nípa ST-Ecoparvis?",
        "surface": "Àgbègbè tó fẹ́ bò (m²)", "type_pave": "Irú pavé",
        "zone": "Àgbègbè ifijiṣẹ́", "pluie": "Ìpele ìjì líle",
        "couleur_titre": "Àṣàyàn àwọ̀",
        "couleur_q": "Ṣé o fẹ́ àwọ̀?",
        "naturel": "Àdánidá (kò sí àfikún)",
        "couleur_unie": "Àwọ̀ kan (+500 FCFA/m²)",
        "melange": "Àpapọ̀ àwọ̀ (iye owó yàtọ̀)",
        "nb_couleurs": "Iye àwọ̀",
        "couleurs_dispo": "Yan àwọ̀ rẹ",
        "forme_titre": "Ìrísí pavé",
        "motif_titre": "Àpẹẹrẹ lórí pavé",
        "motif_std": "Àpẹẹrẹ àdánidá",
        "motif_perso": "Àpẹẹrẹ tìrẹ (fọ́tò WhatsApp)",
        "superficie_titre": "Báwo ni o ṣe fẹ́ tẹ àgbègbè rẹ?",
        "manuelle": "Tẹ pẹ̀lú ọwọ́",
        "carte": "Nípasẹ̀ maapu",
        "carte_info": "Ya àgbègbè rẹ lórí maapu láti ṣe iṣiro.",
        "montant": "Apapọ̀ Iye Owó",
        "commander": "Fí àṣẹ",
        "nom": "Orúkọ rẹ / Ilé-iṣẹ́",
        "contact_label": "Nọ́mbà WhatsApp",
        "btn_wa": "Ṣẹ̀dá àṣẹ lórí WhatsApp",
        "historique": "Ìtàn Àṣẹ Mi",
        "contact_page": "Kan Sí Wa",
        "plastique": "kg ègbin pilasitiki tí a yọ kúrò ní àyíká!",
        "resistance": "Agbára pavé",
        "simulation": "Ìjì líle tẹ̀síwájú",
        "specs": "Àlàyé & Ìfọ̀rọ̀wérọ̀",
        "galerie": "Àwòrán ST-Ecoparvis",
        "galerie_sous": "Wo àwọn pavé àti iṣẹ́ wa",
    }
}

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1B5E20; text-align: center; margin-bottom: 5px; }
    .slogan { font-size: 16px; color: #4CAF50; text-align: center; font-style: italic; margin-bottom: 10px; }
    .section-title { font-size: 24px; font-weight: bold; color: #2E7D32; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #E8F5E9; padding-bottom: 5px; }
    .card { background-color: #F1F8E9; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 15px; }
    .eco-badge { background-color: #E8F5E9; color: #2E7D32; padding: 15px; border-radius: 8px; border: 1px dashed #2E7D32; text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 20px; }
    .contact-card { background-color: #F1F8E9; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 15px; font-size: 16px; }
    .color-notice { background-color: #FFF8E1; padding: 10px; border-radius: 8px; border-left: 4px solid #FFC107; margin-bottom: 10px; font-size: 14px; }
    .logo-box { background: linear-gradient(135deg, #1B5E20, #2E7D32); padding: 18px 36px; border-radius: 16px; display: inline-flex; align-items: center; gap: 14px; box-shadow: 0 8px 32px rgba(27,94,32,0.35); margin-bottom: 10px; }
    .logo-brand { font-size: 28px; font-weight: 900; color: #fff; letter-spacing: 2px; }
    .logo-brand span { color: #A5D6A7; }
    .logo-tag { font-size: 10px; color: #C8E6C9; letter-spacing: 3px; text-transform: uppercase; }
    .historique-card { background: #F9FBE7; border-left: 4px solid #8BC34A; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #1B5E20; color: white; }
    </style>
""", unsafe_allow_html=True)

# ─── Langue ──────────────────────────────────────────────────────────────────
langue = st.sidebar.selectbox("🌍 Langue / Language", list(TRADUCTIONS.keys()))
T = TRADUCTIONS[langue]

# ─── Logo ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; justify-content:center; margin-bottom:8px;">
  <div class="logo-box">
    <span style="font-size:40px;">♻️</span>
    <div>
      <div class="logo-brand"><span>ST-</span>ECOPARVIS</div>
      <div class="logo-tag">Pavés Écologiques · Bénin</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="slogan">"{T["slogan"]}"</div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;color:#555;'>{T['sous_titre']}</p>", unsafe_allow_html=True)

# ─── Navigation ──────────────────────────────────────────────────────────────
menu = st.sidebar.selectbox("Navigation", T["nav"])

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
if menu == T["nav"][0]:
    # Carousel d'images
    images_carousel = [
        "/mnt/user-data/uploads/1000427947.jpg",  # Pavé tenu en main
        "/mnt/user-data/uploads/1000427961.jpg",  # Pavés turquoise/or
        "/mnt/user-data/uploads/1000427945.jpg",  # Pavés hexagonaux bleus
        "/mnt/user-data/uploads/1000428515.jpg",  # Pavés colorés
        "/mnt/user-data/uploads/1000427951.jpg",  # Pavés hexagonaux
        "/mnt/user-data/uploads/1000427983.jpg",  # Motifs plastique
    ]

    captions = [
        "Pavé Écologique ST-Ecoparvis",
        "Mélange Premium Turquoise & Or",
        "Pavés Hexagonaux Bleus",
        "Gamme Colorée ST-Ecoparvis",
        "Pavés Haute Performance",
        "Dalles Plastique Recyclé",
    ]

    if "carousel_idx" not in st.session_state:
        st.session_state.carousel_idx = 0

    img_path = images_carousel[st.session_state.carousel_idx]
    try:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = "jpeg"
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:10px;">
            <img src="data:image/{ext};base64,{b64}"
                 style="width:100%; max-height:380px; object-fit:cover; border-radius:12px;
                        box-shadow:0 4px 20px rgba(0,0,0,0.2);" />
            <p style="color:#555; font-style:italic; margin-top:6px;">
                {captions[st.session_state.carousel_idx]}
            </p>
        </div>
        """, unsafe_allow_html=True)
    except:
        pass

    col_prev, col_dots, col_next = st.columns([1, 4, 1])
    with col_prev:
        if st.button("◀"):
            st.session_state.carousel_idx = (st.session_state.carousel_idx - 1) % len(images_carousel)
            st.rerun()
    with col_dots:
        dots = " ".join(["🟢" if i == st.session_state.carousel_idx else "⚪" for i in range(len(images_carousel))])
        st.markdown(f"<div style='text-align:center;font-size:12px;'>{dots}</div>", unsafe_allow_html=True)
    with col_next:
        if st.button("▶"):
            st.session_state.carousel_idx = (st.session_state.carousel_idx + 1) % len(images_carousel)
            st.rerun()

    st.markdown(f'<div class="section-title">{T["vision"]}</div>', unsafe_allow_html=True)
    st.write("""
    ST-Ecoparvis transforme les défis environnementaux en solutions durables.
    Nos pavés sont conçus à base de déchets plastiques recyclés, offrant une résistance exceptionnelle
    à la compression tout en favorisant une excellente gestion des eaux de ruissellement.
    """)
    st.markdown(f"""
    ### {T["pourquoi"]}
    * **Zéro Résidu :** Valorisation maximale des déchets plastiques qui encombrent nos villes.
    * **Haute Performance :** Une durabilité et une résistance supérieures aux pavés en ciment classiques.
    * **Éco-citoyenneté :** Chaque commande participe directement à la dépollution de notre environnement.
    """)
    st.info("Utilisez le menu de gauche pour accéder aux outils de calcul et passer commande.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CALCULATEUR
# ══════════════════════════════════════════════════════════════════════════════
elif menu == T["nav"][1]:
    st.markdown(f'<div class="section-title">Simulateur de Commande & Calculs Techniques</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧱 Paramètres du Projet")

        # ── Superficie ──────────────────────────────────────────────────────
        st.markdown(f"#### 🗺️ {T['superficie_titre']}")
        mode_superficie = st.radio("", [T["manuelle"], T["carte"]], horizontal=True)

        surface = 10.0
        if mode_superficie == T["manuelle"]:
            surface = st.number_input(T["surface"], min_value=1.0, value=10.0, step=1.0)
        else:
            st.info(T["carte_info"])
            try:
                import folium
                from streamlit_folium import st_folium
                from shapely.geometry import Polygon

                m = folium.Map(location=[6.3654, 2.4183], zoom_start=13)
                folium.plugins.Draw(
                    export=True,
                    draw_options={"polygon": True, "rectangle": True,
                                  "circle": False, "marker": False,
                                  "polyline": False, "circlemarker": False}
                ).add_to(m)
                result = st_folium(m, height=350, width=None)

                if result and result.get("last_active_drawing"):
                    coords = result["last_active_drawing"]["geometry"]["coordinates"][0]
                    poly = Polygon([(c[0], c[1]) for c in coords])
                    # conversion degrés → m² approximative (Bénin ~6°N)
                    import math
                    lat_rad = math.radians(6.3654)
                    m_per_deg_lat = 111132.92
                    m_per_deg_lon = 111132.92 * math.cos(lat_rad)
                    area_deg2 = poly.area
                    surface = area_deg2 * m_per_deg_lat * m_per_deg_lon
                    st.success(f"Superficie calculée : **{surface:,.1f} m²**")
                else:
                    surface = st.number_input(T["surface"], min_value=1.0, value=10.0, step=1.0)
            except ImportError:
                st.warning("Module carte non disponible. Saisie manuelle activée.")
                surface = st.number_input(T["surface"], min_value=1.0, value=10.0, step=1.0)

        # ── Type de pavé ─────────────────────────────────────────────────────
        type_pave = st.selectbox(T["type_pave"], [
            "Pavé Drainant (Éco)", "Pavé Autobloquant Classique", "Pavé Haute Résistance"
        ])

        # ── Forme ────────────────────────────────────────────────────────────
        st.markdown(f"#### 🔷 {T['forme_titre']}")
        formes = {
            "Carré ⬛": 0, "Rectangle ▬": 0,
            "Hexagone ⬡ (+300 FCFA/m²)": 300,
            "Forme H/I/S/Z (+500 FCFA/m²)": 500,
            "Forme personnalisée (+1000 FCFA/m²)": 1000
        }
        forme_choisie = st.selectbox(T["forme_titre"], list(formes.keys()))
        supplement_forme = formes[forme_choisie]

        # ── Motif ────────────────────────────────────────────────────────────
        st.markdown(f"#### 🎭 {T['motif_titre']}")
        motifs_std = {
            "Lisse (sans motif)": 0,
            "Briques classiques 🧱": 300,
            "Chevrons / Hérringbone ↗": 300,
            "Hexagones ⬡": 300,
            "Quadrillage ⊞": 300,
            "Losanges / Damier ◇": 300,
            "Cercles ○": 300,
            "Opus romain (multi-rectangles)": 300,
            "Galets / Organiques 〰": 300,
            "Spirale / Rosace 🌸 (+800 FCFA/m²)": 800,
        }
        option_motif = st.radio(T["motif_titre"], [T["motif_std"], T["motif_perso"]])
        if option_motif == T["motif_std"]:
            motif_choisi = st.selectbox("", list(motifs_std.keys()))
            supplement_motif = motifs_std[motif_choisi]
        else:
            motif_choisi = "Motif personnalisé"
            supplement_motif = 1000
            st.markdown("""
            <div class="color-notice">
            📸 <b>Info :</b> Après votre commande, envoyez la photo de votre motif
            sur notre WhatsApp. Supplément : <b>+1000 FCFA/m²</b>
            </div>""", unsafe_allow_html=True)

        # ── Couleur ──────────────────────────────────────────────────────────
        st.markdown(f"#### 🎨 {T['couleur_titre']}")
        couleurs_dispo = ["Rouge brique 🔴", "Vert 🟢", "Jaune 🟡",
                          "Gris anthracite ⬛", "Violet 🟣", "Bleu 🔵",
                          "Noir ⬛", "Blanc ⬜", "Orange 🟠"]

        option_couleur = st.radio(T["couleur_q"], [
            T["naturel"], T["couleur_unie"], T["melange"]
        ])
        supplement_couleur = 0
        couleur_choisie = "Naturel"

        if option_couleur == T["couleur_unie"]:
            supplement_couleur = 500
            couleur_choisie = st.selectbox(T["couleurs_dispo"], couleurs_dispo)
            st.markdown(f"""<div class="color-notice">
            ⚠️ Supplément couleur : <b>+500 FCFA/m²</b></div>""", unsafe_allow_html=True)

        elif option_couleur == T["melange"]:
            nb_couleurs = st.slider(T["nb_couleurs"], 2, 5, 2)
            supplement_couleur = nb_couleurs * 500
            couleurs_selectionnees = st.multiselect(
                T["couleurs_dispo"], couleurs_dispo,
                max_selections=nb_couleurs
            )
            couleur_choisie = " + ".join(couleurs_selectionnees) if couleurs_selectionnees else "Mélange"
            st.markdown(f"""<div class="color-notice">
            🎨 {nb_couleurs} couleurs sélectionnées → Supplément : <b>+{supplement_couleur} FCFA/m²</b>
            </div>""", unsafe_allow_html=True)

        # ── Zone de livraison ─────────────────────────────────────────────────
        zone_livraison = st.selectbox(T["zone"], [
            "Cotonou / Calavi", "Porto-Novo", "Abomey / Bohicon",
            "Parakou", "Retrait sur place (Gratuit)"
        ])

        # ── Intensité pluie ──────────────────────────────────────────────────
        intensite_pluie = st.select_slider(T["pluie"],
            options=["Faible", "Modérée", "Forte (Saison des pluies)"])

        # ── Configs pavé ─────────────────────────────────────────────────────
        if type_pave == "Pavé Drainant (Éco)":
            prix_unitaire = 5000; plastique_par_m2 = 12.5; resistance = "~30 MPa"
            drainage_info = {"Faible": "🟢 Absorption totale instantanée.",
                             "Modérée": "🟢 Évacuation fluide.",
                             "Forte (Saison des pluies)": "🟡 Absorption maximale activée."
                             }[intensite_pluie]
        elif type_pave == "Pavé Autobloquant Classique":
            prix_unitaire = 4500; plastique_par_m2 = 14.0; resistance = "~45 MPa"
            drainage_info = {"Faible": "🟢 Légère infiltration par les joints.",
                             "Modérée": "🟡 Ruissellement standard.",
                             "Forte (Saison des pluies)": "🔴 Risque de stagnation."
                             }[intensite_pluie]
        else:
            prix_unitaire = 6500; plastique_par_m2 = 18.5; resistance = "~55 MPa"
            drainage_info = "❌ Structure étanche haute densité."

        # ── Frais de livraison proportionnels ────────────────────────────────
        nb_paves_estimes = surface * 20  # ~20 pavés/m²
        if zone_livraison == "Retrait sur place (Gratuit)":
            frais_livraison = 0
        elif zone_livraison == "Cotonou / Calavi":
            frais_livraison = 5000 + (surface * 300)
            if nb_paves_estimes > 500: frais_livraison += 10000  # camion
        elif zone_livraison == "Porto-Novo":
            frais_livraison = 7000 + (surface * 300)
            if nb_paves_estimes > 500: frais_livraison += 10000
        elif zone_livraison == "Abomey / Bohicon":
            frais_livraison = 10000 + (surface * 400)
            if nb_paves_estimes > 400: frais_livraison += 15000
        else:  # Parakou
            frais_livraison = 20000 + (surface * 500)
            if nb_paves_estimes > 300: frais_livraison += 20000
        # Arrondi à 500 FCFA près
        frais_livraison = round(frais_livraison / 500) * 500

    # ── Colonne droite ────────────────────────────────────────────────────────
    with col2:
        st.subheader(f"📊 {T['specs']}")
        total_plastique = surface * plastique_par_m2

        st.markdown(f"""
        <div class="eco-badge">
            🎉 {T['plastique'].split('kg')[0].strip()} :<br>
            <span style="font-size:24px;color:#1B5E20;">{total_plastique:,.1f} kg</span>
            de déchets plastiques !
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h4>⚙️ {T['specs']}</h4>
            <p><b>{T['resistance']} :</b> {resistance}</p>
            <p><b>Forme :</b> {forme_choisie}</p>
            <p><b>Motif :</b> {motif_choisi}</p>
            <p><b>Couleur :</b> {couleur_choisie}</p>
            <p><b>{T['simulation']} ({intensite_pluie.lower()}) :</b><br>{drainage_info}</p>
            <p><b>Pavés estimés :</b> ~{int(nb_paves_estimes)} unités</p>
        </div>""", unsafe_allow_html=True)

    # ── Calcul financier ──────────────────────────────────────────────────────
    prix_total_m2 = prix_unitaire + supplement_couleur + supplement_forme + supplement_motif
    montant_paves = surface * prix_total_m2
    montant_total = montant_paves + frais_livraison

    st.markdown("---")
    st.markdown(f"### 💰 {T['montant']} : **{montant_total:,.0f} FCFA**")
    st.caption(
        f"Pavés: {surface:.0f}m² × {prix_unitaire:,} FCFA = {surface*prix_unitaire:,.0f} FCFA"
        f" | Couleur: +{surface*supplement_couleur:,.0f}"
        f" | Forme: +{surface*supplement_forme:,.0f}"
        f" | Motif: +{surface*supplement_motif:,.0f}"
        f" | Transport: {frais_livraison:,.0f} FCFA"
    )

    # ── Commande WhatsApp ─────────────────────────────────────────────────────
    st.markdown(f'<div class="section-title">📩 {T["commander"]}</div>', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        nom_client = st.text_input(T["nom"])
    with col_c2:
        contact = st.text_input(T["contact_label"])

    if st.button(T["btn_wa"]):
        if nom_client and contact:
            sauvegarder_devis(nom_client, contact, type_pave, surface, zone_livraison,
                              couleur_choisie, forme_choisie, motif_choisi,
                              montant_total, total_plastique)

            texte_message = (
                f"♻️ *NOUVELLE COMMANDE ST-ECOPARVIS*\n\n"
                f"👤 *Nom :* {nom_client}\n"
                f"📞 *Contact :* {contact}\n"
                f"📍 *Zone :* {zone_livraison}\n\n"
                f"🧱 *Détails :*\n"
                f"- Type : {type_pave}\n"
                f"- Forme : {forme_choisie}\n"
                f"- Motif : {motif_choisi}\n"
                f"- Couleur : {couleur_choisie}\n"
                f"- Surface : {surface} m²\n"
                f"- 🌿 Impact Éco : {total_plastique:,.1f} kg recyclés !\n\n"
                f"💵 *Détail Financier :*\n"
                f"- Pavés : {montant_paves:,.0f} FCFA\n"
                f"- Transport : {frais_livraison:,.0f} FCFA\n"
                f"💰 *TOTAL : {montant_total:,.0f} FCFA*"
            )
            msg_enc = urllib.parse.quote(texte_message)
            lien_wa = f"https://wa.me/22969710623?text={msg_enc}"
            st.success("✅ Commande prête ! Cliquez ci-dessous.")
            st.markdown(f"[➡️ Ouvrir WhatsApp et envoyer la commande]({lien_wa})")
            st.info("📬 Nous vous répondrons sous **24h** pour confirmer votre commande et organiser la livraison. Merci de votre confiance !")

            # ── Paiement Mobile Money ────────────────────────────────────
            st.markdown("---")
            st.markdown("### 💳 Payer votre commande via Mobile Money")
            col_mtn, col_moov = st.columns(2)
            with col_mtn:
                st.markdown(f"""
                <div style="background:#FFD700;padding:16px;border-radius:10px;text-align:center;">
                    <h4 style="color:#1a1a1a;">📱 MTN Mobile Money</h4>
                    <p style="font-size:20px;font-weight:bold;color:#1a1a1a;">+229 69 71 06 23</p>
                    <p style="color:#333;font-size:13px;">Au nom de : ST-Ecoparvis</p>
                    <p style="color:#333;font-size:13px;">Montant : <b>{montant_total:,.0f} FCFA</b></p>
                </div>""", unsafe_allow_html=True)
            with col_moov:
                st.markdown(f"""
                <div style="background:#0066CC;padding:16px;border-radius:10px;text-align:center;">
                    <h4 style="color:white;">📱 Celtiis</h4>
                    <p style="font-size:20px;font-weight:bold;color:white;">+229 92 62 41 33</p>
                    <p style="color:#ddd;font-size:13px;">Au nom de : ST-Ecoparvis</p>
                    <p style="color:#ddd;font-size:13px;">Montant : <b>{montant_total:,.0f} FCFA</b></p>
                </div>""", unsafe_allow_html=True)
            st.warning("⚠️ Après paiement, envoyez la capture d'écran de votre reçu sur WhatsApp pour confirmer votre commande.")

            # ── Notification email ───────────────────────────────────────
            envoyer_email_notification(nom_client, contact, type_pave, surface, montant_total, zone_livraison)
        else:
            st.error("Veuillez remplir votre nom et votre contact.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — GALERIE
# ══════════════════════════════════════════════════════════════════════════════
elif menu == T["nav"][2]:
    st.markdown(f'<div class="section-title">{T["galerie"]}</div>', unsafe_allow_html=True)
    st.write(T["galerie_sous"])

    galerie_images = [
        ("/mnt/user-data/uploads/1000427947.jpg", "Pavé Écologique"),
        ("/mnt/user-data/uploads/1000427961.jpg", "Mélange Turquoise & Or"),
        ("/mnt/user-data/uploads/1000427945.jpg", "Hexagones Bleus"),
        ("/mnt/user-data/uploads/1000428515.jpg", "Pavés Colorés"),
        ("/mnt/user-data/uploads/1000427951.jpg", "Pavés Haute Performance"),
        ("/mnt/user-data/uploads/1000427959.jpg", "Fabrication Pavés"),
        ("/mnt/user-data/uploads/1000427965.jpg", "Pose sur Chantier"),
        ("/mnt/user-data/uploads/1000427983.jpg", "Dalles Plastique"),
        ("/mnt/user-data/uploads/1000428526.jpg", "Stock Production"),
        ("/mnt/user-data/uploads/1000428527.jpg", "Technicien & Pavés"),
    ]

    cols = st.columns(3)
    for i, (path, caption) in enumerate(galerie_images):
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            cols[i % 3].markdown(f"""
            <div style="margin-bottom:12px;">
                <img src="data:image/jpeg;base64,{b64}"
                     style="width:100%;border-radius:8px;object-fit:cover;height:180px;" />
                <p style="text-align:center;font-size:12px;color:#555;">{caption}</p>
            </div>""", unsafe_allow_html=True)
        except:
            pass

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CONTACT
# ══════════════════════════════════════════════════════════════════════════════
elif menu == T["nav"][3]:
    st.markdown(f'<div class="section-title">📞 {T["contact_page"]}</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="contact-card">
        <h4>♻️ ST-Ecoparvis</h4>
        <p><i>"Chaque déchet est une brique d'avenir"</i></p><br>
        <p>📱 <b>WhatsApp / Appel :</b> +229 69 71 06 23</p>
        <p>📱 <b>Second numéro :</b> +229 92 62 41 33</p>
        <p>📧 <b>Email :</b> eloisemable17@gmail.com</p>
        <p>📍 <b>Localisation :</b> Bénin <i>(adresse en cours de finalisation)</i></p>
    </div>""", unsafe_allow_html=True)
    st.info("Pour toute commande, utilisez le **Calculateur Technique & Devis** dans le menu.")

    st.markdown('<div class="section-title">❓ Questions Fréquentes</div>', unsafe_allow_html=True)
    with st.expander("⏱️ Combien de temps pour la livraison ?"):
        st.write("La livraison est effectuée sous **3 à 7 jours ouvrables** selon votre zone. Cotonou/Calavi : 3 jours. Parakou : 5-7 jours.")
    with st.expander("🌧️ Les pavés résistent-ils à la pluie et à la chaleur ?"):
        st.write("Oui ! Nos pavés intègrent un **traitement UV** et résistent parfaitement aux fortes chaleurs et aux pluies. Ils ne se déforment pas dans le temps.")
    with st.expander("🧱 Puis-je voir un échantillon avant de commander ?"):
        st.write("Bien sûr ! Contactez-nous sur WhatsApp au **+229 69 71 06 23** pour organiser une présentation d'échantillons.")
    with st.expander("💰 Les prix affichés sont-ils définitifs ?"):
        st.write("Les prix du simulateur sont des **estimations**. Le montant définitif vous sera confirmé après étude de votre projet par notre équipe sous 24h.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — HISTORIQUE
# ══════════════════════════════════════════════════════════════════════════════
elif menu == T["nav"][4]:
    st.markdown(f'<div class="section-title">📋 {T["historique"]}</div>', unsafe_allow_html=True)
    contact_search = st.text_input("Entrez votre numéro WhatsApp pour voir vos devis :")
    if contact_search:
        rows = get_historique(contact_search)
        if rows:
            for row in rows:
                st.markdown(f"""
                <div class="historique-card">
                    📅 <b>{row[1]}</b> — {row[3]}<br>
                    🗺️ Zone : {row[6]} | Surface : {row[5]} m²<br>
                    🎨 Couleur : {row[7]} | Forme : {row[8]} | Motif : {row[9]}<br>
                    🌿 Plastique recyclé : {row[11]:,.1f} kg<br>
                    💰 <b>Total : {row[10]:,.0f} FCFA</b>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Aucun devis trouvé pour ce numéro.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — TÉMOIGNAGES
# ══════════════════════════════════════════════════════════════════════════════
elif menu == T["nav"][5]:
    st.markdown('<div class="section-title">⭐ Témoignages Clients</div>', unsafe_allow_html=True)
    st.write("Ce que nos clients disent de ST-Ecoparvis :")

    temoignages = [
        {"nom": "Kouassi A.", "ville": "Cotonou", "note": "⭐⭐⭐⭐⭐",
         "texte": "Des pavés d'une qualité exceptionnelle ! Ma cour est magnifique et plus aucune flaque d'eau après la pluie. Je recommande vivement ST-Ecoparvis."},
        {"nom": "Fatou M.", "ville": "Porto-Novo", "note": "⭐⭐⭐⭐⭐",
         "texte": "Service rapide et professionnel. Les pavés colorés que j'ai commandés sont exactement comme je les voulais. Livraison dans les délais."},
        {"nom": "Rodrigue K.", "ville": "Abomey", "note": "⭐⭐⭐⭐⭐",
         "texte": "J'ai pavé toute mon entrée avec ST-Ecoparvis. Résistance excellente, même sous le trafic lourd. Et en plus on contribue à l'écologie !"},
        {"nom": "Marie-Claire D.", "ville": "Calavi", "note": "⭐⭐⭐⭐⭐",
         "texte": "L'application est très facile à utiliser. J'ai fait mon devis en 2 minutes et reçu ma commande rapidement. Très satisfaite !"},
        {"nom": "Ibrahim S.", "ville": "Parakou", "note": "⭐⭐⭐⭐⭐",
         "texte": "Le mélange de couleurs que j'ai choisi est superbe. Mes voisins me demandent tous où j'ai trouvé ces pavés. Merci ST-Ecoparvis !"},
    ]

    for t in temoignages:
        st.markdown(f"""
        <div class="card" style="margin-bottom:12px;">
            <p style="font-size:20px;">{t['note']}</p>
            <p style="font-style:italic;color:#333;">"{t['texte']}"</p>
            <p style="color:#2E7D32;font-weight:bold;">— {t['nom']}, {t['ville']}</p>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — ADMIN
# ══════════════════════════════════════════════════════════════════════════════
elif menu == T["nav"][6]:
    st.markdown('<div class="section-title">🔐 Tableau de Bord Admin</div>', unsafe_allow_html=True)

    if "admin_connecte" not in st.session_state:
        st.session_state.admin_connecte = False

    if not st.session_state.admin_connecte:
        mdp = st.text_input("Mot de passe admin :", type="password")
        if st.button("Se connecter"):
            if mdp == "Takane20":
                st.session_state.admin_connecte = True
                st.rerun()
            else:
                st.error("❌ Mot de passe incorrect.")
    else:
        st.success("✅ Connecté en tant qu'administrateur")
        if st.button("Se déconnecter"):
            st.session_state.admin_connecte = False
            st.rerun()

        # Statistiques globales
        conn = sqlite3.connect("ecoparvis_historique.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM devis")
        nb_devis = c.fetchone()[0]
        c.execute("SELECT SUM(montant_total) FROM devis")
        total_ca = c.fetchone()[0] or 0
        c.execute("SELECT SUM(plastique_kg) FROM devis")
        total_plastique = c.fetchone()[0] or 0
        c.execute("SELECT * FROM devis ORDER BY id DESC")
        toutes_commandes = c.fetchall()
        conn.close()

        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("📋 Total Devis", nb_devis)
        col_s2.metric("💰 CA Estimé", f"{total_ca:,.0f} FCFA")
        col_s3.metric("🌿 Plastique Recyclé", f"{total_plastique:,.1f} kg")

        st.markdown("---")
        st.markdown("### 📋 Toutes les commandes")
        if toutes_commandes:
            for row in toutes_commandes:
                st.markdown(f"""
                <div class="historique-card">
                    📅 <b>{row[1]}</b> | 👤 {row[2]} | 📞 {row[3]}<br>
                    🧱 {row[4]} | 📐 {row[5]} m² | 📍 {row[6]}<br>
                    🎨 {row[7]} | 🔷 {row[8]} | 🎭 {row[9]}<br>
                    🌿 {row[11]:,.1f} kg recyclés | 💰 <b>{row[10]:,.0f} FCFA</b>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Aucune commande encore enregistrée.")
