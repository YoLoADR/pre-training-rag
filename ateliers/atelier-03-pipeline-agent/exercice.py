"""
═══════════════════════════════════════════════════════════════════════════
Atelier 03 — Pipeline + Agent ReAct (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : construire un agent multi-outils ReAct.

5 TODOs :
  1. Construire l'EnsembleRetriever (FAISS + ChromaDB)
  2. Lister les 4 outils (RAG, énergie, marketplace, météo)
  3. Assembler l'AgentExecutor via create_react_agent
  4. Activer return_intermediate_steps=True pour voir la trace ReAct
  5. Poser la question multi-outils et compter les Actions

Lancer :  python ateliers/atelier-03-pipeline-agent/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

# TODO 1 — importer get_ensemble_retriever depuis homebutler.rag.retriever
# from homebutler.rag.retriever import ...

# TODO 2 — importer les 4 outils déjà fournis dans homebutler.agent.tools
# from homebutler.agent.tools import (search_docs_tool, analyze_energy_tool,
#                                     find_products_tool, get_weather_tool)

# TODO 3 — importer create_react_agent + AgentExecutor + hub
# from langchain import hub
# from langchain.agents import create_react_agent, AgentExecutor
# from homebutler.llm.provider import get_llm


QUESTION_MULTI_OUTILS = (
    "Il va faire -5°C demain, comment je prépare ma maison et "
    "que puis-je commander à un producteur local pour me réchauffer ?"
)


def main() -> None:
    # ─── TODO 1 — EnsembleRetriever ─────────────────────────────────────
    # Vérifier d'abord que les deux index sont construits
    # (voir README → pré-requis "Construire les deux index").
    # retriever = get_ensemble_retriever(faiss_k=4, chroma_k=3)
    # docs = retriever.invoke("Quelle est la marque de ma chaudière ?")
    # print(f"Ensemble retourne {len(docs)} chunks fusionnés")
    raise NotImplementedError("TODO 1 — construire l'EnsembleRetriever")

    # ─── TODO 2 — Les 4 outils ──────────────────────────────────────────
    # tools = [search_docs_tool, analyze_energy_tool,
    #          find_products_tool, get_weather_tool]
    # for t in tools:
    #     print(f"  - {t.name}: {t.description[:60]}...")

    # ─── TODO 3 — Assembler l'agent ReAct ───────────────────────────────
    # llm = get_llm(temperature=0.1, max_tokens=2048)
    # prompt = hub.pull("hwchase17/react-chat")  # supporte chat_history
    # agent = create_react_agent(llm, tools, prompt)
    # executor = AgentExecutor(
    #     agent=agent,
    #     tools=tools,
    #     verbose=True,
    #     max_iterations=8,
    #     handle_parsing_errors=True,
    #     return_intermediate_steps=True,  # ← TODO 4
    # )

    # ─── TODO 5 — Question multi-outils + compter les Actions ───────────
    # result = executor.invoke({"input": QUESTION_MULTI_OUTILS,
    #                           "chat_history": []})
    # steps = result.get("intermediate_steps", [])
    # tools_used = [step[0].tool for step in steps]
    # print(f"\n=== Outils appelés ({len(steps)}) : {tools_used}")
    # print(f"=== Réponse finale :\n{result['output']}")


if __name__ == "__main__":
    main()
