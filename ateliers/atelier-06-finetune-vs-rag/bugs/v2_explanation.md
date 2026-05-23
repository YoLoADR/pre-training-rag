# Bug v2 — BLEU score pour mesurer le ton/style (métrique inadaptée)

## Contexte

BLEU (Bilingual Evaluation Understudy) est une métrique conçue pour évaluer les traductions automatiques. Elle mesure le chevauchement de n-grammes entre une réponse générée et une référence. Elle est inadaptée pour mesurer la qualité conversationnelle ou le ton "Merenza" parce qu'elle punit les paraphrases de bonne qualité.

Exemple : "Bonjour, votre chaudière est garantie 5 ans" vs "Bonsoir, la garantie de votre chaudière est de 5 ans" → même sens, BLEU très bas car les mots sont différents.

## Affirmations Vrai / Faux

**1. "BLEU est une bonne métrique pour mesurer si une réponse adopte le bon ton (chaleureux, concis, formel)."**

[ ] Vrai   [ ] Faux

**2. "Un score BLEU de 0.05 peut correspondre à une réponse de très haute qualité."**

[ ] Vrai   [ ] Faux

**3. "La cosine similarity entre embeddings est une meilleure alternative que BLEU pour le style."**

[ ] Vrai   [ ] Faux

**4. "Un LLM-judge avec rubric explicite est subjectif et donc moins fiable que BLEU."**

[ ] Vrai   [ ] Faux

**5. "Si on a 1000 paires (question, réponse de référence) annotées à la main, BLEU devient une bonne métrique."**

[ ] Vrai   [ ] Faux

---

## Réponses commentées

1. **FAUX** — BLEU mesure la similarité lexicale avec une référence. Le ton "chaleureux" peut être exprimé avec des mots très différents : "N'hésitez pas !", "Je suis là pour vous", "Avec plaisir !". BLEU pénalise toutes ces variantes si elles ne sont pas dans la référence.

2. **VRAI** — Un BLEU de 0.05 signifie 5% de n-grammes en commun avec la référence. Une paraphrase parfaite qui reformule toute la phrase avec des synonymes peut avoir un BLEU < 0.10. En traduction, des systèmes SOTA ont des BLEU ~ 0.40 — déjà considéré comme excellent.

3. **VRAI en partie** — La cosine similarity entre embeddings (ex: `text-embedding-3-small`) mesure la proximité sémantique, pas lexicale. "Bonjour" et "Bonsoir" sont sémantiquement très proches. BERTScore améliore encore ce point. Mais aucune de ces métriques ne capture "la chaleur du ton" aussi bien qu'un LLM-judge avec critères explicites.

4. **FAUX** — Un LLM-judge avec rubric explicite et reproductible (ex: "Est-ce que la réponse dit 'je' une fois ? Est-ce qu'elle propose une action concrète ? Est-ce qu'elle évite le jargon technique ?") est plus fiable que BLEU pour le style. La subjectivité du LLM-judge est contrôlée par la précision du rubric.

5. **FAUX** — Même avec 1000 références, BLEU reste une métrique lexicale. Si les 1000 références sont rédigées dans un style très varié (ce qui est réaliste), BLEU continue de pénaliser les bonnes réponses hors-vocabulaire. La taille du dataset de référence n'est pas le problème principal de BLEU.
