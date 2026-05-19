"""
Pré-télécharge le modèle d'embeddings via fastembed (~100 Mo ONNX quantisé).
À lancer une seule fois avant la formation, idéalement avec une bonne connexion.
Cache : ~/.cache/fastembed/
"""

from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main():
    print(f"Téléchargement du modèle d'embeddings : {MODEL_NAME}")
    print("(~100 Mo ONNX quantisé — cache dans ~/.cache/fastembed/)")
    model = TextEmbedding(model_name=MODEL_NAME)

    test_phrases = [
        "Comment fonctionne ma chaudière ?",
        "Quelle est la température recommandée la nuit ?",
    ]
    embeddings = list(model.embed(test_phrases))
    print(f"\n✓ Modèle prêt — dimension des embeddings : {len(embeddings[0])}")
    print(f"  Test encodage : {len(test_phrases)} phrases -> {len(embeddings)} vecteurs")
    print("\nLe modèle est maintenant en cache — les prochains chargements seront instantanés.")


if __name__ == "__main__":
    main()
