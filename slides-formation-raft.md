📝 Slide 1 : Programme de la formation — 3 jours pour maîtriser RAG et Fine Tuning

POURQUOI avoir une vue d'ensemble avant de plonger dans les détails ?

Une formation dense de 3 jours sur des technologies qui évoluent vite peut rapidement perdre le fil. Ce slide est la carte du voyage : à chaque instant, vous saurez où vous en êtes et pourquoi l'étape du moment est nécessaire pour celle qui suit. Chaque chapitre construit une couche du projet fil rouge HomeButler AI.

| Jour | Chapitre | Titre | Ce que vous saurez faire |
|------|----------|-------|--------------------------|
| 1 | 1 | Introduction aux LLM et concepts RAG | Situer LLM, RAG et Fine Tuning dans l'écosystème IA |
| 1 | 2 | Création d'un RAG simple avec Python | Indexer des PDFs, interroger un vectorstore, évaluer la qualité |
| 2 | 3 | Intégration dans un pipeline RAG | Assembler un agent ReAct multi-outils avec LangChain |
| 2 | 4 | Fine-tuning avec HuggingFace | Préparer un dataset LoRA/QLoRA, lancer un entraînement |
| 3 | 5 | Déploiement, optimisation et supervision | Quantiser, exposer via FastAPI, monitorer en production |
| 3 | 6 | Fine Tuning vs RAG | Choisir la bonne architecture avec un arbre de décision |

Fil rouge **HomeButler AI** : à la fin du Jour 3, vous aurez construit une application de conciergerie domestique intelligente — agent ReAct, pipeline RAG, API FastAPI, interface Streamlit, déployée sur VPS avec Docker Compose.

> 💡 60 % du temps est consacré aux travaux pratiques. La théorie sert à comprendre pourquoi les choix techniques sont faits — pas à mémoriser des formules.


📝 Slide 2 : Historique — de l'attention aux systèmes hybrides (2017-2026)

POURQUOI retracer l'histoire avant de coder ?

Les technologies RAG et Fine Tuning ne sont pas apparues de nulle part. Chacune répond à une limite concrète de la précédente génération. Comprendre la généalogie permet de comprendre les contraintes actuelles — et d'anticiper les prochaines ruptures.

| Année | Événement | Limite résolue | Nouvelle limite créée |
|-------|-----------|----------------|----------------------|
| 2017 | Transformer — "Attention Is All You Need" (Vaswani et al.) | RNN lent et séquentiel | Coût quadratique de l'attention |
| 2018 | BERT + GPT-1 | Pas de pré-entraînement généraliste | Fine-tuning complet très coûteux |
| 2020 | GPT-3 (175B) — few-shot sans réentraînement | Besoin de fine-tuner pour chaque tâche | Knowledge cutoff, hallucinations |
| 2020 | RAG — Lewis et al., Meta AI (arxiv:2005.11401) | Connaissance figée dans les poids | Latence de retrieval |
| 2022 mars | InstructGPT (RLHF) — 1,3B > 175B en qualité humaine | LLM difficile à aligner sur les intentions | Alignement coûteux en annotations |
| 2022 nov | ChatGPT — 100 M utilisateurs en 2 mois | IA de langage réservée aux experts | Attentes irréalistes sur les capacités |
| 2021 | LoRA (Hu et al., arxiv:2106.09685) | Fine-tuning complet = 140 GB GPU | Rank à tuner, qualité légèrement réduite |
| 2023 | QLoRA (Dettmers et al., arxiv:2305.14314) | LoRA nécessite encore GPU A100 | Complexité de la quantification 4-bit |
| 2023 | LLaMA (Meta) + Mistral (Paris) | LLM open-source de qualité insuffisante | Infrastructure GPU pour self-hosting |
| 2024 | RAFT (Zhang et al., arxiv:2403.10131) | RAG et FT combinés naïvement = fragilité au bruit | Complexité d'entraînement sur oracle + distracteurs |

> 💡 Chaque technologie de ce cours est la réponse directe à une limite documentée. Quand vous rencontrez une contrainte en projet, c'est probablement déjà dans cette timeline — et la solution aussi.


📝 Slide 3 : Comparatifs et tendances 2026 — où en est l'écosystème ?

POURQUOI s'intéresser aux tendances avant de commencer ?

L'écosystème LLM évolue tous les 3 à 6 mois. Les outils que vous apprenez aujourd'hui seront les fondations — mais certains choix techniques de 2023 sont déjà obsolètes. Ce slide positionne les décisions du cours dans le contexte actuel et donne des repères pour anticiper les prochains changements.

**Comparatif modèles open-source vs fermés (mai 2026)**

| Modèle | Type | Paramètres | Points forts | Usage recommandé |
|--------|------|-----------|-------------|-----------------|
| GPT-4o (OpenAI) | Fermé | Non divulgué | Multimodal, SOTA général | Production cloud, budget disponible |
| Claude Sonnet 4 (Anthropic) | Fermé | Non divulgué | Raisonnement, code, sécurité | Production cloud, conformité |
| Llama 3.1 70B (Meta) | Open-source | 70B | Qualité proche GPT-4, Apache 2.0 | Self-hosting GPU |
| Mistral Large (Mistral AI) | Fermé/Open | 123B | Excellent français, efficace | Projets francophones |
| Mistral 7B / Mixtral 8×7B | Open-source | 7B / 47B | Léger, rapide, Apache 2.0 | CPU/GPU modeste, fine-tuning |
| Gemma 2 (Google) | Open-source | 9B / 27B | Efficace, licence permissive | Recherche, éducation |

**Tendances 2026 à connaître**

| Tendance | Ce qui change | Impact pour ce cours |
|----------|--------------|----------------------|
| RAG multi-modal | Images + texte dans le même index | Nos principes de chunking s'appliquent aux deux |
| Agents autonomes long-horizon | Boucles multi-étapes sans intervention humaine | Pattern ReAct reste la base — on l'étend |
| LLM sur device (smartphones) | Modèles < 3B quantisés en 4-bit | QLoRA et GGUF deviennent encore plus stratégiques |
| Coûts d'inférence divisés par 10 en 3 ans | GPT-4 coûtait 100× plus cher en 2023 | L'arbitrage cloud vs local se rééquilibre |
| Réglementation IA (EU AI Act) | Obligations de traçabilité et d'explicabilité | LangSmith/Langfuse deviennent des outils de conformité |

⚠️ **Point de vigilance** — Les benchmarks publics (MMLU, HumanEval) mesurent des capacités générales. Votre cas d'usage métier peut donner des classements très différents. Toujours évaluer sur vos propres données avant de choisir un modèle.

---

Chapitre 1 : Introduction aux LLM et concepts RAG — Jour 1


🎯 Objectif du chapitre

Comprendre pourquoi les LLM ont transformé l'IA en trois ans, identifier leurs limites fondamentales (hallucination, knowledge cutoff), situer le RAG et le Fine Tuning comme les deux réponses complémentaires à ces limites, et découvrir le projet fil rouge HomeButler AI que vous construirez sur les 3 jours de formation.


📝 Slide 1 : L'explosion des LLM 2017-2024 — pourquoi maintenant ?

POURQUOI un tel changement en si peu de temps ?

Avant 2017, les modèles de langage étaient des architectures séquentielles (RNN, LSTM) entraînées sur des tâches isolées. L'article "Attention Is All You Need" (Vaswani et al., Google Brain, 2017) a tout changé en introduisant le mécanisme de self-attention, qui permet à chaque token de "regarder" tous les autres simultanément. Le parallélisme massif rendu possible par les GPU a fait le reste.

| Année | Modèle / Événement | Rupture |
|-------|-------------------|---------|
| 2017 | Transformer (Vaswani et al.) | Self-attention remplace RNN/CNN — parallélisme GPU massif |
| 2018 | BERT + GPT-1 | Pré-entraînement + fine-tuning devient le nouveau paradigme |
| 2020 | GPT-3 175B | Few-shot learning sans réentraînement |
| 2022 mars | InstructGPT (RLHF, 1,3B params) | Surpasse GPT-3 175B sur l'évaluation humaine |
| 2022 nov | ChatGPT | 100 millions d'utilisateurs en 2 mois — record absolu |
| 2023 | LLaMA (Meta) + Mistral (Paris) | Open-source démocratise l'accès aux grands modèles |
| 2024 | Llama 3, Mistral Large, Claude 3 | Convergence qualité open-source / fermé |

> 💡 ChatGPT est l'application qui a atteint 100 millions d'utilisateurs le plus vite de l'histoire du numérique — deux fois plus vite que TikTok.

⚠️ **Idée reçue n°1** — "Plus grand = meilleur" : InstructGPT avec 1,3 milliards de paramètres surpasse GPT-3 avec 175 milliards après alignement RLHF. La technique d'entraînement compte autant que la taille.


📝 Slide 2 : L'architecture Transformer — l'attention est tout

POURQUOI toutes les IA de langage partagent-elles la même architecture depuis 2017 ?

Le Transformer a résolu trois problèmes que les architectures précédentes ne pouvaient pas traiter efficacement : les dépendances à longue portée dans le texte, le parallélisme à l'entraînement, et la capacité à généraliser à des tâches très différentes sans réarchitecturer le modèle.

L'intuition du mécanisme d'attention : chaque token calcule un score d'importance avec chaque autre token de la séquence. Le mot "banque" dans "je vais à la banque" et dans "la banque du fleuve" produit des représentations différentes grâce à ce contexte dynamique.

| Critère | Avant Transformer (RNN/LSTM) | Après Transformer |
|---------|------------------------------|-------------------|
| Parallélisme entraînement | Séquentiel (lent) | Massif (GPU-friendly) |
| Dépendances longues | Difficile (gradient vanishing) | Natif (self-attention) |
| Scalabilité | Limitée | Quasi-illimitée (GPT-3 → GPT-4) |
| Multimodalité | Non | Texte + images + code + audio |

Les 5 composants à retenir : Tokenizer → Embedding → Self-Attention → Feed-Forward → Output distribution

> 💡 Un LLM ne "comprend" pas le texte au sens humain — il prédit le prochain token le plus probable selon les patterns statistiques de son corpus d'entraînement. Cette nuance est fondamentale pour anticiper les hallucinations.


📝 Slide 3 : Forces et faiblesses d'un LLM — connaître les limites avant de coder

POURQUOI anticiper les limites d'un LLM évite des bugs coûteux en production ?

Un LLM entraîné une fois est gelé dans le temps. Il ne connaît pas les événements postérieurs à sa date de coupure, peut inventer des faits avec une confiance apparente, et ses performances dégradent sur les raisonnements formels complexes. Connaître ces limites dès le départ oriente les choix d'architecture.

| Dimension | Force | Limite réelle |
|-----------|-------|---------------|
| Connaissance générale | Vaste corpus d'entraînement | Knowledge cutoff (figé à la date d'entraînement) |
| Génération de texte | Fluide, cohérente, multilingue | Hallucinations : 8 à 42 % selon le domaine |
| Polyvalence | Code, traduction, résumé, Q&A | Raisonnement formel et mathématique fragile |
| Personnalisation | Fine-tuning possible | Catastrophic forgetting sans précautions |
| Déploiement | API standardisées | Coût par token + latence non nulle |

> 💡 Le taux d'hallucination varie de 8 % sur des questions factuelles générales à 42 % sur des domaines techniques sans contexte fourni (benchmarks 2024). Le RAG ramène ce taux à 0-6 %.

⚠️ **Piège classique** — Tester un LLM uniquement sur des cas favorables pendant le développement : en production, les cas-limites révèlent les failles au pire moment.


📝 Slide 4 : L'écosystème Python LLM — la carte des outils

POURQUOI cartographier l'écosystème avant d'ouvrir un notebook ?

En 2026, l'écosystème LLM Python compte des centaines de bibliothèques. Sans carte mentale des 4 couches fonctionnelles, on installe des outils redondants, on résout les mauvais problèmes avec les mauvais outils, et on accumule des dépendances incompatibles.

| Couche | Outils principaux | Rôle dans la chaîne |
|--------|------------------|---------------------|
| Modèles et API | HuggingFace Hub, Anthropic API, Ollama, OpenAI | Accéder au LLM (local ou cloud) |
| Orchestration | LangChain 0.3, LlamaIndex, Haystack | Enchaîner les appels, gérer la mémoire, les agents |
| Vectorstores | FAISS (local), ChromaDB (persistant), Pinecone (cloud) | Stocker et rechercher les embeddings |
| Évaluation et observabilité | LangSmith, Langfuse, MLflow, RAGAs | Tracer, débugger, mesurer la qualité |

Dans ce cours, chaque outil correspond à un rôle précis. On n'installe rien "au cas où".

> 💡 La règle d'or : choisir l'outil le plus simple qui résout le problème. Un appel API direct surpasse LangChain pour un usage ponctuel sans chaîne.


📝 Slide 5 : Open-source vs modèles fermés — une décision d'architecture

POURQUOI le choix du modèle est-il une décision d'architecture et non de préférence ?

Choisir entre Mistral, LLaMA et GPT-4 ou Claude engage des décisions sur la confidentialité des données, le coût d'inférence, la capacité de personnalisation, et la dépendance à un fournisseur. Ce choix conditionne toute l'architecture du système.

| Critère | Open-source (Mistral, Llama 3) | Fermé (GPT-4, Claude, Gemini) |
|---------|-------------------------------|-------------------------------|
| Coût d'inférence | Hébergement propre (fixe) | $0,01 à $0,06 par 1 000 tokens |
| Confidentialité | Données on-premise | Données envoyées au provider |
| Fine-tuning | Total (accès aux poids) | Limité ou payant (API) |
| Performance SOTA | Proche (Mistral surpasse GPT-3.5) | Légèrement supérieure en 2025 |
| Maintenance infra | À votre charge | Gérée par le provider |
| Offline possible | Oui (Ollama, Jan.ai) | Non |

⚠️ **Piège** — Choisir open-source par principe sans GPU disponible : un modèle 7B quantisé sur CPU peut prendre 20 à 60 secondes par réponse, ce qui rend l'application inutilisable.


📝 Slide 6 : Qu'est-ce que le RAG ? — l'origine du problème

POURQUOI le RAG est-il né d'un problème de dates et non d'un problème de taille ?

Un LLM entraîné sur des données jusqu'en décembre 2023 ne connaît rien de ce qui s'est passé ensuite. Il ne connaît pas non plus vos documents internes, vos contrats, vos notices produits. La solution naïve — réentraîner le modèle — coûte des millions de dollars et prend des semaines. Lewis et al. (Meta AI, 2020) ont proposé une alternative : injecter dynamiquement le contexte pertinent dans le prompt.

| Problème | Sans RAG | Avec RAG |
|----------|----------|----------|
| Données récentes (post-entraînement) | Hallucination ou "je ne sais pas" | Récupérées dynamiquement depuis l'index |
| Documents propriétaires | Inconnus du modèle | Indexés et retrouvables à la demande |
| Source de l'information | Opaque (paramètres du modèle) | Traçable (chunk source retourné) |
| Mise à jour des connaissances | Réentraînement coûteux | Réindexation rapide (minutes) |
| Taux d'hallucination | 8 à 42 % | 0 à 6 % |

> 💡 RAG = mémoire externe non-paramétrique. Le modèle reste gelé, seule la base de données évolue. C'est l'origine du papier de référence : Lewis et al., "RAG for Knowledge-Intensive NLP Tasks", Meta AI, 2020 (arxiv:2005.11401).


📝 Slide 7 : Qu'est-ce que le Fine Tuning ? — apprendre vs mémoriser

POURQUOI fine-tuner un modèle quand on peut déjà lui passer du contexte dans le prompt ?

Le RAG résout le problème des connaissances manquantes. Il ne résout pas le problème du comportement : ton de marque, style de réponse, raisonnement spécialisé métier, format de sortie contraint. Pour ces cas, il faut modifier les poids du modèle, c'est-à-dire le fine-tuner.

| Technique | Mécanisme | Modifie les poids ? | Coût de mise en œuvre |
|-----------|-----------|--------------------|-----------------------|
| Prompting seul | Instructions dans le prompt | Non | Quasi nul |
| RAG | Contexte injecté dynamiquement | Non | Moyen (indexation) |
| Fine-tuning complet | Tous les paramètres réentraînés | Oui (100 %) | Élevé (GPU A100) |
| LoRA / QLoRA (PEFT) | Petites matrices ajoutées aux poids gelés | Partiellement (0,1-1 %) | Faible à modéré |

Évolution historique : BERT full fine-tuning (2018) → LoRA (Hu et al., juin 2021) → QLoRA (Dettmers et al., mai 2023) → RAFT combinant RAG et FT (Zhang et al., mars 2024).

> 💡 Analogie : le RAG donne au modèle une bibliothèque à consulter. Le fine-tuning lui enseigne un nouveau métier. Les deux peuvent coexister dans la même architecture.


📝 Slide 8 : RAG vs Fine Tuning — première vue d'ensemble

POURQUOI choisir le bon outil dès le départ évite des semaines de refactorisation ?

La confusion entre RAG et Fine Tuning est l'une des erreurs de conception les plus fréquentes en 2024-2025. Certains projets fine-tunent pour des données qui changent chaque semaine (coût de réentraînement permanent) ; d'autres utilisent le RAG pour des besoins de style et de ton (résultat médiocre malgré un retrieval parfait). Ce tableau est à garder sous la main lors de la phase de conception.

| Critère | RAG gagne | Fine Tuning gagne |
|---------|-----------|-------------------|
| Données changeant fréquemment | ✓ Réindexation rapide | ✗ Réentraînement coûteux |
| Ton et style de marque | ✗ Le contexte ne change pas le comportement | ✓ Modification des poids |
| Citations et traçabilité requises | ✓ Chunk source retourné | ✗ Connaissance opaque |
| Budget GPU limité | ✓ Pas d'entraînement | ✗ GPU obligatoire |
| Latence critique (< 500 ms) | ✗ Retrieval ajoute 500 ms | ✓ Réponse directe |
| Moins de 500 exemples disponibles | ✓ Pas de données d'entraînement requises | ✗ Overfitting quasi garanti |
| Mise en production en < 1 semaine | ✓ | ✗ |

> 💡 Dans 90 % des projets, le RAG est la première étape. Le Fine Tuning vient ensuite combler les gaps que le RAG ne peut pas combler.


📝 Slide 9 : 5 idées reçues à démystifier

POURQUOI les idées reçues sur les LLM génèrent-elles des erreurs de conception coûteuses ?

Les cinq idées reçues suivantes reviennent systématiquement dans les projets IA. Chacune conduit à des décisions d'architecture défectueuses ou à des attentes irréalistes envers les modèles.

| Idée reçue | Réalité mesurée |
|-----------|-----------------|
| "Plus grand = meilleur" | InstructGPT 1,3B > GPT-3 175B après RLHF — la technique compte autant que la taille |
| "Les LLM comprennent le langage" | Prédiction de token suivant — pas de modèle du monde, pas de compréhension causale |
| "Le Fine Tuning suffit" | Knowledge cutoff + coût de réentraînement permanent pour les données changeantes |
| "Le RAG est complexe" | 50 lignes Python avec LangChain suffisent pour un premier prototype fonctionnel |
| "Les hallucinations sont rares" | 8 à 42 % sans RAG selon le domaine — mesurées sur benchmarks 2024 |

⚠️ **Risque réel** — Exposer un LLM en production sans évaluation d'hallucination : plusieurs entreprises ont subi des incidents clients (réponses incorrectes présentées avec confiance) dont le coût réputationnel a dépassé le coût de développement.


📝 Slide 10 : HomeButler AI — le projet fil rouge des 3 jours

POURQUOI construire une vraie application de bout en bout plutôt que des exemples isolés ?

Les exemples isolés illustrent des concepts mais ne montrent pas comment les composants interagissent, ni quels pièges surviennent à l'intégration. HomeButler AI est une application de conciergerie domestique intelligente — réelle, fonctionnelle, déployable — que vous construirez couche par couche au fil de la formation.

| Composant | Technologie | Chapitre qui le construit |
|-----------|-------------|--------------------------|
| 6 PDFs notices + CSV énergie 365j | PyMuPDF (fitz) + Pandas | Chapitre 2 |
| Pipeline RAG + vectorstores | FAISS + ChromaDB + FastEmbedEmbeddings | Chapitre 2 |
| Agent ReAct 4 outils | LangChain 0.3 + hwchase17/react | Chapitre 3 |
| Dataset 150 Q&A pairs | Scripts génération + format JSONL | Chapitre 4 |
| API REST sécurisée | FastAPI 0.115 + 4 routers | Chapitre 5 |
| Interface utilisateur | Streamlit (4 pages) + Gradio (prototype) | Chapitre 5 |
| Déploiement reproductible | Docker Compose + VPS Linux | Chapitre 5 |

Architecture cible : Utilisateur → Streamlit → FastAPI → Agent ReAct → RAG + 4 services

> 💡 HomeButler tourne sur Mac Intel (Python 3.13.5) et sur VPS Linux via Docker. Chaque piège d'installation rencontré est documenté et sera montré en TP.


🎓 Ce que vous devez retenir — Chapitre 1

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| Timeline 2017-2024 | ChatGPT = disruption en 2 mois — comprendre le contexte explique l'urgence actuelle |
| Architecture Transformer | Base commune à tous les LLM — comprendre l'attention explique les forces et les limites |
| Hallucinations 8-42 % | Chiffre à citer en projet pour justifier l'investissement RAG |
| Écosystème en 4 couches | Choisir le bon outil pour le bon rôle évite les dépendances inutiles |
| Open-source vs fermé | Décision d'architecture avec conséquences coût, confidentialité, maintenance |
| RAG = mémoire externe | Répond au problème du knowledge cutoff sans réentraînement |
| Fine Tuning = adaptation comportementale | Pour le style, le ton, le raisonnement spécialisé — pas pour les données qui changent |
| RAG d'abord, FT ensuite | 90 % des projets suivent cet ordre — valider le gap avant de fine-tuner |
| 5 idées reçues | Les connaître prévient les erreurs de conception les plus fréquentes |
| HomeButler AI | 40 fichiers, 6 chapitres, un système hybride complet à la fin du Jour 3 |


➡️ Prochain chapitre

Les fondations théoriques sont posées. On passe maintenant à la pratique : comprendre les 5 composantes d'un RAG (embedding, vectorstore, chunking, retrieval, génération), comparer les stratégies de découpage, et appliquer ces concepts immédiatement aux 6 PDFs notices de HomeButler AI.

---

Chapitre 2 : Création d'un RAG simple avec Python — Jour 1


🎯 Objectif du chapitre

Maîtriser les 5 composantes d'un pipeline RAG (chargement, découpage, embedding, stockage vectoriel, récupération + génération), identifier la stratégie de chunking adaptée à son type de document, comprendre les métriques d'évaluation, et appliquer ces concepts aux données HomeButler AI pour produire un premier chatbot fonctionnel.


📝 Slide 1 : Les 5 composantes d'un RAG — le flux de bout en bout

POURQUOI comprendre chaque étape avant de copier un tutoriel ?

Les tutoriels RAG donnent souvent l'impression que "ça marche" sans expliquer pourquoi. En production, les problèmes viennent presque toujours d'une étape mal configurée — et sans comprendre le rôle de chaque composant, on ne sait pas où chercher. Les 5 étapes se divisent en deux phases temporelles très différentes.

| Étape | Ce que ça fait | Phase | Fréquence d'exécution |
|-------|---------------|-------|----------------------|
| 1. Chargement | Lire PDFs, CSV, JSON, pages web | Indexation | Une fois (ou à chaque mise à jour) |
| 2. Découpage (chunking) | Diviser les documents en segments cohérents | Indexation | Une fois |
| 3. Embedding | Convertir chaque chunk en vecteur numérique | Indexation | Une fois |
| 4. Stockage vectoriel | Indexer les vecteurs pour recherche rapide | Indexation | Une fois |
| 5. Récupération + Génération | Retrouver les chunks pertinents → répondre | Inférence | À chaque requête utilisateur |

> 💡 Les étapes 1 à 4 sont des coûts fixes (calculés une seule fois). L'étape 5 est le coût variable (exécuté à chaque question). Optimiser les étapes 1-4 améliore la qualité ; optimiser l'étape 5 réduit la latence.


📝 Slide 2 : Les embeddings — transformer du texte en vecteurs

POURQUOI la similitude sémantique n'est-elle pas un simple calcul de mots-clés ?

Une recherche par mots-clés échoue sur les synonymes et les paraphrases : "voiture" ne correspond pas à "automobile", "comment réparer" ne correspond pas à "procédure de maintenance". Les embeddings convertissent le texte en vecteurs denses où la distance entre vecteurs représente la proximité sémantique, indépendamment des mots exacts utilisés.

| Modèle d'embedding | Dimension | Taille | Multilingue | Usage recommandé |
|---------------------|-----------|--------|-------------|-----------------|
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 100 Mo (ONNX) | ✓ | Notre formation — CPU, multilingue |
| BAAI/bge-base-en-v1.5 | 768 | 270 Mo | ✗ | Projets anglophones performance |
| text-embedding-ada-002 | 1 536 | API cloud | ✗ | Production OpenAI (payant) |
| mxbai-embed-large | 1 024 | 350 Mo | Partiel | Qualité SOTA locale |

Dans HomeButler, on utilise FastEmbedEmbeddings avec paraphrase-multilingual-MiniLM-L12-v2 — 384 dimensions, ONNX (sans torch), environ 100 Mo en cache.

⚠️ **Piège** — Le premier chargement du modèle d'embedding télécharge 100 à 470 Mo dans `~/.cache`. Prévoir ce délai avant le TP et tester la connexion réseau.


📝 Slide 3 : Bases de données vectorielles — FAISS, ChromaDB, Pinecone

POURQUOI ne pas stocker les embeddings dans un simple tableau NumPy ou un DataFrame Pandas ?

Pour 100 chunks, un DataFrame suffit. Pour 100 000 chunks, la recherche brute (calculer la distance avec chaque vecteur) prend plusieurs secondes. Les bases vectorielles utilisent des structures d'indexation spécialisées (HNSW, IVF) qui permettent une recherche en quelques millisecondes même sur des millions de vecteurs.

| Critère | FAISS | ChromaDB | Pinecone |
|---------|-------|----------|----------|
| Type | Bibliothèque in-memory | Base locale persistante | SaaS cloud géré |
| Persistance | Sauvegarde manuelle (.index) | Automatique (dossier local) | Automatique (cloud) |
| Filtrage métadonnées | Limité | Natif | Natif + avancé |
| Scalabilité | Limité par la RAM | Millions de chunks | Milliards de vecteurs |
| Coût | Gratuit | Gratuit | Payant au-delà du free tier |
| Cas HomeButler | ✓ Recherche principale (vitesse) | ✓ Persistance entre sessions | ✗ |

> 💡 HomeButler utilise les deux simultanément via EnsembleRetriever : FAISS pour la vitesse de recherche (poids 0,6) et ChromaDB pour la persistance et le filtrage par métadonnées (poids 0,4).


📝 Slide 4 : Chunking — l'art de découper les documents

POURQUOI la qualité du découpage détermine-t-elle 80 % de la qualité du RAG ?

Le LLM ne "lit" jamais vos documents entiers. Il reçoit uniquement les fragments (chunks) que le retriever a jugés pertinents. Si un chunk coupe une explication au milieu d'une phrase, le LLM répond à partir d'un contexte incomplet. Si un chunk est trop grand, il dilue l'information pertinente dans du bruit.

| Stratégie | Principe | Avantage | Inconvénient | Idéale pour |
|-----------|---------|---------|-------------|-------------|
| Fixed-size | 400 tokens fixes, 50 tokens overlap | Simple, prévisible | Coupe les phrases, ignore la structure | Données non structurées (logs, CSV) |
| Recursive Character | Séparateurs hiérarchiques (paragraphe → ligne → phrase → espace) | Respecte la structure naturelle | Taille variable | PDFs structurés avec titres (notre cas) |
| Semantic (SemanticChunker) | Découpe aux ruptures sémantiques mesurées | Très cohérent thématiquement | Lent, coûteux, embedding requis | Corpus premium, petits volumes |

Dans HomeButler, les 3 stratégies sont utilisées en parallèle sur les 6 PDFs notices. Le TP mesure laquelle donne le meilleur rappel sur le jeu de questions de test.


📝 Slide 5 : Bonnes pratiques de chunking

POURQUOI 80 % de la qualité d'un RAG se joue au moment du découpage ?

Le chunking est une décision irréversible à l'indexation. Si on se rend compte 3 semaines plus tard que la taille choisie est mauvaise, il faut réindexer l'ensemble du corpus. Mieux vaut passer 2 heures à tester différentes configurations avant de passer en production.

| Décision | Bonne pratique | Anti-pattern à éviter |
|----------|---------------|----------------------|
| Taille de chunk | 400 à 512 tokens (contexte lisible, pas trop dilué) | 50 tokens (trop fragmenté) ou 2 000 tokens (context overflow) |
| Overlap | 10 à 20 % (40 à 100 tokens) | 0 % overlap — perd les transitions entre chunks |
| Métadonnées | Ajouter source, numéro de page, date dans chaque chunk | Aucune métadonnée — impossible de filtrer par source ou période |
| Séparateurs | Adapter au format du document (PDF ≠ Markdown ≠ CSV) | Même stratégie pour tous les types de documents |
| Validation | Inspecter visuellement 20 chunks tirés au sort avant d'indexer | Indexer sans relecture et découvrir les problèmes en prod |

⚠️ **Piège FAISS** — Réindexer sans supprimer l'index précédent accumule les chunks en doublon. Toujours supprimer le fichier .index ou utiliser l'option `force_rebuild` avant une réindexation complète.


📝 Slide 6 : Recherche sémantique et récupération

POURQUOI retrouver les bons documents est-il plus difficile qu'il n'y paraît ?

La recherche sémantique dense fonctionne bien sur les questions avec synonymes et paraphrases. Mais elle rate souvent les termes techniques exacts, les numéros de référence, les noms propres. La recherche sparse (BM25) excelle sur les correspondances exactes mais ignore la sémantique. L'approche hybride combine les deux.

| Méthode | Principe | Force | Limite |
|---------|----------|-------|--------|
| Dense (cosine similarity) | Vecteur requête vs vecteurs corpus | Sémantique, synonymes, multilingue | Moins efficace sur termes exacts |
| Sparse (BM25) | Fréquence et rareté des mots-clés | Correspondance exacte, rapide | Ignore la sémantique |
| Hybride (EnsembleRetriever) | Dense (0,6) + BM25 (0,4) pondérés | Cumule les forces des deux | Plus complexe à configurer |
| MMR (Max Marginal Relevance) | Pertinence + diversité | Évite les doublons dans les résultats | Léger trade-off qualité/vitesse |

Stat clé : le RAG avec retrieval hybride atteint 89 % d'accuracy sur des tâches de QA ouvert, contre 60 à 70 % sans retrieval.

> 💡 Dans HomeButler, l'EnsembleRetriever combine FAISS (dense, poids 0,6) et ChromaDB (BM25, poids 0,4) avec MMR activé pour éviter de renvoyer plusieurs fois le même passage.


📝 Slide 7 : Reranking — pourquoi les 5 premiers ne suffisent pas

POURQUOI récupérer 10 chunks pour n'en garder que 3 dans le prompt final ?

Le retriever initial (bi-encoder) est rapide mais imprécis. Il retourne les k chunks les plus proches vectoriellement, mais "proche" ne signifie pas toujours "pertinent pour la question posée". Un reranker (cross-encoder) évalue chaque paire (question, chunk) séparément, avec une précision bien supérieure, au prix d'une latence supplémentaire.

| Étape | Modèle type | Vitesse | Précision | Rôle |
|-------|------------|---------|-----------|------|
| Retrieval initial (bi-encoder) | Modèle d'embedding | Rapide (< 50 ms) | Bonne | Candidats larges (top-10 à top-20) |
| Reranking (cross-encoder) | cross-encoder/ms-marco | Modéré (100 à 200 ms) | Très bonne | Sélection finale (top-3 à top-5) |
| Sans reranking | — | Rapide | Variable | Bruit possible dans le contexte LLM |

> 💡 Le reranking est souvent la seule optimisation qui produit un gain immédiatement visible sur la qualité des réponses, sans modifier l'indexation ni le modèle. Gain mesuré : +15 à 30 % de précision selon les benchmarks RAGAs 2024.


📝 Slide 8 : Métriques d'évaluation d'un RAG

POURQUOI mesurer un RAG autrement qu'avec "ça marche" ou "ça marche pas" ?

Sans métriques objectives, il est impossible de comparer deux configurations de chunking, de choisir entre deux modèles d'embedding, ou de détecter une régression après une mise à jour. Le framework RAGAs (2023) propose 4 métriques complémentaires qui couvrent les deux parties du pipeline.

| Métrique | Ce qu'elle mesure | Valeur cible | Symptôme si faible |
|----------|------------------|--------------|-------------------|
| Faithfulness | La réponse est-elle fidèle aux chunks récupérés ? | > 0,85 | Hallucination post-retrieval — le LLM invente malgré le contexte |
| Answer Relevance | La réponse répond-elle à la question posée ? | > 0,80 | Prompt ou template mal formulé |
| Context Precision | Les chunks récupérés sont-ils pertinents ? | > 0,75 | Chunking ou modèle d'embedding à revoir |
| Context Recall | Le bon chunk a-t-il été récupéré ? | > 0,70 | Top-k trop petit ou index de mauvaise qualité |

⚠️ **Piège** — Évaluer uniquement avec des questions que vous avez vous-même écrites et dont vous connaissez les réponses : biais de confirmation. Utiliser les 150 Q&A pairs HomeButler comme jeu de test indépendant.


📝 Slide 9 : Anti-patterns RAG — les erreurs classiques

POURQUOI la majorité des projets RAG en production échouent-ils sur des détails d'implémentation ?

Le RAG est simple à prototyper en 50 lignes mais difficile à faire fonctionner en production. Les 5 anti-patterns suivants représentent 80 % des problèmes rencontrés dans les projets réels.

| Anti-pattern | Symptôme observable | Correction |
|-------------|---------------------|------------|
| Chunking fixe sans overlap | Réponses tronquées, contexte coupé au milieu d'une explication | Recursive splitter + 10-20 % overlap |
| Pas de reranking | Réponses génériques, bruit dans le contexte | Ajouter cross-encoder après retrieval initial |
| Context window débordé | Erreur de tokens ou réponse incohérente | Limiter chunk_size × top_k < fenêtre contexte |
| Aucune métadonnée sur les chunks | Impossible de filtrer par source ou date | Enrichir chaque chunk à l'indexation (source, page, date) |
| FAISS rechargé sans le flag requis | Erreur silencieuse ou crash au chargement | Toujours `allow_dangerous_deserialization=True` |


📝 Slide 10 : HomeButler RAG — construire la première brique

POURQUOI les concepts RAG s'appliquent-ils directement aux données HomeButler ?

Les 6 PDFs de notices équipements, le CSV d'énergie 365 jours, et le catalogue de 30 producteurs locaux constituent la base documentaire de HomeButler. Ce slide montre comment chaque concept du chapitre se traduit en une décision concrète d'implémentation.

| Source de données | Format | Nb documents | Stratégie chunking retenue |
|------------------|--------|-------------|---------------------------|
| Notices équipements | 6 PDFs (PyMuPDF / fitz) | ~150 pages | Recursive Character Splitter |
| Données énergie | CSV 365 jours | 1 fichier | Fixed-size par ligne |
| Catalogue producteurs | JSON 30 entrées | 1 fichier | Document entier (pas de découpage) |
| Q&A paires training | JSONL 150 paires | Dataset FT | Indexation séparée (Chapitre 4) |

Résultat après indexation : 49 chunks → FAISS (recherche principale) + ChromaDB (persistance entre sessions). Embedding : paraphrase-multilingual-MiniLM-L12-v2, 384 dimensions, 100 Mo via FastEmbed (ONNX, sans torch).

> 💡 PyMuPDF s'installe avec `pip install pymupdf` mais s'importe avec `import fitz` — ce nom hérité du projet original FreeMuPDF est une source de confusion documentée. C'est le genre de piège qu'on ne voit qu'en installation réelle.


🎓 Ce que vous devez retenir — Chapitre 2

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| 5 composantes RAG | Indexation = une fois. Retrieval + Génération = à chaque requête |
| Embedding ≠ mots-clés | Similitude sémantique capture synonymes et paraphrases |
| FAISS vs ChromaDB | FAISS pour la vitesse, ChromaDB pour la persistance — HomeButler utilise les deux |
| Recursive splitter pour PDFs | Respecte la structure naturelle des documents |
| 400-512 tokens + 10 % overlap | Consensus industrie pour le meilleur rappel |
| EnsembleRetriever hybride | Dense (0,6) + BM25 (0,4) = cumul des forces |
| Reranking | +15 à 30 % de précision pour un surcoût de 100-200 ms |
| 4 métriques RAGAs | Faithfulness / Answer Relevance / Context Precision / Context Recall |
| allow_dangerous_deserialization | Requis pour charger un index FAISS sauvegardé localement |
| import fitz (pas pymupdf) | Piège de nommage documenté — installer pymupdf, importer fitz |


➡️ Prochain chapitre

Le pipeline RAG est opérationnel et les données HomeButler sont indexées. On passe maintenant à l'orchestration : pourquoi utiliser un framework comme LangChain, comment assembler un pipeline complet, et comment implémenter un agent ReAct capable de choisir entre 4 sources de données différentes.

---

Chapitre 3 : Intégration dans un pipeline RAG — Jour 2


🎯 Objectif du chapitre

Comprendre pourquoi un framework d'orchestration accélère le développement, comparer LangChain, LlamaIndex et Haystack pour choisir en connaissance de cause, assembler un pipeline RAG complet avec LangChain 0.3, implémenter le pattern ReAct pour les agents multi-outils, et connecter l'observabilité via LangSmith ou Langfuse.


📝 Slide 1 : Pourquoi un framework ? Appels API directs vs orchestration

POURQUOI ne pas simplement appeler l'API d'Anthropic ou d'Ollama directement ?

Pour un appel unique sans contexte, l'API directe est la meilleure option. Mais dès qu'on ajoute une deuxième étape (retrieval, mémoire conversationnelle, outil externe, switch de provider), le code "artisanal" croît exponentiellement en complexité et en fragilité. Les frameworks résolvent ces problèmes de composition.

| Critère | Appels API directs | Framework LangChain 0.3 |
|---------|-------------------|-------------------------|
| Changement de LLM (Claude → Ollama) | Réécriture du code d'inférence | Changer une variable d'environnement |
| Pipeline RAG complet | ~200 lignes de code | ~20 lignes avec LCEL |
| Mémoire conversationnelle | À coder from scratch | ConversationBufferMemory intégré |
| Traçabilité des appels | Logs custom à implémenter | LangSmith natif (zéro import) |
| Agent multi-outils | Architecture complexe | AgentExecutor + liste de tools |

⚠️ **Piège** — Utiliser LangChain pour un simple appel LLM sans chaîne ni agent : on rajoute une dépendance lourde pour aucun bénéfice. La règle : n'utiliser un framework que quand il y a au moins deux étapes à composer.


📝 Slide 2 : LangChain — histoire, architecture et LCEL

POURQUOI LangChain est-il devenu le standard de facto en seulement 18 mois ?

LangChain a été lancé en octobre 2022 par Harrison Chase, une semaine avant ChatGPT. Il a profité de l'explosion d'intérêt pour les LLM pour devenir le dépôt GitHub le plus étoilé de sa catégorie en 2023. La version 0.3 (2024) a introduit LCEL (LangChain Expression Language) qui simplifie radicalement l'écriture des pipelines.

| Module LangChain | Rôle | Exemple HomeButler |
|-----------------|------|--------------------|
| Document Loaders | Charger PDFs, JSON, CSV, pages web | PyMuPDFLoader sur les 6 notices |
| Text Splitters | Découper les documents | RecursiveCharacterTextSplitter |
| Vectorstores | Indexer et rechercher | FAISS.from_documents() + ChromaDB |
| Chains (LCEL) | Assembler des étapes avec l'opérateur \| | retrieval_chain |
| Agents | Décider quelle action effectuer | AgentExecutor avec 4 tools ReAct |
| Callbacks | Observer les appels LLM | LangSmithCallbackHandler |

> 💡 LangChain 0.3 = LCEL. Le style legacy (LLMChain, SimpleSequentialChain) est déprécié mais encore fonctionnel. Ne pas mélanger les deux styles dans un même projet.


📝 Slide 3 : LangChain vs LlamaIndex vs Haystack — choisir le bon outil

POURQUOI le choix du framework impacte-t-il la maintenabilité du projet sur 2 ans ?

Les trois frameworks ont des forces différentes. Choisir le mauvais oblige à réécrire une partie de l'architecture quand les besoins évoluent. LangChain est le plus généraliste, LlamaIndex le plus optimisé pour le RAG pur, Haystack le plus orienté pipelines NLP d'entreprise.

| Critère | LangChain 0.3 | LlamaIndex 0.10 | Haystack 2.x |
|---------|--------------|----------------|-------------|
| Lancé | Octobre 2022 | Novembre 2022 | 2019 (deepset) |
| Focus principal | Orchestration générale + agents | RAG + indexation de données | Pipelines NLP / RAG entreprise |
| Agents | ✓ Natif, ReAct, multi-tools | ✓ QueryEngine Agent | ✓ Pipeline agents |
| Observabilité | LangSmith (natif, zéro config) | Phoenix / LlamaDebugger | Hayhooks |
| Communauté | Très large | Large | Moyenne |
| Cas HomeButler | ✓ Choix retenu | Alternatif possible pour RAG pur | ✗ |

Notre choix : LangChain 0.3 pour sa polyvalence agent + RAG + switch LLM, et parce que le programme RAFT l'utilise comme référence pédagogique.


📝 Slide 4 : Pipeline RAG complet avec LangChain

POURQUOI visualiser le pipeline complet avant de coder évite-t-il les refactorisations ?

Un pipeline RAG LangChain est une chaîne de 6 composants. Si on comprend le rôle de chacun avant de coder, on évite 80 % des erreurs d'architecture (mauvais ordre, mauvais types de retour, incompatibilités entre versions).

| Étape | Composant LangChain | Ce qu'il produit |
|-------|---------------------|-----------------|
| 1. Chargement | PyMuPDFLoader | Liste de Document objects |
| 2. Découpage | RecursiveCharacterTextSplitter | Liste de chunks (Document) |
| 3. Embedding | FastEmbedEmbeddings | Vecteurs 384 dimensions |
| 4. Indexation | FAISS.from_documents() | Index vectoriel .index |
| 5. Retrieval | EnsembleRetriever (FAISS + ChromaDB) | Chunks les plus pertinents |
| 6. Génération | create_retrieval_chain() | Réponse finale + sources |

Le flux LCEL s'écrit comme une composition d'étapes avec l'opérateur pipe — chaque étape reçoit la sortie de la précédente sans code de collage explicite.

⚠️ **Piège LCEL vs legacy** — Ne pas utiliser en même temps LLMChain (legacy) et LCEL (nouveau) dans le même fichier : comportements différents sur la gestion des erreurs et le streaming.


📝 Slide 5 : Tool Chains — orchestrer plusieurs sources de données

POURQUOI HomeButler a-t-il besoin de combiner 4 sources différentes dans le même agent ?

Une question utilisateur comme "est-ce que ma consommation d'électricité est normale ce mois-ci vu la météo ?" nécessite de croiser les données énergie, les données météo, et peut-être les notices d'équipement. Aucune source seule ne peut répondre. L'agent doit décider quelles sources interroger et dans quel ordre.

| Outil | Description | Données interrogées | Type de retour |
|-------|-------------|---------------------|---------------|
| search_docs | Recherche RAG dans les notices | 6 PDFs FAISS/ChromaDB | Chunks + source |
| analyze_energy | Détecte anomalies énergie | CSV 365 jours | Anomalies détectées, stats |
| find_products | Trouve producteurs locaux (haversine) | JSON 30 producteurs GPS | Liste triée par distance |
| weather_tool | Météo actuelle + cache | API externe + TTLCache 1h | Température, conditions |

Chaque outil est une fonction Python ordinaire décorée pour être reconnue par LangChain — pas de dépendance au LLM, pas de complexité cachée.

> 💡 Le découplage est total : chaque outil peut être testé indépendamment, modifié sans casser les autres. C'est l'architecture que HomeButler utilise dans `homebutler/agent/tools.py`.


📝 Slide 6 : Agents LLM — de la chaîne à la décision autonome

POURQUOI un agent répond-il mieux à une question multi-sources qu'une simple chaîne ?

Une chaîne LangChain exécute toujours les mêmes étapes dans le même ordre. Elle ne peut pas s'adapter à la question posée. Un agent, lui, reçoit la question, décide quels outils appeler, observe les résultats, et décide si une étape supplémentaire est nécessaire. Cette flexibilité est essentielle dès qu'on a plusieurs sources de données.

| Dimension | Chain LangChain | Agent LangChain |
|-----------|----------------|----------------|
| Flux d'exécution | Prédéfini, séquentiel | Dynamique, décisionnel |
| Outils utilisés | Toujours les mêmes dans le même ordre | Choisis par le LLM selon la question |
| Correction d'erreur | Impossible (linéaire) | Peut réessayer avec une autre approche |
| Coût en tokens | Prévisible | Variable (plus élevé) |
| Cas idéal | Q&A simple, résumé, traduction | Multi-sources, multi-étapes, logique conditionnelle |

⚠️ **Piège** — Un agent sans limite de tours peut boucler indéfiniment, surtout avec des modèles open-source moins fiables sur le format de sortie. Toujours fixer `max_iterations=8` et `handle_parsing_errors=True`.


📝 Slide 7 : Pattern ReAct — Thought, Action, Observation

POURQUOI ReAct est-il le pattern d'agent le plus robuste pour les LLM généralistes ?

ReAct (Yao et al., 2022) est un pattern d'inférence où le LLM alterne entre phases de raisonnement (Thought) et phases d'action (Action + Observation). Cette alternance rend le processus transparent, débogable, et auto-correcteur : si une action retourne un résultat inattendu, le LLM peut raisonner à nouveau avant la prochaine action.

| Phase | Ce que le LLM écrit | Exemple sur une question HomeButler |
|-------|---------------------|-------------------------------------|
| Thought | Raisonnement interne | "La question concerne l'énergie. Je dois appeler analyze_energy." |
| Action | Nom de l'outil + paramètre | analyze_energy("juin 2026") |
| Observation | Résultat retourné | "Anomalie détectée : +200 % en juin par rapport à la moyenne" |
| Thought | Décision suivante | "L'anomalie est identifiée. Je peux formuler la réponse." |
| Final Answer | Réponse à l'utilisateur | "Oui, votre consommation de juin est anormalement élevée..." |

Dans HomeButler, le prompt utilisé est `hwchase17/react` (LangChain Hub) — testé et validé sur Claude API et Ollama. Ne pas le modifier sans raison.


📝 Slide 8 : Observabilité — tracer chaque appel avec LangSmith ou Langfuse

POURQUOI un système LLM non tracé est-il impossible à optimiser ?

Sans traçabilité, on ne sait pas quel chunk a été récupéré pour une réponse incorrecte, quel outil l'agent a appelé en premier, ni combien de tokens coûte chaque requête. L'observabilité LLM est différente de l'observabilité applicative classique : on trace le contenu sémantique, pas seulement les métriques techniques.

| Donnée tracée | Utilité | Outil |
|--------------|---------|-------|
| Prompt complet envoyé au LLM | Débugger les mauvaises réponses | LangSmith / Langfuse |
| Réponse brute du LLM | Voir les erreurs de parsing | LangSmith / Langfuse |
| Chunks récupérés + scores | Vérifier la qualité du retrieval | LangSmith |
| Latence par étape | Identifier le goulot (retrieval vs LLM) | LangSmith |
| Coût en tokens | Estimer la facture mensuelle | LangSmith |

HomeButler supporte les deux via la variable `TRACING_PROVIDER` : `langsmith` pendant la formation (zéro configuration avec LangChain) ou `langfuse` en production (self-hostable, RGPD-friendly, pattern singleton `LangfuseService`).


📝 Slide 9 : Erreurs communes dans les pipelines LangChain

POURQUOI les pipelines LangChain tombent-ils souvent pour des raisons évitables ?

La plupart des problèmes ne viennent pas de l'algorithmique RAG mais de détails d'intégration : gestion des versions, état des composants entre requêtes, parsing des sorties LLM. Ces 5 erreurs représentent 80 % des tickets de support LangChain en 2024-2025.

| Erreur | Symptôme | Cause | Solution |
|--------|----------|-------|----------|
| Agent en boucle infinie | Timeout, coût explosif | max_iterations absent, Ollama mal configuré | handle_parsing_errors=True + max_iterations=8 |
| Réponses dégradées après mise à jour | Comportement inattendu | Mélange LCEL et legacy chains | Choisir un seul style, ne pas mélanger |
| Lenteur au démarrage | 10 à 30 s par requête | Agent et vectorstores rechargés à chaque requête | Lifespan FastAPI + @st.cache_resource |
| Chunks non retrouvés | Réponses génériques | Top-k trop petit (k=1 ou k=2) | Augmenter k à 4-6 + activer reranking |
| Erreur de parsing LLM | "Could not parse LLM output" | Modèle open-source dévie du format ReAct | handle_parsing_errors=True + prompt hwchase17/react |


📝 Slide 10 : HomeButler Pipeline — l'agent ReAct avec 4 outils

POURQUOI la logique ReAct est-elle la bonne architecture pour HomeButler ?

HomeButler répond à des questions qui peuvent nécessiter 1 à 4 sources différentes selon le contexte. La logique ReAct permet à l'agent de décider dynamiquement quels outils interroger, dans quel ordre, avec quelle combinaison — sans que le développeur ait à coder tous les cas possibles explicitement.

| Fichier | Rôle | Contenu principal |
|---------|------|------------------|
| homebutler/agent/tools.py | Définit les 4 outils | search_docs, analyze_energy, find_products, weather_tool |
| homebutler/agent/react_agent.py | Crée l'AgentExecutor | Prompt hwchase17/react + 4 tools + max_iterations=8 |
| api/main.py | Initialise l'agent | Lifespan FastAPI — une seule initialisation au démarrage |
| api/routers/chat.py | Expose l'agent | Endpoint POST /chat avec streaming optionnel |

3 anomalies injectées dans les données énergie pour le TP : juin +200 %, décembre +150 %, mars -60 %. L'agent doit les détecter via `analyze_energy` et les expliquer en croisant avec les données météo via `weather_tool`.

> 💡 L'agent est initialisé une seule fois au démarrage de l'API (pattern lifespan FastAPI). Sans ce pattern, chaque requête rechargerait le modèle et l'index FAISS — latence 10 à 30 secondes par appel.


🎓 Ce que vous devez retenir — Chapitre 3

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| Framework = accélérateur de composition | LangChain surpasse l'API directe dès qu'il y a une chaîne ou un agent |
| LangChain 0.3 LCEL | Syntaxe pipe — ne pas mélanger avec les classes legacy |
| LangChain pour agents, LlamaIndex pour RAG pur | Choisir selon le besoin dominant du projet |
| Pipeline RAG en 6 étapes | Load → Split → Embed → Index → Retrieve → Generate |
| 4 outils HomeButler | search_docs / analyze_energy / find_products / weather_tool |
| Chain vs Agent | Chain = séquentiel fixe. Agent = décisionnel dynamique. |
| ReAct (Yao 2022) | Thought → Action → Observation — pattern le plus robuste |
| max_iterations=8 + handle_parsing_errors | Évite les boucles infinies avec modèles open-source |
| LangSmith vs Langfuse | LangSmith natif LangChain (formation) / Langfuse self-hosted (production) |
| Lifespan FastAPI | Initialiser l'agent une fois, pas à chaque requête |


➡️ Prochain chapitre

Le pipeline RAG est en place et l'agent ReAct orchestre les 4 sources de données. On explore maintenant quand et comment fine-tuner le modèle de base — LoRA, QLoRA, préparation des données, estimation des ressources GPU, et construction du dataset HomeButler de 150 paires Q&A.

---

Chapitre 4 : Fine-tuning avec HuggingFace — Jour 2


🎯 Objectif du chapitre

Comprendre quand le Fine Tuning surpasse le RAG, distinguer Full Fine-Tuning / LoRA / QLoRA en termes de ressources et de qualité, maîtriser la préparation d'un dataset d'entraînement, estimer les coûts GPU, et appliquer ces concepts au dataset de 150 paires Q&A du projet HomeButler AI.


📝 Slide 1 : Quand le RAG ne suffit pas — 4 cas d'usage du Fine Tuning

POURQUOI fine-tuner alors qu'on a déjà un RAG fonctionnel ?

Le RAG résout le problème de la connaissance manquante. Il ne résout pas le problème du comportement : comment le modèle répond, pas ce qu'il dit. Si le LLM doit adopter un ton de marque spécifique, utiliser un format de sortie contraint, ou raisonner selon une logique métier absente de son entraînement, le contexte RAG ne suffit pas. Il faut modifier les poids.

| Cas d'usage | Pourquoi le RAG est insuffisant | Ce que le Fine Tuning apporte |
|-------------|--------------------------------|-------------------------------|
| Ton et style de marque | Le contexte du prompt ne modifie pas le comportement général | Les poids encodent le nouveau style |
| Raisonnement métier spécialisé | La logique métier absente du corpus d'entraînement n'est pas récupérable | Le modèle apprend le raisonnement spécifique |
| Latence critique < 500 ms | Le retrieval ajoute 400 à 800 ms incompressibles | Réponse directe sans étape de recherche |
| Format de sortie complexe strict | Le LLM ignore les contraintes de format malgré les instructions | Entraînement sur exemples du format cible |

> 💡 Fine-tuner ne remplace pas le RAG dans HomeButler — les deux coexistent. Le Fine Tuning adapte le comportement, le RAG apporte la connaissance dynamique.


📝 Slide 2 : Full Fine Tuning vs PEFT — la révolution de l'efficacité

POURQUOI 99 % des praticiens utilisent-ils PEFT plutôt que le Fine Tuning complet ?

Le Fine Tuning complet d'un modèle 7B nécessite de stocker les gradients et les états de l'optimiseur pour tous les 7 milliards de paramètres — soit 100 à 140 Go de VRAM sur GPU. La plupart des équipes n'ont pas accès à ce niveau de ressources. PEFT (Parameter-Efficient Fine-Tuning) résout ce problème en n'entraînant qu'une infime fraction des paramètres.

| Méthode | Paramètres entraînés | GPU minimum | Coût estimé 2026 | Qualité relative |
|---------|---------------------|-------------|------------------|-----------------|
| Full Fine Tuning | 100 % | 4× A100 80 GB | $2 000 à 5 000 | Référence (100 %) |
| LoRA (rank 16) | 0,1 à 1 % | 1× A100 40 GB | $200 à 500 | 95 à 98 % |
| QLoRA (4-bit + LoRA) | 0,1 à 1 % | 1× RTX 4090 24 GB | $100 à 300 | 92 à 96 % |
| Prompting seul | 0 % | Aucun GPU | $0 | Variable |

LoRA a été introduit par Hu et al. en juin 2021 (arxiv:2106.09685). QLoRA par Dettmers et al. en mai 2023 (arxiv:2305.14314). Ces deux papiers ont rendu le Fine Tuning accessible à des milliers d'équipes sans infrastructure massive.


📝 Slide 3 : LoRA — l'intuition des matrices de rang faible

POURQUOI LoRA fonctionne-t-il avec si peu de paramètres entraînés ?

L'hypothèse de LoRA : lors d'un Fine Tuning standard, les changements de poids ont une dimension intrinsèque faible. Cela signifie que la "direction" dans laquelle les poids doivent évoluer peut être représentée par de très petites matrices. LoRA exploite cette propriété en ajoutant deux petites matrices (A et B) à chaque couche d'attention — sans toucher aux poids originaux.

Fonctionnement (sans formule mathématique) : à chaque couche cible, on ajoute une branche parallèle composée de deux matrices de faible rang. Pendant l'entraînement, seules ces matrices sont mises à jour. À l'inférence, leur contribution est fusionnée avec les poids originaux — zéro surcoût de latence.

| Hyperparamètre | Valeur de départ | Effet sur le Fine Tuning |
|----------------|-----------------|--------------------------|
| Rank (r) | 8 à 16 | Plus élevé = plus de capacité, plus de risque d'overfitting |
| Alpha | 2× rank (16 à 32) | Échelle des adaptateurs — ratio signal/bruit |
| Couches cibles | q_proj, v_proj | Couches d'attention — les plus impactantes |
| Dropout LoRA | 0,05 à 0,1 | Régularisation — réduit l'overfitting |

⚠️ **Piège** — Choisir un rank trop élevé (r=64) sur un petit dataset (< 500 exemples) : le modèle mémorise les exemples d'entraînement au lieu de généraliser. Commencer à r=8 ou r=16.


📝 Slide 4 : QLoRA — fine-tuner sur un GPU grand public

POURQUOI QLoRA a-t-il démocratisé le Fine Tuning en mai 2023 ?

Avant QLoRA, fine-tuner un modèle 7B nécessitait au minimum 40 Go de VRAM — un GPU A100 loué à plusieurs centaines d'euros par heure. QLoRA a rendu la même opération possible sur un RTX 4090 grand public (24 Go) en combinant 3 innovations simultanées.

| Innovation QLoRA | Ce que ça fait | Impact mémoire GPU |
|-----------------|---------------|-------------------|
| Quantification 4-bit NF4 | Modèle de base chargé en 4-bit (au lieu de 16-bit) | Divise par 4 la mémoire du modèle de base |
| Paged Optimizers | Gestion CPU/GPU du swap des états optimizer | Évite les erreurs OOM pendant l'entraînement |
| Adaptateurs LoRA en bf16 | Les matrices A et B restent en précision haute | Gradients stables malgré la base quantifiée |

Avant QLoRA : fine-tuner un 70B = 4× A100 80 GB. Après QLoRA : fine-tuner un 70B = 2× A100 48 GB. Fine-tuner un 7B = 1× RTX 4090 24 GB.

> 💡 Pour la formation, l'entraînement QLoRA s'exécute sur GPU cloud ou VPS. Sur Mac Intel (sans CUDA), on prépare le dataset et les configurations — le lancement se fait en TP sur une instance cloud.


📝 Slide 5 : Préparation des données — le facteur numéro 1

POURQUOI 500 exemples de qualité surpassent-ils 5 000 exemples bruyants ?

Le Fine Tuning encode les patterns des données d'entraînement dans les poids du modèle. Si ces données contiennent des erreurs, des incohérences ou un manque de diversité, le modèle fine-tuné répond avec les mêmes défauts — mais avec une plus grande confiance. La qualité des données est le levier le plus impactant.

| Critère de qualité | Bonne pratique | Anti-pattern à éviter |
|-------------------|---------------|----------------------|
| Volume | 500 à 2 000 paires de haute qualité | 10 000 paires auto-générées sans relecture humaine |
| Format | Instruction / Réponse (Alpaca) ou Chat (ShareGPT) — cohérent sur tout le dataset | Format incohérent entre exemples |
| Diversité | Couvrir tous les cas d'usage cibles | 80 % du dataset sur le même type de question |
| Nettoyage | Corriger les fautes, valider les réponses | Laisser les réponses incorrectes ou incomplètes |
| Split | 80 % train / 10 % validation / 10 % test | Pas de validation set = overfitting invisible jusqu'en production |

Dans les benchmarks HuggingFace 2024, la qualité des données explique 60 % de la variance de performance finale, indépendamment de la méthode de Fine Tuning choisie.


📝 Slide 6 : Hyperparamètres clés du Fine Tuning LoRA

POURQUOI certains hyperparamètres font-ils échouer un Fine Tuning même avec de bonnes données ?

Même avec un dataset parfait, un learning rate trop élevé peut effacer la connaissance générale du modèle dès la première epoch. Un nombre d'epochs trop élevé mémorise les exemples au lieu de les généraliser. Ces 5 hyperparamètres méritent une attention particulière.

| Hyperparamètre | Valeur recommandée (départ) | Symptôme si mal réglé |
|----------------|-----------------------------|-----------------------|
| Learning rate | 1e-4 à 5e-4 | Trop élevé : catastrophic forgetting. Trop bas : aucun apprentissage |
| Batch size | 4 à 8 (+ gradient accumulation 4) | Trop petit : gradient bruité. Trop grand : OOM |
| Nombre d'epochs | 1 à 3 | > 3 epochs sur petit dataset : mémorisation parfaite, généralisation nulle |
| Warmup steps | 10 % des steps totaux | Sans warmup : instabilité et perte forte au démarrage |
| LoRA rank | 8 à 16 (départ) | Trop élevé sur peu de données : overfitting. Trop bas : underfitting |

⚠️ **Piège** — Entraîner 10 epochs sur 150 exemples comme dans HomeButler : le modèle atteint une loss de validation proche de 0 mais ne généralise plus sur de nouvelles questions.


📝 Slide 7 : GPU et ressources — estimer avant de lancer

POURQUOI estimer les ressources nécessaires avant de lancer l'entraînement ?

Un entraînement lancé sans estimation préalable peut se terminer par une erreur OOM (Out of Memory) après 30 minutes — avec facturation GPU mais sans résultat. La matrice ci-dessous permet de choisir la bonne instance cloud avant de commencer.

| Modèle de base | Méthode | GPU minimum | Durée estimée (1 000 steps) | Coût cloud estimé 2026 |
|----------------|---------|-------------|----------------------------|------------------------|
| 7B paramètres | QLoRA | RTX 4090 24 GB | 1 à 2 heures | $5 à $15 |
| 7B paramètres | LoRA | A100 40 GB | 30 à 60 minutes | $10 à $20 |
| 13B paramètres | QLoRA | 2× RTX 4090 | 2 à 4 heures | $20 à $40 |
| 70B paramètres | QLoRA | 2× A100 48 GB | 8 à 16 heures | $100 à $300 |
| Mac Intel | Tout | ✗ Aucun GPU CUDA | — | Formation uniquement |

> 💡 Sur Mac Intel (notre environnement de formation), le Fine Tuning GPU n'est pas possible (absence de CUDA). On prépare le dataset et les configs localement — l'entraînement s'exécute sur GPU cloud.


📝 Slide 8 : Évaluation — savoir si le Fine Tuning a fonctionné

POURQUOI "ça répond mieux" n'est-il pas une métrique d'évaluation ?

Sans métriques objectives, il est impossible de comparer deux checkpoints, de décider quand arrêter l'entraînement, ou de détecter un overfitting. L'évaluation d'un Fine Tuning combine des métriques automatiques (rapides, reproductibles) et une évaluation humaine (lente mais seule vraie mesure de qualité).

| Métrique | Ce qu'elle mesure | Limite |
|----------|------------------|--------|
| Perplexité (PPL) | Fluidité des réponses générées | Ne mesure pas la justesse factuelle |
| BLEU | Similarité mot-à-mot avec une réponse de référence | Pénalise la créativité, dépassé pour les LLM |
| F1 token overlap | Couverture des tokens attendus | Bonne pour la QA extractive |
| Semantic Similarity | Distance cosinus entre réponse générée et référence | Bonne pour la paraphrase |
| Évaluation humaine (50-100 ex.) | Qualité globale perçue | Coûteux mais seul gold standard |

Bonne pratique : automatiser avec 3 métriques (PPL + F1 + Semantic Similarity) sur le jeu de validation, puis valider manuellement 50 exemples avant tout déploiement.


📝 Slide 9 : 5 pièges classiques du Fine Tuning

POURQUOI la plupart des premiers Fine Tunings donnent-ils des résultats décevants ?

Le Fine Tuning combine des décisions de données, d'architecture et d'hyperparamètres. Une seule mauvaise décision peut ruiner un entraînement de plusieurs heures. Ces 5 pièges représentent 80 % des échecs documentés dans les projets réels.

| Piège | Symptôme | Correction |
|-------|----------|------------|
| Catastrophic forgetting | Le modèle "oublie" l'anglais ou les compétences générales après FT en français | Mélanger 20-30 % de données générales avec les données métier |
| Overfitting sur petit dataset | Train loss → 0, val loss monte — mémorisation parfaite, généralisation nulle | LoRA rank faible + early stopping sur la val loss |
| Mauvais base model | Modèle anglophone FT sur données françaises = réponses bilingues incohérentes | Choisir Mistral pour le français, Llama pour l'anglais |
| Learning rate trop élevé | Réponses incohérentes dès l'epoch 1, loss diverge | LR 1e-4 max + warmup 10 % des steps |
| Pas de split validation | Overfitting découvert en production, pas pendant l'entraînement | Toujours 80/10/10 — valider avant chaque déploiement |

⚠️ **Piège spécifique Mac Intel** — Python 3.14 + onnxruntime 1.26+ = incompatible sur macOS x86_64 (Microsoft a arrêté le support Intel). Solution : Python 3.13.5 + pin `onnxruntime==1.23.2`.


📝 Slide 10 : HomeButler Dataset — les 150 paires Q&A pour le Fine Tuning

POURQUOI HomeButler utilise-t-il 150 paires Q&A synthétiques pour le Fine Tuning ?

En situation réelle, un dataset de Fine Tuning se construit à partir de conversations réelles validées par des experts. Dans le cadre de la formation, les 150 paires sont générées synthétiquement pour couvrir les 4 catégories de questions de HomeButler et illustrer le format Alpaca utilisé par la plupart des outils HuggingFace.

| Type de question | Nb de paires | Exemple de sujet | Source des données |
|-----------------|-------------|------------------|-------------------|
| Notices équipements | ~50 | "Comment réinitialiser le thermostat Netatmo ?" | 6 PDFs |
| Analyse énergie | ~30 | "Ma consommation de juin est-elle anormale ?" | CSV anomalies |
| Producteurs locaux | ~30 | "Quels fromagers sont à moins de 20 km ?" | JSON 30 producteurs |
| Conciergerie générale | ~40 | "Recommande un plombier disponible ce week-end" | Génération synthétique |

Format JSONL Alpaca : chaque entrée comporte trois champs — `instruction` (la question), `input` (contexte optionnel), `output` (réponse attendue). Script générateur : `scripts/generate_qa_dataset.py`.

> 💡 En production, 500 paires minimum validées humainement sont recommandées. Ces 150 paires illustrent la structure — pas les volumes réels. La règle qualité > quantité s'applique particulièrement ici.


🎓 Ce que vous devez retenir — Chapitre 4

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| 4 cas d'usage FT | Ton, raisonnement spécialisé, latence, format — le RAG ne couvre pas ces besoins |
| LoRA = 99 % des poids gelés | Fine-tuner sans modifier les poids originaux — réversible |
| QLoRA = 4-bit + LoRA | Fine-tuner un 7B sur un RTX 4090 24 Go |
| Qualité > quantité des données | 500 bons exemples > 5 000 bruyants — documenté sur benchmarks HuggingFace |
| Learning rate 1e-4 à 5e-4 | Trop élevé = catastrophic forgetting dès l'epoch 1 |
| Rank 8-16 pour commencer | Augmenter uniquement si la val loss stagne |
| Split 80/10/10 | Sans validation set, l'overfitting est invisible jusqu'en production |
| Mac Intel + Python 3.14 | Incompatible onnxruntime — utiliser Python 3.13.5 + pin 1.23.2 |
| Dataset HomeButler | 150 paires JSONL format Alpaca, 4 types de questions |
| Évaluation automatique + humaine | 3 métriques auto + 50 exemples humains avant déploiement |


➡️ Prochain chapitre

Le modèle est fine-tuné. Comment le quantiser pour l'inférence sur CPU ou GPU limité, l'exposer via FastAPI, créer une interface Streamlit, superviser son comportement en production, et déployer l'ensemble de HomeButler sur VPS avec Docker Compose ?

---

Chapitre 5 : Déploiement, bonnes pratiques, optimisation et supervision — Jour 3


🎯 Objectif du chapitre

Maîtriser les étapes du passage en production d'un système LLM (quantisation, API, interface, conteneurisation), choisir entre Ollama et Jan.ai selon le contexte, implémenter la supervision avec LangSmith ou Langfuse, anticiper les 5 risques de sécurité principaux, et déployer HomeButler AI sur VPS Linux.


📝 Slide 1 : Du prototype à la production — les 5 étapes

POURQUOI un modèle qui fonctionne dans un notebook ne fonctionne-t-il pas forcément en production ?

Un notebook s'exécute une fois, séquentiellement, par une seule personne. Une application en production reçoit des requêtes simultanées, doit répondre en moins de 2 secondes, gérer les erreurs, et fonctionner 24h/24. Chaque étape du passage en production révèle des problèmes invisibles dans le notebook.

| Étape | Ce qui change | Piège typique |
|-------|--------------|---------------|
| 1. Notebook | Test séquentiel, itération rapide | Pas reproductible, pas isolé |
| 2. API locale FastAPI | Exposition via HTTP | Modèle rechargé à chaque requête sans lifespan |
| 3. API sécurisée | Rate limiting, auth, injection filter | Headers CORS oubliés, pas de validation input |
| 4. Interface utilisateur Streamlit | Rechargement à chaque interaction | @st.cache_resource oublié = crash Streamlit |
| 5. Conteneurisation Docker | Reproductibilité cross-OS | Dépendances OS (onnxruntime, CUDA) non gérées |

> 💡 HomeButler documente chaque piège de ces 5 étapes — rencontrés et résolus lors de la construction de l'application. Ce n'est pas de la théorie.


📝 Slide 2 : Quantisation — GGUF, GPTQ, AWQ

POURQUOI quantiser un modèle avant de le déployer sur GPU ou CPU limité ?

Un modèle 7B en précision complète (FP16) occupe 14 Go de VRAM. Sur un serveur avec 8 Go de VRAM ou sur CPU, ce n'est pas déployable. La quantisation réduit la précision des poids (de 16-bit à 4-bit ou 8-bit), divisant la taille par 2 à 4 tout en conservant 90 à 95 % de la qualité.

| Format | Algorithme | Qualité conservée | Vitesse | Compatibilité |
|--------|-----------|-------------------|---------|---------------|
| GGUF (llama.cpp) | Format fichier universel | 92 % | Bonne | CPU + GPU partiel — Ollama ✓ |
| GPTQ | Quantification 4-bit par colonne | 90 % | Rapide | GPU uniquement (RTX 3060+) |
| AWQ | Activation-Aware Weight Quantization | 95 % | Modérée | GPU (RTX 4080+) |

Recommandation pratique : GGUF Q4_K_M = meilleur ratio qualité/vitesse pour 8 à 16 Go de RAM, format natif d'Ollama.

> 💡 AWQ offre la meilleure qualité (95 %) mais nécessite une étape de calibration. GGUF est le format le plus universel — il tourne en CPU/GPU mixte et c'est le format par défaut d'Ollama.


📝 Slide 3 : Déploiement local — Ollama vs Jan.ai

POURQUOI deux solutions pour déployer localement, et quand choisir laquelle ?

Ollama et Jan.ai répondent au même besoin (inférence locale sans envoi de données à un provider cloud) mais pour des profils utilisateurs différents. Le choix dépend de l'intégration LangChain et du niveau technique de l'utilisateur final.

| Critère | Ollama | Jan.ai |
|---------|--------|--------|
| Interface | CLI + API REST (port 11434) | Interface graphique desktop |
| Lancement | `ollama run mistral` | Clic dans l'application |
| Accélération GPU | NVIDIA CUDA + Apple Metal + AMD ROCm | NVIDIA + Metal |
| Intégration LangChain | ✓ ChatOllama natif | ✗ Pas d'API standard compatible |
| Format modèles | GGUF natif | GGUF natif |
| Debug | CLI, logs visibles | GUI, logs opaques |
| Cas HomeButler | LLM_PROVIDER=ollama sur VPS | Démonstration pour utilisateurs non-techniques |

⚠️ **Piège** — ChatAnthropic utilise le paramètre `max_tokens`, ChatOllama utilise `num_predict`. Le switch LLM_PROVIDER de HomeButler gère cette différence dans `homebutler/llm/provider.py`.


📝 Slide 4 : API avec FastAPI — les patterns de production

POURQUOI FastAPI est-il le standard de fait pour exposer un LLM en Python ?

FastAPI combine la performance asynchrone (ASGI), la validation automatique des données (Pydantic), la documentation OpenAPI auto-générée, et le support natif du streaming — toutes les caractéristiques nécessaires pour une API LLM en production.

| Pattern | Rôle | Détail dans HomeButler |
|---------|------|------------------------|
| Lifespan (startup/shutdown) | Initialiser agent + vectorstores une seule fois | asynccontextmanager dans api/main.py |
| StreamingResponse | Réponse token par token en temps réel | Endpoint POST /chat |
| Rate limiting | Limiter les abus et les coûts API | 10 requêtes/minute par IP |
| Timeout | Éviter les requêtes bloquantes | 30 à 120 secondes selon la taille du modèle |
| Middleware injection filter | Bloquer les prompt injections avant parsing | Regex FR + EN sur le body avant traitement |

Les 4 routers HomeButler : `/chat` (agent ReAct), `/consumption/analyze` (analyse énergie), `/products/search` (recherche producteurs), `/orders` (gestion commandes).


📝 Slide 5 : Interfaces utilisateur — Gradio vs Streamlit

POURQUOI avoir deux interfaces dans HomeButler (Gradio et Streamlit) ?

Gradio permet de créer un prototype interactif en moins de 15 lignes — idéal pour démontrer rapidement une fonctionnalité. Streamlit permet de construire une application multi-pages maintenable sur le long terme. HomeButler utilise les deux selon le contexte.

| Critère | Gradio 5.x | Streamlit 1.x |
|---------|-----------|--------------|
| Prototype minimal | ~10 lignes | ~30 lignes |
| Multi-pages | Tabs uniquement | Pages natives (st.navigation) |
| Cache ressources LLM | Non | @st.cache_resource (indispensable) |
| Public cible | Démonstration, chercheur | Application métier, data scientist |
| Rechargement sur modification | Automatique | Automatique |
| Usage HomeButler | gradio_prototype.py (démo) | app.py + 4 pages (production) |

⚠️ **Piège Streamlit** — Sans `pip install -e .` sur le package `homebutler`, Streamlit ne trouve pas les imports locaux et génère `ModuleNotFoundError: No module named 'homebutler'`. Résolu par la création de `pyproject.toml` + `pip install -e .`.


📝 Slide 6 : Supervision LLM — LangSmith vs MLflow

POURQUOI l'observabilité LLM est-elle différente de l'observabilité ML classique ?

L'observabilité ML classique trace des métriques numériques (loss, accuracy, temps d'inférence). L'observabilité LLM doit tracer du contenu sémantique : le prompt exact envoyé, la réponse brute reçue, les chunks récupérés par le retriever, le coût en tokens. LangSmith est conçu spécifiquement pour cela.

| Critère | LangSmith | MLflow 2.x |
|---------|-----------|-----------|
| Tracing natif LLM | ✓ (prompt + réponse + tokens + latence) | Partiel (plugin LLM) |
| Intégration LangChain | Automatique (zéro import) | Manuelle |
| Debug chaînes et agents | ✓ Replay pas-à-pas | ✗ |
| Métriques ML classiques | ✗ | ✓ (loss, accuracy, confusion matrix) |
| Self-hosted | Payant | ✓ Gratuit |
| RGPD / données sensibles | Données envoyées à LangChain Inc. | On-premise possible |

HomeButler : `TRACING_PROVIDER=langsmith` pendant la formation (LangSmith natif, zéro configuration avec LangChain 0.3) ou `langfuse` en production (self-hosted, conforme RGPD, pattern singleton `LangfuseService`).


📝 Slide 7 : Sécurité — 5 risques critiques d'exposition d'un LLM

POURQUOI sécuriser un LLM est-il différent de sécuriser une API REST classique ?

Une API REST classique traite des données structurées avec une logique déterministe. Un LLM traite du texte libre et produit des sorties non déterministes influencées par les instructions reçues. Un attaquant peut injecter des instructions dans le texte libre pour modifier le comportement du modèle — ce qui n'existe pas dans une API REST traditionnelle.

| Risque | Description | Mitigation dans HomeButler |
|--------|-------------|---------------------------|
| Prompt injection | L'utilisateur insère "Ignore les instructions et..." | Middleware regex FR+EN avant parsing du body |
| Exfiltration via RAG | Requête malicieuse récupère des données sensibles du vectorstore | Contrôle d'accès sur les collections ChromaDB |
| Credentials exposés | Token API hardcodé dans le code source | Variables d'environnement + .env dans .gitignore |
| Absence de rate limiting | Coût API illimité → facture explosive | 10 req/min par IP minimum |
| Logs insuffisants | Impossible de détecter un abus a posteriori | LangSmith / Langfuse : tout tracer |

⚠️ **OWASP Gen AI 2025** — Le prompt injection est classé risque #1 dans le Top 10 LLM d'OWASP. Plusieurs incidents documentés en 2024 impliquant des chatbots d'entreprise qui ont divulgué des données internes suite à des injections.


📝 Slide 8 : Bonnes pratiques de production

POURQUOI ces pratiques différencient-elles un POC d'une application maintenue sur 6 mois ?

Un POC peut ignorer le cache, les variables d'environnement, et le monitoring. Une application en production qui coûte $50/mois d'API et répond à 1 000 utilisateurs ne peut pas se permettre ces lacunes.

| Pratique | Pourquoi | Implémentation dans HomeButler |
|----------|----------|-------------------------------|
| Cache TTL pour les appels fréquents | Réduit la latence et le coût API | cachetools.TTLCache (1h pour la météo) |
| Variables d'environnement | Sécurité + portabilité entre environnements | .env.example versionné, .env dans .gitignore |
| Retry avec backoff exponentiel | Résistance aux pannes transitoires de l'API LLM | tenacity ou httpx retry |
| Graceful degradation | L'app reste utilisable si un service est indisponible | Fallback texte si le RAG échoue |
| Health check endpoint | Monitoring infra et load balancer | GET /health retourne statut de tous les composants |


📝 Slide 9 : Erreurs courantes au déploiement

POURQUOI les déploiements LLM échouent-ils souvent pour des raisons non-ML ?

La plupart des incidents en déploiement LLM ne viennent pas de la qualité du modèle ou du pipeline RAG — ils viennent de détails d'intégration, de dépendances mal gérées, et de patterns d'initialisation incorrects.

| Erreur | Symptôme | Solution documentée |
|--------|----------|---------------------|
| Modèle rechargé à chaque requête | Latence 10 à 30 s, OOM possible | Lifespan FastAPI + @st.cache_resource Streamlit |
| CORS mal configuré | Erreur bloquante depuis le frontend | CORSMiddleware avec origins explicites |
| Pas de rate limiting | Coût API explosif en cas d'usage intensif | SlowAPI ou middleware custom |
| python-multipart trop ancien | Gradio crash au démarrage (0.0.12 incompatible) | python-multipart >= 0.0.18 |
| Package homebutler non installé | ModuleNotFoundError dans Streamlit | pip install -e . après requirements.txt |


📝 Slide 10 : HomeButler Déploiement — architecture complète

POURQUOI Docker Compose est-il le bon outil pour déployer HomeButler sur VPS ?

Docker Compose définit l'ensemble des services (API, UI, modèle) dans un seul fichier déclaratif. Il garantit la reproductibilité entre environnements (Mac, Linux, VPS), isole les dépendances OS critiques (onnxruntime, CUDA), et permet de démarrer l'application complète avec une seule commande.

| Composant | Port | Fichier source | Dépendances |
|-----------|------|----------------|-------------|
| FastAPI API | 8000 | api/main.py + 4 routers | Agent ReAct + RAG + services |
| Streamlit | 8501 | homebutler/app.py | 4 pages UI + agent |
| Gradio prototype | 7860 | gradio_prototype.py | Agent direct |
| Docker Compose | — | docker-compose.yml | api/Dockerfile + ui/Dockerfile |

Cibles de déploiement :
- Mac Intel : Python 3.13.5 + onnxruntime 1.23.2 (pinné — 1.26+ ARM-only sur macOS)
- Mac ARM (M1-M4) : Python 3.13 ou 3.14 + onnxruntime récent
- Linux x86_64 VPS : Docker (Python 3.13+ ok + onnxruntime récent)

> 💡 Sur Mac Intel, Python 3.14 est incompatible avec onnxruntime 1.24+ car Microsoft a abandonné le support macOS x86_64 à partir de cette version. Solution : pin `onnxruntime==1.23.2` dans requirements.txt.


🎓 Ce que vous devez retenir — Chapitre 5

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| 5 étapes notebook → production | Chaque étape révèle des problèmes invisibles dans le notebook |
| GGUF Q4_K_M | Meilleur format universel CPU/GPU pour Ollama |
| Ollama vs Jan.ai | Ollama = intégration LangChain / Jan.ai = démonstration GUI |
| Lifespan FastAPI | Agent initialisé une fois — pas à chaque requête |
| @st.cache_resource Streamlit | Évite le rechargement du modèle à chaque interaction |
| pip install -e . | Résout ModuleNotFoundError homebutler dans Streamlit |
| LangSmith = observabilité LLM native | Trace prompt + réponse + latence + coût automatiquement |
| 5 risques sécurité | Prompt injection, exfiltration RAG, credentials, rate limiting, logs |
| python-multipart >= 0.0.18 | Fix de compatibilité Gradio 5.x — 0.0.12 incompatible |
| Mac Intel + onnxruntime 1.23.2 | 1.26+ ARM-only sur macOS — pin indispensable |


➡️ Prochain chapitre

L'application HomeButler est déployée. Il est temps de répondre à la question stratégique finale : quand choisir RAG, quand choisir Fine Tuning, comment les combiner, et comment le papier RAFT (Zhang et al. 2024) apporte une réponse formelle à cette question.

---

Chapitre 6 : Fine Tuning vs RAG — Jour 3


🎯 Objectif du chapitre

Maîtriser les critères de choix entre RAG, Fine Tuning et architecture hybride, comprendre l'apport du papier RAFT (Zhang et al. 2024), calculer le Total Cost of Ownership sur 12 mois, disposer d'un arbre de décision applicable immédiatement en projet, et valider l'architecture finale de HomeButler AI.


📝 Slide 1 : Pourquoi cette question est stratégique en 2026

POURQUOI le mauvais choix entre RAG et Fine Tuning peut-il coûter 3 mois de retard ?

En 2023-2024, des centaines d'équipes ont fine-tuné des modèles sur des données qui changeaient toutes les semaines — se retrouvant à réentraîner en permanence à un coût non planifié. D'autres ont utilisé le RAG pour des besoins de style et de ton, passant des mois en prompt engineering sans jamais atteindre la qualité souhaitée. La décision RAG vs FT est une décision d'architecture, pas un choix technique secondaire.

| Mauvais choix | Conséquence concrète | Coût estimé de correction |
|--------------|---------------------|--------------------------|
| FT pour des données changeant chaque semaine | Réentraînement permanent non planifié | $2 000/mois GPU + 2 semaines/mois ingénieur |
| RAG pour un besoin de ton de marque | Prompt engineering sans fin, qualité médiocre | 3 mois de patches inefficaces |
| Ni RAG ni FT (prompting seul) | Hallucinations en production → incident client | Coût réputationnel difficile à chiffrer |
| Hybride prématuré | Complexité × 3, maintenance lourde | 4 semaines supplémentaires pour le MVP |

> 💡 En 2026, la décision RAG vs FT vs hybride est devenue une compétence d'architecture LLM à part entière — autant que le choix entre SQL et NoSQL l'était pour les bases de données.


📝 Slide 2 : Comparaison approfondie — 8 critères de décision

POURQUOI 8 critères et pas un seul "ça dépend" ?

Le "ça dépend" est vrai mais inutilisable. Ces 8 critères permettent de trancher en moins de 10 minutes dans la plupart des contextes projet. Ils couvrent les dimensions données, comportement, contraintes opérationnelles et budget.

| Critère | RAG | Fine Tuning | Hybride RAG + FT |
|---------|-----|-------------|-----------------|
| Données changeant fréquemment | ✓ | ✗ | ✓ |
| Style et ton de marque | ✗ | ✓ | ✓ |
| Citations et traçabilité | ✓ | ✗ | ✓ |
| Latence critique < 500 ms | ✗ | ✓ | Partiel |
| Budget GPU limité | ✓ | ✗ | Partiel |
| Moins de 500 exemples disponibles | ✓ | ✗ | ✗ |
| Raisonnement métier très spécialisé | ✗ | ✓ | ✓ |
| Mise en production en < 1 semaine | ✓ | ✗ | ✗ |


📝 Slide 3 : Quand choisir le RAG

POURQUOI le RAG est-il la solution dominante dans 70 % des projets LLM ?

Le RAG présente un avantage décisif dans la majorité des contextes réels : il ne nécessite pas de GPU pour l'entraînement, se met en production en quelques jours, et s'adapte à des données qui changent sans réentraînement. Sa limite principale est comportementale, pas factuelle.

| Scénario | Pourquoi le RAG gagne | Exemple concret |
|----------|----------------------|-----------------|
| Données changeant souvent | Réindexation en minutes vs réentraînement en heures | Catalogue produit mis à jour quotidiennement |
| Traçabilité requise | Le chunk source est retourné avec la réponse | Audit légal, conformité, référencement |
| Budget < $1 000 au lancement | Pas de GPU, pas d'entraînement | Startup, POC, projet solo |
| Moins de 500 exemples disponibles | FT sur < 500 exemples = overfitting quasi garanti | Domaine nouveau sans historique de Q&A |
| Plusieurs domaines distincts | Indexer N corpus sans fine-tuner N fois | Assistant multi-produits |

Stat clé : RAG atteint 89 % d'accuracy sur des tâches de QA ouvert, contre 60 à 70 % sans retrieval (benchmarks 2024).


📝 Slide 4 : Quand choisir le Fine Tuning

POURQUOI le Fine Tuning est-il irremplaçable dans certains scénarios précis ?

Le Fine Tuning modifie le comportement fondamental du modèle, pas seulement ses connaissances. C'est la seule technique qui permet d'encoder un style de communication, une logique de raisonnement, ou des contraintes de format dans les poids — de façon permanente et sans surcoût de prompt à chaque requête.

| Scénario | Pourquoi le Fine Tuning gagne | Exemple concret |
|----------|-------------------------------|-----------------|
| Ton et style de marque strict | Le contexte RAG ne modifie pas le comportement général | Chatbot avec personnalité et vocabulaire propriétaires |
| Latence critique < 500 ms | Pas de retrieval = réponse directe | Interface temps réel, jeu vidéo, assistant vocal |
| Confidentialité totale | Modèle local, aucune donnée sortante | Données médicales, secrets industriels |
| Raisonnement métier très spécialisé | Logique absent du corpus d'entraînement général | Droit fiscal spécialisé, calcul d'ingénierie |
| Format de sortie complexe et strict | Entraînement sur exemples du format cible | Générateur de contrats, code propriétaire |

Stat clé : FT seul atteint 91 % d'accuracy, légèrement supérieur au RAG seul sur les tâches de raisonnement complexe.


📝 Slide 5 : Architecture hybride — le meilleur des deux mondes

POURQUOI combiner RAG et Fine Tuning dans le même système ?

L'architecture hybride répond à un besoin simple : dans un même produit, certains aspects nécessitent de la connaissance dynamique (RAG) et d'autres nécessitent un comportement adapté (FT). Imposer l'un ou l'autre comme seule solution, c'est accepter de sacrifier une dimension.

| Couche | Rôle | Technologie dans HomeButler |
|--------|------|----------------------------|
| Modèle de base fine-tuné | Ton conciergerie, format de réponse, raisonnement domestique | LoRA sur 150 Q&A HomeButler |
| Retrieval (RAG) | Connaissance à jour — notices, énergie, producteurs | FAISS + ChromaDB + EnsembleRetriever |
| Prompt d'assemblage | Combine le contexte récupéré et l'instruction | Template hwchase17/react |
| Observabilité | Trace les deux couches simultanément | LangSmith ou Langfuse |

Résultat sur benchmarks : hybride RAG + FT = 96 % d'accuracy, contre 89 % pour le RAG seul et 91 % pour le FT seul.

⚠️ **Avertissement** — L'hybride est plus complexe à maintenir. Il se justifie uniquement quand les deux couches apportent chacune une valeur mesurée et irremplaçable. Commencer simple, mesurer le gap, puis ajouter la couche manquante.


📝 Slide 6 : RAFT — Retrieval Augmented Fine Tuning (Zhang et al. 2024)

POURQUOI RAFT apporte-t-il une avancée par rapport au simple RAG ou au simple FT ?

RAG et FT sont deux techniques distinctes que l'on peut combiner naïvement. RAFT (Zhang et al., mars 2024, Berkeley + Microsoft) propose une approche différente : entraîner explicitement le modèle à utiliser le contexte récupéré quand il est pertinent, et à l'ignorer quand il est du bruit. Cette robustesse au bruit est absent dans les architectures hybrides naïves.

| Aspect | RAG classique | Fine Tuning classique | RAFT |
|--------|--------------|----------------------|------|
| Contexte utilisé | Récupéré dynamiquement | Absent (mémoire paramétrique) | Entraîné sur oracle + documents distracteurs |
| Apprentissage du bruit | Non | Non | Oui — le modèle apprend à filtrer |
| Généralisation hors domaine | Bonne | Limitée | Bonne (transfer learning préservé) |
| Accuracy domaine spécialisé | 85 % | 82 % | 92 % |

Référence complète : Zhang et al., "RAFT: Adapting Language Model to Domain Specific RAG", arxiv:2403.10131, mars 2024.

> 💡 L'intuition RAFT : si on entraîne toujours avec les bons documents, le modèle devient dépendant du retrieval. En mélangeant oracle (bons docs) et distracteurs (mauvais docs), le modèle apprend à être sélectif.


📝 Slide 7 : Benchmarks comparatifs — les chiffres réels

POURQUOI les benchmarks doivent-ils être interprétés avec précaution ?

Les chiffres comparatifs sont utiles pour orienter une décision, pas pour la prendre seul. Un RAG bien configuré peut surpasser un FT mal préparé, et inversement. Les benchmarks mesurent des architectures optimisées dans des conditions contrôlées — les résultats réels dépendent de la qualité des données et de l'implémentation.

| Type de tâche | RAG seul | FT seul | Hybride / RAFT |
|--------------|----------|---------|----------------|
| QA factuel ouvert | 89 % | 79 % | 94 % |
| QA domaine spécialisé (médical) | 82 % | 88 % | 96 % |
| Complétion de code | 72 % | 91 % | 93 % |
| QA multi-étapes (raisonnement) | 74 % | 81 % | 91 % |
| Génération de style et de ton | 65 % | 94 % | 95 % |

Lecture : le RAG gagne sur les tâches factuelles ouvertes. Le FT gagne sur le style et le raisonnement spécialisé. L'hybride gagne sur toutes les dimensions mais au prix d'une complexité accrue.


📝 Slide 8 : Total Cost of Ownership sur 12 mois

POURQUOI le coût réel d'un système LLM s'évalue-t-il sur 12 mois et non au lancement ?

Le coût de setup initial est souvent l'élément le plus visible mais pas forcément le plus important. Les coûts récurrents (infrastructure, mises à jour, réentraînement) peuvent dépasser le setup en quelques mois. Le TCO sur 12 mois est la métrique décisionnelle correcte.

| Poste de coût | RAG seul | Fine Tuning seul | Hybride RAG + FT |
|--------------|----------|-----------------|-----------------|
| Setup initial | $500 à $1 000 | $500 à $2 000 | $1 500 à $3 000 |
| Infrastructure mensuelle | $50 à $200 | $200 à $500 | $300 à $700 |
| Mise à jour des données | Réindexation (1 à 2h) | Réentraînement ($500 à $2 000) | Réindexation + réentraînement trimestriel |
| Total estimé 12 mois | $1 000 à $3 000 | $3 000 à $8 000 | $5 000 à $12 000 |

> 💡 Le RAG a le TCO le plus bas pour des données qui changent souvent. Le FT amortit son coût sur des données stables avec un fort volume de requêtes. L'hybride se justifie quand les deux apportent une valeur mesurée.


📝 Slide 9 : Arbre de décision — RAG, Fine Tuning ou Hybride ?

POURQUOI avoir un arbre de décision plutôt que des règles générales ?

Les règles générales ("utiliser le RAG quand les données changent") sont faciles à retenir mais difficiles à appliquer sur un cas concret. Un arbre de décision positionne les critères dans le bon ordre et produit une recommandation non ambiguë en 4 questions.

Flux de décision (à appliquer dans l'ordre) :

Étape 1 — Vos données changent-elles plus d'une fois par mois ?
- OUI → RAG fortement recommandé (aller à l'étape 3)
- NON → aller à l'étape 2

Étape 2 — Avez-vous plus de 500 exemples de qualité pour entraîner ?
- NON → RAG (pas assez de données pour le FT)
- OUI → aller à l'étape 3

Étape 3 — Avez-vous un besoin fort de style, de ton, ou de raisonnement spécialisé ?
- NON → RAG seul (architecture simple, TCO faible)
- OUI → aller à l'étape 4

Étape 4 — Avez-vous le budget GPU et 2 à 4 semaines pour le Fine Tuning ?
- NON → RAG + prompting avancé (augmentation de contexte)
- OUI → Architecture hybride RAG + Fine Tuning

⚠️ **Règle importante** — Ne jamais commencer par l'hybride. Toujours valider le RAG seul en premier, mesurer le gap de qualité, puis décider si le Fine Tuning vaut l'investissement sur la base d'un écart mesuré.


📝 Slide 10 : HomeButler Final — architecture hybride complète

POURQUOI HomeButler utilise-t-il une architecture hybride RAG + Fine Tuning ?

HomeButler répond aux 4 critères qui justifient l'hybride : des données qui changent (notices, énergie, producteurs) nécessitant le RAG, et un besoin de ton de conciergerie + format de réponse structuré nécessitant le Fine Tuning. Les 3 jours de formation ont construit chaque couche de cette architecture.

| Couche | Composant | Rôle dans HomeButler |
|--------|-----------|---------------------|
| Embedding et RAG | FastEmbedEmbeddings + FAISS + ChromaDB + EnsembleRetriever | Répondre sur les notices, l'énergie et les producteurs |
| Fine Tuning | LoRA sur 150 Q&A HomeButler (format Alpaca) | Ton conciergerie + format de réponse adapté |
| Orchestration | LangChain 0.3 + ReAct (hwchase17/react) | Décider quel outil appeler et dans quel ordre |
| API | FastAPI + 4 routers + middleware sécurité | Exposer l'application au frontend |
| Interface | Streamlit 4 pages + Gradio prototype | Expérience utilisateur |
| Infrastructure | Docker Compose + VPS Linux | Déploiement reproductible cross-OS |
| Observabilité | LangSmith (formation) / Langfuse (production) | Tracer, débugger, optimiser |

> 💡 En 3 jours, vous avez construit une application complète de 40 fichiers répartis en 10 phases. Chaque chapitre correspond à une couche de cette architecture — de l'indexation des PDFs au déploiement Docker sur VPS.


🎓 Ce que vous devez retenir — Chapitre 6

| Concept | Pourquoi c'est important |
|---------|--------------------------|
| 8 critères de décision | Tableau à conserver pour chaque nouveau projet LLM |
| RAG = données volatiles + traçabilité | 89 % accuracy, TCO $1 000 à $3 000/an |
| FT = style + raisonnement + latence | 91 % accuracy, TCO $3 000 à $8 000/an |
| Hybride = meilleur des deux | 96 % accuracy, TCO $5 000 à $12 000/an |
| RAFT (Zhang et al. 2024) | Entraîner sur oracle + distracteurs = robustesse au bruit de retrieval |
| TCO 12 mois | Coût réel = setup + infra mensuelle + mises à jour récurrentes |
| Arbre de décision en 4 questions | Choisir RAG, FT ou hybride en moins de 10 minutes |
| Commencer par le RAG | Valider d'abord, fine-tuner sur le gap mesuré — jamais l'inverse |
| HomeButler = architecture hybride | FastEmbed + FAISS/ChromaDB (RAG) + LoRA (FT) + LangChain + FastAPI + Streamlit + Docker |
| Ne jamais commencer par l'hybride | Complexité × 3 — se justifie uniquement sur valeur mesurée |
