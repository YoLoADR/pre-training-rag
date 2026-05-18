"""
Génère un CSV de consommation électrique sur 365 jours avec saisonnalité et 3 anomalies.
Les anomalies sont volontairement injectées pour les exercices de détection.
"""

import os
import numpy as np
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "energy")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "consumption.csv")

np.random.seed(42)  # reproductibilité


def generate():
    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    day_of_year = np.arange(365)

    # Consommation de base : 8 kWh/j en été, +40% en hiver (sinusoïde)
    base = 8.0
    seasonal = base * (1.0 + 0.45 * np.cos(2 * np.pi * day_of_year / 365))

    # Bruit gaussien ±10%
    noise = np.random.normal(0, 0.10 * base, 365)
    consumption = seasonal + noise

    # ─── Anomalie 1 : 18-25 juin (jours 169-176) ─────────────────────────────
    # Climatiseur oublié allumé pendant une semaine → pic +220%
    consumption[169:177] *= 3.2

    # ─── Anomalie 2 : 15-20 décembre (jours 349-354) ─────────────────────────
    # Résistance électrique d'appoint laissée allumée → pic +160%
    consumption[349:355] *= 2.6

    # ─── Anomalie 3 : 8-10 mars (jours 67-69) ────────────────────────────────
    # Baisse suspecte (absence + thermostat mal réglé ou compteur ?)
    consumption[67:70] *= 0.3

    # Température extérieure : sinusoïde décalée + bruit (Paris)
    temp_ext = 13.0 - 13.0 * np.cos(2 * np.pi * day_of_year / 365) + np.random.normal(0, 2.5, 365)
    temp_ext = np.clip(temp_ext, -10, 40)

    # Prix au kWh (tarif réglementé EDF 2024, HP)
    prix_kwh = 0.2276

    # Coût en euros
    cout_eur = consumption * prix_kwh

    df = pd.DataFrame(
        {
            "date": dates,
            "consommation_kwh": consumption.round(2),
            "temperature_ext_c": temp_ext.round(1),
            "prix_kwh_eur": prix_kwh,
            "cout_eur": cout_eur.round(2),
        }
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d")

    # Résumé de validation
    print(f"  ✓ {OUTPUT_FILE}")
    print(f"     Lignes : {len(df)}")
    print(f"     Conso annuelle : {df['consommation_kwh'].sum():.0f} kWh")
    print(f"     Cout annuel : {df['cout_eur'].sum():.0f} EUR")
    print(f"     Max : {df['consommation_kwh'].max():.1f} kWh (le {df.loc[df['consommation_kwh'].idxmax(), 'date'].strftime('%d/%m')})")
    print(f"     Min : {df['consommation_kwh'].min():.1f} kWh (le {df.loc[df['consommation_kwh'].idxmin(), 'date'].strftime('%d/%m')})")


if __name__ == "__main__":
    print("Generation des donnees de consommation electrique...")
    generate()
