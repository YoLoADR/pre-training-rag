import json
import math
from homebutler import config

# Coordonnées par défaut du logement de référence
DEFAULT_LAT = 48.835
DEFAULT_LON = 2.240


def load_producers(json_path: str | None = None) -> list[dict]:
    path = json_path or config.PRODUCERS_JSON
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distance en km entre deux coordonnées GPS (formule haversine)."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.asin(math.sqrt(a))


def search_producers(
    query: str = "",
    product_type: str = "",
    max_distance_km: float = 50.0,
    user_lat: float = DEFAULT_LAT,
    user_lon: float = DEFAULT_LON,
    delivery_only: bool = False,
    limit: int = 10,
) -> list[dict]:
    """
    Recherche des producteurs/artisans selon critères.
    Retourne la liste triée par distance.
    """
    producers = load_producers()
    results = []

    for p in producers:
        dist = haversine(user_lat, user_lon, p["latitude"], p["longitude"])

        if dist > max_distance_km:
            continue
        if delivery_only and not p.get("livraison", False):
            continue
        if product_type and product_type.lower() not in p["type"].lower():
            continue
        if query:
            q = query.lower()
            searchable = (
                p["nom"].lower()
                + " "
                + p["type"].lower()
                + " "
                + " ".join(p.get("produits", [])).lower()
                + " "
                + p.get("description", "").lower()
            )
            if q not in searchable:
                continue

        result = dict(p)
        result["distance_calculee_km"] = round(dist, 1)
        results.append(result)

    results.sort(key=lambda x: x["distance_calculee_km"])
    return results[:limit]


def format_producers_for_llm(producers: list[dict]) -> str:
    """Formate les producteurs pour injection dans un prompt LLM."""
    if not producers:
        return "Aucun producteur trouvé correspondant à votre recherche."

    lines = []
    for p in producers:
        livraison = "avec livraison" if p.get("livraison") else "vente directe uniquement"
        min_cmd = f", commande min {p['min_commande_eur']}€" if p.get("min_commande_eur") else ""
        produits = ", ".join(p.get("produits", [])[:5])
        lines.append(
            f"- **{p['nom']}** ({p['type']}, {p['distance_calculee_km']} km, {livraison}{min_cmd})\n"
            f"  Produits : {produits}\n"
            f"  Horaires : {p.get('horaires', 'N/A')} — Tél : {p.get('phone', 'N/A')}"
        )

    return "\n".join(lines)
