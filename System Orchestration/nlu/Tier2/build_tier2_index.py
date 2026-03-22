import json
import re
import joblib
import numpy as np

from sentence_transformers import SentenceTransformer


class Tier2IndexBuilder:
    def __init__(
        self,
        dataset_paths: list[str],
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
        output_path: str = "tier2_index.pkl",
    ):
        self.dataset_paths = dataset_paths
        self.model_name = model_name
        self.output_path = output_path
        self.model = SentenceTransformer(model_name)

    def normalize_text(self, text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)
        return text

    def load_multiple_jsonl(self) -> tuple[list[str], list[str]]:
        texts = []
        intents = []

        for file_path in self.dataset_paths:
            print(f"Loading file: {file_path}")

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
                        continue

                    text = self.normalize_text(str(row["user"]))
                    intent = str(row["intent"]).strip()

                    if text and intent:
                        texts.append(text)
                        intents.append(intent)

        if not texts:
            raise ValueError("No valid data found in any dataset files.")

        print(f"\nTotal combined samples: {len(texts)}")
        return texts, intents

    def build(self):
        texts, intents = self.load_multiple_jsonl()

        print("Creating embeddings...")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        payload = {
            "model_name": self.model_name,
            "texts": texts,
            "intents": intents,
            "embeddings": embeddings,
        }

        joblib.dump(payload, self.output_path)
        print(f"\nSaved Tier 2 index to: {self.output_path}")


if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    DATASETS = [
        os.path.join(script_dir, "state3_extracted.jsonl"),
        os.path.join(script_dir, "state2_extracted.jsonl"),
    ]

    builder = Tier2IndexBuilder(
        dataset_paths=DATASETS,
        model_name="paraphrase-multilingual-MiniLM-L12-v2",
        output_path=os.path.join(script_dir, "tier2_index.pkl"),
    )
    builder.build()