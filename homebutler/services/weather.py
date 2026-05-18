import requests
from cachetools import TTLCache, cached
from homebutler import config

# Cache en mémoire — TTL configurable via OPEN_METEO_CACHE_TTL (défaut 1h)
_weather_cache: TTLCache = TTLCache(maxsize=100, ttl=config.OPEN_METEO_CACHE_TTL)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Coordonnées par défaut : Boulogne-Billancourt
DEFAULT_LAT = 48.835
DEFAULT_LON = 2.240


@cached(_weather_cache)
def get_weather_forecast(
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    days: int = 3,
) -> dict:
    """
    Récupère les prévisions météo via l'API Open-Meteo (gratuite, sans clé).
    Résultats mis en cache {OPEN_METEO_CACHE_TTL} secondes.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "weathercode",
        ],
        "current_weather": True,
        "timezone": "Europe/Paris",
        "forecast_days": min(days, 7),
    }
    resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def format_weather_for_llm(lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON, days: int = 3) -> str:
    """Formate les prévisions météo pour injection dans un prompt LLM."""
    try:
        data = get_weather_forecast(lat, lon, days)
    except Exception as e:
        return f"Impossible de récupérer la météo : {e}"

    daily = data.get("daily", {})
    times = daily.get("time", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wind = daily.get("windspeed_10m_max", [])

    current = data.get("current_weather", {})
    lines = [f"Météo actuelle : {current.get('temperature', '?')}°C, vent {current.get('windspeed', '?')} km/h\n"]
    lines.append("Prévisions :")
    for i in range(min(len(times), days)):
        pluie = f", pluie {precip[i]:.1f}mm" if precip else ""
        vent_str = f", vent {wind[i]:.0f} km/h" if wind else ""
        lines.append(f"  {times[i]}: {tmin[i]}°C – {tmax[i]}°C{pluie}{vent_str}")

    return "\n".join(lines)
