import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


texts = [
    "FastAPI creates a web application.",
    "The database connection uses MySQL.",
    "Authentication is handled using JWT tokens."
]


embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")


dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


query = "How does authentication work?"

query_embedding = model.encode([query])

query_embedding = np.array(query_embedding).astype("float32")


distances, indices = index.search(
    query_embedding,
    k=2
)


print("Query:", query)

print("\nTop results:")

for rank, index_position in enumerate(indices[0], start=1):
    print(
        f"{rank}. {texts[index_position]}"
    )

print("\nDistances:", distances[0])