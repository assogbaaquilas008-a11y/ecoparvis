import streamlit as st

import urllib.parse

# Configuration de la page
st.set_page_config(page_title="Ecoparvis - Pavés Écologiques", page_icon="🌱", layout="wide")

# Style CSS personnalisé complet
st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1B5E20; text-align: center; margin-bottom: 10px; }
    .section-title { font-size: 24px; font-weight: bold; color: #2E7D32; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #E8F5E9; padding-bottom: 5px; }
    .card { background-color: #F1F8E9; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 15px; }
    .eco-badge { background-color: #E8F5E9; color: #2E7D32; padding: 15px; border-radius: 8px; border: 1px dashed #2E7D32; text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #1B5E20; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌱 ECOPARVIS - Gestion & Optimisation</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #555;'>Conception de pavés recyclés, zéro résidu et haute performance.</p>", unsafe_allow_html=True)

# Barre latérale de navigation
menu = st.sidebar.selectbox("Navigation", ["Accueil & Concept", "Calculateur Technique & Devis", "Galerie Réalisations"])

# --- OPTION 1 : ACCUEIL ---
if menu == "Accueil & Concept":
    st.markdown('<div class="section-title">Notre Vision</div>', unsafe_allow_html=True)
    st.write("""
    Ecoparvis transforme les défis environnementaux en solutions durables. 
    Nos pavés sont conçus à base de déchets plastiques recyclés, offrant une résistance exceptionnelle à la compression tout en favorisant une excellente gestion des eaux de ruissellement.
    """)
    
    st.markdown("""
    ### Pourquoi choisir Ecoparvis ?
    *   **Zéro Résidu :** Valorisation maximale des déchets plastiques qui encombrent nos villes.
    *   **Haute Performance :** Une durabilité et une résistance supérieures aux pavés en ciment classiques.
    *   **Éco-citoyenneté :** Chaque commande participe directement à la dépollution de notre environnement.
    """)
    st.info("Utilisez le menu de gauche pour accéder aux outils de calcul et passer commande.")

# --- OPTION 2 : CALCULATEUR & DEVIS (Version Finale et Complète) ---
elif menu == "Calculateur Technique & Devis":
    st.markdown('<div class="section-title">Simulateur de Commande & Calculs Techniques</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧱 Paramètres du Projet")
        surface = st.number_input("Surface à couvrir (en m²)", min_value=1.0, value=10.0, step=1.0)
        type_pave = st.selectbox("Type de pavé", ["Pavé Drainant (Éco)", "Pavé Autobloquant Classique", "Pavé Haute Résistance"])
        
        # --- NOUVEAU : SIMULATION DE LIVRAISON ---
        zone_livraison = st.selectbox("Zone de livraison", ["Abomey / Bohicon", "Cotonou / Calavi", "Porto-Novo", "Parakou", "Retrait sur place (Gratuit)"])
        
        # --- NOUVEAU : INTENSITÉ DE LA PLUIE ---
        intensite_pluie = st.select_slider("Intensité de pluie simulée", options=["Faible", "Modérée", "Forte (Saison des pluies)"])
        
        # Configuration des coefficients (Prix de base et plastique)
        if type_pave == "Pavé Drainant (Éco)":
            prix_unitaire = 5000  # Modifie ce chiffre si tu veux changer ton prix de vente au m²
            plastique_par_m2 = 12.5  
            resistance = "~30 MPa"
            
            # Logique dynamique du drainage selon la pluie
            if intensite_pluie == "Faible":
                drainage_info = "🟢 Absorption totale instantanée. Aucun ruissellement."
            elif intensite_pluie == "Modérée":
                drainage_info = "🟢 Évacuation fluide. Sol sec en quelques minutes."
            else:
                drainage_info = "🟡 Absorption maximale activée. Réduction drastique des flaques par rapport au béton."
                
        elif type_pave == "Pavé Autobloquant Classique":
            prix_unitaire = 4500
            plastique_par_m2 = 14.0  
            resistance = "~45 MPa"
            
            if intensite_pluie == "Faible":
                drainage_info = "🟢 Légère infiltration par les joints."
            elif intensite_pluie == "Modérée":
                drainage_info = "🟡 Ruissellement standard. Prévoir une légère pente."
            else:
                drainage_info = "🔴 Risque de stagnation si le terrain n'est pas incliné."
                
        else:
            prix_unitaire = 6500
            plastique_par_m2 = 18.5  
            resistance = "~55 MPa"
            drainage_info = "❌ Structure étanche haute densité. L'eau ruisselle entièrement (Idéal pour canaliser vers un caniveau)."

        # Logique de calcul des frais de livraison indicatifs
        if zone_livraison == "Retrait sur place (Gratuit)":
            frais_livraison = 0
        elif zone_livraison == "Abomey / Bohicon":
            frais_livraison = 5000
        elif zone_livraison == "Cotonou / Calavi" or zone_livraison == "Porto-Novo":
            frais_livraison = 15000
        else:  # Parakou
            frais_livraison = 25000

    with col2:
        st.subheader("📊 Estimations Techniques & Matières")
        
        # Calculateur de matières premières ("Zéro Résidu")
        total_plastique_reclycle = surface * plastique_par_m2
        
        # Affichage de la valeur écologique positive
        st.markdown(f"""
            <div class="eco-badge">
                🎉 Grâce à cette commande, vous retirez de la nature :<br>
                <span style="font-size: 24px; color: #1B5E20;">{total_plastique_reclycle:,.1f} kg</span> de déchets plastiques !
            </div>
        """, unsafe_allow_html=True)
        
        # Carte des détails techniques
        st.markdown(f"""
        <div class="card">
            <h4>⚙️ Spécifications & Simulation</h4>
            <p><b>Résistance mécanique :</b> {resistance}</p>
            <p><b>Simulation face à une pluie {intensite_pluie.lower()} :</b><br>{drainage_info}</p>
        </div>
        """, unsafe_allow_html=True)

    # Calcul financier global
    montant_pavet = surface * prix_unitaire
    montant_total = montant_pavet + frais_livraison
    
    st.markdown("---")
    st.markdown(f"### 💰 Montant Total Estimé : **{montant_total:,.0f} FCFA**")
    st.caption(f"(Détail : Pavés = {montant_pavet:,.0f} FCFA | Transport = {frais_livraison:,.0f} FCFA pour {zone_livraison})")
    
    # Section Commande WhatsApp
    st.markdown('<div class="section-title">📩 Passer la commande</div>', unsafe_allow_html=True)
    
    col_client1, col_client2 = st.columns(2)
    with col_client1:
        nom_client = st.text_input("Votre Nom / Entreprise")
    with col_client2:
        contact = st.text_input("Numéro de téléphone (WhatsApp)")
    
    if st.button("Générer et envoyer la commande sur WhatsApp"):
        if nom_client and contact:
            # Message WhatsApp structuré avec toutes les options incluses
            texte_message = (
                f"🌱 *NOUVELLE COMMANDE ECOPARVIS*\n\n"
                f"👤 *Nom :* {nom_client}\n"
                f"📞 *Contact :* {contact}\n"
                f"📍 *Zone de Livraison :* {zone_livraison}\n\n"
                f"🧱 *Détails du projet :*\n"
                f"- Modèle : {type_pave}\n"
                f"- Surface : {surface} m²\n"
                f"- 🍃 *Impact Éco :* {total_plastique_reclycle:,.1f} kg de plastique recyclés !\n\n"
                f"💵 *Détail Financier :*\n"
                f"- Coût pavés : {montant_pavet:,.0f} FCFA\n"
                f"- Transport : {frais_livraison:,.0f} FCFA\n"
                f"💰 *TOTAL ESTIMÉ : {montant_total:,.0f} FCFA*"
            )
            
            message_encode = urllib.parse.quote(texte_message)
            # Remplacer par ton vrai numéro WhatsApp (ex: 229XXXXXXXX)
            numero_whatsapp = "229XXXXXXXX" 
            lien_wa = f"https://wa.me/{numero_whatsapp}?text={message_encode}"
            
            st.success("Lien de commande prêt ! Cliquez ci-dessous pour l'envoyer.")
            st.markdown(f"[➡️ Cliquer ici pour ouvrir WhatsApp et envoyer la commande]({lien_wa})")
        else:
            st.error("Veuillez remplir votre nom et votre contact avant de générer le lien.")

# --- OPTION 3 : GALERIE ---
elif menu == "Galerie Réalisations":
    st.markdown('<div class="section-title">Galerie Ecoparvis</div>', unsafe_allow_html=True)
    st.write("Aperçu de nos modules de pavés et chantiers réalisés :")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://via.placeholder.com/400x300.png?text=Pave+Drainant+Recycle", caption="Moule Pavé Écologique Drainant")
    with col2:
        st.image("https://via.placeholder.com/400x300.png?text=Apercu+Chantier", caption="Rendu final - Zone Piétonne")
	