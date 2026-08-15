from github import Github

from .github_service import (
    get_github_client,
    get_file_content
)
from .chunking_service import chunk_code
from .code_search_service import search_code


REPO_NAME = "fastapi/fastapi"
FILE_PATH = "fastapi/applications.py"


github = get_github_client()

repository = github.get_repo(REPO_NAME)

content = get_file_content(
    repository,
    FILE_PATH
)

chunks = chunk_code(content)

print("Repository:", repository.full_name)
print("File:", FILE_PATH)
print("Total chunks:", len(chunks))


query = "How is the FastAPI application initialized?"

results = search_code(
    chunks,
    query,
    top_k=3
)


print("\nQuery:", query)

print("\nRelevant code:")

for index, result in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print(result["text"])
    print("Distance:", result["distance"])