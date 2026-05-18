"""
Page Logement — Informations sur le logement et accès aux documents.
"""

import os
import streamlit as st

st.title("🏠 Mon Logement")
st.caption("Informations et documents de votre logement")

# ── Informations générales ────────────────────────────────────────────────────
st.subheader("📋 Informations générales")
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        **Adresse :** 28 avenue des Chênes
        **Ville :** 92100 Boulogne-Billancourt
        **Type :** Appartement F3
        **Surface :** 68 m² (Carrez : 66,4 m²)
        **Étage :** 3ème (avec ascenseur)
        """
    )
with col2:
    st.markdown(
        """
        **Propriétaire :** M. Jean-Pierre MARTIN
        **Loyer :** 1 250 € / mois
        **Charges :** 120 € / mois
        **Durée bail :** 3 ans (01/03/2024 → 28/02/2027)
        **Syndic :** Cabinet IMMO CONSEIL
        """
    )

# ── DPE ───────────────────────────────────────────────────────────────────────
st.subheader("⚡ Diagnostic de Performance Énergétique (DPE)")
col1, col2, col3 = st.columns(3)
col1.metric("Classe énergie", "D", help="230 kWh/m²/an — seuil classe D : 180-250")
col2.metric("Classe GES", "E", help="52 kg CO2eq/m²/an")
col3.metric("Coût annuel estimé", "1 530 €", help="Fourchette : 1 300-1 760 €/an")

st.progress(60, text="Classe D — Amélioration possible vers C avec isolation fenêtres")

with st.expander("💡 Travaux recommandés pour passer en classe C"):
    st.markdown(
        """
        **Travaux prioritaires (gain estimé 35-40%) :**
        1. 🪟 Remplacement fenêtres → triple vitrage (4 000-6 000€, aide MaPrimeRenov possible)
        2. 🌡 Isolation ponts thermiques (1 500-2 500€)

        **Sans travaux (économies immédiates) :**
        - Régler le thermostat à 19°C le jour / 16°C la nuit → -15%
        - Purger les radiateurs chaque année → -5%
        - Installer des robinets thermostatiques (200-400€) → -10%
        """
    )

# ── Équipements ────────────────────────────────────────────────────────────────
st.subheader("🔧 Équipements")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        **🔥 Chaudière**
        Viessmann Vitodens 100-W
        26 kW — Gaz naturel
        Installée en 2019
        Prochaine révision : automne 2024
        """
    )
with col2:
    st.markdown(
        """
        **💨 VMC**
        Zehnder ComfoAir Q 350
        Double flux — Rendement 93%
        Filtres G4 : nettoyage mensuel
        Filtres F7 : remplacement /6 mois
        """
    )
with col3:
    st.markdown(
        """
        **👕 Lave-linge**
        Bosch Série 6 WAU28P90FF
        9 kg — 1400 tr/min
        Classe A
        Filtre vidange : nettoyage mensuel
        """
    )

# ── Documents disponibles ──────────────────────────────────────────────────────
st.subheader("📄 Documents du logement")

docs_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "documents")
doc_info = {
    "bail_location.pdf": ("📋 Bail de location", "Contrat de bail 3 ans — Camille DUPONT"),
    "reglement_copropriete.pdf": ("🏢 Règlement de copropriété", "Résidence Les Chênes — 24 lots"),
    "notice_chaudiere.pdf": ("🔥 Notice chaudière", "Viessmann Vitodens 100-W — 26 kW"),
    "notice_vmc.pdf": ("💨 Notice VMC", "Zehnder ComfoAir Q 350 — Double flux"),
    "notice_lave_linge.pdf": ("👕 Notice lave-linge", "Bosch Série 6 WAU28P90FF"),
    "dpe.pdf": ("⚡ DPE", "Diagnostic classe D — Valide jusqu'au 15/01/2034"),
}

if os.path.exists(docs_dir):
    for filename, (label, description) in doc_info.items():
        filepath = os.path.join(docs_dir, filename)
        col1, col2, col3 = st.columns([3, 4, 2])
        with col1:
            st.markdown(f"**{label}**")
        with col2:
            st.caption(description)
        with col3:
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    st.download_button(
                        "⬇ Télécharger",
                        data=f,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"dl_{filename}",
                        use_container_width=True,
                    )
            else:
                st.warning("Non généré")
else:
    st.warning(
        "Documents non disponibles. Lancez : `python scripts/generate_documents.py`"
    )

# ── Contacts utiles ───────────────────────────────────────────────────────────
st.divider()
st.subheader("📞 Contacts utiles")
col1, col2, col3 = st.columns(3)
col1.info("**Syndic :** Cabinet IMMO CONSEIL\nTél : 01 46 03 00 00")
col2.info("**Chauffagiste :** Plomberie MARTIN\nTél : 06 11 22 33 44 (urgences 24h/24)")
col3.info("**Électricien :** Élec. BERNARD\nTél : 06 55 44 33 22")
