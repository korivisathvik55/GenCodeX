from .embedding_service import create_embeddings
from .vector_store import VectorStore


def search_code(chunks, query, top_k=3):
    if not chunks:
        return []

    embeddings = create_embeddings(chunks)

    dimension = embeddings.shape[1]

    store = VectorStore(dimension)

    store.add(
        embeddings,
        chunks
    )

    query_embedding = create_embeddings([query])

    results = store.search(
        query_embedding,
        top_k=top_k
    )

    return results