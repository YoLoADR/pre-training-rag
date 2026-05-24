# Insights — Guides élèves ateliers RAG

Insights accumulés au fil de la conception du plan v2 et de son exécution. À enrichir à chaque session.

---

## 2026-05-23 — Conception plan v1 puis audit critique → v2

### Insight 1 — Le vrai problème n'est pas pédagogique, il est outillé

Le plan v1 listait les bons mécanismes (Double piste, Bug Hunt, Mission noire, Checkpoints) mais les laissait au niveau **déclaration**. L'audit a montré qu'**aucun mécanisme n'était vérifiable** dans v1 :
- Le prompt-guard était "mentionné mais pas spécifié" — donc skippable
- Le Bug Hunt était un fichier `buggy_v1.py` à diff trivialement avec `solution.py`
- Le checkpoint "à voix haute" supposait un formateur disponible
- Le setup matériel n'était pas outillé

**Leçon** : un mécanisme pédagogique non outillé = un mécanisme inexistant. v2 ajoute systématiquement le **fichier ou script qui rend le mécanisme vérifiable** (hook `UserPromptSubmit`, patches git + tests pytest, `check_atelier_ready.sh`, `checkpoint_N.py` auto-corrigé).

### Insight 2 — Le calibrage additif est un piège classique

v1 disait "2h Core + 45min Sprint + 1h Bonus = additif". Mais Sprint était présenté comme "version condensée pour les lents" — donc Sprint et Core sont **mutuellement exclusifs**, pas additifs. Total réel : 3h45+, qui dépasse la demi-journée.

**Leçon** : v2 explicite les **rails parallèles** : 20min Setup → 1h40 Core → fork (30min Sprint **XOR** 60min Bonus) → 10min Wrap. Total 3h30 dur. Sprint = chemin alternatif si score Core < 60%, Bonus = chemin alternatif si score ≥ 80%.

### Insight 3 — Le repo a déjà beaucoup de matière exploitable

L'audit du Plan agent + Explore agent a révélé que le repo contient déjà :
- `evaluate_rag.py` avec LLM-judges faithfulness + answer relevance (At.02) — réutilisable directement pour la section 📊 Mesure-toi
- `gradio_demo.py` UI (At.03) — Bonus tout fait
- `prepare_dataset.py` + `explore_dataset.py` (At.04) — manips Core
- `evaluate_pipeline.py` + `grille_decision.md` (At.06) — livrable Core
- `checklist.md` + `test_securite.sh` (At.05) — vérification finale

**Leçon** : v1 proposait de réinventer ce qui existe déjà. v2 ajoute un tableau §5 d'articulation explicite : ce qui est réutilisé, ce qui est référencé, ce qui est renommé (`README.md` → `README-formateur.md`), ce qui est déplacé (`solution.py` → branche `solution/at0X`).

### Insight 4 — Le scope leak At.05/06 est un vrai bug, pas un détail

Le `tps.md` ligne 676 signale que les routes `/rag/evaluate`, `/chat/compare`, `/rag/compare-strategies` apparaissent dans Swagger At.05 alors qu'elles sont scope At.06. Le commit récent `feedb98 fix(verify): vérifier les fichiers trackés par git` montre que `verify_branch_scope.sh` a déjà été contourné une fois.

**Décision tranchée v2** : feature flag `ENABLE_COMPARE_ROUTES` dans `api/main.py`, default `false`. Activé seulement via `.env` de l'atelier 06. C'est l'unique façon de garantir que l'élève At.05 ne voie pas ces routes dans Swagger.

### Insight 5 — Sources pédagogiques valident l'approche, mais 2 sont préprints/produits

L'agent bibliographique a trouvé 12 sources solides (Freeman PNAS 2014, Kapur 2008, Bjork 2011, Sweller 1994, Mazur 1997, Kosmyna MIT 2025, Lee Microsoft CHI 2025, Prather ICER 2024, RAGAS, RAFT, Anthropic Cookbook…). Tableau de mapping plan→sources dans §2.

**Attention** :
- Kosmyna 2025 (MIT — Your Brain on ChatGPT) est un **préprint arXiv**, pas peer-reviewed. À présenter comme "résultat préliminaire fort", pas comme acquis.
- Le Wagon Kitt et Recurse Self-Directives sont des sources **produit/industrie**, pas académiques. À utiliser comme illustrations.

### Insight 6 — Le public non-tech est sous-estimé dans `tps.md`

Le formateur (utilisateur) a explicitement signalé que le chapitre Fine-tuning (At.04) est inaccessible aux non-techs : GPU, VRAM, lr, grid search, HF Hub, W&B, QLoRA quantization sont jetés sans définition. Les analogies présentes (cuisinier, prises électriques) fonctionnent mais sont noyées.

**Décision v2** :
- Mini-lexique jargon→analogie obligatoire en tête du Carnet de bord At.04 (16 termes tabulés)
- Règle généralisée transversalement (§3) : tous les ateliers doivent avoir leur mini-lexique
- Les "🐛 erreurs communes" doivent être **reformulées en langage non-tech** (ex: "j'ai mis un learning rate trop grand → le modèle explose" au lieu de "lr=1e-2 → NaN")
- Quiz `check_1.py` vérifie 3 termes au hasard du lexique avec ses propres mots

### Insight 7 — Atelier 01 et 04 sont structurellement trop courts si on s'en tient au scope v1

Ateliers à risque de **sous-occupation** (45 min réels au lieu de 2h) :
- At.01 : 5 questions à un LLM + observer → manque top_p, seed, system prompt, few-shot pour atteindre 2h
- At.04 : si on retire le training Colab, il reste `prepare_dataset.py` + EDA = 45 min

**Décision v2** :
- At.01 : scope étendu (top_p, seed, system vs user prompt, few-shot prompting)
- At.04 : training Colab **inclus** dans le Core (renvoi à notebook `notebooks/at04_finetuning_lora.ipynb` à créer si absent), pas en Bonus

Ateliers à risque de **débordement** :
- At.03 : ReAct + Ensemble + 3 tools + mémoire → vraiment dense, **4h réels probable**. Le Sprint et le Bonus doivent être strictement séparés pour ne pas dépasser 3h30.
- At.05 : setup Langfuse (compte cloud + 2 clés) = 15-20 min cachés. À pré-traiter au Pré-vol.

### Insight 8 — L'illusion de compétence est documentée, c'est un vrai phénomène

Prather et al. ICER 2024 ("The Widening Gap"), Lee Microsoft CHI 2025 et Coutinho ICER 2025 confirment empiriquement que les vibe-codeurs novices voient leurs difficultés métacognitives **amplifiées** par l'IA, pas réduites. C'est pile le profil de l'élève qui pose problème dans cette formation.

**Conséquence design** : les Checkpoints doivent être **bloqueurs** (pass/fail binaire à la Specifications Grading — Nilson 2015), pas optionnels. Le score Core final décide automatiquement de Sprint vs Bonus — pas de choix élève qui retomberait dans le piège "je vais quand même tenter le Bonus alors que je n'ai pas compris le Core".

---

## 2026-05-23 — Exécution plan v2 : Phase 0 + Agents parallèles

### Insight 9 — feature flag mieux dans les routers que dans main.py

Le flag `ENABLE_COMPARE_ROUTES` a été implémenté dans `api/routers/rag.py` et `api/routers/chat.py` (pas dans `main.py` comme prévu initialement). Raison : FastAPI ne permet pas de surcharger une route déjà enregistrée via `include_router`. L'approche module-level variable (`_ENABLE_COMPARE = os.getenv(...)`) + `include_in_schema=_ENABLE_COMPARE` sur le décorateur + guard dans le handler est plus propre et vérifiable.

### Insight 10 — Langfuse pinné à 2.57.1 dans requirements_atelier05.txt (safe)

Le fichier existant pinnait déjà `langfuse==2.57.1` (v2.x). Les breaking changes v4 (mars 2026) ne posent donc pas de problème pour les stagiaires qui suivent les requirements. Le risque est seulement si quelqu'un fait `pip install langfuse --upgrade` pendant l'atelier. Avertissement ajouté dans le GUIDE-ELEVE.md At.05 et dans atelier-00-prevol.

### Insight 11 — ChromaDB telemetry : variable d'env suffisante

Le workaround communautaire le plus fiable est la variable d'env `ANONYMIZED_TELEMETRY=false` (pas le paramètre Python `Settings(anonymized_telemetry=False)` qui ne propage pas via `Chroma.from_documents()`). Ajouté dans `.env.example` et dans le guide At.03 Pré-vol.

### Insight 12 — Rate limits Anthropic : risque réel sur At.03 (ReAct)

Tier 1 Anthropic = 50 RPM pour claude-sonnet. At.03 ReAct = 5-10 appels/question. Sur 10 stagiaires simultanés = jusqu'à 900 req/min théorique → nettement au-dessus de la limite. Solution : clé API par stagiaire (ou groupe 2-3), et LLM_PROVIDER=ollama comme fallback. Ajouté dans les avertissements At.03 et dans atelier-00-prevol.

### Insight 13 — FAISS ARM64 OK depuis faiss-cpu 1.13.2 (déc 2025)

Wheels natives ARM64 disponibles. Incompatibilité cross-architecture si index partagé entre machines x86/ARM. Note dans atelier-00-prevol.

### Insight 14 — fastembed embedding divergence (bug #368) silencieux

fastembed et sentence-transformers donnent des embeddings différents pour paraphrase-multilingual-MiniLM-L12-v2 (~cosine 0.609). Pas un crash, mais une dégradation silencieuse de qualité si on mélange les deux backends. La formation reste cohérente sur un seul backend (fastembed via langchain_community). Avertissement dans atelier-00-prevol.

### Décisions prises
- feature flag: routers (pas main.py)
- Langfuse: warning "ne pas upgrader" dans guides At.05 + At.00
- ChromaDB: `ANONYMIZED_TELEMETRY=false` dans .env.example + guide At.03
- Rate limits: avertissement At.03 + Ollama comme fallback

### Questions levées
- Faut-il créer solution.py pour At.04 (pas encore de solution dans le repo) ? À trancher avec le formateur.
- Le pre-vol At.00 est-il obligatoire ou recommandé ? Impact sur At.01 (30 min de setup perdues si non fait).

---

## Pistes / questions ouvertes à explorer plus tard

- **Coût Anthropic** : pas chiffré dans v1. À mesurer en pilote At.03 (le pire cas, ReAct = 10-30 calls × 3 essais × 10 stagiaires). Si > 5€/stagiaire, switcher At.03 vers Claude Haiku ou Ollama local.
- **Compatibilité Cursor vs Claude Code** : le hook `UserPromptSubmit` est spécifique Claude Code. Pour Cursor, le `.cursorrules` n'a pas de mécanisme d'interception équivalent. Risque : un vibe-codeur Cursor contourne plus facilement que celui sur Claude Code. À investiguer.
- **Auto-évaluation LLM-judge** : si l'élève juge son agent par son agent, la rubric doit être très stricte (sinon l'agent valide tout). Tester sur At.02 pilote.
- **Pré-vol obligatoire vs optionnel** : si Pré-vol non fait la veille, At.01 prend 1h de setup au lieu de 20 min. Bloquer ? Recommander ? À trancher avec le formateur.
- **Langue du dataset At.04** : 150 paires Q/R en FR. Mais risque de catastrophic forgetting sur l'anglais. Le `tps.md` recommande 20-30% de données générales mais ce n'est pas mis en pratique. Worth-it d'ajouter au Core ou en Bonus ?

---

## Format pour les prochaines mises à jour

À chaque session de travail sur ce projet, ajouter :

```
## YYYY-MM-DD — [Titre court de la session]

### Insight N — [titre]
[Texte]

### Décisions prises
- [...]

### Questions levées
- [...]
```
