# Insights — Enrichissement API/LLM HomeButler

## Découvertes techniques

### LangChain 0.3.14 — imports corrects
- `AsyncIteratorCallbackHandler` → `langchain.callbacks.streaming_aiter` (PAS `langchain_core.callbacks`)
- `ConversationBufferWindowMemory` → `langchain.memory` ✅
- `hub.pull('hwchase17/react-chat')` → input_variables: `['agent_scratchpad', 'chat_history', 'input', 'tool_names', 'tools']` ✅
- Différence clé : `react` vs `react-chat` — le second supporte `{chat_history}`

### FastAPI — pattern middleware
- `raise HTTPException` dans un middleware = HTTP 500 (bugfix déjà appliqué avant ce sprint)
- `return JSONResponse(status_code=400, ...)` est le pattern correct
- `slowapi` : décorateur `@limiter.limit("30/minute")` nécessite `request: Request` en premier param

### Anthropic prompt caching
- Header beta requis : `"anthropic-beta": "prompt-caching-2024-07-31"`
- Via `model_kwargs={"extra_headers": {...}}` dans `ChatAnthropic`
- Cache effectif à partir de ~1024 tokens (system prompt HomeButler = ~120 tokens → trop court pour être rentable seul, mais le contexte RAG injecté le fait dépasser le seuil)

### Agent ReAct avec mémoire
- `hwchase17/react-chat` requiert `chat_history` dans l'invocation
- `ConversationBufferWindowMemory(k=6, memory_key="chat_history", return_messages=True, output_key="output")`
- Le `output_key="output"` est critique pour éviter l'ambiguïté avec `intermediate_steps`

### Recall@K — évaluation RAG
- Ground truth : mots-clés extraits de l'`output` de référence (JSONL)
- Heuristique : si le texte d'un chunk retourné contient ≥1 mot-clé de la réponse → hit
- Recall@K = nb_questions_avec_hit_dans_topK / nb_questions_total

## Décisions d'implémentation
- Le streaming utilise `AsyncIteratorCallbackHandler` de `langchain.callbacks.streaming_aiter`
- Le mode `compare` lance 3 coroutines en parallèle avec `asyncio.gather`
- `get_session_agent()` crée un agent distinct par `session_id` (dict en mémoire, pas Redis)
- La mémoire est en RAM → reset si API redémarre (acceptable pour le contexte formation)

## Découvertes BLOCs 7-10 (2026-05-20)

### slowapi — pattern correct pour rate limiting dans router
- Créer `api/limiter.py` avec `limiter = Limiter(key_func=get_remote_address)` partagé
- Importer ce module dans `main.py` ET dans chaque router qui l'utilise
- Ne PAS recréer un Limiter() dans chaque fichier (instances indépendantes → pas de partage du compteur)
- Le décorateur `@limiter.limit("30/minute")` nécessite `request: Request` comme premier paramètre du handler
- Résultat validé : 35 requêtes parallèles → 21×200 + 14×429 ✅

### /rag/compare-strategies — paramètre dans l'URL
- L'endpoint prend `query: str` directement (FastAPI query param), pas dans le body JSON
- Correct : `POST /rag/compare-strategies?query=purger+radiateurs`
- Incorrect : `POST /rag/compare-strategies` avec body `{"query": "..."}`

### augment_qa_dataset.py — résultat réel
- 150 paires originales → 521 avant dédup → 431 après dédup (pas 500)
- La déduplication supprime les reformulations trop proches (variantes parfois quasi-identiques)
- Acceptable pour le TP : la doc dit "~500 paires" et 431 couvre 150 originals + 281 variantes

### Notebook 03 — architecture choisie
- 27 cellules (15 code, 12 markdown) → structure pédagogique complète
- Cellules code= exécutables sur Colab T4, pseudocodes pour les étapes nécessitant A100
- Dataset chargé depuis GitHub raw URL avec fallback local (robuste en Colab)
- Section distillation intentionnellement en pseudocode (hors portée GPU T4)

---

## Comparaison des approches — comportement observé (2026-05-20)

### `POST /chat/compare` — différences constatées sur une question métier

Question test : *"Quelle est la marque de ma chaudière ?"*

| Mode | Comportement | Réponse type |
|---|---|---|
| `llm_only` | Hallucine — invente une marque générique | "Votre chaudière est probablement une Bosch ou Viessmann..." |
| `rag_only` | Factuel — cite le PDF | "Votre chaudière est une **Viessmann Vitodens 100-W**" + sources[] |
| `agent` | Orchestré — utilise l'outil RAG puis synthétise | Même précision que rag_only + propose des artisans si besoin |

**Valeur pédagogique** : montre exactement la grille de décision du draft.md (LLM seul → hallucine, RAG → factuel, agent → orchestré).

### `POST /rag/compare-strategies?query=...` — différences entre chunkers

Résultat validé sur *"comment purger mes radiateurs"* :
- `fixed` : 4 chunks | sources: `[dpe.pdf, notice_chaudiere.pdf, bail_location.pdf, notice_vmc.pdf]`
- `recursive` : 4 chunks | sources: `[dpe.pdf, notice_chaudiere.pdf, bail_location.pdf, notice_vmc.pdf]`
- `ensemble` : **5 chunks** | sources: `[notice_lave_linge.pdf, dpe.pdf, notice_chaudiere.pdf, bail_location.pdf, notice_vmc.pdf]`

**Observation** : l'ensemble récupère un document supplémentaire (notice_lave_linge.pdf) grâce à la combinaison FAISS+ChromaDB — montre concrètement la valeur du retrieval hybride.

### `POST /rag/evaluate` — Recall@K par stratégie

Validé sur 10 questions, stratégie `ensemble` :
- recall@1 = **0.70** (7/10 questions trouvées dès le 1er chunk)
- recall@3 = **0.80** (8/10 questions trouvées dans le top-3)
- recall@5 = **1.00** (10/10 questions trouvées dans le top-5)

Pour comparer les stratégies (TP J1), appeler l'endpoint 3 fois en changeant `strategy` : `fixed`, `recursive`, `ensemble`.

### `GET /chat/stream` — SSE validé
Réponse arrivant token par token : `data: #\n\ndata:  Bonjour ! 👋\n\ndata: ...`
Signal de fin : `data: [DONE]`

### Piège `POST /rag/compare-strategies` — paramètre URL et non body
Le paramètre `query` est un **FastAPI query param** (dans l'URL), pas dans le body JSON :
- ✅ `POST /rag/compare-strategies?query=purger+radiateurs`
- ❌ `POST /rag/compare-strategies` + body `{"query":"..."}`  → query=None dans la réponse
