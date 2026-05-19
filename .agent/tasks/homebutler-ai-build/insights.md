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

### Python 3.14 → utiliser Python 3.13 pour ce projet
La machine a Python 3.14.3, 3.13.5 et 3.12.13 installés.
**Python 3.14 est incompatible** avec `sentence-transformers` et `torch` : aucun wheel pip disponible (confirmé mai 2026).
**Solution : recréer le venv avec Python 3.13** (`python3.13 -m venv .venv`).
Sentence-transformers supporte officiellement jusqu'à Python 3.13 (même en v5.5.0).
faiss-cpu : version 1.13.2 requise (1.8.0 n'a pas de wheel Python 3.13/3.14).

### Données énergie
- 365 lignes CSV générées avec succès
- 32 anomalies détectées (z-score > 2.0 sur fenêtre 30j) pour 3 anomalies injectées — normal car la fenêtre glissante "voit" plusieurs jours autour du pic

### Marketplace
- 30 producteurs avec coordonnées GPS réalistes autour de Boulogne-Billancourt
- Recherche haversine fonctionnelle : 7 producteurs légumes dans 15km

## Étapes restantes (à faire par l'utilisateur)

1. Mettre `ANTHROPIC_API_KEY` dans `.env`
2. `pip install -r requirements.txt` complet (attention aux wheels Python 3.14)
3. `python scripts/preload_models.py` — télécharge `paraphrase-multilingual-MiniLM-L12-v2`
4. Indexation RAG initiale
5. Test end-to-end : uvicorn + streamlit

---

*Dernière mise à jour : Implémentation complète — commit 6efc690 pushé sur GitHub*
