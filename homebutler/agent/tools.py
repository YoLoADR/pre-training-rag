"""
Les 4 outils métier de l'agent ReAct HomeButler.
Chaque outil est un wrapper LangChain autour d'un service métier.
"""

from langchain.tools import Tool


# ── Outil 1 : Recherche documentaire (RAG) ───────────────────────────────────

def _search_home_docs(query: str) -> str:
    """Recherche dans les documents du logement via RAG."""
    try:
        from homebutler.rag.retriever import retrieve, format_docs_for_context
        docs = retrieve(query, use_ensemble=True, k=4)
        if not docs:
            return "Aucun document pertinent trouvé pour cette question."
        return format_docs_for_context(docs)
    except FileNotFoundError as e:
        return f"Index RAG non disponible : {e}"


search_docs_tool = Tool(
    name="search_home_docs",
    func=_search_home_docs,
    description=(
        "Recherche dans les documents du logement : bail, règlement de copropriété, "
        "notices d'équipements (chaudière, VMC, lave-linge), DPE. "
        "Utilise cet outil pour toute question sur le fonctionnement d'un équipement, "
        "les droits et obligations, ou les caractéristiques du logement. "
        "Input : question ou mots-clés en français."
    ),
)


# ── Outil 2 : Analyse de la consommation énergétique ─────────────────────────

def _analyze_energy_consumption(query: str) -> str:
    """Analyse les données de consommation électrique du logement."""
    try:
        from homebutler.services.energy import load_consumption, format_summary_for_llm
        df = load_consumption()
        return format_summary_for_llm(df)
    except FileNotFoundError:
        return (
            "Données de consommation non disponibles. "
            "Lancez : python scripts/generate_energy_data.py"
        )


analyze_energy_tool = Tool(
    name="analyze_energy_consumption",
    func=_analyze_energy_consumption,
    description=(
        "Analyse la consommation électrique du logement sur les 12 derniers mois. "
        "Détecte les anomalies (pics ou chutes inhabituels), calcule les statistiques mensuelles "
        "et annuelles, et identifie les mois les plus coûteux. "
        "Utilise cet outil pour toute question sur la consommation d'énergie, la facture électrique, "
        "ou pour identifier des comportements anormaux. "
        "Input : question sur l'énergie (ex: 'ma consommation est-elle normale ?')"
    ),
)


# ── Outil 3 : Recherche de producteurs locaux ─────────────────────────────────

def _find_local_products(query: str) -> str:
    """Recherche des producteurs/artisans locaux."""
    try:
        from homebutler.services.marketplace import search_producers, format_producers_for_llm
        results = search_producers(query=query, max_distance_km=30, limit=5)
        if not results:
            # Fallback: try each word of the query individually
            for word in query.lower().split():
                if len(word) > 3:
                    results = search_producers(query=word, max_distance_km=30, limit=5)
                    if results:
                        break
        if not results:
            # Last resort: return all producers within 30 km
            results = search_producers(query="", max_distance_km=30, limit=5)
        return format_producers_for_llm(results)
    except FileNotFoundError:
        return (
            "Catalogue producteurs non disponible. "
            "Lancez : python scripts/generate_producers.py"
        )


find_products_tool = Tool(
    name="find_local_products",
    func=_find_local_products,
    description=(
        "Recherche des producteurs locaux et artisans à proximité du logement. "
        "Couvre : légumes, fruits, pain, fromage, viande, épicerie fine, "
        "artisans (plombier, électricien, peintre, serrurier, menuisier, jardinier). "
        "Utilise cet outil pour trouver où commander de la nourriture locale, "
        "ou pour trouver un artisan pour une réparation. "
        "Input : produit ou type d'artisan recherché (ex: 'légumes bio', 'plombier', 'pain')."
    ),
)


# ── Outil 4 : Météo ───────────────────────────────────────────────────────────

def _get_weather_forecast(query: str = "") -> str:
    """Récupère les prévisions météo des 3 prochains jours."""
    try:
        from homebutler.services.weather import format_weather_for_llm
        return format_weather_for_llm(days=3)
    except Exception as e:
        return f"Impossible de récupérer la météo : {e}"


get_weather_tool = Tool(
    name="get_weather_forecast",
    func=_get_weather_forecast,
    description=(
        "Récupère les prévisions météo des 3 prochains jours pour le logement "
        "(Boulogne-Billancourt, région parisienne). "
        "Indique les températures min/max, les précipitations et le vent. "
        "Utilise cet outil quand l'utilisateur mentionne la météo, le froid, la pluie, "
        "ou pour des conseils liés aux conditions climatiques. "
        "Input : toute question sur la météo ou une chaîne vide."
    ),
)


# ── Liste complète des outils ─────────────────────────────────────────────────

ALL_TOOLS = [
    search_docs_tool,
    analyze_energy_tool,
    find_products_tool,
    get_weather_tool,
]
