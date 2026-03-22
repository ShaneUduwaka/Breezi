from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv()

openai_client = OpenAI()
qdrant = QdrantClient(path="qdrant_data")

COLLECTION_NAME = "my_collection"
EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def search_documents(query: str, limit: int = 3):
    query_embedding = get_embedding(query)

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit
    )

    return results


def main():
    print("Simple RAG search")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question: ")

        if query.lower() == "exit":
            print("Goodbye!")
            break

        results = search_documents(query)

        print("\nTop matching results:\n")
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result.payload['text']}")
        print()


if __name__ == "__main__":
    main()