# Bug v3 — Latence mesurée sur 1 seul appel (biais cold-start)

## Contexte

Le premier appel à un pipeline RAG ou à l'agent initialise le vectorstore, charge les embeddings en mémoire, crée la session LLM. Ce "cold start" est 2 à 10 fois plus lent que les appels suivants. Mesurer la latence sur ce seul appel donne une estimation fortement sur-estimée, non représentative du cas d'usage réel.

## Affirmations Vrai / Faux

**1. "Mesurer la latence sur 1 appel est suffisant si le code est déterministe."**

[ ] Vrai   [ ] Faux

**2. "Le cold-start penalty disparaît après le 1er appel dans la même session uvicorn."**

[ ] Vrai   [ ] Faux

**3. "La p95 de latence est inutile si on mesure la latence moyenne sur 10 appels."**

[ ] Vrai   [ ] Faux

**4. "Pour comparer llm_only vs rag_only vs agent, il faut mesurer sur les mêmes questions exactement."**

[ ] Vrai   [ ] Faux

**5. "Ignorer le 1er appel dans le calcul de latence est une triche — on cache les vrais temps."**

[ ] Vrai   [ ] Faux

---

## Réponses commentées

1. **FAUX** — Même dans un code déterministe, la latence dépend du réseau (Anthropic API), de la charge CPU, du garbage collector Python, du cache LRU de FAISS. Sur 1 appel, tu mesures un seul point de la distribution — tu ne sais pas si c'est représentatif.

2. **VRAI partiellement** — Après le 1er appel, l'agent ReAct est initialisé (voir `get_singleton_agent()` dans `api/main.py`), le vectorstore est chargé. Les appels suivants n'ont plus ce coût. Mais le réseau (latence Anthropic), le garbage collector et la charge CPU varient à chaque appel.

3. **FAUX** — La moyenne cache les extrêmes. Si 9 appels prennent 2s et 1 appel prend 45s (timeout partial, network hiccup), la moyenne est ~6s — qui ne représente ni le cas normal (2s) ni le pire cas (45s). La p95 révèle ce dernier.

4. **VRAI** — Si tu mesures `llm_only` sur la question "Quelle est la marque de ma chaudière ?" et `agent` sur "Prépare-moi un dîner", tu ne compares pas la même difficulté. La comparaison doit être contrôlée : mêmes questions, même ordre, même session.

5. **FAUX** — Ignorer le 1er appel est une pratique standard en benchmark système (warm-up). En prod, les utilisateurs ne voient pas le 1er appel (l'API a déjà tourné depuis X heures). La métrique pertinente est la latence des appels "steady-state", pas la latence de démarrage.
