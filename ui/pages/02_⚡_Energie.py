"""
Page Énergie — Dashboard Plotly de la consommation électrique.
"""

import os
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("⚡ Tableau de bord Énergie")
st.caption("Analyse de votre consommation électrique sur 12 mois")


@st.cache_data(ttl=300)
def load_energy_data():
    """Charge les données depuis l'API (ou directement le CSV)."""
    try:
        resp = requests.get(f"{API_URL}/consumption/stats", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        # Fallback : lire directement le CSV
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
            from homebutler.services.energy import (
                load_consumption, get_annual_stats, get_monthly_summary, detect_anomalies
            )
            df = load_consumption()
            stats = get_annual_stats(df)
            monthly = get_monthly_summary(df)
            anomalies = detect_anomalies(df)
            return {
                "annual_kwh": stats["total_kwh"],
                "annual_eur": stats["total_eur"],
                "avg_daily_kwh": stats["avg_daily_kwh"],
                "anomaly_count": stats["anomaly_count"],
                "monthly_summary": monthly,
                "anomalies": [
                    {"date": str(a["date"])[:10], "consommation_kwh": a["consommation_kwh"]}
                    for a in anomalies
                ],
            }
        except Exception as e:
            return None


data = load_energy_data()

if data is None:
    st.error("Données non disponibles. Lancez `python scripts/generate_energy_data.py` puis l'API.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Consommation annuelle", f"{data['annual_kwh']:.0f} kWh")
col2.metric("Coût annuel", f"{data['annual_eur']:.0f} €")
col3.metric("Moyenne journalière", f"{data['avg_daily_kwh']:.1f} kWh/j")
col4.metric("Anomalies détectées", data["anomaly_count"], delta=f"{data['anomaly_count']} pics", delta_color="inverse")

st.divider()

# ── Graphique mensuel ─────────────────────────────────────────────────────────
monthly = pd.DataFrame(data["monthly_summary"])
if not monthly.empty:
    st.subheader("📊 Consommation mensuelle")
    fig_monthly = px.bar(
        monthly,
        x="month",
        y="total_kwh",
        color="avg_temp",
        color_continuous_scale="RdBu_r",
        labels={"month": "Mois", "total_kwh": "kWh", "avg_temp": "Temp. moy (°C)"},
        title="Consommation mensuelle (kWh) — couleur = température extérieure",
    )
    fig_monthly.update_traces(hovertemplate="<b>%{x}</b><br>%{y:.0f} kWh")
    st.plotly_chart(fig_monthly, use_container_width=True)

# ── Graphique journalier avec anomalies ───────────────────────────────────────
try:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from homebutler.services.energy import load_consumption, detect_anomalies
    df = load_consumption()
    anomalies_df = pd.DataFrame(detect_anomalies(df))

    st.subheader("📈 Consommation journalière & anomalies")
    fig_daily = go.Figure()

    fig_daily.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["consommation_kwh"],
            name="Consommation (kWh)",
            line=dict(color="#1f77b4", width=1),
            opacity=0.7,
        )
    )

    if not anomalies_df.empty:
        fig_daily.add_trace(
            go.Scatter(
                x=anomalies_df["date"],
                y=anomalies_df["consommation_kwh"],
                mode="markers",
                name="Anomalies",
                marker=dict(color="red", size=8, symbol="x"),
                hovertemplate="<b>Anomalie</b><br>%{x}<br>%{y:.1f} kWh",
            )
        )

    fig_daily.update_layout(
        title="Consommation journalière (kWh) — anomalies en rouge",
        xaxis_title="Date",
        yaxis_title="kWh",
        hovermode="x unified",
    )
    st.plotly_chart(fig_daily, use_container_width=True)

except Exception as e:
    st.warning(f"Graphique journalier non disponible : {e}")

# ── Analyse LLM ───────────────────────────────────────────────────────────────
st.divider()
st.subheader("🤖 Analyse intelligente")
question = st.text_input(
    "Posez une question sur votre consommation :",
    value="Ma consommation est-elle dans la norme pour un appartement de 68 m2 ?",
)
if st.button("Analyser avec HomeButler", type="primary"):
    with st.spinner("Analyse en cours..."):
        try:
            resp = requests.post(
                f"{API_URL}/consumption/analyze",
                json={"question": question},
                timeout=60,
            )
            resp.raise_for_status()
            result = resp.json()
            st.success(result["analysis"])
        except Exception as e:
            st.error(f"Erreur : {e}")
