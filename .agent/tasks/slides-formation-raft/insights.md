# Insights — Slides Formation RAFT

## Format gamma.app (validé sur exemples existants)

- Gamma interprète les `📝 Slide N :` comme séparateurs de slides
- Pas de heading markdown (`#`) nécessaire — la structure visuelle est donnée par les emojis et le texte
- Les tableaux markdown s'affichent bien dans Gamma
- Les callouts `> 💡` créent des blocs visuels distincts
- Les `⚠️ **Titre**` créent des warnings visuels
- **Blocs de code ``` = problème connu dans Gamma** — remplacer systématiquement par tableaux ou pseudo-flux textuel

## Structure des examples inspirants

Les deux fichiers de référence (`slides-inspiration-1.md` et `slides-inspiration-2.md`)
couvrent Claude Code / MCP / Sub-agents — **thématique différente**, mais format identique
à reproduire pour la formation RAG/FT.

Chaque slide suit le schéma :
1. `POURQUOI [question] ?` (ouvre le slide avec la motivation)
2. Paragraphe d'explication (contexte, histoire, chiffres)
3. Tableau comparatif (souvent 2-4 colonnes)
4. Callout `> 💡` ou avertissement `⚠️`

## Contenu HomeButler AI (données techniques précises)

**Stack validée et testée sur Mac Intel Python 3.13.5 :**
- `langchain==0.3.14`, `langchain-core==0.3.41`, `langchain-anthropic==0.3.0`
- `faiss-cpu==1.8.0` (ou 1.13.2 pour Python 3.14)
- `chromadb==0.5.23`
- `fastembed>=0.8.0` (remplace sentence-transformers — ONNX, 100 Mo vs 470 Mo)
- `pymupdf==1.25.1` (s'installe `pymupdf`, s'importe `import fitz`)
- `onnxruntime==1.23.2` (Mac Intel bloqué sur cette version — 1.24+ ARM-only)
- `python-multipart>=0.0.18` (Gradio 5.x incompatible avec 0.0.12)
- `FastAPI==0.115.6`, `streamlit>=1.38`, `gradio==5.9.1`
- `cachetools` pour TTLCache météo

**40 fichiers en 10 phases :**
- Phase 1 (5) : bootstrap (config, env, README)
- Phase 2 (5) : génération données (6 PDFs, CSV 365j énergie, 30 producteurs JSON, 150 Q&A JSONL)
- Phase 3 (3) : abstraction LLM (provider switch, prompts)
- Phase 4 (4) : services métier (energy, marketplace, weather)
- Phase 5 (3) : pipeline RAG (ingestion PyMuPDF, vectorstore FAISS+ChromaDB, EnsembleRetriever)
- Phase 6 (3) : agent ReAct (tools.py 4 outils, react_agent.py)
- Phase 7 (6) : FastAPI (4 routers : chat, consumption, products, orders)
- Phase 8 (5) : UI (Gradio prototype + Streamlit 4 pages)
- Phase 9 (2) : notebooks éducatifs (01_llm_baseline, 02_ingestion_vectorisation)
- Phase 10 (3) : infrastructure Docker Compose

**4 outils ReAct :**
- `search_docs` : RAG FAISS/ChromaDB sur 6 PDFs
- `analyze_energy` : détection anomalies CSV (3 injectées : juin +200%, déc +150%, mars -60%)
- `find_products` : recherche haversine parmi 30 producteurs locaux
- `weather_tool` : API météo + cache TTLCache 1h

**Pièges documentés dans insights.md homebutler :**
1. `import fitz` (pas `import pymupdf`)
2. `FAISS.load_local(allow_dangerous_deserialization=True)`
3. `handle_parsing_errors=True` + `max_iterations=8` pour Ollama
4. `@st.cache_resource` sur agent + vectorstores
5. `pip install -e .` nécessaire pour imports Streamlit (`pyproject.toml`)
6. FastAPI `lifespan` pour init agent (pas à chaque requête)
7. Python 3.14 + Mac Intel = incompatible onnxruntime
8. `python-multipart>=0.0.18` pour Gradio 5.x
9. ChromaDB 0.4+ : `PersistentClient(path=...)` (pas `chromadb.Client()`)
10. LangSmith (formation) vs Langfuse (prod) via `TRACING_PROVIDER` env var

## Insights de recherche internet (stats et dates clés)

**Timeline LLM :**
- 2017 : Transformer (Vaswani et al., "Attention Is All You Need")
- 2018 : BERT (bidirectionnel) + GPT-1
- 2020 : GPT-3 175B, Lewis et al. RAG paper (Meta AI, arxiv:2005.11401)
- 2022 mars : InstructGPT (RLHF) — 1,3B > 175B
- 2022 nov : ChatGPT — 100M users en 2 mois (record absolu)
- 2022 oct : LangChain (Harrison Chase) + LlamaIndex (Jerry Liu, "GPT Index")
- 2023 fév : LLaMA (Meta, 7B-70B, open-source)
- 2023 juin : Mistral 7B (Mistral AI, Paris, Apache 2.0)
- 2021 juin : LoRA (Hu et al., arxiv:2106.09685)
- 2023 mai : QLoRA (Dettmers et al., arxiv:2305.14314)
- 2024 mars : RAFT (Zhang et al., arxiv:2403.10131, Berkeley + Microsoft)
- 2023 : Ollama (CLI llama.cpp), Jan.ai (GUI desktop)

**Stats clés :**
- Hallucinations sans RAG : 8-42% selon domaine
- RAG réduit hallucinations à 0-6%
- RAG : 89% accuracy vs 60-70% sans retrieval
- LoRA : -99% paramètres entraînables vs Full FT
- QLoRA : fine-tune 70B sur 2× A100 48GB (vs 4× A100 80GB pour Full FT)
- Coût LoRA : $200-500 vs Full FT $2 000-5 000
- Chunk size optimal : 400-512 tokens, 10-20% overlap
- Latence RAG optimisée : 1-2s total (retrieval 500ms + génération 500ms)
- Reranking : +15-30% précision
- Hybride RAG+FT : 96% accuracy vs RAG 89% vs FT seul 91%
- TCO 12 mois : RAG $1k-3k / FT $3k-8k / Hybride $5k-12k
- GGUF Q4_K_M : 92% qualité, AWQ : 95%, GPTQ : 90%

## Décisions de rédaction

- **Slide 10 de chaque chapitre = slide HomeButler** — dédié au fil rouge
- **Pas de numérotation des chapitres dans les titres** (Chapitre 1, pas Ch. 1.1)
- **Tableaux 4-5 colonnes max** pour rester lisibles dans Gamma
- **1 seul callout et 1 seule warning max par slide** pour ne pas surcharger
- **Stats toujours sourcées** (auteur + année) quand disponibles
- **Pas de markdown headers (#)** — structure portée par les emojis

## État d'avancement

- **2026-05-20** : Plan approuvé, structure de tâche créée, exécution en cours
- Slides rédigés : 0/60 → en cours d'écriture
