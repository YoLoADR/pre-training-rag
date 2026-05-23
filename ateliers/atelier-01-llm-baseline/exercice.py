"""
═══════════════════════════════════════════════════════════════════════════
Atelier 01 — LLM Baseline (exercice à compléter)
═══════════════════════════════════════════════════════════════════════════

Objectif : observer un LLM sans contexte → hallucinations + température.

5 TODOs :
  1. Instancier le LLM via get_llm()
  2. Poser 5 questions sur le logement et noter les réponses
  3. Comparer temperature=0 vs temperature=0.9
  4. (Optionnel) Basculer LLM_PROVIDER=ollama et relancer
  5. Noter quelles questions reçoivent des réponses inventées

Lancer :  python ateliers/atelier-01-llm-baseline/exercice.py
═══════════════════════════════════════════════════════════════════════════
"""

# ─── Imports déjà fournis ────────────────────────────────────────────────
from langchain_core.messages import HumanMessage

# TODO 1 — importer get_llm depuis homebutler.llm.provider
# from homebutler.llm.provider import ...


# ─── Questions fil rouge HomeButler ──────────────────────────────────────
QUESTIONS_LOGEMENT = [
    "Quelle est la marque de ma chaudière ?",
    "À quelle température dois-je régler ma chaudière la nuit ?",
    "Quelle est la classe énergétique (DPE) de mon logement ?",
    "Quel est le numéro à appeler en cas de fuite d'eau dans mon bail ?",
    "Quels sont les producteurs locaux disponibles près de chez moi ?",
]


def poser_questions(llm, questions: list[str], label: str = "") -> None:
    """Pose une liste de questions au LLM et affiche les réponses."""
    print(f"\n{'═'*72}\n{label}\n{'═'*72}")
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}] {q}")
        response = llm.invoke([HumanMessage(content=q)])
        print(f"    → {response.content[:300]}")
        if len(response.content) > 300:
            print("      [...]")


def main() -> None:
    # TODO 1 — Instancier un LLM avec température basse (0.1)
    # llm = get_llm(temperature=0.1)
    raise NotImplementedError("TODO 1 — instancier le LLM via get_llm()")

    # TODO 2 — Poser les 5 questions du logement et lire les réponses.
    # Question à se poser : la réponse est-elle vraie ? Comment le savoir ?
    # poser_questions(llm, QUESTIONS_LOGEMENT, "Run #1 — temperature=0.1")

    # TODO 3 — Recréer un LLM avec temperature=0.9 et reposer la MÊME question
    # (la première). Lancer 2 fois → observer si la réponse change.
    # llm_aleatoire = get_llm(temperature=0.9)
    # for run in (1, 2):
    #     resp = llm_aleatoire.invoke([HumanMessage(content=QUESTIONS_LOGEMENT[0])])
    #     print(f"\nRun aléatoire #{run} : {resp.content[:200]}")

    # TODO 4 — (Optionnel, si Ollama installé)
    # Modifier .env : LLM_PROVIDER=ollama
    # Relancer ce script → get_llm() utilisera automatiquement Ollama.
    # Pourquoi possible ? l'abstraction provider.py lit la variable à chaque appel.

    # TODO 5 — Noter dans un commentaire ici quelles questions ont reçu
    # des réponses inventées vs "je ne sais pas". Indice : 5/5 sont inventées.
    # Réponses inventées : ___________________________________
    # Réponses "je ne sais pas" : _____________________________


if __name__ == "__main__":
    main()
