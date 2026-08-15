import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, embeddings, texts):
        embeddings = np.array(
            embeddings
        ).astype("float32")

        self.index.add(embeddings)

        self.texts.extend(texts)

    def search(self, query_embedding, top_k=3):
        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):
            if index == -1:
                continue

            results.append({
                "text": self.texts[index],
                "distance": float(distance)
            })

        return results