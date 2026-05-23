"""
═══════════════════════════════════════════════════════════════════════════
Atelier 03 — Pipeline + Agent ReAct (solution corrigée + commentaires)
═══════════════════════════════════════════════════════════════════════════

Pour une exécution la plus simple, on réutilise les fonctions de
homebutler.agent.react_agent (factory déjà testée en production).

Lancer :  python ateliers/atelier-03-pipeline-agent/solution.py
═══════════════════════════════════════════════════════════════════════════
"""

from homebutler.agent.react_agent import get_session_agent_debug
from homebutler.agent.tools import ALL_TOOLS
from homebutler.rag.retriever import get_ensemble_retriever


QUESTION_MULTI_OUTILS = (
    "Il va faire -5°C demain, comment je prépare ma maison et "
    "que puis-je commander à un producteur local pour me réchauffer ?"
)


def main() -> None:
    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT RAG : EnsembleRetriever — fusionner plusieurs sources
    # ──────────────────────────────────────────────────────────────────
    # FAISS  (poids 0.6) : recherche dense par similarité (embeddings)
    # Chroma (poids 0.4) : complément, filtres métadonnées disponibles
    # → meilleur recall que n'importe lequel des deux retrievers seul
    # → utile quand le vocabulaire de la question diverge des chunks
    # ═══════════════════════════════════════════════════════════════════
    retriever = get_ensemble_retriever(faiss_k=4, chroma_k=3)
    sample = retriever.invoke("Quelle est la marque de ma chaudière ?")
    print(f"EnsembleRetriever → {len(sample)} chunks fusionnés (FAISS+Chroma)")

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT AGENT : 4 outils — un par capability métier
    # ──────────────────────────────────────────────────────────────────
    # search_home_docs        → RAG sur les PDFs du logement
    # analyze_energy_consumption → CSV consommation 12 mois
    # find_local_products     → JSON 30 producteurs locaux
    # get_weather_forecast    → API Open-Meteo (cache 1h)
    #
    # La description de chaque outil est CRITIQUE : c'est sur cette base
    # que le LLM décide quel outil utiliser. À soigner !
    # ═══════════════════════════════════════════════════════════════════
    print("\nOutils disponibles :")
    for t in ALL_TOOLS:
        print(f"  - {t.name}")

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT AGENT : ReAct loop (Reason + Act)
    # ──────────────────────────────────────────────────────────────────
    # Thought       → le LLM réfléchit ("je vais d'abord vérifier la météo")
    # Action        → choisit un outil (ex: get_weather_forecast)
    # Action Input  → l'input passé à l'outil
    # Observation   → résultat de l'outil
    # ... boucle jusqu'à "Final Answer" (max_iterations=8 par défaut)
    #
    # debug=True → return_intermediate_steps expose la trace dans le résultat.
    # ═══════════════════════════════════════════════════════════════════
    executor = get_session_agent_debug()

    print(f"\n═══ Question multi-outils ═══\n{QUESTION_MULTI_OUTILS}\n")
    result = executor.invoke({
        "input": QUESTION_MULTI_OUTILS,
        "chat_history": [],
    })

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT AGENT : Inspecter la trace ReAct
    # ──────────────────────────────────────────────────────────────────
    # intermediate_steps = [(AgentAction, observation), ...]
    # → on extrait les noms d'outils pour vérifier la diversité d'usage.
    # ═══════════════════════════════════════════════════════════════════
    steps = result.get("intermediate_steps", [])
    tools_used = [step[0].tool for step in steps]
    distinct = sorted(set(tools_used))

    print(f"\n═══ Trace ReAct ({len(steps)} steps, {len(distinct)} outils distincts) ═══")
    for i, (action, obs) in enumerate(steps, 1):
        print(f"\n  Step {i} — Action: {action.tool}")
        print(f"           Input:  {str(action.tool_input)[:120]}")
        print(f"           Obs:    {str(obs)[:120]}")

    print(f"\n═══ Outils distincts appelés : {distinct}")
    print(f"\n═══ Réponse finale ═══\n{result['output']}")

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT AGENT : Mémoire conversationnelle (ConversationBufferWindowMemory)
    # ──────────────────────────────────────────────────────────────────
    # k=6 → garde les 6 derniers tours (3 questions + 3 réponses)
    # Si on relance executor.invoke avec la même instance, l'agent voit
    # l'historique → "tu as dit quoi à propos de la chaudière ?" fonctionne.
    # En production : 1 instance par session_id, reset si l'API redémarre.
    # ═══════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    main()
