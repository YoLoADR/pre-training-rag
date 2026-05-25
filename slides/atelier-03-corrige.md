📝 Slide 1 : Atelier 03 — Pipeline Agent ReAct (mission en un coup d'œil)

POURQUOI passer du RAG à l'agent ?

Le RAG de AT02 répond bien à « Quelle est la marque de ma chaudière ? » (réponse statique dans les PDFs). Il rate « Il fait -5 °C demain, comment je prépare ma maison et que puis-je commander à un producteur local ? » — qui nécessite la météo (API externe), la notice chaudière (RAG) et le catalogue producteurs (autre service), assemblés dans un raisonnement. C'est exactement ce qu'un agent ReAct fait : il alterne RAISONNEMENT (Thought) et ACTION (appel d'outil) jusqu'à la réponse finale.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| `tools.py` (DÉJÀ FOURNI corrigé) | 4 outils LangChain : RAG, météo, énergie, marketplace | Lecture pédagogique du pattern `@tool` — pas le pivot AT03 |
| `vectorstore_chroma.py` (DÉJÀ FOURNI) | Wrapper ChromaDB (filtres métadonnées) | Transposition de FAISS — faible valeur ajoutée à blanker |
| `retriever.py` → `get_ensemble_retriever` (À CODER) | Combine FAISS (60 %) + Chroma (40 %) | Concept hybrid retrieval — équilibre sens + filtre |
| `react_agent.py` → `get_agent_executor` (À CODER) | Assemble LLM + prompt ReAct + tools en un AgentExecutor | Concept central : la boucle ReAct |

> 💡 **Branche élève** : `git checkout student/03-pipeline-agent`. Scope réduit Rev 2 : seulement 2 fonctions blankées (vs 4 envisagé) pour rester sous le budget 1h40.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI ne pas blanker `tools.py` ?

`tools.py` est 4 fois le même pattern `@tool` LangChain (RAG, météo, énergie, marketplace). En blanker 4 fois ferait dépasser le calibrage 1h40 sans ajouter de valeur pédagogique nouvelle (l'élève voit le pattern UNE fois dans `react_agent.py` quand il regarde comment `ALL_TOOLS` est consommé). De même, `vectorstore_chroma.py` est une transposition mécanique de `vectorstore_faiss.py` (déjà codé en AT02).

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

FAISS est excellent en recherche sémantique pure (« cherche le concept proche de cette question »). ChromaDB ajoute le filtrage par métadonnées (« cherche uniquement dans les docs de type 'équipement' »). Combiner les deux via `EnsembleRetriever` (Reciprocal Rank Fusion) augmente le Recall de 5 à 15 points par rapport à FAISS seul, en gardant la diversité des sources.

**Évolution à apporter** :

```python
# AVANT : NotImplementedError
# APRÈS :

def get_ensemble_retriever(faiss_k=4, chroma_k=3):
    # AVANTAGE : un seul retriever en sortie, qui DÉLÈGUE en interne aux deux
    # vector stores. Le reste du code (agent, /rag/retrieve) ne change pas.
    faiss_retriever  = get_faiss_retriever(k=faiss_k)
    chroma_retriever = get_chroma_retriever(k=chroma_k)

    return EnsembleRetriever(
        retrievers=[faiss_retriever, chroma_retriever],
        weights=[0.6, 0.4],
        #  ↑ POIDS CRITIQUES. Dans le RRF (Reciprocal Rank Fusion), le score
        #    final d'un chunk = somme pondérée de 1/(rank+k_smoothing) de chaque
        #    retriever. Poids 0.6/0.4 = FAISS DOMINE mais Chroma corrige les cas
        #    où le filtre métadonnées apporte un chunk que FAISS rate.
        #
        #    Si on mettait [0.5, 0.5] : ex aequo — bon pour la diversité mais
        #    on perd parfois la précision sémantique pure de FAISS.
        #    Si on mettait [1.0, 0.0] : c'est FAISS seul — pas d'apport Chroma.
    )
```

| Stratégie | Recall@5 typique | Cas d'usage |
|-----------|------------------|-------------|
| FAISS seul (poids [1.0, 0.0]) | 0.72 | Questions sémantiques pures |
| FAISS dominant ([0.6, 0.4]) | 0.85 | Mix sémantique + besoin de diversité |
| Chroma dominant ([0.3, 0.7]) | 0.78 | Données très structurées (filtres prioritaires) |

> 💡 **Analogie** : un sommelier qui combine SA mémoire (FAISS, sens du goût) et le CATALOGUE filtré (Chroma, par région/cépage). Les deux signaux pondérés donnent la meilleure recommandation.


📝 Slide 4 : Concept #2 — La boucle ReAct (le détective)

POURQUOI ReAct plutôt qu'un appel LLM unique avec tous les contextes ?

Si on injecte la météo + 4 chunks RAG + 5 producteurs dans un seul prompt, on dépasse vite le contexte du modèle ET on dilue l'attention. ReAct résout ça en mode incrémental : le LLM RÉFLÉCHIT à ce dont il a besoin, APPELLE UN seul outil, LIT l'observation, puis recommence. Au bout de 3-5 itérations, il a tout ce qu'il faut, sans surcharge.

**Évolution à apporter** :

```python
# AVANT : NotImplementedError
# APRÈS :

def get_agent_executor(verbose=True, debug=False, memory=None):
    # AVANTAGE : on factorise la création de l'agent. Le même builder est
    # appelé par get_session_agent() (avec mémoire) ET get_singleton_agent()
    # (sans, pour l'API). DRY.

    llm = get_llm(temperature=0.1, max_tokens=2048)
    #  ↑ T=0.1 (factuel) + max_tokens=2048 (l'agent peut produire 5 Thought/
    #    Action/Observation avant la réponse finale — donc plus de tokens
    #    nécessaires qu'un appel direct).

    # On tente le prompt OFFICIEL via le hub LangChain.
    # AVANTAGE : "react-chat" supporte {chat_history} (mémoire conversationnelle),
    # vs le simple "react" qui ne la supporte pas.
    try:
        prompt = hub.pull("hwchase17/react-chat")
    except Exception:
        # Fallback OFFLINE : si pas d'accès internet, on utilise notre version
        # locale du prompt ReAct (définie dans _build_fallback_prompt).
        prompt = _build_fallback_prompt()

    callbacks = _setup_tracing()  # Langfuse ou LangSmith selon TRACING_PROVIDER

    # Construit l'AGENT (sans exécuteur) : un Runnable qui produit l'output
    # ReAct au format texte structuré.
    agent = create_react_agent(llm, ALL_TOOLS, prompt)

    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=verbose,
        max_iterations=8,
        #  ↑ ANTI-BOUCLE INFINIE. Si le LLM hésite, il peut boucler indéfiniment
        #    (Thought → Action → Observation → Thought → ...). 8 itérations =
        #    largement assez pour 3-5 outils + réponse finale. Au-delà : abandon.
        handle_parsing_errors=True,
        #  ↑ Le LLM produit parfois un format non conforme (ex: pas de "Action:").
        #    Au lieu de crasher, on récupère gracieusement et on re-prompte.
        return_intermediate_steps=debug,
        #  ↑ Si debug=True, l'AgentExecutor expose la trace complète à l'API
        #    (pour le mode debug du /chat). Sinon on ne renvoie que la réponse
        #    finale (économise les tokens dans la réponse HTTP).
        memory=memory,
        #  ↑ ConversationBufferWindowMemory(k=6) injecté par session_id pour
        #    permettre la mémoire conversationnelle ("comme tu m'as dit avant").
        callbacks=callbacks if callbacks else None,
    )
```

> 💡 **Analogie détective** : Sherlock Holmes ne répond pas à « qui a tué le colonel ? » par une intuition. Il fait : *Thought : « il me faut l'arme »* → *Action : interroge le valet* → *Observation : couteau dans la cuisine* → *Thought : « maintenant le mobile »* → *Action : lit les lettres* → ... → *Final Answer*. ReAct = le détective scripté.


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
# → test vert ; agent respecte max_iterations=8 ; intermediate_steps contient
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

⚠️ **Piège AT03** — `tools.py` reste corrigé (scope Rev 2). Si tu te retrouves à modifier `tools.py`, c'est que tu sors du périmètre. Garde-fou : le `.claude/CLAUDE.md` te le rappellera.

> 💡 **Tip** : avant de regarder le diff, modifie `weights=[0.5, 0.5]` puis `[0.8, 0.2]` et observe l'impact sur le test. C'est le meilleur moyen d'INTERNALISER l'effet des poids.
