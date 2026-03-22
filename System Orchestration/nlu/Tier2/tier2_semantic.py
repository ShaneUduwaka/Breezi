import re
import joblib
import numpy as np

from collections import defaultdict
from sentence_transformers import SentenceTransformer


class Tier2SemanticRouter:
    def __init__(
        self,
        index_path: str = "tier2_index.pkl",
        confidence_threshold: float = 0.78,
        top_k: int = 5,
    ):
        self.index_path = index_path
        self.confidence_threshold = confidence_threshold
        self.top_k = top_k

        payload = joblib.load(index_path)

        self.model_name = payload["model_name"]
        self.texts = payload["texts"]
        self.intents = payload["intents"]
        self.embeddings = payload["embeddings"]

        self.model = SentenceTransformer(self.model_name)

    def normalize_text(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)
        return text

    def predict(self, user_text: str) -> dict:
        clean_text = self.normalize_text(user_text)

        query_embedding = self.model.encode(
            [clean_text],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        # cosine similarity because embeddings are normalized
        scores = np.dot(self.embeddings, query_embedding)

        top_indices = np.argsort(scores)[::-1][:self.top_k]

        top_matches = []
        intent_scores = defaultdict(list)

        for idx in top_indices:
            score = float(scores[idx])
            intent = self.intents[idx]
            text = self.texts[idx]

            top_matches.append({
                "intent": intent,
                "text": text,
                "score": round(score, 4),
            })

            intent_scores[intent].append(score)

        # score each intent by average of its matched examples
        aggregated_scores = {
            intent: sum(score_list) / len(score_list)
            for intent, score_list in intent_scores.items()
        }

        best_intent = max(aggregated_scores, key=aggregated_scores.get)
        best_score = aggregated_scores[best_intent]

        if best_score >= self.confidence_threshold:
            return {
                "status": "SUCCESS",
                "tier": 2,
                "intent": best_intent,
                "confidence": round(best_score, 4),
                "source": "semantic_search",
                "top_matches": top_matches,
            }

        return {
            "status": "FALLBACK",
            "tier": 2,
            "intent": best_intent,
            "confidence": round(best_score, 4),
            "source": "semantic_search",
            "top_matches": top_matches,
            "reason": "Low semantic confidence. Send to Tier 3.",
        }


if __name__ == "__main__":
    import sys
    import os
    
    try:
        router = Tier2SemanticRouter(
            index_path="tier2_index.pkl",
            confidence_threshold=0.78,
            top_k=5,
        )
    except FileNotFoundError:
        print("Error: tier2_index.pkl not found.")
        print("Please run: python Tier2/build_tier2_index.py")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Tier 2 Semantic Router - Interactive Prediction Mode")
    print("=" * 50)

    if len(sys.argv) > 1:
        # If text provided as argument, predict and exit
        user_input = " ".join(sys.argv[1:])
        print(f"\nUser: {user_input}")
        result = router.predict(user_input)
        print(f"Prediction: {result}")
    else:
        # Interactive loop
        while True:
            try:
                user_input = input("\nEnter text (or 'quit' to exit): ").strip()
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break
                if not user_input:
                    continue
                result = router.predict(user_input)
                print(f"Result: {result}")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")