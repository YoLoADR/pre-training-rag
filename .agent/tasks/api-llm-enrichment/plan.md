# Plan — Complétion RAFT : API/LLM + Notebooks + Scripts manquants

## Contexte

Analyse d'écart exhaustive entre le **programme PDF RAFT** (3 jours, PLB v2026-0512) et l'implémentation actuelle. Le projet couvre bien le fil rouge HomeButler mais présente **4 zones lacunaires majeures** :

1. **API/LLM trop légère** : `POST /chat` renvoie une string, sans mode, sans sources, sans mémoire, sans métriques — impossible de démontrer les comparaisons exigées par le PDF
2. **Notebook 01 incomplet** : utilise Ollama, mais le TP J1 exige "Setup Conda + test via HuggingFace Transformers"
3. **Notebook 03 absent** : J2 après-midi (LoRA, QLoRA, augmentation, MLFlow, GGUF) n'existe pas
4. **Script d'augmentation absent** : draft.md dit "150 paires…augmentées à 500" — `augment_qa_dataset.py` manquant

### Table d'écart PDF ↔ projet

| Objectif PDF | Module concerné | État | Action |
|---|---|---|---|
| TP J1 : "Quel type de question échoue sans retrieval ?" | `chat.py` | ❌ Pas de mode `llm_only` | Ajouter `mode` param |
| TP J1 : test Conda + HuggingFace Transformers | `01_llm_baseline.ipynb` | ❌ Ollama seulement | Ajouter cellules HF |
| TP J1 : "Quelle stratégie offre le meilleur rappel ?" | API RAG | ❌ Endpoint absent | Créer `POST /rag/evaluate` |
| J2 : LlamaIndex / Haystack mentionnés | notebooks | ❌ Absent | Cellule comparaison dans nb02 |
| TP J2 : Pipeline RAG agent exemple concret | `react_agent.py` | ⚠️ Pas de mémoire session | Ajouter `ConversationBufferWindowMemory` |
| TP J2 : fine-tuning LoRA sur dataset client | `03_finetuning_lora.ipynb` | ❌ Manquant | Créer notebook Colab |
| J2 : Augmentation des données (150→500) | scripts | ❌ Manquant | Créer `augment_qa_dataset.py` |
| J2 : Évaluation métriques fine-tuning | `03_finetuning_lora.ipynb` | ❌ Manquant | BLEU/ROUGE + qualitatif |
| J2 : Distillation de modèles | notebooks | ❌ Absent | Cellule explication nb03 |
| J3 : Quantization + GGUF + Ollama | notebooks | ❌ Absent | Cellule GGUF dans nb03 |
| J3 : Jan.ai et Ollama (logiciels) | notebooks/README | ❌ Absent | Section dans nb03 |
| J3 TP : "Quels risques exposition modèle ?" | `api/main.py` | ⚠️ Injection seulement | Rate limiting + API key |
| J3 : "Supervision avec LangSmith ou MLFlow" | notebooks | ⚠️ Langfuse en prod, MLFlow absent | MLFlow dans nb03 |
| J3 TP : "Evaluation comparative des résultats" | API | ❌ Endpoint absent | Créer `POST /chat/compare` |
| J3 : Prompt caching (optimisation) | `provider.py` | ❌ Absent | Ajouter `get_llm_cached()` |
| J3 : Streaming (déploiement réel) | API | ❌ Absent | Ajouter `GET /chat/stream` |
| Mémoire conversationnelle (UX production) | `react_agent.py` | ❌ Stateless | Session memory par `session_id` |
| Sources / transparence RAG | `chat.py` | ❌ Non retourné | Retourner `sources[]` |
| Token usage tracking | `chat.py` | ❌ Non retourné | Retourner `token_usage` |
| Debug / trace agent (pédagogie J2) | `chat.py` | ❌ Absent | Flag `debug` + `steps[]` |

---

## Fichiers à modifier

| Fichier | Nature | Raison |
|---|---|---|
| `api/routers/chat.py` | Réécriture complète | Mode, debug, sources, token_usage, mémoire, compare, stream |
| `api/routers/rag.py` | Création | /rag/retrieve, /rag/evaluate, /rag/compare-strategies |
| `api/main.py` | Modification mineure | Include rag router + rate limiting |
| `homebutler/llm/provider.py` | Ajout | `get_llm_cached()` + streaming param |
| `homebutler/llm/prompts.py` | Ajout | `BARE_LLM_TEMPLATE` (mode sans RAG) |
| `homebutler/agent/react_agent.py` | Refactor | Session memory + debug + `get_session_agent()` |
| `homebutler/rag/retriever.py` | Ajout param | `strategy` param dans `retrieve()` |
| `notebooks/01_llm_baseline.ipynb` | Ajout cellules | Section HuggingFace Transformers (Colab) |
| `notebooks/02_ingestion_vectorisation.ipynb` | Ajout cellule | LlamaIndex/Haystack comparaison |
| `scripts/augment_qa_dataset.py` | Création | Augmentation 150→500 paires |
| `notebooks/03_finetuning_lora.ipynb` | Création | LoRA/QLoRA complet pour Colab |

---

## Implémentation détaillée

---

### BLOC 1 — `api/routers/chat.py` : Réécriture complète

**Nouveaux modèles Pydantic :**
```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="default")
    mode: Literal["agent", "rag_only", "llm_only"] = "agent"
    debug: bool = False

class SourceDoc(BaseModel):
    source: str           # nom du PDF
    page: int | None
    excerpt: str          # 150 premiers chars du chunk

class ChatResponse(BaseModel):
    response: str
    session_id: str
    llm_provider: str
    mode: str
    sources: list[SourceDoc] = []
    token_usage: dict | None = None   # {"input_tokens": n, "output_tokens": n}
    steps: list[str] = []             # trace ReAct si debug=True
```

**Logique des 3 modes dans `POST /chat` :**

- **`llm_only`** : `BARE_LLM_TEMPLATE | get_llm()`. Pas de contexte injecté. Retourne `token_usage` via `result.usage_metadata`. Sert à démontrer les hallucinations (J1 matin "wow effect").

- **`rag_only`** : `retrieve(query)` → `format_docs_for_context(docs)` → `RAG_QA_TEMPLATE | get_llm_cached()`. Retourne `sources[]` (chunks utilisés avec excerpt). Sert à démontrer le RAG pur (J1 après-midi).

- **`agent`** (défaut) : `get_session_agent(session_id)`. Si `debug=True` : `AgentExecutor(return_intermediate_steps=True)` → `steps[]` = ["Thought: ...", "Action: search_home_docs", "Observation: ..."]. Retourne aussi `sources[]` si l'outil RAG a été appelé.

**`POST /chat/compare` — démo pédagogique centrale (J3 TP) :**
```python
@router.post("/compare")
async def chat_compare(req: ChatRequest):
    """
    Lance la même question dans les 3 modes en parallèle.
    Permet la comparaison LLM seul vs RAG vs agent (J3 après-midi).
    """
    import asyncio
    # 3 appels parallèles avec asyncio.gather
    results = await asyncio.gather(
        _call_llm_only(req.message),
        _call_rag_only(req.message),
        _call_agent(req.message, req.session_id),
    )
    return {
        "question": req.message,
        "llm_only": results[0],    # {"response", "token_usage"}
        "rag_only": results[1],    # {"response", "sources", "token_usage"}
        "agent": results[2],       # {"response", "sources", "steps", "token_usage"}
    }
```
Correspond directement à la grille de décision du draft.md (LLM seul vs RAG vs Fine-tuné vs Hybride) et au TP J3 "Evaluation comparative des résultats".

**`GET /chat/stream` — SSE (J3 déploiement) :**
```python
from fastapi.responses import StreamingResponse
from langchain_core.callbacks import AsyncIteratorCallbackHandler

@router.get("/stream")
async def chat_stream(message: str, session_id: str = "default"):
    """Streaming SSE — démontre un déploiement réel (J3 matin)."""
    handler = AsyncIteratorCallbackHandler()
    llm_stream = get_llm(temperature=0.1, streaming=True, callbacks=[handler])
    
    async def generate():
        task = asyncio.create_task(
            (BARE_LLM_TEMPLATE | llm_stream).ainvoke({"question": message})
        )
        async for token in handler.aiter():
            yield f"data: {token}\n\n"
        await task
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

### BLOC 2 — `api/routers/rag.py` : Nouveaux endpoints pédagogiques (RAG)

**`POST /rag/retrieve` — transparence RAG (J1 après-midi) :**
```python
class RetrieveRequest(BaseModel):
    query: str
    strategy: Literal["fixed", "recursive", "ensemble"] = "ensemble"
    k: int = Field(default=5, ge=1, le=10)

class ChunkResult(BaseModel):
    rank: int
    source: str
    page: int | None
    excerpt: str     # 200 chars
    char_count: int

@router.post("/retrieve")
async def rag_retrieve(req: RetrieveRequest) -> dict:
    """
    Retourne les chunks récupérés pour une query.
    Permet de voir QUE récupère le RAG et depuis quel document.
    Pédagogie : J1 après-midi, chunking + retrieval.
    """
```
Appelle `retrieve(query, use_ensemble=(strategy=="ensemble"), k=req.k)` ou les retrievers individuels selon `strategy`.

**`POST /rag/evaluate` — benchmark Recall@K (TP J1) :**
```python
class EvaluateRequest(BaseModel):
    strategy: Literal["fixed", "recursive", "ensemble"] = "ensemble"
    sample_size: int = Field(default=20, ge=5, le=50)

@router.post("/evaluate")
async def rag_evaluate(req: EvaluateRequest) -> dict:
    """
    Calcule Recall@1, @3, @5 sur les N premières paires du QA dataset.
    Ground truth = le champ category + keywords de la réponse de référence.
    Correspond au TP J1 : 'Quelle stratégie de découpage offre le meilleur rappel ?'
    """
```
Pour chaque `(input, output)` du `concierge_qa.jsonl` : on lance `retrieve(input)`, on vérifie si au moins un doc retourné contient les mots-clés de `output`. Retourne :
```json
{
  "strategy": "ensemble",
  "questions_tested": 20,
  "recall_at_1": 0.65,
  "recall_at_3": 0.85,
  "recall_at_5": 0.90,
  "avg_chunks_retrieved": 4.7,
  "per_question": [...]
}
```

**`POST /rag/compare-strategies` — comparaison 3 chunkers (J1 après-midi) :**
```python
@router.post("/compare-strategies")
async def compare_strategies(query: str) -> dict:
    """
    Lance fixed + recursive + ensemble sur la même query.
    Montre la différence de chunks récupérés selon la stratégie.
    """
```
Retourne pour chaque stratégie : `chunks_count`, `sources[]`, `top_excerpt`.

---

### BLOC 3 — `homebutler/llm/provider.py` : Prompt caching + streaming

**Ajouter `get_llm_cached()` :**
```python
def get_llm_cached(temperature: float = 0.1, max_tokens: int = 1024):
    """
    Version Anthropic avec prompt caching (beta 'prompt-caching-2024-07-31').
    Réduit le coût token du system prompt de ~90% après le premier appel.
    Pédagogie J3 : optimisation production.
    """
    if config.LLM_PROVIDER == "anthropic":
        return ChatAnthropic(
            model=config.ANTHROPIC_MODEL,
            api_key=config.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_tokens=max_tokens,
            model_kwargs={
                "extra_headers": {"anthropic-beta": "prompt-caching-2024-07-31"}
            },
        )
    return get_llm(temperature, max_tokens)
```

**Ajouter paramètre `streaming` :**
```python
def get_llm(temperature=0.1, max_tokens=1024, streaming=False):
    # ajouter streaming=streaming dans ChatAnthropic et ChatOllama
```

---

### BLOC 4 — `homebutler/llm/prompts.py` : BARE_LLM_TEMPLATE

```python
BARE_LLM_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", CONCIERGE_SYSTEM_PROMPT),
    ("human", "{question}"),
])
```
Ce template **n'injecte aucun contexte documentaire** — intentionnel pour la démo de hallucination (J1 matin). Utilisé par `mode="llm_only"`.

---

### BLOC 5 — `homebutler/agent/react_agent.py` : Mémoire de session + debug

**Refactoring `get_session_agent()` :**
```python
from langchain.memory import ConversationBufferWindowMemory

_sessions: dict[str, AgentExecutor] = {}

def get_session_agent(session_id: str = "default") -> AgentExecutor:
    """
    Retourne un agent avec mémoire conversationnelle par session_id.
    k=6 : garde les 6 derniers tours (3 questions + 3 réponses).
    Pédagogie J2 : agent qui garde le contexte conversationnel.
    """
    if session_id not in _sessions:
        memory = ConversationBufferWindowMemory(
            k=6,
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
        )
        _sessions[session_id] = get_agent_executor(memory=memory)
    return _sessions[session_id]
```

Le prompt hub `hwchase17/react-chat` (variante avec `chat_history`) sera utilisé à la place de `hwchase17/react` pour supporter la mémoire. Fallback local mis à jour pour inclure `{chat_history}`.

**`get_agent_executor()` avec `return_intermediate_steps` conditionnel :**
```python
def get_agent_executor(verbose=True, debug=False, memory=None) -> AgentExecutor:
    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=verbose,
        max_iterations=8,
        handle_parsing_errors=True,
        return_intermediate_steps=debug,  # pour le mode debug de l'API
        memory=memory,
        callbacks=callbacks or None,
    )
```

---

### BLOC 6 — `api/main.py` : Rate limiting + sécurité renforcée

**Ajouter `slowapi` pour le rate limiting (J3 TP "risques exposition") :**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

Décorateur sur les endpoints sensibles :
```python
@router.post("")
@limiter.limit("30/minute")   # max 30 requêtes/min par IP
async def chat(request: Request, req: ChatRequest):
```

**Étendre les patterns d'injection** (actuellement 10 regex) :
Ajouter : `"répète tes instructions"`, `"what is your system prompt"`, `"DAN mode"`, `"developer mode"`, `"simulate"`, `"roleplay"`, `"jeu de rôle"`, `"fais semblant"`, `"en tant qu'IA sans restrictions"`.

**Ajouter validation API Key optionnelle :**
```python
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if config.API_KEY and api_key != config.API_KEY:
        raise HTTPException(status_code=401, detail="Clé API invalide")
```

**Inclure le nouveau router :**
```python
from api.routers import chat, consumption, products, orders, rag
app.include_router(rag.router)
```

**Ajouter `slowapi` à `requirements.txt`.**

---

### BLOC 7 — `notebooks/01_llm_baseline.ipynb` : Cellules HuggingFace (J1 TP)

Ajouter **4 cellules** en début de notebook (marquées `# 🔵 COLAB SEULEMENT`) :

**Cellule A — Install Colab :**
```python
# !pip install transformers torch accelerate
```

**Cellule B — HuggingFace pipeline() :**
```python
from transformers import pipeline

# Charge un LLM open-source via HuggingFace (nécessite GPU T4 sur Colab)
generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2",
                     device_map="auto", torch_dtype="auto")
```

**Cellule C — Test des 5 questions (même questions que section Ollama) :**
```python
for q in QUESTIONS:
    resp = generator(f"[INST] {q} [/INST]", max_new_tokens=200)[0]["generated_text"]
    print(f"Q: {q[:50]}...\nR: {resp[-200:]}\n")
```

**Cellule D — Comparaison HuggingFace vs Ollama :**
Tableau comparatif `HF pipeline vs Ollama via LangChain` : setup, vitesse, intégration LangChain, usage en production.

Garder toutes les cellules Ollama existantes, mais les marquer `# 🟢 LOCAL + COLAB`.

---

### BLOC 8 — `notebooks/02_ingestion_vectorisation.ipynb` : Cellule LlamaIndex + Weaviate

Ajouter **1 cellule** après la section FAISS/ChromaDB :

**Cellule — Panorama des outils de pipeline (PDF mentionne LlamaIndex, Haystack, Weaviate) :**
```python
# LlamaIndex : alternative à LangChain (syntaxe plus concise pour l'indexation)
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# documents = SimpleDirectoryReader("data/documents").load_data()
# index = VectorStoreIndex.from_documents(documents)
# query_engine = index.as_query_engine()
# print(query_engine.query("Quelle est la marque de ma chaudière ?"))

# Comparaison des outils
outils = pd.DataFrame({
    "Outil": ["LangChain", "LlamaIndex", "Haystack"],
    "Point fort": ["Agents + écosystème", "Index avancés + LLM routing", "Pipeline NLP industriel"],
    "Usage typique": ["Agents, RAG custom", "Knowledge bases, RAG", "NLP prod enterprise"],
    "Courbe d'apprentissage": ["Moyenne", "Faible", "Élevée"],
})
print(outils.to_string(index=False))
```

Et un tableau de comparaison `FAISS vs ChromaDB vs Weaviate` (conceptuel, pas d'implémentation Weaviate) :
```python
vectorstores = pd.DataFrame({
    "Base": ["FAISS", "ChromaDB", "Weaviate"],
    "Type": ["En mémoire/fichier", "SQLite local", "Serveur distant"],
    "Filtres metadata": ["Non natif", "Oui", "Oui (avancé)"],
    "Mise à l'échelle": ["Limité", "Moyen", "Production-grade"],
    "Usage dans ce projet": ["Notices figées", "FAQ dynamique", "Production VPS"],
})
```

---

### BLOC 9 — `scripts/augment_qa_dataset.py` : Augmentation 150→500 paires

**Objectif** : Passer de 150 à ~500 paires via 3 techniques d'augmentation (PDF : "Augmentation des données").

```python
"""
Augmente le dataset QA de 150 à ~500 paires via :
  1. Paraphrase de la question (variation de formulation)
  2. Reformulation de la réponse (variation de style mais même information)
  3. Questions négatives / contre-exemples
"""

def paraphrase_question(q: str) -> list[str]:
    """Génère 2 variantes de formulation pour chaque question."""
    # Règles linguistiques simples (sans LLM pour reproductibilité)
    variants = []
    # Variante 1 : forme interrogative → forme affirmative
    if q.startswith(("Comment", "Pourquoi", "Quand", "Où", "Que", "Quel")):
        variants.append(q.replace("Comment ", "De quelle manière ").replace("?", " ?"))
    # Variante 2 : ajout de contexte HomeButler
    variants.append(f"En tant que locataire, {q[0].lower()}{q[1:]}")
    return variants[:2]

def augment_dataset(input_path, output_path, target_size=500):
    ...
    # Lit concierge_qa.jsonl (150 paires)
    # Pour chaque paire, génère des variantes
    # Shuffles et limite à target_size
    # Écrit augmented_concierge_qa.jsonl
```

Output : `data/qa_dataset/augmented_concierge_qa.jsonl` (500 paires, catégorisées).
Le script original `concierge_qa.jsonl` (150 paires) est préservé.

---

### BLOC 10 — `notebooks/03_finetuning_lora.ipynb` : LoRA/QLoRA complet (Colab)

Notebook en **8 sections** pour Google Colab (GPU T4, 15-20 min d'entraînement) :

**Section 1 — Théorie : Fine Tuning Complet vs LoRA vs QLoRA**
```markdown
| Approche | Params modifiés | VRAM | Temps | Cas d'usage |
|---|---|---|---|---|
| Full fine-tuning | 100% (7B = 28 Go) | 80+ Go | 10h+ | Réentraînement complet |
| LoRA | ~0.1% (matrices Q,V) | 16 Go | 1-2h | Adaptation domaine |
| QLoRA | idem mais 4-bit | 8-10 Go | 1-2h | GPU accessible (T4) |
```
Explication des matrices LoRA : `W = W₀ + α × (BA)` où B et A sont de rang r.

**Section 2 — Setup Colab**
```python
# !pip install transformers peft trl bitsandbytes datasets mlflow accelerate
# import drive pour récupérer concierge_qa.jsonl
```

**Section 3 — Chargement et augmentation du dataset**
```python
# Charge augmented_concierge_qa.jsonl (500 paires)
# Affiche distribution par catégorie (équipements, droits, énergie, marketplace)
# Convertit au format instruction Mistral : "<s>[INST] {instruction}\n{input} [/INST] {output} </s>"
# Split train/test : 450/50
```

**Section 4 — Chargement modèle base en QLoRA 4-bit**
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    quantization_config=bnb_config,
    device_map="auto",
)
```

**Section 5 — Configuration LoRA**
```python
from peft import LoraConfig, get_peft_model
lora_config = LoraConfig(
    r=8,                          # rang des matrices adaptatrices
    lora_alpha=16,                # facteur de mise à l'échelle
    target_modules=["q_proj", "v_proj"],  # matrices Q et V de l'attention
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```
Explication pédagogique : impact de `r` (rang) sur le nombre de paramètres entraînés.

**Section 6 — Entraînement avec SFTTrainer + MLFlow**
```python
import mlflow
mlflow.set_experiment("homebutler-finetuning")

with mlflow.start_run():
    mlflow.log_params({"r": 8, "lora_alpha": 16, "epochs": 3, "dataset_size": 450})
    
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=lora_config,
        max_seq_length=512,
        args=TrainingArguments(
            output_dir="./homebutler-lora",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            logging_steps=25,
            eval_steps=50,
            save_steps=100,
            learning_rate=2e-4,
            fp16=True,
            report_to="none",  # MLFlow gère le tracking
        ),
    )
    trainer.train()
    mlflow.log_metrics({"final_loss": trainer.state.log_history[-1]["loss"]})
```

**Section 7 — Évaluation : avant/après + métriques**
```python
# Comparaison qualitative : 5 questions de test
questions_test = [
    "Mon lave-linge fait un bruit bizarre, que faire ?",
    "Quelle est la température de nuit pour ma chaudière ?",
    "Puis-je avoir un chien dans mon appartement ?",
    "Ma consommation est-elle normale ?",
    "Où trouver du pain artisanal près de chez moi ?"
]

# Modèle BASE (avant fine-tuning) → ton neutre, générique
# Modèle FINE-TUNÉ → ton HomeButler, chaleureux, propose des artisans
for q in questions_test:
    print(f"Q: {q}")
    print(f"AVANT: {model_base.generate(q)[:200]}")
    print(f"APRÈS: {model_finetuned.generate(q)[:200]}\n")

# Métriques quantitatives (ROUGE-L sur test set)
from rouge_score import rouge_scorer
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
# Calcule ROUGE-L sur 50 exemples test
```

**Section 8 — Distillation (concept + code)**
```python
# Distillation : compresser les connaissances d'un "teacher" (grand modèle) 
# dans un "student" (modèle plus petit)
# Teacher : Claude claude-sonnet-4-6 (Anthropic API)
# Student : Phi-3 mini 3.8B ou Mistral 7B fine-tuné

# Génération de labels "soft" via le teacher :
# teacher_logits = teacher(question)  # distribution de probabilités
# student_loss = KL_divergence(student_logits, teacher_logits)  # distillation loss

# Note : La distillation est hors scope de ce TP (nécessite GPU A100+)
# On la montre conceptuellement ici.
```

**Section 9 — Quantization GGUF + Ollama**
```bash
# Après entraînement : merge LoRA + export GGUF 4-bit
# !pip install llama-cpp-python
# python -c "
# from peft import PeftModel
# merged = PeftModel.from_pretrained(base_model, './homebutler-lora').merge_and_unload()
# merged.save_pretrained('./homebutler-merged')
# "
# Sur machine locale avec llama.cpp :
# ./convert-hf-to-gguf.py ./homebutler-merged --outtype q4_k_m --outfile homebutler-q4.gguf
# Taille : 7B → ~4.1 Go (vs 14 Go en FP16)

# Ollama : charger le modèle local
# Modelfile :
# FROM ./homebutler-q4.gguf
# SYSTEM "Tu es HomeButler, conciergerie domestique..."
# ollama create homebutler -f Modelfile
# ollama run homebutler
```
Puis : changer `LLM_PROVIDER=ollama` dans `.env` → tout le projet bascule.

---

## Ordre d'exécution recommandé

1. **Bloc 3-4-5** (`provider.py`, `prompts.py`, `react_agent.py`) — fondations, les blocs suivants en dépendent
2. **Bloc 1** (`chat.py`) — enrichissement principal
3. **Bloc 2** (`rag.py`) — nouveaux endpoints
4. **Bloc 6** (`main.py`) — rate limiting + inclure rag router
5. **Bloc 9** (`augment_qa_dataset.py`) — script simple et indépendant
6. **Bloc 7** (cellules notebook 01) — ajout non destructif
7. **Bloc 8** (cellule notebook 02) — ajout non destructif
8. **Bloc 10** (notebook 03) — le plus long, mais indépendant

---

## Vérification end-to-end

```bash
# 0. Restart API après changements
source .venv/bin/activate && pip install slowapi && uvicorn api.main:app --port 8000 --reload

# 1. Mode llm_only (doit halluciner — J1 matin)
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Quelle est la marque de ma chaudière ?","mode":"llm_only"}'
# Attendu : réponse vague ou inventée + token_usage{"input_tokens":..., "output_tokens":...}

# 2. Mode rag_only avec debug (doit citer notice_chaudiere.pdf — J1 après-midi)
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Quelle est la marque de ma chaudière ?","mode":"rag_only","debug":true}'
# Attendu : "Viessmann" + sources[{source:"notice_chaudiere.pdf", page:1, excerpt:"..."}]

# 3. Compare 3 modes en parallèle (J3 TP — évaluation comparative)
curl -X POST http://localhost:8000/chat/compare \
  -H 'Content-Type: application/json' \
  -d '{"message":"Quelle est la marque de ma chaudière ?"}'
# Attendu : llm_only hallucine, rag_only = Viessmann, agent = Viessmann + artisans

# 4. Mémoire conversationnelle
curl -X POST http://localhost:8000/chat -d '{"message":"Quelle est ma chaudière ?","session_id":"s1"}'
curl -X POST http://localhost:8000/chat -d '{"message":"Et quand faut-il la réviser ?","session_id":"s1"}'
# Attendu : 2e réponse utilise le contexte de la 1ère (sait qu'on parle de la Viessmann)

# 5. RAG retrieve (transparence J1)
curl -X POST http://localhost:8000/rag/retrieve \
  -d '{"query":"température nuit chaudière","strategy":"recursive","k":4}'
# Attendu : 4 chunks de notice_chaudiere.pdf avec excerpts

# 6. RAG evaluate (Recall@K J1 TP)
curl -X POST http://localhost:8000/rag/evaluate \
  -d '{"strategy":"recursive","sample_size":20}'
# Attendu : recall_at_3 >= 0.70

# 7. RAG compare-strategies (J1 après-midi — 3 chunkers)
curl -X POST http://localhost:8000/rag/compare-strategies \
  -d '{"query":"comment purger mes radiateurs"}'
# Attendu : 3 blocs fixed/recursive/ensemble avec chunks différents

# 8. Streaming SSE (J3 déploiement)
curl -N "http://localhost:8000/chat/stream?message=Bonjour+HomeButler"
# Attendu : tokens arrivant un par un (data: Bon\ndata:jour\n...)

# 9. Rate limiting (J3 sécurité)
for i in {1..35}; do curl -s -o /dev/null -w "%{http_code}\n" \
  -X POST http://localhost:8000/chat -d '{"message":"test"}'; done
# Attendu : 30 × 200, puis 5 × 429 (Too Many Requests)

# 10. Augmentation dataset
source .venv/bin/activate && python scripts/augment_qa_dataset.py
# Attendu : data/qa_dataset/augmented_concierge_qa.jsonl avec ~500 paires
wc -l data/qa_dataset/augmented_concierge_qa.jsonl
```
