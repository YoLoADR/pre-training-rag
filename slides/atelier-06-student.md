📝 Slide 1 : Atelier 06 — Évaluation comparative RAG vs Hybride (mission en un coup d'œil)

POURQUOI clôturer la formation par un atelier d'évaluation ?

Après 5 ateliers à construire, l'élève a un agent fonctionnel. Mais devant un comité ou un client, la VRAIE question est : « RAG ou Fine-Tuning, ou les deux (RAFT) ? combien ça coûte, combien c'est lent, combien c'est juste ? ». Cet atelier produit un TABLEAU MARKDOWN signé avec Recall@k, latence et grille décision TCO pour 3 cas d'usage métier. Sans chiffres, pas d'argument.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| `load_qa()` (FOURNI) | Charge 20 paires de référence du dataset HomeButler | Le ground truth |
| `evaluate_strategies()` (À CODER TODO 2) | POST `/rag/evaluate` × 3 stratégies de chunking | Compare fixed / recursive / ensemble |
| `compare_modes()` (À CODER TODO 3) | POST `/chat` × 5 questions × 3 modes | Compare llm_only / rag_only / agent |
| `show_latency_summary()` (FOURNI) | mean + median par mode | Latence = critère TCO majeur |
| `show_summary()` (À CODER TODO 5) | Tableau Markdown + benchmarks RAFT 2024 | Le livrable visuel pour le comité |
| `grille_decision.md` | À COMPLÉTER manuellement (rédaction) | Recommandation argumentée par cas d'usage |

> 💡 **Branche élève** : `git checkout student/06-finetune-vs-rag`. Particularité : nécessite `ENABLE_COMPARE_ROUTES=true` pour activer `/rag/evaluate` et `/chat/compare` (désactivés par défaut en AT05).


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI un seul fichier à blanker pour AT06 ?

Le scope AT06 = **évaluation comparative + grille décision**. Tout le reste est déjà fait (AT01-05). Le seul fichier porteur du concept central = `evaluate_pipeline.py`. Le delta entre `atelier/05` et `atelier/06` côté API = 4 lignes (timeout retiré sur chat.py) — pas la peine de blanker des deltas anémiques. L'atelier vit dans `evaluate_pipeline.py` (~150 lignes, 6 TODOs documentés).

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

Tentation de l'élève : `from homebutler.rag.retriever import retrieve` puis appel direct. C'EST PIRE. En passant par HTTP, on évalue **la stack TELLE QU'ELLE TOURNERA EN PROD** : routing FastAPI, sérialisation, latence réseau locale, validation Pydantic, exceptions HTTP. C'est le mode « bout-en-bout » qui révèle les régressions que les imports directs masquent.

**Évolution à apporter** (TODO 2) :

```python
# AVANT : NotImplementedError
# APRÈS :

def evaluate_strategies(sample_size: int = 20) -> dict:
    print("\n═══ TODO 2 — POST /rag/evaluate pour 3 stratégies ═══")
    out = {}
    for strategy in ("fixed", "recursive", "ensemble"):
        # AVANTAGE : on MESURE la latence ICI, côté client — c'est ce qui
        # compte pour l'expérience utilisateur. Mesurer côté serveur biaise
        # (oublie le coût de sérialisation + transport).
        t0 = time.time()

        r = requests.post(
            f"{API}/rag/evaluate",
            json={"strategy": strategy, "sample_size": sample_size},
        )
        elapsed = time.time() - t0

        if r.status_code != 200:
            # On NE crashe pas tout le script pour une stratégie qui rate
            # (ex: index manquant pour 'ensemble'). On loggue et on continue.
            print(f"  {strategy}: HTTP {r.status_code}")
            continue

        data = r.json()
        out[strategy] = data
        # Format aligné avec les colonnes du tableau récap (Slide 5).
        # f"{x:.2f}" → 2 décimales suffisent pour des recalls (0.00–1.00).
        print(f"  {strategy:10s}  Recall@1={data['recall_at_1']:.2f}  "
              f"Recall@3={data['recall_at_3']:.2f}  Recall@5={data['recall_at_5']:.2f}  "
              f"({elapsed:.1f}s)")
    return out
```

| Stratégie | Recall@5 typique (HomeButler) | Cas d'usage |
|-----------|-------------------------------|-------------|
| fixed     | 0.65–0.75 | Documents uniformes (logs, tableaux) |
| recursive | 0.80–0.88 | Documents textuels (notices, bail) — **DEFAULT** |
| ensemble  | 0.85–0.92 | Quand on a aussi un Chroma avec métadonnées riches |

> 💡 **Piège** — si tu vois `Recall@5 < 0.4`, ce n'est PAS la stratégie de chunking. C'est probablement l'index FAISS qui n'a pas été reconstruit après changement de stratégie. Re-lance `python scripts/build_index.py --strategy=…`.


📝 Slide 4 : Concept #2 — Comparer 3 modes sur les mêmes questions

POURQUOI mesurer la latence DE CHAQUE appel (pas une moyenne globale) ?

Une moyenne globale cache la **variance**. Un mode peut être rapide en moyenne mais avec un p99 (99e percentile) catastrophique — c'est ce qui bloque en prod. Garder le détail par appel permet de calculer mean + median + p95 + p99.

**Évolution à apporter** (TODO 3) :

```python
# AVANT : NotImplementedError
# APRÈS :

def compare_modes(questions: list[str]) -> dict:
    print("\n═══ TODO 3 — Comparaison 3 modes (llm_only / rag_only / agent) ═══")
    results = {"llm_only": [], "rag_only": [], "agent": []}
    latencies = {"llm_only": [], "rag_only": [], "agent": []}

    # DOUBLE BOUCLE intentionnelle :
    #   outer = questions (5 questions étalons)
    #   inner = modes (3 modes par question)
    # AVANTAGE : on évalue CHAQUE question dans CHAQUE mode → on peut afficher
    # un tableau "question x mode" pour le rapport (vu le formateur).
    for q in questions:
        for mode in ("llm_only", "rag_only", "agent"):
            t0 = time.time()
            r = requests.post(
                f"{API}/chat",
                json={"message": q, "mode": mode},
                timeout=60,
                #  ↑ 60 s = larges marges. L'agent ReAct peut prendre 30 s
                #    avec 5-8 itérations + appels LLM. llm_only ≈ 2 s.
            )
            elapsed = time.time() - t0
            latencies[mode].append(elapsed)

            if r.status_code == 200:
                results[mode].append(r.json().get("response", ""))
                print(f"  [{mode:10s}] {q[:50]:50s}  → {elapsed:.1f}s")
            else:
                # On enregistre l'échec mais on ne crashe pas — utile pour
                # voir si un mode est instable (rate limit, timeout, etc.).
                results[mode].append(f"HTTP {r.status_code}")

    return {"answers": results, "latencies": latencies}
```

| Mode      | Latence moyenne (s) | Tokens / réponse | Faithfulness |
|-----------|--------------------|--------------------|-------------|
| llm_only  | 1-2                | ~150 (court)        | 0.20 (hallucine) |
| rag_only  | 3-5                | ~300                | 0.85+ (factuel) |
| agent     | 8-15               | ~500 (avec ReAct)   | 0.80+ (multi-source) |


📝 Slide 5 : Concept #3 — Tableau récapitulatif Markdown + benchmarks RAFT

POURQUOI produire du Markdown affiché en console ?

L'élève peut copier-coller la sortie console DIRECTEMENT dans son rapport Markdown (PR description, notion, slack). Pas besoin d'écrire un parser séparé. Et l'alignement par `f"{x:<12}"` donne un tableau lisible même en monospace.

**Évolution à apporter** (TODO 5) :

```python
# AVANT : NotImplementedError
# APRÈS :

def show_summary(strategies_eval: dict, latencies: dict) -> None:
    print("\n═══ TODO 5 — Tableau récapitulatif ═══")

    # AVANTAGE : les f-strings avec alignement ({x:<12} = padding gauche 12 chars)
    # produisent du texte qui RESSEMBLE à un tableau Markdown — collable direct.
    print(f"{'Stratégie':<12} {'R@1':>6} {'R@3':>6} {'R@5':>6}")
    for strategy, data in strategies_eval.items():
        print(f"{strategy:<12} {data['recall_at_1']:>6.2f} "
              f"{data['recall_at_3']:>6.2f} {data['recall_at_5']:>6.2f}")

    # On affiche les benchmarks de l'article RAFT (Zhang et al. 2024, arxiv:2403.10131)
    # comme RÉFÉRENCE. Si nos chiffres sont LOIN de ces benchmarks, c'est un signal.
    print("\nÀ COMPARER aux benchmarks Slide 7 Chapitre 6 (RAFT Zhang et al. 2024) :")
    print("  RAG ensemble    : Recall@5 attendu ~ 0.87")
    print("  RAG fixed-size  : Recall@5 attendu ~ 0.72")
    print("  LLM seul        : Recall@5 ≈ 0.15 (pas de retrieval, invente)")
    print("  Hybride (RAFT)  : 94 % QA factuel, 95 % style, 96 % médical")
```

**Sortie attendue** (à copier dans le rapport) :
```
Stratégie       R@1    R@3    R@5
fixed          0.55   0.68   0.72
recursive      0.65   0.80   0.85
ensemble       0.72   0.85   0.87

À COMPARER aux benchmarks RAFT 2024 :
  RAG ensemble    : Recall@5 attendu ~ 0.87  ← on EST À LA CIBLE ✓
  RAG fixed-size  : Recall@5 attendu ~ 0.72  ← OK
  ...
```


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

> 💡 **Critère formateur** : la grille doit citer des CHIFFRES mesurés par l'élève (pas juste des opinions). « 3 s » ≠ « rapide ».


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

> 💡 **Livrable final formation** : `evaluate_pipeline.py` exécuté + `grille_decision.md` complété + slides de présentation au comité. Tu sors avec un argumentaire CHIFFRÉ pour défendre une architecture RAG/FT/Hybride sur n'importe quel cas d'usage.
