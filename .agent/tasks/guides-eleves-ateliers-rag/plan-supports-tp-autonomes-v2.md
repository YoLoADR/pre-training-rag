# Plan v2 — Supports TP autonomes & ludiques pour les 6 ateliers RAG HomeButler

> Cette v2 corrige les trous identifiés par l'audit (calibrage additif, prompt-guard non spécifié, Bug Hunt anti-cheat manquant, scope leak At.05/06, fichiers existants ignorés, auto-évaluation absente). Elle intègre par ailleurs (a) un tableau de variables/métriques manipulables par atelier et (b) une bibliographie pédagogique validant l'approche.

---

## 1. Context

**Problème** : la formation RAG HomeButler (6 ateliers, 1 par demi-journée, public = employés d'entreprise) a besoin de supports élèves qui :

1. **Calibrent la demi-journée (~3h30 effectifs)** — les précédents guides étaient soit trop courts (élèves désœuvrés), soit trop denses (élèves perdus).
2. **Évitent le "tuto qu'on suit en pilote auto"** — actuel `examples-supports/GUIDE-ELEVE.md` (Claude Code 1.1) est un step-by-step linéaire : trop directif pour des employés qui doivent acquérir un vrai réflexe.
3. **Gèrent les 2 profils** : l'élève "blank" qui code tout à la main vs l'élève "vibe-coding" qui délègue à Cursor/Claude Code. Aujourd'hui, le second tape `/init` puis `implémente l'atelier 02` et se retrouve avec une solution sans avoir rien appris (cf. Prather 2024, Lee/Microsoft 2025 sur l'**illusion de compétence** induite par GenAI chez les apprenants).
4. **Restent dans le scope de l'atelier en cours** — le vibe-codeur qui demande à Claude "fais-moi tout l'atelier 02" risque de récupérer du code agent ReAct (atelier 03) ou du fine-tuning (atelier 04). Le commit récent `feedb98 fix(verify): vérifier les fichiers trackés par git` montre qu'il y a déjà eu un problème de scope qui leakait via `scripts/verify_branch_scope.sh`.
5. **Permettent d'observer / mesurer / comparer** des alternatives techniques avec des métriques chiffrées (recall@k, latence, perplexité, hallucination rate, etc.) — sans déborder.

**Outcome visé** : 6 fichiers `GUIDE-ELEVE.md`, un par dossier `ateliers/atelier-0X-*/`, autonomes, ludiques, calibrés 3h30, qui font apprendre les 2 profils via les **mêmes missions** mais avec une **liberté assumée sur la façon de les réaliser** — chaque atelier débouchant sur un **mini-benchmark mesurable** que le stagiaire peut défendre.

---

## 2. Fondements pédagogiques (synthèse pour formateur)

L'approche n'est pas inventée : elle s'appuie sur des cadres validés. Tableau condensé (sources complètes en Annexe A).

| Choix du plan | Fondement | Source clé |
|---|---|---|
| Refus du tuto linéaire | Active learning → +0,47 SD perf STEM | Freeman et al. 2014 PNAS |
| Mission noire (concevoir avant code) | Productive failure | Kapur 2008/2014 |
| Bug Hunt placé au milieu | Desirable difficulties + interleaving | Bjork & Bjork 2011 |
| Core/Sprint/Bonus + scope strict | Cognitive load theory (extraneous load) | Sweller 1994/2019 |
| Indices Build / Garde-fou Vibe | Scaffolding (ZPD Vygotsky) | van de Pol 2010 |
| Double piste Build/Vibe assumée | Differentiated instruction (content/process/product) | Tomlinson 2017 |
| Checkpoints "explique à voix haute" | Peer Instruction | Mazur 1997, Crouch & Mazur 2001 |
| Critères auto-vérifiables binaires | Specifications grading + Test-driven learning | Nilson 2015, Janzen & Saiedian 2006 |
| Mission noire = "brief client" | Challenge-Based Learning (Engage→Investigate→Act) | Apple CBL 2008, Gallagher & Savage 2023 |
| Justification anti-vibe-coding | Cognitive offloading / dette cognitive | Kosmyna MIT 2025, Lee Microsoft CHI 2025, Gerlich 2025 |
| Métriques RAG (Recall@k, faithfulness…) | RAG Triad / RAGAS / RAFT | DeepLearning.AI Advanced RAG, RAGAS 2024, Zhang 2024 |

Ces références alimentent (a) l'argumentaire à donner aux stagiaires en intro pour qu'ils acceptent les contraintes, (b) la justification interne du formateur sur le pourquoi de chaque mécanisme.

---

## 3. Approche pédagogique — 4 mécanismes + outillage

> **Règle transversale — vulgarisation systématique** : public = employés d'entreprise, pas data scientists. Tout terme jargon (GPU, VRAM, recall, embedding, MMR, ReAct, p95, CORS, slowapi, SSE, etc.) **doit être** défini dans le Carnet de bord avec : (1) une phrase courte non-jargonneuse, (2) une analogie quotidienne. Voir le tableau exemplaire dans §8 atelier 04 — à reproduire pour les autres ateliers en s'appuyant sur les analogies déjà présentes dans `tps.md` (cuisine, GPS, dictionnaire papier, etc.) mais en les complétant systématiquement avec un mini-lexique en tête de chaque Carnet de bord.



### Mécanisme 1 — Double piste Build / Vibe **assumée et vérifiable**

Au début de chaque atelier, l'élève **déclare sa piste** :

- 🛠️ **Piste Build** — code à la main. Claude Code/Cursor en mode `plan` ou fermé. Le guide donne API/imports clés, **jamais le code complet**.
- 🎮 **Piste Vibe** — délégation OK, mais validation d'une étape conditionnée à : (a) expliquer la décision en 3 phrases, (b) modifier 1 paramètre clé et **prédire** l'impact, (c) débugger un bug intentionnel (Bug Hunt).

**Outillage du prompt-guard (manquant dans v1)** :

- Chaque atelier livre un fichier `ateliers/atelier-0X-*/.claude/CLAUDE.md` qui override le `CLAUDE.md` racine et liste les contraintes scope (concepts autorisés / interdits / mots-clés bloqués).
- Un fichier `ateliers/atelier-0X-*/.cursorrules` pour les utilisateurs Cursor (équivalent).
- Un hook `UserPromptSubmit` dans `ateliers/atelier-0X-*/.claude/settings.json` qui matche les mots-clés hors-scope (ex. atelier 02 : "agent", "react", "tool calling", "fine-tun", "lora") et injecte un rappel **inviolable** : *"Cet atelier est limité au scope X/Y/Z. Question hors-scope détectée → réponds : 'On verra ça dans l'atelier N, concentre-toi sur Y'."*. C'est **vérifiable** (le fichier doit exister, `verify_branch_scope.sh` peut être étendu pour le confirmer), pas optionnel.

### Mécanisme 2 — Bug Hunt **anti-cheat**

Section `🐛 Casse-moi ça` au milieu de chaque atelier. **Refonte par rapport à v1** (qui était skipable trivialement) :

- **Pas de fichier `buggy_v1.py` en clair** : les bugs sont livrés sous forme de **patches git** (`ateliers/atelier-0X-*/bugs/v1.patch`) à appliquer via `git apply` sur `exercice.py`. L'élève ne voit pas la diff sans l'appliquer.
- **Test fourni qui doit passer après réparation** : chaque bug a un `bugs/test_v1.py` (pytest) exécutable. Le bug est qualifié réparé quand le test passe.
- **`solution.py` déplacé sur une branche `solution/at0X`** non checkoutée par défaut. Le vibe-codeur ne peut pas `cat solution.py` pour comparer.
- **Comportement observable plutôt que ligne fautive** : par ex. atelier 02 → "`pytest bugs/test_recall.py` retourne `assert recall_at_5 >= 0.7 → 0.31`". L'élève doit instrumenter, inspecter, raisonner ; pas juste lire un diff.
- **Grille d'explication QCM auto-corrigeable** (`bugs/v1_explanation.md` avec 3-5 affirmations vrai/faux) : force la verbalisation de la cause-racine après le fix.

Source des bugs : tirée directement des blocs **"🐛 Erreurs communes des devs"** déjà recensés dans `ateliers/tps.md` pour chaque atelier (entre 6 et 10 erreurs déjà rédigées par atelier).

### Mécanisme 3 — Mission noire (briefing client)

Chaque atelier cadré comme un brief client HomeButler. Format imposé :

```
🎯 Mission
Le PM HomeButler te demande : "[besoin formulé en langage métier, pas en jargon ML]"
Livrable attendu : [output démontrable, ex. "une démo CLI qui répond à 5 questions avec sources citées"]
Critères de succès auto-vérifiables : [ex. "Recall@5 ≥ 0.80", "réponse < 5s p95", "0 hallucination sur questions privées"]
Tu as 2h.
```

Le code n'est pas donné. Le guide fournit un **Carnet de bord** (concepts à mobiliser, API à connaître, pièges) mais pas la suite d'étapes prête à copier.

Format inspiré du **Challenge-Based Learning** d'Apple (Engage → Investigate → Act).

### Mécanisme 4 — Checkpoints **auto-évaluables sans formateur**

À chaque palier (3 par atelier en moyenne), un encadré `✋ Checkpoint`. **Refonte par rapport à v1** (qui supposait un formateur disponible) :

3 dispositifs combinés, l'élève choisit selon le contexte :

- **(a) Mini-quiz écrit auto-corrigé** : script `ateliers/atelier-0X/checkpoints/check_N.py` qui pose 3 QCM/QROC et corrige (mots-clés attendus). Format inspiré de **Specifications grading** (Nilson 2015) : pass/fail binaire.
- **(b) LLM-judge avec rubric explicite** : un prompt-template à coller dans Claude : *"Voici mon explication de [concept]. Évalue selon les 3 critères X/Y/Z, sois sévère et liste ce qui manque"*. L'élève fait juger son agent par son agent.
- **(c) Démo visible** (si formateur ou pair disponible) : "tu dois pouvoir montrer le résultat à ton voisin et expliquer 1 paramètre". Format **Peer Instruction** de Mazur.
- **(d) Pour aller plus loin** : un **quiz oral chronométré 5 min** en fin d'atelier (10 questions). Si <60%, on suggère le Sprint plutôt que le Bonus pour la suite.

**Sans validation du checkpoint → on ne passe pas à l'étape suivante.** Explicite dans le guide.

### Calibrage Core / Sprint / Bonus — **rails parallèles, pas additifs** (correction v1)

| Phase | Durée | Statut |
|---|---|---|
| **🚦 Setup** | 20 min | Obligatoire — script `check_atelier_ready.sh N` |
| **🎯 Tronc commun (Core)** | 1h40 | Obligatoire — Mission + manips clés + Bug Hunt + checkpoints |
| **Fork au checkpoint final du Core** | — | l'élève choisit selon son score |
| ⚡ **Sprint** (chemin alternatif si en retard / score <60%) | 30 min | Version condensée des dernières étapes |
| 🏆 **Bonus** (si score ≥80% et avance) | 60-70 min | Défis avancés **dans le scope** |
| **🎓 Wrap-up** | 10 min | Mini-quiz final 5-10 questions |

**Total max : 3h30.** Sprint et Bonus sont **mutuellement exclusifs**. Ce point manquait dans v1 qui suggérait Core + Sprint + Bonus = 3h45.

---

## 4. Garde-fou scope strict — **outillé**

Règle absolue : la section Bonus ne doit JAMAIS introduire un concept réservé à un atelier ultérieur.

| Atelier | Scope **autorisé** (explicité) | **Interdit** (atelier suivant) |
|---|---|---|
| 01 LLM Baseline | LLM, prompt, **temperature, top_p, seed, system vs user prompt, few-shot, max_tokens**, knowledge cutoff, modèle/provider | RAG, embeddings, agents, FT |
| 02 RAG Simple FAISS | Chunking (fixed/recursive/semantic), embeddings, FAISS, similarity vs MMR, k, fetch_k, **metadata sur chunks**, recall@k, **faithfulness/answer relevance** | EnsembleRetriever, Chroma, agents, FT |
| 03 Pipeline Agent | EnsembleRetriever (FAISS+Chroma), poids, ReAct, tools, mémoire conversationnelle, max_iterations | FT, déploiement API, Streamlit, RAFT |
| 04 Fine-tuning | LoRA/QLoRA, dataset Alpaca, split 80/10/10, perplexité, lr, r, epochs, overfitting, catastrophic forgetting | API FastAPI, Streamlit, RAFT, comparatif |
| 05 Déploiement | FastAPI, Streamlit, prompt injection (regex), rate limit, Langfuse, CORS, auth API key, streaming SSE | RAFT, eval comparative (= At.06) |
| 06 FT vs RAG | RAFT (théorique), eval comparative llm_only/rag_only/agent, TCO break-even | — (atelier final) |

**Concepts ajoutés vs v1** (en gras) : combler les trous identifiés par l'audit (At.01 top_p/seed/few-shot, At.02 metadata, etc.) — pour atteindre les 2h réelles.

**Implémentation outillée du garde-fou** :

| Mécanisme | Fichier | Effet |
|---|---|---|
| `CLAUDE.md` local atelier | `ateliers/atelier-0X-*/.claude/CLAUDE.md` | Override le racine ; liste concepts autorisés/interdits |
| `.cursorrules` local atelier | `ateliers/atelier-0X-*/.cursorrules` | Idem pour Cursor |
| Hook `UserPromptSubmit` | `ateliers/atelier-0X-*/.claude/settings.json` | Détecte mots-clés hors-scope → injection système |
| `scripts/verify_branch_scope.sh` (existant, à étendre) | racine | Vérif scope code après commit (déjà OK) + vérif fichiers `.claude/` présents (à ajouter) |

**Décision sur le scope leak At.05 / At.06** (en suspens dans v1) : **option retenue = feature flag**. Ajouter dans `api/main.py` un check `os.getenv("ENABLE_COMPARE_ROUTES") == "true"` pour les routes `/rag/evaluate`, `/chat/compare`, `/rag/compare-strategies`. Atelier 05 part avec `ENABLE_COMPARE_ROUTES=false` (les routes n'apparaissent pas dans Swagger). Atelier 06 active la variable dans son `.env`. Une PR séparée commitée *avant* la rédaction des guides.

---

## 5. Cohabitation avec les fichiers existants

L'audit a montré que le repo contient **déjà** des supports partiellement redondants avec ce qu'on veut produire :

| Fichier existant | Statut | Décision |
|---|---|---|
| `ateliers/atelier-0X-*/README.md` | actuel = mix instructions élève + contexte formateur | **Renommer en `README-formateur.md`** ; le `GUIDE-ELEVE.md` devient l'**unique point d'entrée élève** |
| `ateliers/atelier-0X-*/exercice.py` | squelette à compléter | **Référencé** par le guide ("ouvre `exercice.py` et complète la fonction `chunk_with_strategy`"), pas dupliqué |
| `ateliers/atelier-0X-*/solution.py` | solution complète | **Déplacée sur branche `solution/at0X`** pour éviter le `cat solution.py` du vibe-codeur. Récupérable post-checkpoint final. |
| `ateliers/atelier-02-*/evaluate_rag.py` | LLM-judge faithfulness/answer-relevance déjà codé | **Réutilisé** comme outil de mesure dans la section "📊 Mesure-toi" du guide At.02 |
| `ateliers/atelier-03-*/gradio_demo.py` | UI Gradio | **Démo Bonus** (déjà fournie, on n'y touche pas) |
| `ateliers/atelier-04-*/prepare_dataset.py` + `explore_dataset.py` | génération + EDA | **Réutilisés** comme manips Core At.04 |
| `ateliers/atelier-05-*/checklist.md` + `test_securite.sh` | sécurité | **Intégrés** dans la "Vérification finale" At.05 (référencés, pas réécrits) |
| `ateliers/atelier-06-*/evaluate_pipeline.py` + `grille_decision.md` | benchmark + grille | **Réutilisés** comme livrables Core/Bonus At.06 |
| `homebutler/` (package : `llm/`, `rag/`, `agent/`, etc.) | modules importés par les solutions | **Boîte à outils** — l'élève l'importe (sans la modifier) ; les `GUIDE-ELEVE.md` documentent les fonctions clés à utiliser |
| `notebooks/` | présumé Colab FT At.04 | À **vérifier** l'existence ; sinon créer un colab `notebooks/at04_finetuning_lora.ipynb` minimaliste |
| `api/main.py`, `api/routers/`, `api/limiter.py` | API FastAPI | **Inchangé**, sauf feature-flag scope leak (cf. §4) |
| `ui/` | Streamlit | À **inspecter**, possiblement déjà fonctionnel |
| `scripts/check_atelier_ready.sh` | **à créer** | Vérif setup (cf. §6) |
| `examples-supports/GUIDE-ELEVE.md` | Anti-modèle pédagogique (tuto linéaire) ET source de conventions visuelles | **On garde les encadrés `> 🔧 Manipulation`, les tableaux, la check-list de fin, les "Pièges à connaître". On casse le step-by-step linéaire.** Mention explicite en intro du gabarit : "Ce guide diffère de l'ancien : pas de notice à suivre — une mission à accomplir." |
| `examples-supports/reflexion-challenge.md` | format défis ouverts (POURQUOI/Contexte/Question/Pistes) | **Gabarit obligatoire** pour chaque défi Bonus de chaque atelier |
| `ateliers/tps.md` | transcription session formateur (1015 lignes) | **Reste source de vérité formateur**. Les blocs "🧠 Vulgarisation", "🐛 Erreurs communes", "🔗 Pont projet", "✅ Critères de succès" y sont déjà rédigés → recyclés tels quels dans les `GUIDE-ELEVE.md` |

---

## 6. Atelier 00 — "Pré-vol" (30-60 min, à faire la veille)

**Section ajoutée vs v1** pour éviter que chaque atelier perde 30 min en setup.

Livrable : un seul fichier `ateliers/atelier-00-prevol/GUIDE-ELEVE.md` + un script `scripts/check_atelier_ready.sh`. Couvre :

- Clone repo, création `.venv` (un par atelier comme déjà documenté dans `README.md` racine)
- Vérif `claude --version` / `cursor --version`
- Pré-téléchargement des modèles lourds :
  - At.02 : `paraphrase-multilingual-MiniLM-L12-v2` (~120 MB) via un `python -c "from fastembed import …"` qui force le download
  - At.04 : tokenizer Mistral / Colab account vérifié
- Génération des données : `python scripts/generate_documents.py`, `generate_energy_data.py`, `generate_producers.py`
- Pré-construction des index : `python -c "from homebutler.rag... build_faiss_index"`
- Vérif clés API : `ANTHROPIC_API_KEY` OU Ollama tourne (`ollama list`)
- Vérif clé Langfuse (At.05) ou consigne pour s'en créer une (gratuit) : https://cloud.langfuse.com
- Vérif Colab access (At.04)
- Liste des ports utilisés (8000 FastAPI, 8501 Streamlit, 3300 Langfuse local) — détection de conflit

Script `scripts/check_atelier_ready.sh N` : vérifie (a) venv activé, (b) deps installées, (c) clés API valides, (d) PDFs présents, (e) index présent ou reconstructible, (f) ports libres. Renvoie code 0 si prêt, 1 sinon avec message clair.

---

## 7. Structure type d'un `GUIDE-ELEVE.md` atelier (gabarit)

```markdown
# Atelier 0X — [Titre] (demi-journée, ~3h30)

> **Comment ce guide diffère de l'ancien GUIDE-ELEVE.md** : ici tu ne suis pas un step-by-step.
> Tu reçois une mission, des contraintes, des indices ; tu construis. Si tu cherches le tuto,
> ouvre `homebutler/` et lis les modules — mais alors tu n'apprends pas.

## 🚦 Pré-vol (avant de commencer)
- [ ] `bash scripts/check_atelier_ready.sh 0X` retourne OK
- [ ] J'ai lu la section "Périmètre" ci-dessous

## 🎯 La mission
[Brief PM HomeButler en 5 lignes — pas de tech]
**Livrable** : [démo démontrable]
**Critères de succès auto-vérifiables** : [métriques chiffrées]
**Budget temps** : 2h Core (+30 min Sprint OU 60 min Bonus)

## 🚧 Périmètre de cet atelier
- ✅ Dans le scope : [liste explicite des concepts]
- ❌ Hors scope (ateliers suivants) : [liste explicite]
- 🛡️ Garde-fou activé : `.claude/CLAUDE.md` local + hook UserPromptSubmit
  (si tu utilises Claude/Cursor : ne désactive pas ces fichiers)

## 🛠️ vs 🎮 — Choisis ta piste
[Tableau Blank vs Vibe + règles + prompt-guard ref]

## 🧠 Carnet de bord (concepts à mobiliser)
[Vulgarisation 1-paragraphe par concept — recyclé tel quel depuis tps.md]

## 🎯 TRONC COMMUN (1h40)

### Étape 1 — [Action] (25 min)
**Objectif** : [résultat observable]
**Indices** (Build) : [API, imports, fichier à lire dans homebutler/]
**Garde-fou** (Vibe) : [contrainte à donner à ton agent + checkpoint anti-skip]

✋ **Checkpoint 1** — [QCM auto-corrigé `check_1.py` + LLM-judge rubric]

### 🔬 Mini-lab — Fais varier un paramètre (15 min)
[1 variable manipulable + plage + mesure attendue — issu du tableau §9]

### Étape 2 — [Action] (30 min)
...

### 🐛 Casse-moi ça — Bug Hunt (20 min)
```bash
git apply ateliers/atelier-0X-*/bugs/v1.patch
pytest ateliers/atelier-0X-*/bugs/test_v1.py  # doit échouer
# … trouve le bug, répare, re-run le test
```
[3 patches dispo : bugs/v1.patch, v2.patch, v3.patch]

### 📊 Mesure-toi (15 min)
[Métriques à calculer : Recall@5, latence p95, etc. — issu du tableau §9]
[Baseline observée vs ton score]

✋ **Checkpoint final Core** — démo + mini-quiz `check_final.py` (5 questions)
→ Score ≥ 80% : pars en Bonus 🏆
→ Score < 60% : pars en Sprint ⚡
→ Sinon : prends une pause, refais 1 checkpoint, puis Bonus

## ⚡ SPRINT (chemin alternatif, 30 min)
[Version condensée OU rattrapage du concept le plus faiblement maîtrisé]

## 🏆 BONUS (parcours alternatif, 60-70 min)
[Défis avancés au format reflexion-challenge.md : POURQUOI / Contexte / Question / Pistes]
- Défi 1 : [variation paramètres + mesure]
- Défi 2 : [optimisation d'une métrique]
- Bug Hunt avancé : [bug subtil supplémentaire]

## 🎓 Wrap-up (10 min)
- [ ] Critères de succès atteints (tirés du tps.md ✅)
- [ ] Tous les checkpoints validés
- [ ] `bash scripts/verify_branch_scope.sh` passe
- Quiz oral 10 questions chronométré 5 min (auto-évaluation)
- Ce que je retiens en 3 lignes (à écrire) → utile pour Atelier suivant

## 🔗 Pour aller plus loin (hors TP, lecture)
[Le bloc "Pont avec ton projet" déjà rédigé dans tps.md — réutilisé tel quel]
[Lectures complémentaires : 1-2 sources de l'Annexe A en lien avec l'atelier]
```

---

## 8. Contenu spécifique par atelier (synthèse + ajouts post-audit)

Pour chaque atelier, on liste : la mission, ce qui est ajouté au scope (vs v1), les 3 sections nouvelles "🔬 Mini-lab" et "📊 Mesure-toi" (extraites du rapport variables/métriques), le Bug Hunt, et le Bonus.

### Atelier 01 — LLM Baseline

- **Mission** : "Le PM se demande si un LLM seul peut servir d'assistant maison. Démontre-lui sur 5 questions privées + 5 questions générales que non — et chiffre pourquoi."
- **Scope ajouté vs v1** : top_p, seed, system vs user prompt, few-shot prompting (étoffe les 30 min creuses du v1 pour atteindre 2h).
- **Variables manipulables** : `temperature` (0.0–1.0), `max_tokens` (128–4096), `LLM_PROVIDER` (anthropic/ollama), `ANTHROPIC_MODEL` (opus/sonnet/haiku), `OLLAMA_MODEL`. Code : `homebutler/llm/provider.py`, `homebutler/llm/prompts.py`, `config.py`.
- **🔬 Mini-lab Core** : poser 10 fois la même question privée à `T=0` puis `T=0.9` ; compter variance des réponses ; comparer.
- **📊 Mesure-toi** : (a) hallucination rate sur 5 questions privées, (b) determinism rate à T=0, (c) latence Anthropic vs Ollama, (d) tokens consommés.
- **Bug Hunt** : 3 patches — (1) `T=0.9` sur question critique → réponse incohérente ; (2) `max_tokens=50` → réponse tronquée ; (3) prompt sans system → modèle off-topic.
- **Bonus** : comparer Sonnet vs Haiku sur même question (coût + latence + qualité) ; introduire few-shot (3 exemples) et mesurer baisse d'hallucination. Format `reflexion-challenge.md`.
- **Source recyclée** : `tps.md` lignes 1-13.

### Atelier 02 — RAG Simple FAISS

- **Mission** : "Indexe les PDFs HomeButler pour que l'assistant cite la bonne notice. Atteins **Recall@5 ≥ 0.80** et **faithfulness ≥ 0.85**."
- **Scope ajouté** : metadata sur chunks (`{propertyId, docType, page}`), normalisation Unicode des PDFs, judges (faithfulness, answer relevance — déjà codés dans `evaluate_rag.py`).
- **Variables manipulables** : `chunk_size` (256–2048), `chunk_overlap` (0–200), `k` (1–10), `search_type` (similarity vs MMR), `fetch_k` (k–100), stratégie chunking (fixed/recursive/semantic). Code : `homebutler/rag/ingestion.py`, `homebutler/rag/vectorstore_faiss.py`, `homebutler/rag/retriever.py`.
- **🔬 Mini-lab Core** : tester fixed-size vs recursive sur les 5 questions étalons ; tracer Recall@5 et nombre de chunks ; quelle stratégie gagne et pourquoi ?
- **📊 Mesure-toi** : Recall@1/3/5 (avec `evaluate_rag.py`), latence retrieval, contexte size (chars→tokens), faithfulness via LLM-judge, answer relevance. Baseline tps.md : Recall@5 ≈ 0.80.
- **Bug Hunt** : 3 patches — (1) `chunk_size=2000` (trop grand) → bruit ; (2) `chunk_overlap=0` → coupure phrase ; (3) reconstruction index à chaque query → lenteur observable. Tirés des 7 erreurs `tps.md` 133-147.
- **Bonus** : faire varier `chunk_size` ∈ {200, 600, 1500} ; tester MMR vs similarity sur questions à information dispersée. **Interdit Bonus** : EnsembleRetriever, Chroma (= At.03). Format `reflexion-challenge.md`.
- **Source recyclée** : `tps.md` lignes 99-170.

### Atelier 03 — Pipeline Agent ReAct

- **Mission** : "Construis un agent qui croise météo + notices maison + producteurs locaux pour préparer un dîner."
- **Scope** : EnsembleRetriever (FAISS+Chroma), poids, ReAct, 3 tools, mémoire k=6, max_iterations.
- **Variables manipulables** : `faiss_k`, `chroma_k`, `ensemble_weights` ([0.6, 0.4] vs [0.5, 0.5] vs [0.8, 0.2]), `max_iterations` (4/8/12), `temperature` agent (0.1–0.3), `memory_k` (0/6/20). Code : `homebutler/rag/retriever.py`, `homebutler/agent/react_agent.py`, `homebutler/agent/tools.py`.
- **🔬 Mini-lab Core** : comparer EnsembleRetriever 0.6/0.4 vs FAISS seul (1.0/0.0) sur question multi-source.
- **📊 Mesure-toi** : nombre d'outils orchestrés (cible ≥3), Recall@5 ensemble vs FAISS seul (cible : ensemble > FAISS), latence agent, step count, contextual correctness (test sur 2 questions enchaînées : "info chaudière" puis "que tu as dit d'abord" — l'agent doit faire l'anaphore).
- **Bug Hunt** : 3 patches — (1) description d'outil bâclée → outil ignoré ; (2) 15 tools dans la liste → confusion ; (3) ReAct sans max_iterations → boucle. Tirés `tps.md` 323-339.
- **Bonus** : ajouter 1 tool scope-safe (ex `get_indoor_temperature`) ; tester avec/sans mémoire sur dialogue 3 tours. **Interdit Bonus** : FT, Streamlit.
- **Source recyclée** : `tps.md` 343-372.

### Atelier 04 — Fine-tuning LoRA/QLoRA

- **Mission** : "Le PM veut un assistant qui parle 'Merenza' (chaleureux, FR, format strict). Prépare le dataset, explique pourquoi le FT (et pas le RAG) règle ça, et lance le training sur Colab."
- **Scope ajouté** : training réel sur Colab (renvoi à un notebook `notebooks/at04_finetuning_lora.ipynb` à créer si absent). Sans ça, At.04 fait 45 min, pas 2h.
- **Variables manipulables (Mac)** : `dataset size` (100/150/500), split ratio (80/10/10), équilibrage catégories. **(Colab)** : `learning_rate` (1e-5 à 1e-3), `r` LoRA (4/8/64), `epochs` (3/5/10), `batch_size`. Code : `prepare_dataset.py`, `explore_dataset.py`, notebook Colab.

#### 🧠 Vulgarisation **obligatoire** pour public non-tech (correction post-audit)

Le `tps.md` actuel suppose que le lecteur connaît GPU, VRAM, learning rate, Colab T4, grid search, git LFS, HF Hub, quantization. Pour des employés d'entreprise, **chaque concept doit être défini avec une analogie quotidienne** dans le Carnet de bord. Liste exhaustive des termes à vulgariser avant la première manip :

| Terme jargon | Définition courte | Analogie quotidienne |
|---|---|---|
| **GPU** (Graphics Processing Unit) | Carte dédiée aux calculs massivement parallèles. Indispensable au training de gros modèles. | Une cuisine de restaurant avec 100 cuisiniers qui font la même tâche en parallèle, vs. ta cuisine perso (CPU) avec 1 cuisinier polyvalent. |
| **RAM vs VRAM** | RAM = mémoire vive de ton ordi. VRAM = mémoire vive **de la carte graphique** (GPU). Un modèle 7B "tient" en VRAM, pas en RAM. | RAM = ton frigo (large mais lent à accéder). VRAM = ton plan de travail (petit mais ultra-rapide pour cuisiner). |
| **Colab T4 (gratuit)** | Service Google qui te prête un GPU "T4" gratuitement quelques heures par jour, dans un notebook web. | Un coworking gratuit avec une cuisine pro (GPU T4) ; tu peux y aller 4h/jour. |
| **Quantization 4-bit** | Stocker les poids du modèle sur 4 bits au lieu de 16 → 4× moins de mémoire. Coût : légère perte de précision. | Compresser une photo HD en JPG basse qualité : 4× plus léger, presque pas visible. |
| **Mistral-7B = 12 GB VRAM en QLoRA** | Le modèle Mistral à 7 milliards de paramètres, compressé, tient sur 12 GB de mémoire GPU. Le T4 a 15 GB → ça passe. | Une voiture de 7 places (Mistral-7B) qui rentre dans un garage de 12 m² grâce à un démontage astucieux (QLoRA). |
| **Learning rate (`lr`)** | "Pas d'apprentissage". À chaque exemple vu, le modèle ajuste ses poids un peu. `lr` dit de combien. Trop grand → ça part en vrille (loss = NaN). Trop petit → n'apprend rien. | Régler la vitesse d'un cuisinier qui ajuste sa recette : trop vite il rate, trop lentement il ne progresse jamais. |
| **Epoch** | 1 epoch = le modèle a vu **tout** le dataset une fois. 5 epochs = il l'a vu 5 fois. | Relire 5 fois ses fiches de révision avant un examen. |
| **Grid search** | Tester systématiquement plusieurs combinaisons de paramètres (ex: 3 `lr` × 3 `epochs` = 9 essais). | Goûter 9 versions d'une sauce avec 3 doses de sel × 3 doses de sucre pour trouver la meilleure. |
| **Loss / val_loss** | Loss = écart moyen entre la prédiction du modèle et la vraie réponse. On veut qu'il baisse. `val_loss` = pareil sur des questions jamais vues (set de validation). | Note d'un élève qui s'entraîne : `loss` = note aux exercices du cours ; `val_loss` = note au contrôle blanc. |
| **Dataset déséquilibré** | Quand certaines catégories sont sur-représentées (ex: 66 questions "autres" vs 6 "marketplace"). Le modèle apprend bien "autres" et **rate** "marketplace". | Un prof qui ne donne que des exercices de maths : son élève sera nul en français le jour de l'examen. **Fix** : (a) demander au prof d'équilibrer, (b) sur-pondérer les exercices rares ("sur-échantillonner"). |
| **Sur-échantillonner** | Dupliquer (ou créer des variantes) des exemples des catégories sous-représentées pour rééquilibrer. | Faire repasser 10 fois les exercices de français à l'élève pour compenser. |
| **Versionner le dataset** (git LFS / HF Hub) | git classique gère mal les gros fichiers binaires. **git LFS** (Large File Storage) = extension pour stocker les fichiers lourds à part. **HF Hub** = "GitHub des modèles" (HuggingFace). | Une bibliothèque qui a un dépôt spécial pour les encyclopédies (trop lourdes pour les étagères normales). |
| **W&B artifacts** | Weights & Biases = outil pro de suivi d'expériences ML. "Artifacts" = il garde une trace de chaque dataset, chaque modèle entraîné, avec leurs versions. | Un cahier de laboratoire qui photographie chaque éprouvette à chaque manip — tu peux toujours retrouver "celle du mardi 14h". |
| **HF Hub (HuggingFace Hub)** | Plateforme publique où les chercheurs publient leurs modèles. Tu peux télécharger Mistral, Llama, etc. en une ligne de code. | Steam / App Store, mais pour les modèles IA. |
| **Catastrophic forgetting** | Le modèle, en apprenant ton domaine, **oublie** ce qu'il savait avant (anglais, code…). | Un cuisinier qui apprend à fond la pâtisserie et oublie comment faire un steak. **Fix** : mélanger 20-30% d'exercices généraux dans la formation. |
| **Perplexité** | Mesure de "surprise" du modèle face à la bonne réponse. Plus c'est bas, mieux c'est. | Note d'incompréhension. Si la bonne réponse "surprend" le modèle → il l'a mal apprise. |

**Implémentation dans le guide At.04** :

- Le **Carnet de bord** s'ouvre par ce tableau (avant tout concept LoRA/QLoRA).
- Chaque section technique suivante référence le tableau : "ici on va manipuler `lr` (cf. Carnet de bord, ligne *Learning rate*)".
- Le **Mini-quiz check_1.py** vérifie que l'élève sait expliquer 3 termes au hasard du tableau avec ses propres mots.
- **Sur-échantillonnage = manip Core** (pas Bonus) : l'élève le fait sur le dataset 66/6 et observe l'effet via `explore_dataset.py`. Concept "dataset déséquilibré" → traité par la pratique, pas seulement la théorie.
- **Versionnement** : section dédiée "📦 Garde une trace" en fin d'atelier — l'élève sauvegarde son dataset modifié sur HF Hub (compte gratuit créé au Pré-vol) ; pas exigé de comprendre git LFS finement mais comprendre **pourquoi** on ne push pas un .bin de 4 GB sur GitHub direct.
- **Grid search** : présenté en Bonus uniquement (concept avancé). Dans le Core, on fait varier 1 seul paramètre à la fois pour rester lisible.
- **QLoRA/quantization** : analogies filées dans le tps.md (prises électriques, câbles fins) — à **conserver** car elles fonctionnent. Mais ajouter le tableau ci-dessus pour le lexique froid.
- Tous les **🐛 erreurs communes** de la section Bug Hunt sont **reformulés** : remplacer "`lr=1e-2` → loss NaN" par "j'ai mis un learning rate trop grand → le modèle explose et n'apprend plus rien (`loss = NaN`, voir Carnet de bord)".
- **🔬 Mini-lab Core** : explorer la distribution catégories du dataset (déjà déséquilibré 66 vs 6) ; sur-échantillonner la minorité ; recomparer.
- **📊 Mesure-toi** : (Mac) duplication rate, category imbalance ratio, longueur médiane Q/R, % paires > 512 tokens. (Colab) perplexité val, F1 test set par catégorie, ratio val_loss/train_loss (signal overfitting).
- **Bug Hunt** : 3 patches — (1) dataset 100% "autres" (zéro marketplace) → modèle ne sait rien sur marketplace ; (2) `lr=1e-2` → loss NaN au 1er epoch ; (3) absence de val set → overfit invisible. Tirés `tps.md` 525-540.
- **Bonus** : générer 50 paires supplémentaires sur la catégorie minoritaire ; lancer Colab et observer la perplexité ; comparer modèle FT vs baseline sur 5 questions style. **Interdit** : déploiement API, RAFT.
- **Source recyclée** : `tps.md` 400-414 + 544-557.

### Atelier 05 — Déploiement

- **Mission** : "Expose une API HomeButler sécurisée (prompt injection + rate limit + observabilité Langfuse) et un dashboard Streamlit pour la démo."
- **Scope ajouté** : CORS précis, auth API key, streaming SSE (en Bonus). **Scope leak résolu** : `ENABLE_COMPARE_ROUTES=false` par défaut (cf. §4).
- **Variables manipulables** : `temperature`, `max_tokens` par mode, rate limit (10/30/60 req/min/IP), nombre de patterns regex prompt injection, CORS origins. Code : `api/main.py`, `api/routers/chat.py`, `api/limiter.py`, `config.py`.
- **🔬 Mini-lab Core** : déclencher rate limit en burst (envoyer 50 req/30s, observer HTTP 429 + headers `Retry-After`).
- **📊 Mesure-toi** : latence p50/p95 par mode (llm_only/rag_only/agent — sans le mode `compare` qui est At.06), % requêtes injection bloquées (cible 100%), overhead Langfuse en ms.
- **Bug Hunt** : 3 patches — (1) clé API exposée dans réponse JSON ; (2) CORS `*` ; (3) pas de timeout backend → call qui pend 60s. Tirés `tps.md` 720-736.
- **Bonus** : ajouter streaming SSE OU scrubbing PII avant log Langfuse. **Interdit** : eval comparative (= At.06).
- **Source recyclée** : `tps.md` 740-769.

### Atelier 06 — Fine-tuning vs RAG / RAFT

- **Mission** : "Le CTO demande : 'On part RAG, FT, ou les deux ?'. Construis le comparatif sur 10 questions étalons, remplis la grille de décision, et défends ta reco en 5 min."
- **Scope** : RAFT théorique, eval comparative llm_only/rag_only/agent, TCO break-even.
- **Variables manipulables** : modes (`llm_only` / `rag_only` / `agent`), stratégie retrieval (fixed/recursive/ensemble), poids ensemble, max_iterations agent. Endpoint `/rag/evaluate` + `/chat/compare` + `/rag/compare-strategies` (active `ENABLE_COMPARE_ROUTES=true` ici).
- **🔬 Mini-lab Core** : sur 10 questions, mesurer (latence, recall@5, hallucination rate, tokens) × 3 modes. Remplir `grille_decision.md`.
- **📊 Mesure-toi** : recall@1/3/5 par stratégie, latence par mode, % hallucination sur questions privées, style consistency (ton "Merenza"), TCO break-even estimé (FT VPS vs API calls).
- **Bug Hunt** : 3 patches — (1) eval lancée sur train set (illusion 100%) ; (2) métrique BLEU sur ton/style (inadaptée) ; (3) latence mesurée sur 1 seul appel sans warm-up (biais cold-start).
- **Bonus** : présenter RAFT théoriquement (tableau Zhang et al. 2024 : 94% QA vs 89% RAG vs 79% FT) ; mini-débat en duo "FT, RAG ou hybride ?".
- **Format final** : reco écrite (1 page) + soutenance 5 min. C'est l'atelier de **synthèse**, le checkpoint final est la mini-défense orale (peer ou auto-jugée par LLM avec rubric).
- **Source recyclée** : `tps.md` 842-852.

---

## 9. Tableau récapitulatif des variables/métriques (référence pour rédaction)

Tableau dense pour le rédacteur (non destiné aux élèves tel quel — réparti dans chaque guide).

| Catégorie | Paramètre | Plage | Défaut | Atelier(s) | Métrique à observer |
|---|---|---|---|---|---|
| **LLM** | `temperature` | 0.0–1.0 | 0.1 | 01, 05, 06 | variance réponses, hallucination |
| | `max_tokens` | 128–4096 | 1024 | 01, 05, 06 | latence, coût tokens |
| | `LLM_PROVIDER` | anthropic / ollama | anthropic | 01, 05 | coût, latence, qualité |
| | `ANTHROPIC_MODEL` | opus/sonnet/haiku | sonnet-4-6 | 01, 05, 06 | coût, qualité |
| **RAG** | `chunk_size` | 256–2048 | 512 | 02, 06 | Recall@k, contexte size |
| | `chunk_overlap` | 0–200 | 50 | 02 | rupture sens aux frontières |
| | `k` | 1–10 | 4 | 02, 03, 06 | Recall@k, bruit |
| | `search_type` | similarity / mmr | mmr | 02 | diversité top-k |
| | `fetch_k` | k–100 | 20 | 02 | diversité MMR |
| | stratégie | fixed/recursive/semantic | recursive | 02, 06 | Recall@k, latence ingestion |
| **Agent** | `max_iterations` | 2–20 | 8 | 03, 06 | latence, step count |
| | `ensemble_weights` | [w1,w2] | [0.6, 0.4] | 03, 06 | Recall@k hybride vs dense seul |
| | `memory_k` | 0–20 | 6 | 03 | contextual correctness |
| | tools count | 1–7 | 3-4 | 03 | confusion, hallucination outils |
| **FT** | `learning_rate` | 1e-5 à 1e-3 | 5e-4 (LoRA) | 04 | loss stability, perplexité |
| | `r` (LoRA rank) | 4–64 | 8 | 04 | mémoire, qualité |
| | `epochs` | 3–10 | 5 | 04 | overfitting (val_loss / train_loss) |
| | dataset size | 100–1000 | 150 | 04 | généralisation |
| **Deploy** | rate limit | 10/30/60 req/min | 30 | 05 | HTTP 429 |
| | injection patterns | 5–50 | 19 | 05 | % attaques bloquées |

Sources : `homebutler/llm/provider.py`, `homebutler/rag/ingestion.py`, `homebutler/rag/retriever.py`, `homebutler/agent/react_agent.py`, `api/main.py`, `prepare_dataset.py`.

---

## 10. Fichiers à créer / modifier (livrables consolidés)

| Fichier | Action | Notes |
|---|---|---|
| `ateliers/atelier-00-prevol/GUIDE-ELEVE.md` | créer | Setup global + pré-téléchargement modèles |
| `ateliers/atelier-0X-*/GUIDE-ELEVE.md` (×6) | créer | Suit le gabarit §7 |
| `ateliers/atelier-0X-*/README-formateur.md` (×6) | renommer depuis `README.md` | Sépare les rôles formateur/élève |
| `ateliers/atelier-0X-*/.claude/CLAUDE.md` (×6) | créer | Prompt-guard scope |
| `ateliers/atelier-0X-*/.cursorrules` (×6) | créer | Idem pour Cursor |
| `ateliers/atelier-0X-*/.claude/settings.json` (×6) | créer | Hook UserPromptSubmit |
| `ateliers/atelier-0X-*/bugs/v[1-3].patch` (×18) | créer | Patches git |
| `ateliers/atelier-0X-*/bugs/test_v[1-3].py` (×18) | créer | Tests pytest |
| `ateliers/atelier-0X-*/bugs/v[1-3]_explanation.md` (×18) | créer | QCM auto-corrigés |
| `ateliers/atelier-0X-*/checkpoints/check_[1..N].py` (×~20) | créer | Mini-quiz auto-corrigés |
| `scripts/check_atelier_ready.sh` | créer | Vérif setup atelier N |
| `scripts/verify_branch_scope.sh` | étendre | + vérif `.claude/CLAUDE.md` local présent |
| `api/main.py` | modifier | Feature flag `ENABLE_COMPARE_ROUTES` |
| `notebooks/at04_finetuning_lora.ipynb` | créer si absent | Colab FT |
| Branche `solution/at0X` (×6) | créer | Déplacement de `solution.py` hors `main` |

**Pas de modification** des fichiers `tps.md`, `examples-supports/*`, `homebutler/*` (sauf cas justifié).

---

## 11. Stratégie d'exécution recommandée

1. **Phase 0 — Outillage scope-leak et setup** (avant rédaction guides) :
   - Modifier `api/main.py` : feature flag `ENABLE_COMPARE_ROUTES`
   - Écrire `scripts/check_atelier_ready.sh`
   - Étendre `scripts/verify_branch_scope.sh`
   - Créer le gabarit `CLAUDE.md` local + hook UserPromptSubmit + `.cursorrules` (1 fois, paramétrable par atelier)
   - Migrer `solution.py` → branches `solution/at0X`

2. **Phase 1 — Atelier 02 pilote** (modèle qualité) :
   - Rédiger `GUIDE-ELEVE.md` At.02 en intégralité (gabarit §7, contenu §8)
   - Créer les 3 patches `bugs/v[1-3].patch` + tests + explications
   - Créer les checkpoints `check_[1..N].py`
   - Test pilote avec 2 personnes (1 Build, 1 Vibe) chrono en main

3. **Phase 2 — Décliner sur les 5 autres ateliers** (parallélisable une fois le pilote validé).

4. **Phase 3 — Atelier 00 et passe finale de cohérence** :
   - `GUIDE-ELEVE.md` Pré-vol
   - Lecture croisée des "🚧 Périmètre" (anti-leak entre ateliers)
   - Test scope-leak : utiliser un agent qui tente de demander des concepts hors-scope → vérifier que le prompt-guard bloque

---

## 12. Vérification end-to-end (étendue post-audit)

- **Test pilote At.02** : 2 personnes (1 Build, 1 Vibe), chrono.
  - Cibles : Core en 1h40 ±15 min, ≥1 bug trouvé sans peeker, checkpoints expliqués sans relire le guide, score quiz final ≥ 70%.
- **Test anti-scope-leak Vibe** : tenter `claude "ajoute un agent ReAct"` pendant At.02 → vérifier que le hook UserPromptSubmit injecte le refus et que Claude répond "hors-scope, on verra ça en At.03".
- **Test anti-cheat Bug Hunt** : tenter `cat ateliers/atelier-02-*/bugs/v1.patch | claude "trouve le bug"` → si Claude trouve trivialement, le patch est trop évident, à raffiner.
- **Test setup** : exécuter `bash scripts/check_atelier_ready.sh 0X` sur une machine vierge → code 0 ou message d'erreur clair.
- **Test calibrage** : personne lente passe au Sprint après 2h, personne rapide attaque le Bonus → vérifier que personne ne déborde sur At.N+1.
- **Test scope outillé** : `bash scripts/verify_branch_scope.sh` doit passer ; lister les imports `homebutler.*` ne doit révéler que ceux du scope autorisé.
- **Test coût** : mesurer le coût Anthropic estimé par stagiaire pour 1 atelier complet (At.03 le pire, ~10-30 calls × 3 essais ≈ < 2€). Si > 5€, ajuster (cap rate-limit ou switcher At.03 vers Haiku).
- **Relecture finale** : un employé d'entreprise non-formateur lit At.02 à froid → comprend-il la mission sans aide ?

---

## Annexe A — Bibliographie validant l'approche (extraits)

> Liste complète dans le rapport agent (30+ sources). Voici les 10 références incontournables à citer dans l'intro formateur et en "Pour aller plus loin" des guides.

| # | Source | Lien | Justifie |
|---|---|---|---|
| 1 | Freeman et al. 2014, PNAS — *Active learning increases student performance in STEM* | https://www.pnas.org/doi/10.1073/pnas.1319030111 | Refus du tuto linéaire |
| 2 | Kapur 2008, Cognition & Instruction — *Productive Failure* | https://www.tandfonline.com/doi/abs/10.1080/07370000802212669 | Mission noire, Bug Hunt |
| 3 | Bjork & Bjork 2011 — *Desirable Difficulties* | https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf | Bug Hunt au milieu, retrieval practice |
| 4 | Sweller 1994 — *Cognitive Load Theory* | https://pressbooks.pub/learningenvironmentsdesign/chapter/sweller-cognitive-load-theory-learning-difficulty-and-instructional-design/ | Scope strict, Core/Sprint/Bonus |
| 5 | Tomlinson 2017 — *Differentiated Instruction* | (livre) | Double piste Build/Vibe |
| 6 | Crouch & Mazur 2001 — *Peer Instruction* | https://web.mit.edu/jbelcher/www/TEALref/Crouch_Mazur.pdf | Checkpoints à voix haute / démo |
| 7 | Kosmyna et al. 2025 (MIT) — *Your Brain on ChatGPT* | https://arxiv.org/abs/2506.08872 | Légitimer contraintes Vibe (préprint) |
| 8 | Lee, Sarkar et al. 2025 (Microsoft, CHI) — *Impact of GenAI on Critical Thinking* | https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/ | Validation : confiance GenAI ↑ → effort critique ↓ |
| 9 | Prather et al. 2024 (ICER) — *Widening Gap: GenAI for Novice Programmers* | https://dl.acm.org/doi/10.1145/3632620.3671116 | "Illusion de compétence" vibe-coding |
| 10 | RAGAS (Es et al. 2024, EACL) | https://arxiv.org/abs/2309.15217 | Métriques RAG At.02/06 |
| 11 | RAFT (Zhang et al. 2024) | https://arxiv.org/abs/2403.10131 | Atelier 06 Bonus |
| 12 | Anthropic Cookbook — Contextual Retrieval | https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide | Atelier 02 Bonus (re-ranker scope-safe) |

Mapping détaillé plan→sources et liste complète : voir rapport agent bibliographie (peut être recopié dans `examples-supports/bibliographie-pedagogique.md` si on veut un livrable formateur dédié).

---

## Annexe B — Décisions tranchées vs v1

| Trou v1 | Décision v2 |
|---|---|
| Calibrage additif 2h+45min+1h = 3h45 | Rails parallèles : 20min setup + 1h40 Core + (30min Sprint XOR 60min Bonus) + 10min wrap = 3h30 |
| Prompt-guard "mentionné mais pas spécifié" | `CLAUDE.md` local + `.cursorrules` + hook `UserPromptSubmit` (3 fichiers vérifiables par atelier) |
| Bug Hunt skipable par `cat solution.py` | Patches git + tests pytest + branche `solution/at0X` non checkoutée |
| Checkpoints "suppose un formateur" | 3 dispositifs combinés : QCM auto-corrigé + LLM-judge avec rubric + démo pair (optionnel) |
| Setup matériel non traité | Atelier 00 "Pré-vol" + `scripts/check_atelier_ready.sh N` |
| Scope leak `/rag/evaluate` etc. At.05↔06 | Feature flag `ENABLE_COMPARE_ROUTES`, désactivé At.05, activé At.06 |
| Fichiers existants ignorés | Tableau §5 d'articulation explicite ; `README.md` → `README-formateur.md` |
| Atelier 01 trop court (30 min réels) | Scope étendu : top_p, seed, system vs user, few-shot |
| Atelier 04 sans GPU = 45 min réels | Notebook Colab `notebooks/at04_finetuning_lora.ipynb` ajouté en Bonus |
| Bonus flou | Format `reflexion-challenge.md` obligatoire (POURQUOI/Contexte/Question/Pistes) |
| Coût Anthropic non chiffré | Test d'estimation cap < 5€/stagiaire/atelier, sinon switcher Haiku |
| Aucune mécanique contre "illusion de compétence" Vibe | Score quiz final décide Sprint vs Bonus ; LLM-judge sévère sur explications |
| Atelier 04 trop jargonneux (GPU, VRAM, lr, grid search, HF Hub, W&B, QLoRA quantization, déséquilibre dataset) pour public non-tech | Mini-lexique jargon→analogie obligatoire en tête du Carnet de bord At.04 (tableau de 16 termes) ; règle généralisée à tous les ateliers (§3 transversal) ; quiz vérifie 3 termes au hasard ; les "🐛 erreurs communes" reformulées en langage non-tech |
