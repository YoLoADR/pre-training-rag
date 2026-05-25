📝 Slide 1 : Atelier 06 — Évaluation comparative RAG vs Hybride (mission en un coup d'œil)

POURQUOI clôturer la formation par un atelier d'évaluation ?

Après 5 ateliers à construire, tu as un agent fonctionnel. Mais devant un comité ou un client, la VRAIE question est : « RAG ou Fine-Tuning, ou les deux (RAFT) ? combien ça coûte, combien c'est lent, combien c'est juste ? ». Cet atelier produit un TABLEAU MARKDOWN signé avec Recall@k, latence et grille décision TCO pour 3 cas d'usage métier. Sans chiffres, pas d'argument.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| `load_qa()` (FOURNI) | Charge 20 paires de référence du dataset HomeButler | Le ground truth |
| `evaluate_strategies()` (À CODER TODO 2) | POST `/rag/evaluate` × 3 stratégies de chunking | Compare fixed / recursive / ensemble |
| `compare_modes()` (À CODER TODO 3) | POST `/chat` × 5 questions × 3 modes | Compare llm_only / rag_only / agent |
| `show_latency_summary()` (FOURNI) | mean + median par mode | Latence = critère TCO majeur |
| `show_summary()` (À CODER TODO 5) | Tableau Markdown + benchmarks RAFT 2024 | Le livrable visuel |
| `grille_decision.md` | À COMPLÉTER manuellement (rédaction) | Recommandation argumentée par cas d'usage |

> 💡 **Branche élève** : `git checkout student/06-finetune-vs-rag`. Particularité : nécessite `ENABLE_COMPARE_ROUTES=true` pour activer `/rag/evaluate` et `/chat/compare` (désactivés par défaut en AT05).


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI un seul fichier à blanker pour AT06 ?

Le scope AT06 = **évaluation comparative + grille décision**. Tout le reste est déjà fait (AT01-05). Le seul fichier porteur du concept central = `evaluate_pipeline.py`. Le delta entre `atelier/05` et `atelier/06` côté API = 4 lignes — pas la peine de blanker des deltas anémiques. L'atelier vit dans `evaluate_pipeline.py` (~150 lignes, 6 TODOs documentés).

| Fichier | État | Pourquoi |
|---------|------|----------|
| Tous les ateliers AT01-05 | ✅ Acquis | Stack complète opérationnelle |
| `ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py` → `load_qa` | ✅ Fourni (TODO 1) | Utilitaire de chargement |
| `evaluate_pipeline.py` → `evaluate_strategies` | 🛠️ **À CODER (TODO 2)** | Concept central : appel d'API HTTP pour évaluer 3 stratégies |
| `evaluate_pipeline.py` → `compare_modes` | 🛠️ **À CODER (TODO 3)** | Concept central : double boucle d'évaluation |
| `evaluate_pipeline.py` → `show_latency_summary` | ✅ Fourni (TODO 4) | Affichage statistique |
| `evaluate_pipeline.py` → `show_summary` | 🛠️ **À CODER (TODO 5)** | Tableau Markdown + benchmarks RAFT |
| `evaluate_pipeline.py` → `todo_grille` | ✅ Fourni (TODO 6) | Placeholder |
| `grille_decision.md` | À COMPLÉTER (rédaction) | Recommandation 3 cas d'usage |


📝 Slide 3 : Concept #1 — Évaluer 3 stratégies via l'API HTTP

POURQUOI passer par l'API HTTP plutôt qu'importer les fonctions Python ?

Tentation : `from homebutler.rag.retriever import retrieve` puis appel direct. C'EST PIRE. En passant par HTTP, on évalue **la stack TELLE QU'ELLE TOURNERA EN PROD** : routing FastAPI, sérialisation, latence réseau locale, validation Pydantic, exceptions HTTP. C'est le mode « bout-en-bout » qui révèle les régressions que les imports directs masquent.

**Signature à compléter (TODO 2)** :

```python
def evaluate_strategies(sample_size: int = 20) -> dict:
    """Boucle sur 3 stratégies de chunking (fixed/recursive/ensemble),
    appelle POST /rag/evaluate pour chacune, mesure la latence côté client,
    retourne un dict {strategy: response_json}.
    """
    raise NotImplementedError("TODO 2 — voir indices ci-dessous")
```

**Indice léger** — Boucle `for strategy in ("fixed", "recursive", "ensemble"):`. Pour chacune : (1) prends un timestamp avant l'appel, (2) `requests.post(f"{API}/rag/evaluate", json={"strategy": ..., "sample_size": ...})`, (3) calcule l'elapsed, (4) si HTTP 200, stocke `r.json()` dans `out[strategy]` et affiche un récap, sinon log et continue.

**Indice fort** — Pour la latence : `t0 = time.time()` avant le POST, `elapsed = time.time() - t0` après. ⚠️ Ne crashe pas tout le script si une stratégie rate (ex: index manquant) — `if r.status_code != 200: print(f"  {strategy}: HTTP {r.status_code}"); continue`. Format d'affichage : `print(f"  {strategy:10s}  Recall@1={data['recall_at_1']:.2f}  Recall@3={data['recall_at_3']:.2f}  Recall@5={data['recall_at_5']:.2f}  ({elapsed:.1f}s)")`.

| Stratégie | Recall@5 typique (HomeButler) | Cas d'usage |
|-----------|-------------------------------|-------------|
| fixed     | 0.65–0.75 | Documents uniformes (logs, tableaux) |
| recursive | 0.80–0.88 | Documents textuels (notices, bail) — **DEFAULT** |
| ensemble  | 0.85–0.92 | Quand on a aussi un Chroma avec métadonnées riches |

> 💡 **Piège** — si tu vois `Recall@5 < 0.4`, ce n'est PAS la stratégie de chunking. C'est probablement l'index FAISS qui n'a pas été reconstruit après changement de stratégie. Re-lance `python scripts/build_index.py --strategy=…`.

**📚 Dépendances natives utilisées**

- `requests.post(url, json=..., timeout=..., headers=..., params=...) → Response` — appel HTTP POST côté client. Paramètres :
  - `url: str` — URL complète de l'endpoint (ex. `"http://localhost:8000/rag/evaluate"`).
  - `json: dict | None` — corps JSON-encodé. Ajoute automatiquement `Content-Type: application/json`.
  - `data: dict | str | bytes` — alternative pour form data ou raw bytes.
  - `timeout: float | tuple[float, float]` — timeout en secondes. `(connect_timeout, read_timeout)` pour différencier.
  - `headers: dict[str, str]` — headers HTTP custom.
  - `params: dict` — query string params (ex. `?strategy=fixed&k=4`).

- `Response` (retour de `requests.post`) :
  - `.status_code: int` — code HTTP (200, 404, 500, etc.). 200 = OK.
  - `.json() → dict` — parse le body en dict Python. Lève `ValueError` si pas JSON.
  - `.text: str` — body brut en string.
  - `.elapsed: timedelta` — durée mesurée côté `requests` (depuis l'envoi de la requête jusqu'à la réception complète).

- `time.time() → float` — timestamp Unix en secondes (avec microsecondes). Pour mesurer une latence client : `t0 = time.time(); ...; elapsed = time.time() - t0`.


📝 Slide 4 : Concept #2 — Comparer 3 modes sur les mêmes questions

POURQUOI mesurer la latence DE CHAQUE appel (pas une moyenne globale) ?

Une moyenne globale cache la **variance**. Un mode peut être rapide en moyenne mais avec un p99 (99e percentile) catastrophique — c'est ce qui bloque en prod. Garder le détail par appel permet de calculer mean + median + p95 + p99.

**Signature à compléter (TODO 3)** :

```python
def compare_modes(questions: list[str]) -> dict:
    """Double boucle : questions × modes. Pour chaque (question, mode),
    POST /chat avec le bon mode, mesure la latence, stocke la réponse.
    Retourne {"answers": {mode: [responses]}, "latencies": {mode: [seconds]}}.
    """
    raise NotImplementedError("TODO 3 — voir indices ci-dessous")
```

**Indice léger** — Initialise deux dicts : `results = {"llm_only": [], "rag_only": [], "agent": []}` et `latencies = {"llm_only": [], "rag_only": [], "agent": []}`. Double boucle : outer sur `questions`, inner sur les 3 modes. Pour chaque combo, fais un `requests.post(f"{API}/chat", json={"message": q, "mode": mode}, timeout=60)`.

**Indice fort** — `timeout=60` est large mais nécessaire : l'agent ReAct peut prendre 30 s avec 5-8 itérations + appels LLM. llm_only ≈ 2 s. ⚠️ Si HTTP != 200, enregistre quand même `f"HTTP {r.status_code}"` dans `results[mode]` (et la latence) — utile pour voir si un mode est instable (rate limit, timeout). Sinon `results[mode].append(r.json().get("response", ""))`.

| Mode      | Latence moyenne (s) | Tokens / réponse | Faithfulness |
|-----------|--------------------|--------------------|-------------|
| llm_only  | 1-2                | ~150 (court)        | 0.20 (hallucine) |
| rag_only  | 3-5                | ~300                | 0.85+ (factuel) |
| agent     | 8-15               | ~500 (avec ReAct)   | 0.80+ (multi-source) |


**📚 Dépendances natives utilisées**

- `requests.post(...)` (déjà détaillé en Slide 3) — utilisé ici avec **`timeout=60`** car les modes lents (agent ReAct) peuvent prendre 30 s. Sans timeout, un mode bloqué bloque tout le script.

- `list.append(x)` (built-in Python) — accumule les latences dans `latencies[mode]`. Permet de calculer ensuite mean / median / p95 / p99 via `statistics.mean()`, `statistics.median()`, ou `numpy.percentile(arr, 95)`.

- Pattern dict-de-listes : `results = {"llm_only": [], "rag_only": [], "agent": []}` — structure idéale pour collecter en double boucle (outer = questions, inner = modes), puis itérer par mode pour les stats.


📝 Slide 5 : Concept #3 — Tableau récapitulatif Markdown + benchmarks RAFT

POURQUOI produire du Markdown affiché en console ?

Tu peux copier-coller la sortie console DIRECTEMENT dans ton rapport Markdown (PR description, Notion, Slack). Pas besoin d'écrire un parser séparé. Et l'alignement par `f"{x:<12}"` donne un tableau lisible même en monospace.

**Signature à compléter (TODO 5)** :

```python
def show_summary(strategies_eval: dict, latencies: dict) -> None:
    """Affiche un tableau aligné des Recall@k pour 3 stratégies + une section
    'à comparer aux benchmarks RAFT 2024' avec les chiffres de référence.
    """
    raise NotImplementedError("TODO 5 — voir indices ci-dessous")
```

**Indice léger** — Une seule technique : f-strings avec alignement. `f"{x:<12}"` = padding à gauche sur 12 caractères, `f"{x:>6.2f}"` = alignement droite sur 6 caractères avec 2 décimales. Avec ces deux outils, tu produis un tableau aligné qui ressemble visuellement à du Markdown.

**Indice fort** — Header : `print(f"{'Stratégie':<12} {'R@1':>6} {'R@3':>6} {'R@5':>6}")`. Pour chaque stratégie dans `strategies_eval` : `print(f"{strategy:<12} {data['recall_at_1']:>6.2f} {data['recall_at_3']:>6.2f} {data['recall_at_5']:>6.2f}")`. Termine par les benchmarks RAFT 2024 hardcodés : RAG ensemble ~0.87, RAG fixed-size ~0.72, LLM seul ~0.15, Hybride (RAFT) 94 % QA factuel.

**Sortie attendue** (à copier dans ton rapport) :
```
Stratégie       R@1    R@3    R@5
fixed          0.55   0.68   0.72
recursive      0.65   0.80   0.85
ensemble       0.72   0.85   0.87

À COMPARER aux benchmarks RAFT 2024 :
  RAG ensemble    : Recall@5 attendu ~ 0.87  ← tu ES À LA CIBLE ✓
  RAG fixed-size  : Recall@5 attendu ~ 0.72  ← OK
  ...
```


**📚 Dépendances natives utilisées**

- **f-strings Python** avec format mini-language (`f"{val:<12}"` etc.) — directives utiles :
  - `:<12` — alignement GAUCHE sur 12 caractères (padding à droite).
  - `:>6` — alignement DROITE sur 6 caractères (padding à gauche).
  - `:^10` — alignement CENTRÉ sur 10 caractères.
  - `:.2f` — `float` avec 2 décimales.
  - `:>6.2f` — combiné : 6 caractères, alignement droite, 2 décimales.
  - `:,` — séparateur de milliers (ex. `f"{1234567:,}"` → `"1,234,567"`).
  - `:e` — notation scientifique (ex. `f"{0.0000123:.2e}"` → `"1.23e-05"`).

- Aucun parser Markdown nécessaire : Python natif suffit. La sortie console alignée par f-strings reste lisible dans un `.md` rendu en monospace (GitHub, Notion, Slack).


📝 Slide 6 : La grille de décision TCO (à rédiger manuellement)

POURQUOI la rédaction manuelle de `grille_decision.md` ?

Les chiffres mesurés ne disent PAS « il faut RAG vs FT vs Hybride pour le cas RH ». Cette décision est un RAISONNEMENT qui combine : (a) la nature du problème (connaissance manquante vs style), (b) le volume de données, (c) le budget récurrent, (d) la latence acceptable, (e) la sensibilité des données (cloud vs on-premise). C'est le LIVRABLE INTELLECTUEL de la formation.

**Template à remplir** (3 cas d'usage métier) :

```markdown
# Grille de décision RAG vs FT vs Hybride (RAFT) — 3 cas

## Cas 1 : Chatbot RH interne (politique RH, congés, mobilité)
- **Volume** : 200 documents PDF, mises à jour mensuelles
- **Recommandation** : RAG seul
- **Justification** :
  - Connaissance qui CHANGE souvent (politique RH révisée chaque mois) → RAG
    permet de réindexer en 5 min, vs FT qui demande 2-3 jours.
  - Pas besoin de modifier le TON (assistant générique acceptable).
  - Coût mesuré : 0.005 $/question avec Claude Sonnet + ensemble retriever.
  - Latence mesurée : 3-5 s par question — acceptable pour chatbot interne.

## Cas 2 : Support technique produit IoT (smart home)
- **Volume** : 50 notices, vocabulaire technique spécifique
- **Recommandation** : Hybride (RAFT)
- **Justification** :
  - Connaissance stable (notices) MAIS vocabulaire technique → RAFT entraîne
    le modèle à IGNORER les distracteurs de retrieval (chunks proches mais
    pas pertinents).
  - Gain mesuré dans RAFT paper : +12 % faithfulness sur questions techniques.
  - Surcoût : 1 fine-tuning trimestriel sur Colab Pro (~15 €/mois).

## Cas 3 : Analyse de contrats juridiques (clauses spécifiques)
- **Volume** : 10 000 contrats, format hétérogène
- **Recommandation** : RAG ensemble + métadonnées riches
- **Justification** :
  - Volume trop grand pour FT → RAG obligatoire.
  - FT inadapté : on cherche des CITATIONS précises, pas un style.
  - Métadonnées clés : type de contrat, date, parties → Chroma > FAISS seul.
  - Latence : 5-10 s acceptable (analyse pas temps réel).
```

> 💡 **Critère de qualité** : ta grille doit citer des CHIFFRES mesurés par toi (pas juste des opinions). « 3 s » ≠ « rapide ».


📝 Slide 7 : Récap — démarrer sur la branche `student/06-finetune-vs-rag`

POURQUOI activer `ENABLE_COMPARE_ROUTES` ?

En AT05, les endpoints `/rag/evaluate` et `/chat/compare` sont DÉSACTIVÉS pour éviter qu'un élève AT05 ne s'y égare (scope strict). En AT06, on les active explicitement via une variable d'env. C'est le toggle propre qui transforme l'API « simple chatbot » en « banc d'évaluation ».

```bash
# 1. Setup
git checkout student/06-finetune-vs-rag
source .venv/bin/activate && pip install -e .
bash scripts/check_atelier_ready.sh 06

# 2. Activer les routes de comparaison
echo "ENABLE_COMPARE_ROUTES=true" >> .env
grep ENABLE_COMPARE_ROUTES .env       # vérifier que c'est bien posé

# 3. Démarrer l'API et UN seul terminal
uvicorn api.main:app --port 8000 &
sleep 3
curl -s http://localhost:8000/ | jq    # check up
curl http://localhost:8000/docs        # → Swagger affiche maintenant /rag/evaluate et /chat/compare

# 4. CODER (dans cet ordre)
#    a) evaluate_pipeline.py TODO 2 — evaluate_strategies (le plus simple)
#    b) evaluate_pipeline.py TODO 3 — compare_modes
#    c) evaluate_pipeline.py TODO 5 — show_summary
#    Lancer après chaque ajout :
python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py

# 5. RÉDIGER grille_decision.md (3 cas, justifications chiffrées)
$EDITOR ateliers/atelier-06-finetune-vs-rag/grille_decision.md

# 6. Checkpoint
python ateliers/atelier-06-finetune-vs-rag/checkpoints/check_1.py
#  → 3 questions RAFT + verbalisation pourquoi HTTP vs imports directs

# 7. En dernier recours
git diff student/06-finetune-vs-rag atelier/06-finetune-vs-rag \
  -- ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
```

⚠️ **Si tu obtiens `HTTP 404` sur `/rag/evaluate`** — vérifier que `ENABLE_COMPARE_ROUTES=true` est bien dans le `.env` LU par uvicorn (relancer uvicorn après modif). Le `404` est intentionnel sinon — c'est ce qui empêche l'élève AT05 de tricher.

> 💡 **Livrable final formation** : `evaluate_pipeline.py` exécuté + `grille_decision.md` complété + slides de présentation. Tu sors avec un argumentaire CHIFFRÉ pour défendre une architecture RAG/FT/Hybride sur n'importe quel cas d'usage.
