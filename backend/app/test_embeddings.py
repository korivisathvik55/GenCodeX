from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


texts = [
    "FastAPI creates a web application.",
    "The FastAPI class initializes the application.",
    "Python is a programming language."
]


embeddings = model.encode(texts)


print("Number of texts:", len(texts))
print("Embedding shape:", embeddings.shape)
print("First embedding dimensions:", len(embeddings[0]))