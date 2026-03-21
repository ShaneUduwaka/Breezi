import uuid
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from data import documents

load_dotenv()

openai_client = OpenAI()

# Qdrant in local file mode
qdrant = QdrantClient(path="qdrant_data")

COLLECTION_NAME = "my_collection"
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 1536  # size for text-embedding-3-small


def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def main():
    # Create the collection fresh each time
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    points = []

    for doc in documents:
        embedding = get_embedding(doc)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": doc}
            )
        )

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Done! Your documents are now stored in Qdrant.")


if __name__ == "__main__":
    main()