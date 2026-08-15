from embedding_service import create_embeddings
from vector_store import VectorStore


code_chunks = [
    """
    class FastAPI:
        def __init__(
            self,
            debug: bool = False
        ):
            self.debug = debug
    """,

    """
    def connect_database():
        connection = create_connection()
        return connection
    """,

    """
    def authenticate_user(username, password):
        user = find_user(username)
        return verify_password(
            password,
            user.password
        )
    """
]


embeddings = create_embeddings(code_chunks)


dimension = embeddings.shape[1]

store = VectorStore(dimension)

store.add(
    embeddings,
    code_chunks
)


query = "How is a user authenticated?"

query_embedding = create_embeddings([query])

results = store.search(
    query_embedding,
    top_k=2
)


print("Query:", query)

print("\nRelevant code:")

for result in results:
    print("\n---")
    print(result["text"])
    print("Distance:", result["distance"])