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

---

*Dernière mise à jour : Phase 0 — Bootstrap*
