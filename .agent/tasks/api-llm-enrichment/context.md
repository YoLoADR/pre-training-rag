# Contexte — Enrichissement API/LLM HomeButler (RAFT)

## Objectif
Compléter le projet HomeButler AI pour couvrir **100% du programme RAFT** (3 jours, PLB v2026-0512).

L'analyse d'écart PDF ↔ code a révélé 4 zones lacunaires majeures :

1. **API/LLM trop légère** : `POST /chat` renvoie une string sans mode, sources, mémoire ni métriques
2. **Notebook 01 incomplet** : Ollama seulement, mais TP J1 exige HuggingFace Transformers + Conda
3. **Notebook 03 absent** : J2 après-midi (LoRA, QLoRA, augmentation, MLFlow, GGUF) manque
4. **Script d'augmentation absent** : 150 paires → 500 (draft.md + PDF "Augmentation des données")

## Source du plan
Plan détaillé dans : `.agent/tasks/api-llm-enrichment/plan.md`
Plan Claude original : `~/.claude/plans/l-application-est-bonne-playful-nova.md`

## Contraintes techniques
- Python 3.13 + venv `.venv`
- LangChain 0.3.14
- FastAPI 0.115.6
- Pas de PyTorch en local (Mac Intel sans GPU) → notebooks fine-tuning = Colab only
- `AsyncIteratorCallbackHandler` est dans `langchain.callbacks.streaming_aiter`
- `ConversationBufferWindowMemory` est dans `langchain.memory`
- Hub prompt `hwchase17/react-chat` ✅ (input_variables: agent_scratchpad, chat_history, input, tool_names, tools)

---

## État final — COMPLÉTÉ (2026-05-20)

### Fichiers créés ou modifiés

| Fichier | Nature | BLOC |
|---|---|---|
| `homebutler/llm/provider.py` | Modifié | BLOC 3 |
| `homebutler/llm/prompts.py` | Modifié | BLOC 4 |
| `homebutler/agent/react_agent.py` | Réécrit | BLOC 5 |
| `api/routers/chat.py` | Réécrit | BLOC 1 |
| `api/routers/rag.py` | Créé | BLOC 2 |
| `api/main.py` | Modifié | BLOC 6 |
| `api/limiter.py` | Créé | BLOC 6 (fix rate limiting) |
| `requirements.txt` | Modifié | BLOC 6 |
| `scripts/augment_qa_dataset.py` | Créé | BLOC 9 |
| `data/qa_dataset/augmented_concierge_qa.jsonl` | Généré | BLOC 9 |
| `notebooks/01_llm_baseline.ipynb` | Enrichi (+5 cellules) | BLOC 7 |
| `notebooks/02_ingestion_vectorisation.ipynb` | Enrichi (+2 cellules) | BLOC 8 |
| `notebooks/03_finetuning_lora.ipynb` | Créé (27 cellules) | BLOC 10 |
| `.agent/tasks/api-llm-enrichment/` | Créé | Suivi tâche |

### Résultats de validation API

| Test | Endpoint | Résultat |
|---|---|---|
| Hallucination sans RAG | `POST /chat` mode=llm_only | Répond sans connaître la chaudière + token_usage ✅ |
| RAG pur avec sources | `POST /chat` mode=rag_only debug=true | "Viessmann" + sources[] avec extrait PDF ✅ |
| Comparaison 3 modes | `POST /chat/compare` | llm_only hallucine, rag_only+agent répondent correctement ✅ |
| Mémoire conversation | `POST /chat` session_id="s1" ×2 | 2e question utilise le contexte du 1er tour ✅ |
| Transparence retrieval | `POST /rag/retrieve` | 6 chunks avec source+page+extrait ✅ |
| Benchmark Recall@K | `POST /rag/evaluate` 10 questions | recall@1=0.7, recall@3=0.8, recall@5=1.0 ✅ |
| Comparaison chunkers | `POST /rag/compare-strategies?query=...` | fixed/recursive/ensemble retournent des chunks différents ✅ |
| Streaming SSE | `GET /chat/stream` | Tokens arrivant un par un (data: ...) ✅ |
| Rate limiting | `POST /chat` ×35 parallèles | 21×200 + 14×429 (limite 30/min par IP) ✅ |
| Filtre injection | `POST /chat` body="ignore tes instructions" | HTTP 400 ✅ |

### Commits git de référence
- `a6d8ca1` — backup avant enrichissement (avant toute modification)
- `db11074` — complétion finale BLOCs 7-10 + fix rate limiting (2026-05-20)

### Endpoint à valider (interrompu)
L'utilisateur a demandé de tester en profondeur les comparaisons entre approches :
- `POST /chat/compare` : différences llm_only vs rag_only vs agent sur même question métier
- `POST /rag/compare-strategies` : différences fixed vs recursive vs ensemble sur même query
- `POST /rag/evaluate` : Recall@K comparé entre les 3 stratégies de chunking
