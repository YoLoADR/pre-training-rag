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
