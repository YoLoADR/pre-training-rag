"""
═══════════════════════════════════════════════════════════════════════════
Atelier 01 — LLM Baseline (solution corrigée + commentaires pédagogiques)
═══════════════════════════════════════════════════════════════════════════

Lancer :  python ateliers/atelier-01-llm-baseline/solution.py

Cette solution importe directement depuis homebutler/llm/provider.py
(pas de duplication de code — les commentaires entourent les appels).
═══════════════════════════════════════════════════════════════════════════
"""

from langchain_core.messages import HumanMessage

# Note : on importe le code de production tel quel.
# get_llm() lit LLM_PROVIDER dans .env → bascule automatique Anthropic/Ollama.
from homebutler.llm.provider import get_llm
from homebutler import config


QUESTIONS_LOGEMENT = [
    "Quelle est la marque de ma chaudière ?",
    "À quelle température dois-je régler ma chaudière la nuit ?",
    "Quelle est la classe énergétique (DPE) de mon logement ?",
    "Quel est le numéro à appeler en cas de fuite d'eau dans mon bail ?",
    "Quels sont les producteurs locaux disponibles près de chez moi ?",
]


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT LLM : Hallucination
# ───────────────────────────────────────────────────────────────────────────
# Un LLM produit du texte en prédisant statistiquement le token suivant.
# Il n'a aucun mécanisme de vérification factuelle interne. Quand il ne
# "sait pas", il complète quand même → c'est ce qu'on appelle l'hallucination.
# Sur "marque de votre chaudière", le modèle propose souvent "Viessmann",
# "De Dietrich" ou "Atlantic" — ce qui n'est pas faux statistiquement
# (ce sont les marques les plus fréquentes du dataset web), mais c'est faux
# pour VOTRE logement.
# Le RAG (atelier 02) résout ce problème en injectant les vrais documents.
# ═══════════════════════════════════════════════════════════════════════════
def run_1_baseline_temperature_basse() -> None:
    """Exécution déterministe : temperature=0.1 → réponses très stables."""
    llm = get_llm(temperature=0.1)
    print(f"\n═══ Run 1 — provider={config.LLM_PROVIDER}, temperature=0.1 ═══")
    for i, q in enumerate(QUESTIONS_LOGEMENT, 1):
        response = llm.invoke([HumanMessage(content=q)])
        print(f"\n[{i}] {q}")
        print(f"    → {response.content[:300]}")


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT LLM : Température
# ───────────────────────────────────────────────────────────────────────────
# La température transforme les probabilités du prochain token avant le sampling.
#   T=0   : toujours le token le plus probable (déterministe)
#   T=1   : sampling sur la distribution brute
#   T>1   : aplatit la distribution → plus de diversité, plus d'erreurs
# Pour un assistant factuel (RAG, agent), T=0 à 0.3 est recommandé.
# Pour de la rédaction créative, T=0.7 à 1.0.
# ═══════════════════════════════════════════════════════════════════════════
def run_2_comparer_temperatures() -> None:
    """Lance deux fois la même question avec température élevée → variabilité."""
    llm_aleatoire = get_llm(temperature=0.9)
    question = QUESTIONS_LOGEMENT[0]
    print(f"\n═══ Run 2 — temperature=0.9, 2 essais sur la même question ═══")
    print(f"Question : {question}")
    for run in (1, 2):
        resp = llm_aleatoire.invoke([HumanMessage(content=question)])
        print(f"\n  Essai {run} → {resp.content[:200]}")


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT LLM : Provider Anthropic vs Ollama (knowledge cutoff)
# ───────────────────────────────────────────────────────────────────────────
# Anthropic (Claude) : modèle hébergé, knowledge cutoff ~ janvier 2025.
# Ollama (Mistral/Llama) : modèle local, knowledge cutoff variable selon le modèle.
# Dans les deux cas → AUCUNE connaissance de votre logement privé.
# La bascule provider se fait via une seule variable LLM_PROVIDER=ollama
# dans .env, sans modifier le code (abstraction get_llm()).
# ═══════════════════════════════════════════════════════════════════════════
def info_provider() -> None:
    print(f"\nProvider actif : {config.LLM_PROVIDER}")
    if config.LLM_PROVIDER == "anthropic":
        print(f"Modèle Anthropic : {config.ANTHROPIC_MODEL}")
        print("→ Pour basculer Ollama : LLM_PROVIDER=ollama dans .env")
    else:
        print(f"Modèle Ollama : {config.OLLAMA_MODEL} @ {config.OLLAMA_HOST}")


def main() -> None:
    info_provider()
    run_1_baseline_temperature_basse()
    run_2_comparer_temperatures()

    print("\n" + "═" * 72)
    print("À RETENIR")
    print("═" * 72)
    print(" • 5/5 questions reçoivent une réponse INVENTÉE plausible.")
    print(" • Aucune ne reçoit un honnête 'je ne sais pas'.")
    print(" • Température 0 = déterministe ; température 0.9 = créatif/aléatoire.")
    print(" • Le LLM n'a aucun moyen de vérifier ce qu'il dit → RAG en atelier 02.")


if __name__ == "__main__":
    main()
