📝 Slide 1 : Atelier 03 — Pipeline Agent ReAct (mission en un coup d'œil)

POURQUOI passer du RAG à l'agent ?

Le RAG de AT02 répond bien à « Quelle est la marque de ma chaudière ? » (réponse statique dans les PDFs). Il rate « Il fait -5 °C demain, comment je prépare ma maison et que puis-je commander à un producteur local ? » — qui nécessite la météo (API externe), la notice chaudière (RAG) et le catalogue producteurs (autre service), assemblés dans un raisonnement. C'est exactement ce qu'un agent ReAct fait : il alterne RAISONNEMENT (Thought) et ACTION (appel d'outil) jusqu'à la réponse finale.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| `tools.py` (DÉJÀ FOURNI corrigé) | 4 outils LangChain : RAG, météo, énergie, marketplace | Lecture du pattern `@tool` — pas le pivot AT03 |
| `vectorstore_chroma.py` (DÉJÀ FOURNI) | Wrapper ChromaDB (filtres métadonnées) | Transposition de FAISS — faible valeur ajoutée à blanker |
| `retriever.py` → `get_ensemble_retriever` (À CODER) | Combine FAISS (60 %) + Chroma (40 %) | Concept hybrid retrieval — équilibre sens + filtre |
| `react_agent.py` → `get_agent_executor` (À CODER) | Assemble LLM + prompt ReAct + tools en un AgentExecutor | Concept central : la boucle ReAct |

> 💡 **Branche élève** : `git checkout student/03-pipeline-agent`. Scope réduit : seulement 2 fonctions blankées (vs 4 envisagé) pour rester sous le budget 1h40.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI ne pas blanker `tools.py` ?

`tools.py` est 4 fois le même pattern `@tool` LangChain (RAG, météo, énergie, marketplace). Le blanker 4 fois dépasserait le calibrage 1h40 sans ajouter de valeur pédagogique nouvelle (tu vois le pattern UNE fois dans `react_agent.py` quand tu regardes comment `ALL_TOOLS` est consommé). De même, `vectorstore_chroma.py` est une transposition mécanique de `vectorstore_faiss.py` (déjà codé en AT02).

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/rag/ingestion.py`, `vectorstore_faiss.py` | ✅ Acquis AT02 | RAG déjà fait |
| `homebutler/rag/vectorstore_chroma.py` | ✅ Fourni corrigé | Transposition FAISS — faible nouveauté |
| `homebutler/agent/tools.py` (`ALL_TOOLS`) | ✅ Fourni corrigé | Lecture du pattern `Tool(name, func, description)` |
| `homebutler/agent/react_agent.py` → `get_agent_executor` | 🛠️ **À CODER** | Concept central : ReAct |
| `homebutler/rag/retriever.py` → `get_ensemble_retriever` | 🛠️ **À CODER** | Concept central : hybrid retrieval |
| `homebutler/rag/retriever.py` → `get_faiss_retriever`, `get_chroma_retriever` | ✅ Fourni | Briques consommées par l'ensemble |


📝 Slide 3 : Concept #1 — Hybrid retrieval avec EnsembleRetriever

POURQUOI combiner FAISS et ChromaDB avec des poids ?

FAISS est excellent en recherche sémantique pure (« cherche le concept proche de cette question »). ChromaDB ajoute le filtrage par métadonnées (« cherche uniquement dans les docs de type 'équipement' »). Combiner les deux via une fusion de rangs (RRF, Reciprocal Rank Fusion) augmente le Recall de 5 à 15 points par rapport à FAISS seul, en gardant la diversité des sources.

**Signature à compléter** :

```python
def get_ensemble_retriever(faiss_k=4, chroma_k=3):
    """Combine get_faiss_retriever (déjà écrit) et get_chroma_retriever (idem)
    dans un retriever unique exposant .invoke(query) → list[Document].
    """
    raise NotImplementedError(...)
```

**Indice léger** — LangChain expose une classe `Ensemble…` qui prend une liste de retrievers et une liste de poids (ils doivent sommer à 1.0). Tu instancies tes deux retrievers de base puis tu les empaquettes.

**Indice fort** — `EnsembleRetriever(retrievers=[faiss_retriever, chroma_retriever], weights=[0.6, 0.4])`. Le score final d'un chunk = somme pondérée de `1/(rank + k_smoothing)` de chaque retriever. Poids 0.6/0.4 = FAISS DOMINE mais Chroma corrige les cas où le filtre métadonnées apporte un chunk que FAISS rate. Si tu mettais `[1.0, 0.0]` → FAISS seul (pas d'apport Chroma). Si `[0.5, 0.5]` → ex aequo (bon pour la diversité mais on perd la précision sémantique).

| Stratégie | Recall@5 typique | Cas d'usage |
|-----------|------------------|-------------|
| FAISS seul (poids [1.0, 0.0]) | 0.72 | Questions sémantiques pures |
| FAISS dominant ([0.6, 0.4]) | 0.85 | Mix sémantique + besoin de diversité |
| Chroma dominant ([0.3, 0.7]) | 0.78 | Données très structurées (filtres prioritaires) |

> 💡 **Analogie** : un sommelier qui combine SA mémoire (FAISS, sens du goût) et le CATALOGUE filtré (Chroma, par région/cépage). Les deux signaux pondérés donnent la meilleure recommandation.

**📚 Dépendances natives utilisées**

- `langchain.retrievers.EnsembleRetriever(...)` — combine plusieurs retrievers via Reciprocal Rank Fusion (RRF). Paramètres :
  - `retrievers: list[BaseRetriever]` — liste des retrievers à combiner (ex. `[faiss_retriever, chroma_retriever]`).
  - `weights: list[float]` — un poids par retriever, doit sommer à 1.0 (sinon LangChain normalise). Ex. `[0.6, 0.4]`.
  - `c: int = 60` — constante de lissage du RRF (`score = Σ weight × 1/(rank + c)`). Plus `c` est grand, plus les rangs profonds comptent.
  - `id_key: str | None` — clé metadata pour identifier un doc (pour dédupliquer entre retrievers).

- `vectorstore.as_retriever(search_type, search_kwargs)` — convertit un VectorStore en `Retriever`. Paramètres :
  - `search_type: "similarity" | "mmr" | "similarity_score_threshold"` — `"similarity"` = top-k brut, `"mmr"` = Maximal Marginal Relevance (diversité), `"similarity_score_threshold"` = filtre par score min.
  - `search_kwargs: dict` — ex. `{"k": 4, "fetch_k": 20, "lambda_mult": 0.5}` (lambda_mult pour MMR : 0 = max diversité, 1 = max pertinence).

- Interface `Retriever.invoke(query: str) → list[Document]` — l'API LangChain standard, consommée par les tools et l'AgentExecutor.


📝 Slide 4 : Concept #2 — La boucle ReAct (le détective)

POURQUOI ReAct plutôt qu'un appel LLM unique avec tous les contextes ?

Si on injecte la météo + 4 chunks RAG + 5 producteurs dans un seul prompt, on dépasse vite le contexte du modèle ET on dilue l'attention. ReAct résout ça en mode incrémental : le LLM RÉFLÉCHIT à ce dont il a besoin, APPELLE UN seul outil, LIT l'observation, puis recommence. Au bout de 3-5 itérations, il a tout ce qu'il faut, sans surcharge.

**Signature à compléter** :

```python
def get_agent_executor(verbose=True, debug=False, memory=None):
    """Assemble : LLM + prompt ReAct (hub LangChain ou fallback local) + ALL_TOOLS
    en un AgentExecutor exécutable via .invoke({"input": "...", "chat_history": []}).
    """
    raise NotImplementedError(...)
```

**Indice léger** — Le pattern LangChain ReAct se déroule en 3 étapes : (1) obtenir un LLM (utilise `get_llm()` d'AT01 avec `temperature=0.1, max_tokens=2048`), (2) charger un prompt ReAct (depuis `hub.pull("hwchase17/react-chat")` ou un fallback local), (3) appeler `create_react_agent(llm, ALL_TOOLS, prompt)` puis envelopper dans un `AgentExecutor(...)`.

**Indice fort** — Paramètres clés d'`AgentExecutor` : `tools=ALL_TOOLS`, `max_iterations=8` (anti-boucle infinie ; au-delà de 8, abandon), `handle_parsing_errors=True` (récupère gracieusement les outputs LLM mal formés), `return_intermediate_steps=debug` (expose la trace si debug=True, sinon économise des tokens), `memory=memory` (`ConversationBufferWindowMemory(k=6)` injecté par session_id). Le prompt **`hwchase17/react-chat`** supporte `{chat_history}`, le simple **`react`** ne le supporte pas — choisis le bon.

> 💡 **Analogie détective** : Sherlock Holmes ne répond pas à « qui a tué le colonel ? » par une intuition. Il fait : *Thought : « il me faut l'arme »* → *Action : interroge le valet* → *Observation : couteau dans la cuisine* → *Thought : « maintenant le mobile »* → *Action : lit les lettres* → ... → *Final Answer*. ReAct = le détective scripté.

⚠️ **Piège** — si `max_iterations` est trop bas (1 ou 2), l'agent abandonne avant d'avoir interrogé tous les outils nécessaires. Trop haut (50) et il peut boucler indéfiniment sur un problème mal posé. 8 est le sweet spot pour 3-5 outils + réponse finale.

**📚 Dépendances natives utilisées**

- `langchain.agents.create_react_agent(llm, tools, prompt)` — construit un agent ReAct (Runnable qui produit l'output au format ReAct). Paramètres :
  - `llm: BaseLanguageModel` — le LLM (issu de `get_llm()` d'AT01).
  - `tools: list[BaseTool]` — la liste des outils utilisables (ici `ALL_TOOLS`).
  - `prompt: BasePromptTemplate` — doit contenir `{tools}`, `{tool_names}`, `{agent_scratchpad}`, et optionnellement `{chat_history}` pour la mémoire.

- `langchain.hub.pull(repo_name)` — télécharge un prompt depuis le hub LangChain (https://smith.langchain.com/hub).
  - `repo_name: str` — ex. `"hwchase17/react-chat"` (avec `{chat_history}`) ou `"hwchase17/react"` (sans).
  - ⚠️ Nécessite une connexion internet ; toujours prévoir un fallback local.

- `langchain.agents.AgentExecutor(...)` — wrapper qui exécute la boucle Thought → Action → Observation. Paramètres :
  - `agent: Runnable` — l'agent issu de `create_react_agent`.
  - `tools: list[BaseTool]` — mêmes outils que ceux passés à l'agent.
  - `verbose: bool` — log la boucle en console (utile en dev, à `False` en prod).
  - `max_iterations: int = 15` — anti-boucle infinie. 8 est notre sweet spot.
  - `handle_parsing_errors: bool | str | callable` — `True` = retry gracieux si LLM produit un format mal formé. Sinon crash.
  - `return_intermediate_steps: bool` — `True` expose la trace `[(AgentAction, observation), ...]` dans le résultat (mode debug).
  - `memory: BaseMemory | None` — mémoire conversationnelle injectée (voir ci-dessous).
  - `callbacks: list[BaseCallbackHandler] | None` — handlers de tracing (Langfuse, LangSmith).
  - `early_stopping_method: "force" | "generate"` — `"force"` (default) stop sec à max_iterations ; `"generate"` laisse le LLM produire une réponse finale même si interrompu.

- `langchain.memory.ConversationBufferWindowMemory(k, memory_key, return_messages, input_key, output_key)` — mémoire de fenêtre glissante. Paramètres :
  - `k: int = 5` — nombre de tours de conversation à conserver. 6 est notre default.
  - `memory_key: str` — nom de la variable injectée dans le prompt (ex. `"chat_history"`).
  - `return_messages: bool` — `True` retourne des `BaseMessage`, `False` un `str` formaté.


📝 Slide 5 : Pipeline complet — du message utilisateur à la réponse multi-outils

POURQUOI vue d'ensemble ?

L'agent reçoit la question, choisit l'outil RAG, lit les chunks, puis choisit l'outil météo si besoin, etc. Le tout en boucle. La memory `k=6` garde les 6 derniers tours pour le « comme tu m'as dit avant ».

```
Utilisateur : "Il fait -5 °C demain, comment je prépare ma maison et qu'est-ce que je peux commander à un producteur local ?"
   │
   ▼
[AgentExecutor]
   │ Thought : "Il me faut d'abord la météo réelle de demain"
   │ Action  : get_weather(input="demain")
   │ Observation : "Temp min -5, neige légère"
   │
   │ Thought : "Maintenant la notice chaudière pour le mode hiver"
   │ Action  : search_home_docs(input="chaudière mode hiver -5°C")
   │ Observation : "[notice_chaudiere.pdf, p.4] Activer le mode hivernal..."
   │
   │ Thought : "Et les producteurs locaux pour des plats chauds"
   │ Action  : find_local_products(input="soupe légumes hiver")
   │ Observation : "Ferme Dupont — 5 km — soupes 4€"
   │
   │ Thought : "J'ai tout ce qu'il faut"
   │ Final Answer : "Demain -5°C avec neige. 1) Active le mode hivernal de
   │   ta chaudière Vitodens [notice p.4]. 2) Pour te réchauffer, la Ferme
   │   Dupont (5 km) propose des soupes de saison à 4€."
   ▼
Réponse + sources tracées + 3 outils utilisés (visible si debug=True)
```

**Critère de succès** :
```bash
pytest ateliers/atelier-03-pipeline-agent/bugs/test_v1.py -v
# 🎯 test vert ; agent respecte max_iterations=8 ; intermediate_steps contient
#   au moins 3 outils distincts pour la question multi-source du test.
```


📝 Slide 6 : Récap — démarrer sur la branche `student/03-pipeline-agent`

POURQUOI cet ordre ?

`get_ensemble_retriever` doit exister AVANT que `tools.py` (déjà fourni) puisse importer `retrieve(use_ensemble=True)`. `get_agent_executor` consomme `ALL_TOOLS` qui consomme le retriever. Donc : retriever d'abord, agent ensuite.

```bash
# 1. Setup
git checkout student/03-pipeline-agent
python -m venv .venv && source .venv/bin/activate && pip install -e .
bash scripts/check_atelier_ready.sh 03
# Vérifie que data/faiss_index/ ET data/chroma_db/ existent

# 2. Coder dans l'ordre
#    a) homebutler/rag/retriever.py  → get_ensemble_retriever (poids [0.6, 0.4])
#    b) homebutler/agent/react_agent.py → get_agent_executor (max_iter=8, etc.)

# 3. Tester
pytest ateliers/atelier-03-pipeline-agent/                              # tronc commun
python ateliers/atelier-03-pipeline-agent/checkpoints/check_1.py        # QCM + verbalisation
pytest ateliers/atelier-03-pipeline-agent/bugs/test_v1.py -v            # 🎯 test multi-outils

# 4. En dernier recours
git diff student/03-pipeline-agent atelier/03-pipeline-agent -- homebutler/agent/react_agent.py
git diff student/03-pipeline-agent atelier/03-pipeline-agent -- homebutler/rag/retriever.py
```

⚠️ **Piège AT03** — `tools.py` reste corrigé (hors-scope). Si tu te retrouves à modifier `tools.py`, c'est que tu sors du périmètre. Garde-fou : le `.claude/CLAUDE.md` te le rappellera.

> 💡 **Tip** : avant de regarder le diff, modifie `weights=[0.5, 0.5]` puis `[0.8, 0.2]` et observe l'impact sur le test. C'est le meilleur moyen d'INTERNALISER l'effet des poids.
