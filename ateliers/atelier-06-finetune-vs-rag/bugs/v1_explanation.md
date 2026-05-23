# Bug v1 — Eval lancée sur le train set (illusion 100% recall)

## Contexte

Le script d'évaluation charge le même fichier pour entraîner les index ET pour les évaluer. Comme les questions ont été indexées au moment de la construction du vectorstore, le retriever les retrouve avec 100% de recall. Ce n'est pas un vrai benchmark — c'est un test de mémorisation.

## Affirmations Vrai / Faux

**1. "Un recall@5 de 1.00 sur toutes les stratégies est le signe d'un excellent système RAG."**

[ ] Vrai   [ ] Faux

**2. "La seule façon de détecter ce bug est de regarder le code. L'output seul ne permet pas de le détecter."**

[ ] Vrai   [ ] Faux

**3. "Un overlap de 10% entre train et test est acceptable pour une évaluation RAG."**

[ ] Vrai   [ ] Faux

**4. "Ce bug peut conduire à déployer un système RAG qui sous-performe en production par rapport aux métriques annoncées."**

[ ] Vrai   [ ] Faux

**5. "Pour éviter ce bug, il suffit de ne pas indexer les questions du dataset de test dans le vectorstore."**

[ ] Vrai   [ ] Faux

---

## Réponses commentées

1. **FAUX** — Un recall parfait sur toutes les stratégies est le signal le plus évident d'une fuite de données (data leakage). Dans un vrai benchmark, les stratégies ont des scores différents et imparfaits. Recall@5 = 1.00 pour "fixed" et "ensemble" = suspect.

2. **FAUX** — L'output révèle le problème : si les 3 stratégies donnent recall = 1.00, c'est anormal. Une stratégie fixed-size à chunk=512 ne devrait pas avoir le même recall qu'un ensemble. L'écart nul entre stratégies est le signal d'alerte.

3. **VRAI et FAUX** — 10% d'overlap peut être acceptable si les questions ne sont pas identiques mais seulement similaires thématiquement. En pratique : overlap = 0% est l'objectif pour un benchmark rigoureux. 10% est tolérable si les questions de test testent la généralisation, pas la mémorisation.

4. **VRAI** — C'est exactement le risque. L'équipe annonce "Recall@5 = 0.95", déploie, et découvre en prod que le recall réel est ~0.72. La confiance est érodée, les utilisateurs se plaignent, l'équipe ne comprend pas pourquoi. Le bug de méthodologie est aussi coûteux qu'un bug de code.

5. **VRAI (nécessaire mais pas suffisant)** — Ne pas indexer les questions de test empêche la fuite directe. Mais il faut aussi vérifier que les documents sources des questions de test ne sont pas utilisés pour les questions de train (fuite indirecte via les documents).
