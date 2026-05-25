# GUIDE FORMATEUR — Atelier 06 : Fine-tuning vs RAG / RAFT (3h30)

> Atelier de synthèse finale. L'élève mesure 3 modes, remplit une grille de décision et
> défend une recommandation chiffrée en 5 minutes. Il n'y a pas de bonne réponse universelle :
> la recommandation doit être justifiée par les données que l'élève a mesurées lui-même.

---

## 1. Ce que l'élève doit comprendre à la fin

A la fin de cet atelier, l'élève doit être capable de répondre à ces trois questions sans hésiter :

**Sur les concepts**

RAFT (Retrieval-Augmented Fine-Tuning, Zhang et al. 2024) combine RAG et Fine-Tuning : on entraîne
le modèle en lui donnant pour chaque question le bon document ET des documents distracteurs mélangés
intentionnellement. Le modèle apprend à ignorer le bruit du retriever. RAG seul ne modifie pas les
poids du modèle. Fine-Tuning seul n'utilise pas de contexte externe. RAFT atteint 94 % en QA factuel
contre 89 % pour RAG seul et 79 % pour FT seul.

TCO (Total Cost of Ownership) est le coût total sur 12 mois, pas seulement le coût de setup. Break-even
est le point à partir duquel le Fine-Tuning auto-hébergé devient moins cher que les appels API. Pour
HomeButler à 10k requêtes/mois, le RAG seul coûte ~1700 € an 1 contre ~3600 € pour le FT seul.

**Sur la méthode**

Recall@5 = 0.87 signifie : sur 100 questions test, 87 ont au moins un chunk pertinent parmi les 5
premiers résultats du retriever. Les 13 autres ne trouveront jamais la bonne réponse, même avec le
meilleur LLM en aval. C'est une métrique du retriever, pas de la qualité de la réponse générée.

Si Recall@5 = 1.00 pour toutes les stratégies, c'est un signal d'alarme, pas de performance : cela
signifie que l'évaluation a été lancée sur le jeu d'entraînement (data leakage).

**Sur la décision**

La recommandation finale doit citer au moins trois chiffres mesurés et reconnaître au moins un cas
où elle serait mauvaise. "RAG est mieux" sans chiffre n'est pas une recommandation.

---

## 2. Setup formateur — avant l'atelier

### Vérifications à faire la veille (15 min)

Travailler depuis la racine du projet :

```bash
git checkout atelier/06-finetune-vs-rag
source .venv/bin/activate
```

Vérifier que le fichier `.env` contient bien :

```bash
grep ENABLE_COMPARE_ROUTES .env
# doit afficher : ENABLE_COMPARE_ROUTES=true
```

Sans cette variable, les routes `/rag/evaluate`, `/chat/compare` et `/rag/compare-strategies`
retournent 404 et l'élève passe 30 minutes à chercher un bug qui n'en est pas un.

Générer les données (si pas déjà fait depuis les ateliers précédents) :

```bash
python scripts/generate_documents.py
python scripts/generate_qa_dataset.py
python scripts/generate_energy_data.py
```

Vérifier que le fichier de test QA existe :

```bash
ls data/qa_dataset/concierge_qa.jsonl
ls data/qa_dataset/concierge_qa_test.jsonl
```

Le deuxième fichier (`concierge_qa_test.jsonl`) est distinct du fichier d'entraînement. Si seul
le premier existe, le Bug v1 sera moins lisible car l'élève ne verra pas la séparation train/test.

Démarrer l'API dans un terminal dédié :

```bash
uvicorn api.main:app --port 8000
```

Vérifier dans Swagger (`http://localhost:8000/docs`) que les routes `/rag/evaluate` et
`/chat/compare` apparaissent bien. Si elles n'apparaissent pas, vérifier `ENABLE_COMPARE_ROUTES`.

Tester le script principal depuis un second terminal :

```bash
python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
```

Le script doit afficher un tableau Recall@1/3/5 pour les stratégies fixed, recursive, ensemble,
puis les latences par mode. Durée typique : 3 à 5 minutes selon la machine.

### Valeurs attendues sur votre machine

Gardez ces valeurs sous la main pour aider les élèves à se situer. Elles varient selon le hardware
et la taille du dataset, mais l'ordre relatif reste stable :

| Stratégie  | Recall@5 attendu |
|------------|-----------------|
| ensemble   | ~0.87           |
| recursive  | entre 0.72 et 0.87 |
| fixed      | ~0.72           |

| Mode      | Latence typique |
|-----------|----------------|
| llm_only  | ~2s            |
| rag_only  | ~3s            |
| agent     | 10-30s         |

### Ce qui peut mal tourner

Si `evaluate_pipeline.py` échoue avec `API non joignable` : l'élève n'a pas démarré l'API ou
utilise un port différent. Vérifier que `uvicorn` tourne bien sur le port 8000.

Si la route `/rag/evaluate` retourne 404 : `ENABLE_COMPARE_ROUTES` est absent ou à `false` dans
`.env`. L'API doit être redémarrée après modification du `.env`.

Si le dataset QA est absent : lancer `python scripts/generate_qa_dataset.py` et attendre
la fin de la génération (2 à 5 minutes).

Si les patches `git apply` échouent avec des conflits : cela signifie que l'élève a modifié
`evaluate_pipeline.py` avant d'appliquer le patch. Réinitialiser le fichier :

```bash
git checkout ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
```

---

## 3. Déroulé détaillé

### Vue d'ensemble du temps

| Phase | Durée | Ce que fait l'élève |
|-------|-------|---------------------|
| Tronc commun | 1h40 | Mesure 3 modes, mini-lab stratégies, grille de décision, bug hunt, mesure-toi |
| Sprint | 30 min | Chemin alternatif pour les élèves en retard (arbre de décision + reco minimale) |
| Bonus | 60-70 min | Débat RAFT, mini-débat en duo |
| Soutenance finale | 15 min | Présentation recommandation + évaluation rubric LLM-judge |

### Tronc commun — détail (1h40)

**Etape 1 — Mesurer les 3 modes (30 min)**

L'élève lance `evaluate_pipeline.py` et note les chiffres. Le script fait tout : appels API,
mesure de latence, tableau récapitulatif. Ce n'est pas un exercice de code, c'est un exercice
de lecture critique des résultats.

Pendant que le script tourne (3-5 min), demandez à l'élève : "Sans regarder les résultats,
lequel des trois modes va avoir la latence la plus élevée selon toi ? Pourquoi ?" Cela crée
une anticipation qui rend la lecture des résultats plus active.

Après le script, l'élève doit répondre à trois questions d'investigation avant de continuer :
quel mode a le meilleur Recall@5, quel mode est le plus lent et de combien, et est-ce que
llm_only hallucine sur les questions portant sur les notices HomeButler.

Le Checkpoint 1 valide cette étape :

```bash
python ateliers/atelier-06-finetune-vs-rag/checkpoints/check_1.py
```

Le checkpoint pose trois questions ouvertes : expliquer RAFT, interpréter Recall@5 = 0.87,
calculer le break-even TCO. La notation se fait par mots-clés. Le score minimum pour continuer
est 2 questions sur 3. Si l'élève échoue, il doit relire `grille_decision.md` et relancer
`evaluate_pipeline.py` avant de repasser.

**Mini-lab — Faire varier la stratégie de retrieval (15 min)**

L'élève appelle l'endpoint `/rag/compare-strategies` pour observer la différence entre fixed,
recursive et ensemble sur une même question :

```bash
curl -s -X POST "http://localhost:8000/rag/compare-strategies" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Quelle est la marque de ma chaudière ?", "strategies": ["fixed", "recursive", "ensemble"]}' \
  | python3 -m json.tool
```

Il modifie ensuite les poids de l'EnsembleRetriever dans `homebutler/rag/retriever.py` :
`weights=[0.6, 0.4]` (défaut) vs `[0.5, 0.5]` vs `[0.8, 0.2]`. Il mesure l'impact sur
Recall@5 et note si ensemble dépasse systématiquement FAISS seul.

Ce mini-lab n'a pas de checkpoint associé. Son rôle est de créer de l'intuition sur les
compromis de la stratégie ensemble, qui sera utile pour la grille de décision.

**Etape 2 — Remplir la grille de décision (25 min)**

L'élève ouvre `grille_decision.md` et remplit les 8 critères avec ses chiffres mesurés. Pour
les lignes Fine-Tuning et Hybride qu'il ne peut pas mesurer directement, il utilise les
benchmarks RAFT. La section TCO est déjà préremplie — il adapte au cas HomeButler.

Le point pédagogique clé de cette étape : la grille n'est pas un formulaire à remplir pour
cocher une case. C'est l'outil qui va fonder sa recommandation. Si la grille est remplie avec
des valeurs copiées des benchmarks sans réfléchir, la recommandation qui en découlera sera
creuse.

Posez cette question pendant l'exercice : "Si tu devais enlever 3 critères de la grille pour
simplifier la décision, lesquels garderais-tu absolument ?"

**Bug Hunt — Casse-moi ca (20 min)**

Trois bugs de méthodologie à appliquer, observer et corriger. Les bugs sont dans `bugs/`.

Pour chaque bug, le protocole est le même :
1. Appliquer le patch
2. Lancer le test et observer l'anomalie
3. Formuler une hypothèse sur la cause AVANT de regarder le code ou l'explication
4. Corriger
5. Lire `bugs/v[N]_explanation.md` et répondre aux affirmations Vrai/Faux

Le détail de chaque bug est dans la section 4.

**Mesure-toi (10 min)**

L'élève remplit un tableau synthèse avec ses quatre métriques personnelles : Recall@5,
latence médiane, taux d'hallucination sur questions privées, coût estimé par 1000 requêtes.
Ce tableau devient la source chiffrée de sa recommandation finale.

Le Checkpoint Final valide l'ensemble du tronc commun :

```bash
python ateliers/atelier-06-finetune-vs-rag/checkpoints/check_final.py
```

Score >= 80 % : partir en Bonus. Entre 60 % et 80 % : travailler la reco écrite, puis Bonus.
Moins de 60 % : partir en Sprint.

### Sprint (30 min)

Pour les élèves en retard ou score < 60 % au checkpoint final. Le sprint consolide l'essentiel
en 30 minutes via deux exercices courts.

Sprint 1 : répondre à voix haute aux quatre questions de l'arbre de décision de `grille_decision.md`
appliquées au cas HomeButler.

Sprint 2 : rédiger une recommandation minimale en cinq lignes avec une phrase par dimension
(approche choisie, justification factualité, justification style, TCO, cas où ce serait mauvais).

### Bonus (60-70 min)

Pour les élèves rapides ou score >= 80 % au checkpoint final.

Défi B1 : construire un argument "RAFT vaut l'investissement pour HomeButler" ET le contre-argument.
Lequel est le plus fort ? L'exercice force à réfléchir aux limites du RAG ensemble déjà à 0.87 et au
coût réel d'un dataset avec distracteurs.

Défi B2 : mini-débat en duo (ou seul avec le LLM-judge). Trois minutes pour défendre sa reco avec
trois métriques minimum, deux minutes pour identifier le point de désaccord principal, une minute pour
proposer un test A/B qui permettrait de trancher.

---

## 4. Bug Hunt — ce qui se passe concrètement

### Bug v1 — Eval lancée sur le train set (illusion 100 % recall)

**Comment l'appliquer :**

```bash
git apply ateliers/atelier-06-finetune-vs-rag/bugs/v1.patch
pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v1.py -v
```

**Ce que l'élève observe :** Recall@5 = 1.00 pour les trois stratégies (fixed, recursive,
ensemble). Les trois donnent exactement le même score parfait.

**Ce qui se passe dans le code :** La variable `TRAIN_QA_PATH = QA_PATH` fait pointer le
chargement du dataset de test vers le même fichier que le dataset d'entraînement. Comme toutes
les questions ont été indexées lors de la construction du vectorstore, le retriever les retrouve
avec un recall parfait. Ce n'est pas un benchmark, c'est un test de mémorisation.

**Signal d'alarme à expliquer à l'élève :** dans un vrai benchmark, les trois stratégies ont
des scores différents et imparfaits. Si fixed, recursive et ensemble donnent tous 1.00, c'est
anormal. L'écart nul entre stratégies est le signal d'alerte, visible sans inspecter le code.

**La correction :** supprimer `TRAIN_QA_PATH` et utiliser le fichier séparé
`concierge_qa_test.jsonl` pour l'évaluation.

**La leçon à retenir :** une erreur de méthodologie d'évaluation est aussi dangereuse qu'un bug
de code. L'équipe annonce "Recall@5 = 0.95", déploie, et découvre en production que le recall
réel est ~0.72. La confiance est érodée.

### Bug v2 — BLEU score pour mesurer le ton/style (métrique inadaptée)

**Comment l'appliquer :**

```bash
git apply ateliers/atelier-06-finetune-vs-rag/bugs/v2.patch
pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v2.py -v
```

**Ce que l'élève observe :** la fonction `evaluate_style_quality()` retourne des scores BLEU très
bas y compris pour des réponses de bonne qualité.

**Ce qui se passe dans le code :** BLEU (Bilingual Evaluation Understudy) est une métrique conçue
pour évaluer les traductions automatiques. Elle mesure le chevauchement de n-grammes entre la
réponse générée et une référence. Elle punit sévèrement les paraphrases, même excellentes.

**Exemple concret à donner :** "Bonjour, votre chaudière est garantie 5 ans" vs "Bonsoir, la
garantie de votre chaudière est de 5 ans". Même sens, BLEU très bas car les mots sont différents.
Si on mesure le ton "chaleureux" de HomeButler avec BLEU, toutes les formules de politesse
alternatives seront pénalisées même si elles sont exactement ce qu'on veut.

**La correction :** supprimer la fonction BLEU et utiliser à la place la cosine similarity sur
des embeddings (`text-embedding-3-small`) ou un LLM-judge avec rubric explicite.

**La leçon à retenir :** choisir la bonne métrique pour la bonne dimension. BLEU est adapté pour
la traduction automatique, pas pour la qualité conversationnelle. Un LLM-judge avec critères
explicites est plus fiable qu'une métrique lexicale pour mesurer le style.

### Bug v3 — Latence mesurée sur 1 seul appel (biais cold-start)

**Comment l'appliquer :**

```bash
git apply ateliers/atelier-06-finetune-vs-rag/bugs/v3.patch
pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v3.py -v
```

**Ce que l'élève observe :** la latence affichée pour chaque mode est anormalement élevée.

**Ce qui se passe dans le code :** `q = questions[0]` mesure uniquement la première question
au lieu d'itérer sur toutes. `latencies[mode] = [elapsed]` remplace la liste à chaque itération
au lieu d'ajouter avec `.append(elapsed)`. Résultat : on mesure uniquement le premier appel,
qui est 2 à 5 fois plus lent que les suivants à cause du cold-start (initialisation de l'agent
ReAct, chargement du vectorstore en mémoire).

**Pourquoi le premier appel est-il plus lent :** lors du premier appel, l'API initialise l'agent
ReAct (via `get_singleton_agent()`), charge le vectorstore FAISS depuis le disque et crée la
session LLM. Ces opérations ne se font qu'une fois par session uvicorn. En production, l'API
tourne depuis des heures — les utilisateurs ne voient jamais ce cold-start.

**La correction :** itérer sur toutes les questions avec un boucle et utiliser `.append(elapsed)`
au lieu de `= [elapsed]`. La pratique standard en benchmark est de mesurer sur >= 10 appels,
ignorer le premier (warm-up), et calculer p50 et p95 sur les suivants.

**La leçon à retenir :** mesurer la latence en production signifie mesurer le "steady-state",
pas le démarrage. Le cold-start est une propriété du déploiement, pas du pipeline.

---

## 5. Checkpoints — comment les animer

### Checkpoint 1 (après Etape 1 — Mesurer les 3 modes)

```bash
python ateliers/atelier-06-finetune-vs-rag/checkpoints/check_1.py
```

Le checkpoint pose trois questions en mode terminal interactif. L'élève tape sa réponse, le
script détecte les mots-clés et donne son score.

**Question 1 — Expliquer RAFT en 3 phrases.** L'élève doit mentionner au moins 3 mots-clés parmi :
fine-tuning, rag, combine, distracteur, entraîne, bruit, ignore, documents, zhang. La réponse
attendue : RAFT combine RAG et FT en entraînant le modèle avec documents pertinents ET distracteurs
mélangés, il apprend à ignorer le bruit du retriever, il atteint 94 % QA factuel vs 89 % RAG et
79 % FT.

**Question 2 — Interpréter Recall@5 = 0.87.** L'élève doit mentionner au moins 3 mots-clés parmi :
0.87, 0.72, 5, chunks, bonne réponse, limite, hallucination, retriever. La réponse attendue : sur
100 questions test, 87 ont le bon chunk dans les 5 premiers résultats, 13 questions ne trouveront
jamais la bonne réponse. La limite : Recall@5 mesure le retriever, pas la qualité générée.

**Question 3 — Calculer le break-even TCO.** L'élève doit mentionner au moins 2 mots-clés parmi :
50, 0.01, 1000, break-even, mois, req, rentable, calcul. La réponse attendue : FT an 1 = 3000
(setup) + 12 x 50 (VPS) = 3600 €. API an 1 = 0.01 € x N req/mois x 12 = 0.12N €. Equation :
3600 = 0.12N, donc N = 30 000 req/mois.

**Seuil de passage :** 2 questions sur 3. Si l'élève échoue : le script s'arrête avec un message
"Relis grille_decision.md et relance evaluate_pipeline.py avant de continuer". Ne pas forcer le
passage : la grille de décision et la soutenance finale s'appuient sur ces trois concepts.

**Posture formateur :** ne pas corriger directement. Si l'élève passe avec 2/3, demandez-lui
quelle question il a manquée et ce qu'il comprend de l'explication du script. Cinq minutes ici
évitent 30 minutes d'incompréhension lors de la soutenance.

### Checkpoint Final (après Mesure-toi)

```bash
python ateliers/atelier-06-finetune-vs-rag/checkpoints/check_final.py
```

Cinq questions plus complexes. Score minimal pour la soutenance : 60 %. Score pour le Bonus : 80 %.

**Question 1 — Quand recommander FT seul ?** Mots-clés attendus : style, ton, stable, dataset, 500,
paires. L'élève doit citer deux conditions : données qui changent peu ET ton/style critique ET plus
de 500 paires annotées.

**Question 2 — Deux métriques factuelles + une métrique style.** Mots-clés attendus : recall,
hallucination, faithfulness, cosine, embedding, llm-judge. L'élève doit expliquer pourquoi on ne
peut pas utiliser la même métrique pour les deux dimensions (lexicale vs sémantique).

**Question 3 — Recall@5 = 0.87, bon ou pas ?** L'élève doit contextualiser : bon par rapport
aux benchmarks (89 % RAG Zhang et al.), mais 13 % des utilisateurs reçoivent des réponses
incorrectes sur un service premium.

**Question 4 — Biais cold-start.** Mots-clés attendus : cold, start, warm, premier, initialise,
agent, vectorstore. L'élève doit citer le mécanisme ET la correction (>= 10 appels, ignorer le 1er).

**Question 5 — Recommandation HomeButler avec trois chiffres.** Mots-clés attendus : rag, style,
ton, 0.87, 10k, api, tco, recall, 1700. L'élève doit citer Recall@5 = 0.87, TCO RAG = ~1700 €/an,
et 10k req/mois insuffisant pour justifier le FT.

**Si l'élève score < 60 % :** orienter vers le Sprint. Ne pas bloquer la soutenance — l'élève
peut faire la soutenance avec le rubric LLM-judge même sans avoir tout compris. Mais sans les
chiffres, la soutenance sera vide.

---

## 6. Soutenance finale — comment l'évaluer

### Format

L'élève présente sa recommandation écrite (1 page) en 5 minutes. La présentation peut être :
- orale devant le groupe ou devant le formateur
- écrite soumise au LLM-judge (rubric ci-dessous)
- les deux (présentation orale + auto-évaluation LLM-judge)

### Rubric d'évaluation (3 critères, échelle 1-5)

**Critère 1 — Les chiffres sont-ils cités ?**

L'élève cite au moins deux métriques mesurées (Recall@k, latence, TCO) issues de ses propres
mesures ou des benchmarks RAFT. Une opinion sans chiffre score 1. Deux chiffres cohérents
avec les benchmarks score 3. Trois chiffres mesurés et contextualisés score 5.

**Critère 2 — Une recommandation spécifique est-elle formulée ?**

L'élève choisit une approche (RAG / FT / Hybride) et la justifie. "Ca dépend" sans données
score 1. Une recommandation formulée sans justification score 2. Une recommandation avec
justification chiffrée et un cas où elle serait mauvaise score 4-5.

**Critère 3 — Les trois approches sont-elles comparées ?**

Au moins un critère est comparé pour RAG, FT et Hybride. Une seule approche mentionnée score 1.
Deux approches comparées score 3. Les trois approches comparées avec au moins une dimension
chiffrée pour chacune score 5.

**Seuil de passage : 3/5 sur chaque critère.**

### Comment animer le rubric LLM-judge

Si l'élève utilise le LLM-judge en autonomie, il colle sa recommandation dans Claude avec le
prompt de la section Wrap-up du guide élève. Le prompt demande une évaluation sur les mêmes
3 critères avec un score 1-5 et une critique constructive en 3 lignes.

Si vous évaluez directement :

Lisez la recommandation en silence pendant 1 minute. Notez les chiffres cités (critère 1), la
clarté de la recommandation (critère 2) et les approches comparées (critère 3). Donnez un score
par critère avant de donner un retour oral. Cela évite que le retour oral influence la notation.

### Ce qu'on ne doit pas pénaliser

Ne pas pénaliser une recommandation qui diffère des benchmarks RAFT si elle est justifiée par
les mesures de l'élève. Si l'élève a un hardware différent ou un dataset différent, ses Recall@5
seront différents. Ce qui compte est la cohérence entre ses chiffres et sa conclusion.

Ne pas pénaliser un élève qui recommande RAG seul plutôt que Hybride si son TCO est cohérent
et si ses mesures montrent que Recall@5 = 0.87 est acceptable pour le cas HomeButler.

### Ce qui doit obligatoirement valider

Pour valider la soutenance, l'élève doit :
- citer au moins un chiffre issu de ses propres mesures (pas uniquement les benchmarks théoriques)
- nommer l'approche qu'il recommande pour HomeButler
- expliquer dans quel cas cette recommandation serait mauvaise

---

## 7. Questions fréquentes

**"Quel est le meilleur choix entre RAG, FT et Hybride ?"**

Il n'y a pas de réponse universelle. La question se décompose en trois sous-questions :
les données changent-elles souvent, le ton/style est-il critique, et quel est le budget GPU ?
Pour HomeButler (notices stables, ton conciergerie important, pas de GPU dédié, 10k req/mois),
le RAG seul est le choix rationnel pour démarrer, avec évolution vers Hybride si le volume dépasse
50k req/mois ou si les utilisateurs se plaignent du ton malgré un system prompt soigné.

**"Notre Recall@5 est différent des benchmarks du slide"**

C'est normal. Les benchmarks RAFT (Zhang et al. 2024) sont mesurés sur des datasets médicaux
et académiques. Le dataset HomeButler est plus petit et plus spécialisé. Ce qui compte est
l'ordre relatif entre les stratégies (ensemble > recursive > fixed) et la cohérence avec les
benchmarks de référence (environ 0.87 pour ensemble, 0.72 pour fixed). Si l'ordre relatif est
inversé, c'est un signal d'alerte — vérifier le dataset de test.

**"RAFT c'est compliqué à mettre en place ?"**

Oui. Il faut annoter des questions avec documents pertinents ET documents distracteurs, fine-tuner
le modèle (quelques heures sur Colab T4 pour Mistral-7B), et maintenir deux systèmes (RAG pour
la fraîcheur + modèle fine-tuné pour le style). Le setup coûte ~3500 € selon le TCO de la grille,
avec 1800 €/an en coût récurrent. Ce n'est justifié que si le gain de 5-7 points de recall vs
RAG ensemble est critique pour le cas d'usage (santé, juridique, support premium).

**"Pourquoi llm_only a un si mauvais Recall@5 ?"**

Recall@5 = ~0.15 pour llm_only signifie que sur 100 questions sur les notices HomeButler, le LLM
seul trouve la bonne information dans 15 cas seulement. Les 85 autres ? Il invente ou dit
"je ne sais pas". Les notices de produits, les codes erreur, les références spécifiques au logement
ne sont pas dans les données d'entraînement du LLM. C'est exactement pourquoi le RAG existe.

**"La latence de l'agent est très variable — c'est normal ?"**

Oui. L'agent ReAct fait plusieurs appels LLM en séquence (reasoning + tool calls). Une question
simple peut prendre 5 secondes, une question complexe 30 secondes ou plus. C'est la principale
contre-indication de l'agent pour les cas d'usage à faible tolérance de latence (chatbot temps
réel). Conseil : mesurer p50 ET p95 pour avoir la latence typique et la latence au pire cas.

**"Le score du checkpoint est bas mais l'élève a bien travaillé, je fais quoi ?"**

Le checkpoint mesure la capacité à articuler les concepts, pas l'effort. Un élève qui a bien
travaillé mais ne sait pas expliquer pourquoi Recall@5 = 1.00 est un signal d'alarme a un
trou conceptuel qui va poser problème à la soutenance. Guidez-le avec des questions socratiques :
"Si tu mesures l'évaluation sur les mêmes données qu'on a utilisées pour entraîner, qu'est-ce
qui peut se passer ?" Ne donnez pas la réponse directe.

**"On a pas eu le temps de faire le Bug Hunt"**

Le Bug Hunt est la partie la plus dense pédagogiquement. Si le temps manque, choisissez
un seul des trois bugs, de préférence le v1 (eval sur train set), car il illustre le concept
le plus critique : une méthodologie d'évaluation incorrecte peut donner des résultats parfaits
qui sont entièrement faux.

---

## 8. Signaux d'alerte (élève bloqué)

### L'élève obtient Recall@5 = 1.00 pour toutes les stratégies

C'est le Bug v1 appliqué sans le savoir ou un problème de dataset. Vérifier que l'élève
utilise bien `concierge_qa_test.jsonl` et non `concierge_qa.jsonl` pour le test. Si les deux
fichiers sont absents, relancer `python scripts/generate_qa_dataset.py`.

### L'API retourne 404 sur /rag/evaluate

Cause la plus fréquente : `ENABLE_COMPARE_ROUTES` est absent du `.env` ou l'API n'a pas été
redémarrée après modification. Procédure : arrêter uvicorn, vérifier le `.env` avec
`grep ENABLE_COMPARE_ROUTES .env`, relancer uvicorn.

### Le script evaluate_pipeline.py échoue au démarrage

Vérifier d'abord que l'API tourne (`curl http://localhost:8000/` doit répondre). Ensuite
vérifier que le dataset QA existe (`ls data/qa_dataset/`). Enfin vérifier que le venv est
activé (`which python` doit pointer vers `.venv/bin/python`).

### L'élève ne comprend pas la différence entre Recall@k et précision

Analogie à utiliser : imaginez une recherche Google pour "chaudière Viessmann garantie". Recall@5
mesure si la bonne page est parmi les 5 premiers résultats. La précision mesure si ces 5 résultats
sont tous pertinents. Un retriever peut avoir Recall@5 = 1.00 (la bonne page est toujours là) mais
retourner aussi 4 résultats sans rapport.

### L'élève confond TCO et coût par requête

Le coût par requête (0.01 €/req pour Claude API) est le coût variable. Le TCO intègre le coût
fixe (setup 3000-3500 €) + le coût variable (run) sur 12 mois. Un coût par requête élevé peut
être moins cher en TCO qu'un setup FT coûteux si le volume est faible.

### L'élève veut "faire les trois" sans choisir

C'est une réponse de confort. Demandez : "Si tu avais 2 semaines de développement et 2000 €
de budget cloud, dans quel ordre tu feras quoi ?" Forcer la contrainte de ressources oblige
à prioriser et à argumenter.

### L'élève a une recommandation mais ne peut pas citer un seul chiffre

Retour à l'étape Mesure-toi. La recommandation doit être fondée sur les données mesurées, pas
sur l'impression générale. Demandez : "Sur quels chiffres tu t'appuies pour dire ça ?" Si l'élève
ne peut pas répondre, il n'a pas encore les données pour recommander.

### Les patches git apply échouent avec des conflits

L'élève a modifié `evaluate_pipeline.py` avant d'appliquer le patch. Réinitialiser le fichier
source sans perdre les autres modifications :

```bash
git checkout ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
```

Puis relancer le patch. Si l'élève a des modifications importantes qu'il veut conserver, les
mettre de côté dans un fichier séparé avant de réinitialiser.

### La soutenance est trop courte (moins de 2 minutes)

L'élève n'a pas de chiffres à défendre. Arrêter la soutenance et demander de remplir d'abord
le tableau Mesure-toi. Une soutenance de 5 minutes avec trois métriques est faisable même sans
avoir tout compris. Une soutenance de 30 secondes signifie que l'élève n'a pas de données.
