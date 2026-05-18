"""
Page Marketplace — Carte et recherche de producteurs locaux.
"""

import os
import requests
import streamlit as st
import plotly.express as px
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🛒 Marketplace — Producteurs locaux")
st.caption("Trouvez des producteurs et artisans près de chez vous")

# ── Filtres sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("🔍 Filtres")
    query = st.text_input("Recherche", placeholder="légumes, pain, plombier...")
    product_type = st.selectbox(
        "Catégorie",
        ["", "légumes", "fruits", "pain", "fromage", "viande", "épicerie",
         "artisan-plombier", "artisan-electricien", "artisan-jardinage",
         "artisan-peintre", "artisan-serrurier", "artisan-menuisier"],
        format_func=lambda x: "Toutes" if x == "" else x.title(),
    )
    max_km = st.slider("Distance max (km)", 1, 50, 30)
    delivery_only = st.checkbox("Livraison uniquement")
    st.divider()
    st.caption("📍 Depuis : 28 av. des Chênes, Boulogne-Billancourt")


@st.cache_data(ttl=60)
def fetch_producers(query, product_type, max_km, delivery_only):
    params = {"query": query, "product_type": product_type, "max_km": max_km,
              "delivery_only": delivery_only, "limit": 30}
    try:
        resp = requests.get(f"{API_URL}/products/search", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        # Fallback direct
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
            from homebutler.services.marketplace import search_producers
            return search_producers(query=query, product_type=product_type,
                                    max_distance_km=max_km, delivery_only=delivery_only, limit=30)
        except Exception as e:
            st.error(f"Erreur : {e}")
            return []


producers = fetch_producers(query, product_type, max_km, delivery_only)

if not producers:
    st.info("Aucun producteur trouvé avec ces filtres.")
    st.stop()

st.markdown(f"**{len(producers)} résultat(s)** trouvé(s)")

# ── Carte Plotly ───────────────────────────────────────────────────────────────
df = pd.DataFrame(producers)
df["livraison_label"] = df["livraison"].map({True: "✅ Livraison", False: "🚶 Sur place"})

# Point de référence (logement)
home = pd.DataFrame([{
    "nom": "Mon logement", "latitude": 48.835, "longitude": 2.240,
    "type": "domicile", "distance_calculee_km": 0,
    "livraison_label": "📍 Vous",
}])

fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_name="nom",
    hover_data={"type": True, "distance_calculee_km": True, "livraison_label": True,
                "latitude": False, "longitude": False},
    color="type",
    size_max=15,
    zoom=11,
    mapbox_style="open-street-map",
    title="Producteurs et artisans locaux",
    labels={"distance_calculee_km": "Distance (km)", "type": "Catégorie",
            "livraison_label": "Livraison"},
)
fig.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# ── Liste des résultats ────────────────────────────────────────────────────────
st.subheader("📋 Liste des producteurs")
for p in producers:
    with st.expander(f"**{p['nom']}** — {p.get('type', '').title()} · {p.get('distance_calculee_km', '?')} km"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Produits :** {', '.join(p.get('produits', [])[:5])}")
            st.markdown(f"**Horaires :** {p.get('horaires', 'N/A')}")
            st.markdown(f"**Tél :** {p.get('phone', 'N/A')}")
        with col2:
            livraison = "✅ Livraison disponible" if p.get("livraison") else "🚶 Vente directe uniquement"
            min_cmd = f" (min {p.get('min_commande_eur', 0)}€)" if p.get("min_commande_eur") else ""
            st.markdown(f"**{livraison}**{min_cmd}")
            st.markdown(f"_{p.get('description', '')}_")

        if p.get("livraison"):
            with st.form(key=f"order_{p['id']}"):
                st.markdown("**Commander :**")
                produit = st.selectbox("Produit", p.get("produits", []))
                quantite = st.text_input("Quantité", placeholder="1 kg, 1 barquette...")
                nom = st.text_input("Votre nom")
                submitted = st.form_submit_button("🛒 Commander")
                if submitted and produit and quantite and nom:
                    try:
                        resp = requests.post(
                            f"{API_URL}/order",
                            json={
                                "items": [{"producer_id": p["id"], "produit": produit, "quantite": quantite}],
                                "nom_client": nom,
                            },
                            timeout=10,
                        )
                        resp.raise_for_status()
                        result = resp.json()
                        st.success(f"✅ Commande {result['order_id']} enregistrée !")
                    except Exception as e:
                        st.error(f"Erreur : {e}")
