import pandas as pd
import numpy as np
from homebutler import config


def load_consumption(csv_path: str | None = None) -> pd.DataFrame:
    path = csv_path or config.ENERGY_CSV
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def detect_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> list[dict]:
    """
    Détecte les anomalies via z-score sur une fenêtre glissante de 30 jours.
    threshold=2.0 → valeurs à plus de 2 écarts-types de la moyenne locale.
    """
    rolling_mean = df["consommation_kwh"].rolling(30, min_periods=7).mean()
    rolling_std = df["consommation_kwh"].rolling(30, min_periods=7).std().replace(0, np.nan)
    z_scores = (df["consommation_kwh"] - rolling_mean) / rolling_std
    anomaly_mask = z_scores.abs() > threshold
    anomalies = df[anomaly_mask].copy()
    anomalies["z_score"] = z_scores[anomaly_mask].round(2)
    return anomalies.to_dict("records")


def get_monthly_summary(df: pd.DataFrame) -> list[dict]:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M"))
        .groupby("month")
        .agg(
            total_kwh=("consommation_kwh", "sum"),
            total_eur=("cout_eur", "sum"),
            avg_temp=("temperature_ext_c", "mean"),
            days=("consommation_kwh", "count"),
        )
        .reset_index()
    )
    monthly["month"] = monthly["month"].astype(str)
    monthly["total_kwh"] = monthly["total_kwh"].round(1)
    monthly["total_eur"] = monthly["total_eur"].round(2)
    monthly["avg_temp"] = monthly["avg_temp"].round(1)
    return monthly.to_dict("records")


def get_annual_stats(df: pd.DataFrame) -> dict:
    return {
        "total_kwh": round(df["consommation_kwh"].sum(), 1),
        "total_eur": round(df["cout_eur"].sum(), 2),
        "avg_daily_kwh": round(df["consommation_kwh"].mean(), 2),
        "max_daily_kwh": round(df["consommation_kwh"].max(), 2),
        "min_daily_kwh": round(df["consommation_kwh"].min(), 2),
        "anomaly_count": len(detect_anomalies(df)),
    }


def format_summary_for_llm(df: pd.DataFrame) -> str:
    """Formate les stats énergie pour injection dans un prompt LLM."""
    stats = get_annual_stats(df)
    monthly = get_monthly_summary(df)
    anomalies = detect_anomalies(df)

    last_3_months = monthly[-3:] if len(monthly) >= 3 else monthly
    monthly_str = "\n".join(
        f"  {m['month']}: {m['total_kwh']} kWh ({m['total_eur']}€, temp moy {m['avg_temp']}°C)"
        for m in last_3_months
    )

    anomaly_str = (
        "\n".join(
            f"  {a['date'] if isinstance(a['date'], str) else a['date'].strftime('%Y-%m-%d')}: "
            f"{a['consommation_kwh']} kWh (z-score: {a.get('z_score', '?')})"
            for a in anomalies[:5]
        )
        or "Aucune anomalie détectée"
    )

    return (
        f"Statistiques annuelles :\n"
        f"  Total : {stats['total_kwh']} kWh — {stats['total_eur']}€\n"
        f"  Moyenne journalière : {stats['avg_daily_kwh']} kWh\n\n"
        f"3 derniers mois :\n{monthly_str}\n\n"
        f"Anomalies (pics ou chutes inhabituels) :\n{anomaly_str}"
    )
