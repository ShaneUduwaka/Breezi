import json
import re
import joblib
import numpy as np

from pathlib import Path
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score


class Tier1NLU:
    """
    Tier 1 NLU:
    - Tier 0: small keyword override layer
    - Tier 1: Naive Bayes intent classifier
    """

    def __init__(
        self,
        confidence_threshold: float = 0.72,
        model_path: str = "tier1_model.pkl",
    ):
        self.confidence_threshold = confidence_threshold
        self.model_path = model_path
        self.pipeline: Pipeline | None = None
        self.labels: list[str] = []

        # Keep this SMALL.
        # Only for extremely clear, deterministic triggers.
        self.keyword_rules = {
            "clear_cart": [
                "clear cart",
                "remove all from cart",
                "empty cart",
            ],
            "talk_to_human": [
                "agent",
                "customer service",
                "representative",
            ],
        }

    # -------------------------
    # TEXT CLEANING
    # -------------------------
    def normalize_text(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)
        return text

    # -------------------------
    # LOAD ONE JSONL FILE
    # -------------------------
    def load_jsonl(self, file_path: str) -> tuple[list[str], list[str]]:
        texts = []
        labels = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    row = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Invalid JSON in {file_path} on line {line_number}: {e}"
                    ) from e

                if "intent" not in row or "user" not in row:
                    raise ValueError(
                        f"{file_path} line {line_number} must contain 'intent' and 'user' fields."
                    )

                intent = str(row["intent"]).strip()
                user_text = self.normalize_text(str(row["user"]))

                if not intent or not user_text:
                    continue

                texts.append(user_text)
                labels.append(intent)

        if not texts:
            raise ValueError(f"No valid training rows found in dataset: {file_path}")

        return texts, labels

    # -------------------------
    # LOAD MULTIPLE JSONL FILES
    # -------------------------
    def load_multiple_jsonl(self, file_paths: list[str]) -> tuple[list[str], list[str]]:
        all_texts = []
        all_labels = []

        for file_path in file_paths:
            print(f"Loading file: {file_path}")
            texts, labels = self.load_jsonl(file_path)
            all_texts.extend(texts)
            all_labels.extend(labels)

        if not all_texts:
            raise ValueError("No valid data found in any dataset files.")

        print(f"\nTotal combined samples: {len(all_texts)}")
        return all_texts, all_labels

    # -------------------------
    # OPTIONAL DATA CHECK
    # -------------------------
    def show_dataset_stats(self, labels: list[str]) -> None:
        counts = Counter(labels)

        print("\nDataset summary")
        print("-" * 50)
        print(f"Total examples : {len(labels)}")
        print(f"Total intents  : {len(counts)}")
        print("\nExamples per intent:")
        for intent, count in counts.most_common():
            warning = "  <-- LOW DATA" if count < 10 else ""
            print(f"{intent:35} {count}{warning}")
        print("-" * 50)

    # -------------------------
    # KEYWORD OVERRIDE
    # -------------------------
    def keyword_match(self, text: str) -> dict | None:
        for intent, phrases in self.keyword_rules.items():
            for phrase in phrases:
                if phrase in text:
                    return {
                        "status": "SUCCESS",
                        "tier": 0,
                        "intent": intent,
                        "confidence": 1.0,
                        "source": "keyword_rule",
                    }
        return None

    # -------------------------
    # BUILD MODEL
    # -------------------------
    def build_pipeline(self) -> Pipeline:
        """
        TF-IDF + MultinomialNB:
        - fast
        - strong lightweight baseline
        - good for many intent classes
        - char_wb ngrams help with Sinhala/English mixed text and spelling variation
        """
        return Pipeline(
            steps=[
                (
                    "vectorizer",
                    TfidfVectorizer(
                        lowercase=False,   # already normalized
                        analyzer="char_wb",
                        ngram_range=(2, 5),
                        min_df=1,
                    ),
                ),
                (
                    "classifier",
                    MultinomialNB(alpha=0.3),
                ),
            ]
        )

    # -------------------------
    # INTERNAL TRAIN LOGIC
    # -------------------------
    def _train_from_texts_and_labels(
        self,
        texts: list[str],
        labels: list[str],
        test_size: float = 0.2,
        random_state: int = 42,
    ):
        self.show_dataset_stats(labels)

        # keep only intents that have at least 2 examples
        intent_counts = Counter(labels)
        valid_intents = {intent for intent, count in intent_counts.items() if count >= 2}

        filtered_texts = []
        filtered_labels = []

        for text, label in zip(texts, labels):
            if label in valid_intents:
                filtered_texts.append(text)
                filtered_labels.append(label)

        if not filtered_texts:
            raise ValueError("No valid samples left after filtering low-count intents.")

        self.labels = sorted(set(filtered_labels))

        print(
            f"\nFiltered dataset: {len(filtered_texts)} examples, "
            f"{len(self.labels)} intents"
        )

        x_train, x_test, y_train, y_test = train_test_split(
            filtered_texts,
            filtered_labels,
            test_size=test_size,
            random_state=random_state,
            stratify=filtered_labels,
        )

        self.pipeline = self.build_pipeline()
        self.pipeline.fit(x_train, y_train)

        y_pred = self.pipeline.predict(x_test)

        print("\nEvaluation")
        print("-" * 50)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification report:")
        print(classification_report(y_test, y_pred, digits=4))
        print("-" * 50)

        self.save_model()

    # -------------------------
    # TRAIN FROM ONE FILE
    # -------------------------
    def train(
        self,
        dataset_path: str,
        test_size: float = 0.2,
        random_state: int = 42,
    ):
        texts, labels = self.load_jsonl(dataset_path)
        self._train_from_texts_and_labels(
            texts=texts,
            labels=labels,
            test_size=test_size,
            random_state=random_state,
        )

    # -------------------------
    # TRAIN FROM MULTIPLE FILES
    # -------------------------
    def train_multiple(
        self,
        dataset_paths: list[str],
        test_size: float = 0.2,
        random_state: int = 42,
    ):
        texts, labels = self.load_multiple_jsonl(dataset_paths)
        self._train_from_texts_and_labels(
            texts=texts,
            labels=labels,
            test_size=test_size,
            random_state=random_state,
        )

    # -------------------------
    # SAVE / LOAD
    # -------------------------
    def save_model(self):
        if self.pipeline is None:
            raise ValueError("No trained model to save.")

        payload = {
            "pipeline": self.pipeline,
            "labels": self.labels,
            "confidence_threshold": self.confidence_threshold,
            "keyword_rules": self.keyword_rules,
        }

        joblib.dump(payload, self.model_path)
        print(f"\nSaved model to: {self.model_path}")

    def load_model(self):
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        payload = joblib.load(self.model_path)
        self.pipeline = payload["pipeline"]
        self.labels = payload["labels"]
        self.confidence_threshold = payload["confidence_threshold"]
        self.keyword_rules = payload["keyword_rules"]

        print(f"Loaded model from: {self.model_path}")

    # -------------------------
    # PREDICT
    # -------------------------
    def predict(self, user_text: str) -> dict:
        if self.pipeline is None:
            raise ValueError("Model is not loaded or trained.")

        clean_text = self.normalize_text(user_text)

        # 1) Tier 0 keyword override
        keyword_result = self.keyword_match(clean_text)
        if keyword_result:
            return keyword_result

        # 2) Naive Bayes prediction
        probabilities = self.pipeline.predict_proba([clean_text])[0]
        predicted_index = int(np.argmax(probabilities))
        predicted_intent = self.pipeline.classes_[predicted_index]
        confidence = float(probabilities[predicted_index])

        # Top 3 candidates for debugging
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_3 = [
            {
                "intent": self.pipeline.classes_[i],
                "score": round(float(probabilities[i]), 4),
            }
            for i in top_indices
        ]

        if confidence >= self.confidence_threshold:
            return {
                "status": "SUCCESS",
                "tier": 1,
                "intent": predicted_intent,
                "confidence": round(confidence, 4),
                "source": "naive_bayes",
                "top_3": top_3,
            }

        return {
            "status": "FALLBACK",
            "tier": 1,
            "intent": predicted_intent,
            "confidence": round(confidence, 4),
            "source": "naive_bayes",
            "top_3": top_3,
            "reason": "Low confidence. Send to Tier 2 semantic search.",
        }


if __name__ == "__main__":
    import sys
    import os
    
    nlu = Tier1NLU(
        confidence_threshold=0.72,
        model_path="tier1_model.pkl",
    )

    # Check if model exists and load it; otherwise train from scratch
    if os.path.exists("tier1_model.pkl"):
        print("Loading existing model...")
        nlu.load_model()
    else:
        print("No model found. Training from scratch...")
        DATASETS = [
            "state3_extracted.jsonl",
            "state2_extracted.jsonl",
        ]
        nlu.train_multiple(DATASETS)

    # Interactive mode: accept input from command line or stdin
    print("\n" + "=" * 50)
    print("Tier 1 NLU - Interactive Prediction Mode")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # If text provided as argument, predict and exit
        user_input = " ".join(sys.argv[1:])
        print(f"\nUser: {user_input}")
        result = nlu.predict(user_input)
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
                result = nlu.predict(user_input)
                print(f"Result: {result}")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")