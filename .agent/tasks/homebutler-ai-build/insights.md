# Insights — HomeButler AI Build

> Mise à jour itérative au fil de l'implémentation. Les insights sont des découvertes, décisions, ou pièges rencontrés.

## Initialisation

- Repo GitHub créé : https://github.com/YoLoADR/pre-training-rag (private)
- Projet démarre avec uniquement le fichier spec `HomeButler-AI-Projet-Fil-Rouge.md`
- Le dossier `.agent/tasks/homebutler-ai-build/` sert de mémoire persistante entre les sessions

## Architecture LLM

- Le switch LLM (`LLM_PROVIDER=anthropic|ollama`) est la décision la plus critique car elle conditionne tout le reste
- `ChatAnthropic` nécessite `max_tokens` obligatoire (sinon erreur API) — `ChatOllama` utilise `num_predict`
- Pour la formation, garder le mode ReAct textuel (pas function calling natif) pour montrer le raisonnement Thought→Action→Observation

## Observabilité

- L'utilisateur utilise **Langfuse** (pas LangSmith) dans ses projets prod (`pbn/amplifiire`)
- Pattern Langfuse : singleton `LangfuseService` avec `get_config()` → `{"callbacks": [CallbackHandler()]}`
- Pour le curriculum RAFT, LangSmith reste le primary (s'active via env vars LangChain, 0 import requis)
- Support des deux via `TRACING_PROVIDER=langsmith|langfuse`

## Données fictives

- fpdf2 gère UTF-8 nativement (contrairement à fpdf1) — pas de problème d'accents
- Les PDFs doivent être structurés avec des sections titrées pour que le chunking récursif batte le chunking fixe (effet pédagogique voulu)
- 3 anomalies dans le CSV : juin (pic +200%, climatiseur oublié), décembre (pic +150%), mars (baisse -60%)

## RAG

- `FAISS.load_local()` exige `allow_dangerous_deserialization=True` depuis langchain 0.1.x — piège fréquent
- `pymupdf` s'installe `pip install pymupdf` mais s'importe `import fitz` — source de confusion en formation
- Premier chargement du modèle embeddings `paraphrase-multilingual-MiniLM-L12-v2` : ~470 Mo, download unique dans `~/.cache/huggingface/`
- ChromaDB depuis 0.4.x : utiliser `PersistentClient(path=...)`, pas `chromadb.Client()`

## Agent

- `handle_parsing_errors=True` + `max_iterations=8` indispensables avec Ollama non fine-tuné (respect du format ReAct variable)
- Prompt hub `hwchase17/react` est le plus robuste pour les deux providers

## FastAPI

- Pattern lifespan pour init agent (évite la variable globale) : `@asynccontextmanager async def lifespan(app)`
- Middleware injection filter avant le body parsing pour éviter les attaques

## UI

- `@st.cache_resource` obligatoire sur agent et vectorstores (Streamlit recharge à chaque interaction)
- Gradio 5.x a une API légèrement différente de Gradio 4.x pour `ChatInterface`

## Problèmes rencontrés et solutions

### fpdf2 + caractères non-latin-1
**Problème** : fpdf2 avec les polices Helvetica intégrées ne supporte pas Unicode > latin-1.
Les caractères `—` (tiret em, U+2014) et `→` (flèche droite, U+2192) provoquent `UnicodeEncodeError`.
**Solution** : Remplacer `—` par `-` et `→` par `->` via sed avant génération.
**Alternative future** : Utiliser une police TTF (DejaVu, Liberation) avec `pdf.add_font()`.

### Embeddings : sentence-transformers remplacé par fastembed (Python 3.14)
**Contexte machine** : Python 3.14.3 installé (+ 3.13.5 et 3.12.13 disponibles).
**Erreurs rencontrées lors du pip install** :
1. `faiss-cpu==1.8.0` → pas de wheel Python 3.14 → corrigé en `1.13.2`
2. `pydantic==2.7.1` → conflit avec `langchain 0.3.14` qui exige `>=2.7.4` → assoupli en `>=2.7.4`
3. `numpy==1.26.4` et `pandas==2.2.3` → pas de wheel Python 3.14 → assoupli en `>=2.0.0` / `>=2.2.3`
4. `sentence-transformers==3.3.1` → exige `torch>=1.11.0` → `torch` n'a pas de wheel pip standard Python 3.14 → **remplacé par `fastembed>=0.8.0`**

**Solution retenue : fastembed (sans torch)**
- `fastembed` utilise ONNX Runtime, pas PyTorch → compatible Python 3.14 depuis v0.8.0 (onnxruntime 1.26.0, mai 2026)
- Même modèle : `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (version ONNX quantisée ~100 Mo vs 470 Mo PyTorch)
- LangChain : `FastEmbedEmbeddings` dans `langchain-community` (même API que `HuggingFaceEmbeddings`)
- Cache dans `~/.cache/fastembed/` au lieu de `~/.cache/huggingface/`
- Fichiers modifiés : `requirements.txt`, `homebutler/rag/vectorstore.py`, `scripts/preload_models.py`

### Données énergie
- 365 lignes CSV générées avec succès
- 32 anomalies détectées (z-score > 2.0 sur fenêtre 30j) pour 3 anomalies injectées — normal car la fenêtre glissante "voit" plusieurs jours autour du pic

### Marketplace
- 30 producteurs avec coordonnées GPS réalistes autour de Boulogne-Billancourt
- Recherche haversine fonctionnelle : 7 producteurs légumes dans 15km

## État actuel (2026-05-19)

### Ce qui est fait ✅
- Code complet (40 fichiers), notebooks valides, données générées
- `.env` configuré : ANTHROPIC_API_KEY réelle, Langfuse cloud (`cloud.langfuse.com`)
- `requirements.txt` corrigé pour Python 3.14 : faiss-cpu 1.13.2, pydantic>=2.7.4, fastembed>=0.8.0
- `.venv` existe (Python 3.14.3)

### Blocage en cours ⚠️
- `pip install -r requirements.txt` pas encore terminé avec succès sur Python 3.14
- Le remplacement sentence-transformers → fastembed vient d'être fait (commit à venir)
- Index FAISS et ChromaDB pas encore buildés
- Aucun test end-to-end effectué

### Prochaines étapes (dans l'ordre)
1. `pip install -r requirements.txt` (relancer après le dernier commit)
2. `python scripts/preload_models.py` — télécharge le modèle ONNX (~100 Mo)
3. Indexation RAG (`ingest_all_documents` + `build_faiss_index` + `build_chroma_db`)
4. Scénario 2 → services métier
5. Scénario 4 → retrieval
6. Scénario 5 → agent ReAct (nécessite ANTHROPIC_API_KEY dans env)
7. Scénario 6 → API FastAPI + tests sécurité
8. Scénario 7 → UI Streamlit + Gradio

---

*Dernière mise à jour : 2026-05-19 — fastembed substitution + corrections Python 3.14*

---

## Session 2026-05-19 (suite) — Setup end-to-end validé sur Mac Intel

### Découverte majeure : Python 3.14 incompatible avec Mac Intel

Le commit `2031115` ("replace sentence-transformers with fastembed for Python 3.14 support") était **incomplet** sur Mac Intel. Le vrai blocker n'est ni torch ni sentence-transformers, mais **onnxruntime** (dépendance de chromadb ET fastembed).

**Cartographie onnxruntime / OS / Python (mai 2026)** :

| onnxruntime | macOS x86_64 (Intel) | Py 3.13 | Py 3.14 |
|---|---|---|---|
| 1.26.0 (latest) | ❌ ARM only | ✅ | ✅ |
| 1.24–1.25 | ❌ ARM only | ✅ | ✅ |
| **1.23.x** | **✅ Intel + ARM** | **✅** | ❌ |
| < 1.23 | ❌ | parfois ✅ | ❌ |

Microsoft a migré sa cible macOS d'Intel vers ARM exactement à partir de la version qui ajoute le support Python 3.14. **Aucune combinaison Python 3.14 + Mac Intel n'est possible** sans compiler onnxruntime depuis les sources.

**Solution retenue** : Python **3.13.5** + pin `onnxruntime==1.23.2`. Compatible fastembed (qui exige `>1.21.0, !=1.24.0/1, !=1.20.0` sur Py 3.13).

### Bugs supplémentaires découverts pendant la validation

1. **`python-multipart==0.0.12` incompatible gradio 5.9.1** (exige `>=0.0.18`).
   → bumpé en `python-multipart>=0.0.18`.

2. **`ModuleNotFoundError: No module named 'homebutler'` dans Streamlit**.
   - Cause : Streamlit ne place que le dossier du script (`ui/`) dans `sys.path`, pas la racine projet.
   - Solution propre retenue : créer `pyproject.toml` minimal + `pip install -e .` → le package `homebutler` devient résolvable peu importe le cwd.

3. **`ValueError: 'lat' is not a column` sur la page Marketplace**.
   - Cause : `api/routers/products.py::ProducerResult` n'exposait pas `latitude`/`longitude` alors que le service `search_producers` les renvoie.
   - Solution : ajout des deux champs au modèle Pydantic + au mapping de retour.

### Validation end-to-end réussie

- ✅ `pip install -r requirements.txt` complet (onnxruntime 1.23.2, chromadb 0.5.23, fastembed 0.8.0, langchain 0.3.14, gradio 5.9.1).
- ✅ Modèle d'embeddings préchargé (`paraphrase-multilingual-MiniLM-L12-v2`, 384 dim).
- ✅ Données générées : 6 PDFs, 365j énergie, 30 producteurs, 150 paires Q/A.
- ✅ Indexation : 49 chunks → FAISS + ChromaDB.
- ✅ API FastAPI : `/health`, `/chat` (agent ReAct + RAG + Claude Sonnet 4.6), `/products/search`, `/consumption/analyze` tous testés OK.
- ✅ UIs : Streamlit (8501) et Gradio (7860) démarrent.

### Warnings non-bloquants à connaître

- `LangChainDeprecationWarning: Chroma deprecated, use langchain-chroma` — cosmétique, l'API actuelle marche.
- `Failed to send telemetry event` (chromadb) — bug telemetry de chromadb 0.5.23, sans impact fonctionnel.
- `UserWarning: tuples format for chatbot messages is deprecated` (Gradio) — pré-v6 deprecation.
- `LangSmithMissingAPIKeyWarning` — normal puisque `LANGCHAIN_TRACING_V2=false`.

### Note pour le déploiement / formation

- **Mac Intel** : doit utiliser Python 3.13 + onnxruntime 1.23.2 (cf. ce pin dans requirements.txt).
- **Mac ARM (M1/M2/M3/M4)** : Python 3.13 ou 3.14 + onnxruntime latest fonctionnent.
- **Linux x86_64** (VPS, Docker) : Python 3.13 ou 3.14 + onnxruntime latest fonctionnent. C'est l'env le plus récent.
- **Pour formation cross-OS** : Docker reste la solution la plus propre pour garantir un env identique chez tous les stagiaires.

### Fichiers ajoutés/modifiés cette session

- `requirements.txt` : ajout `onnxruntime==1.23.2`, bump `python-multipart>=0.0.18`.
- `pyproject.toml` (nouveau) : déclaration minimale du package `homebutler` pour `pip install -e .`.
- `api/routers/products.py` : `latitude`/`longitude` ajoutés à `ProducerResult`.

*Dernière mise à jour : 2026-05-19 (soir) — setup end-to-end validé sur Mac Intel + Python 3.13*
