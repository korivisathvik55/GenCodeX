from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github import GithubException

from .chunking_service import chunk_code
from .code_search_service import search_code
from .llm_service import generate_answer
from .github_service import (
    get_repository,
    get_repository_files,
    get_file_content,
    get_github_client
)


app = FastAPI(title="GenCodeX API")


# -----------------------------
# Request Models
# -----------------------------

class RepositoryRequest(BaseModel):
    repo_url: str


class RepositoryContentRequest(BaseModel):
    repo_url: str
    file_path: str


class RepositoryChunkRequest(BaseModel):
    repo_url: str
    file_path: str


class RepositoryAskRequest(BaseModel):
    repo_url: str
    file_path: str
    question: str


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to GenCodeX!",
        "status": "running"
    }


# -----------------------------
# Repository Information
# -----------------------------

@app.post("/repositories")
def repository_info(request: RepositoryRequest):
    try:
        return get_repository(request.repo_url)

    except GithubException as error:
        if error.status == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository not found on GitHub."
            )

        if error.status == 403:
            raise HTTPException(
                status_code=403,
                detail="GitHub access denied or API rate limit reached."
            )

        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {error}"
        )

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# -----------------------------
# Repository Files
# -----------------------------

@app.post("/repositories/files")
def repository_files(request: RepositoryRequest):
    try:
        return get_repository_files(request.repo_url)

    except GithubException as error:
        if error.status == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository not found on GitHub."
            )

        if error.status == 403:
            raise HTTPException(
                status_code=403,
                detail="GitHub access denied or API rate limit reached."
            )

        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {error}"
        )

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# -----------------------------
# Repository File Content
# -----------------------------

@app.post("/repositories/content")
def repository_file_content(
    request: RepositoryContentRequest
):
    if not request.file_path.strip():
        raise HTTPException(
            status_code=400,
            detail="File path cannot be empty."
        )

    try:
        repo_name = request.repo_url.rstrip("/").replace(
            "https://github.com/",
            ""
        )

        github = get_github_client()

        repository = github.get_repo(repo_name)

        content = get_file_content(
            repository,
            request.file_path
        )

        return {
            "repository": repository.full_name,
            "file": request.file_path,
            "content": content
        }

    except GithubException as error:
        if error.status == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository or file not found on GitHub."
            )

        if error.status == 403:
            raise HTTPException(
                status_code=403,
                detail="GitHub access denied or API rate limit reached."
            )

        if error.status == 401:
            raise HTTPException(
                status_code=401,
                detail="GitHub authentication failed."
            )

        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {error}"
        )

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# -----------------------------
# Repository Code Chunks
# -----------------------------

@app.post("/repositories/chunks")
def repository_chunks(
    request: RepositoryChunkRequest
):
    if not request.file_path.strip():
        raise HTTPException(
            status_code=400,
            detail="File path cannot be empty."
        )

    try:
        repo_name = request.repo_url.rstrip("/").replace(
            "https://github.com/",
            ""
        )

        github = get_github_client()

        repository = github.get_repo(repo_name)

        content = get_file_content(
            repository,
            request.file_path
        )

        if not content.strip():
            raise HTTPException(
                status_code=400,
                detail="The selected file is empty."
            )

        chunks = chunk_code(content)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not create code chunks."
            )

        return {
            "repository": repository.full_name,
            "file": request.file_path,
            "total_chunks": len(chunks),
            "chunks": [
                {
                    "chunk_id": index,
                    "content": chunk
                }
                for index, chunk in enumerate(
                    chunks,
                    start=1
                )
            ]
        }

    except GithubException as error:
        if error.status == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository or file not found on GitHub."
            )

        if error.status == 403:
            raise HTTPException(
                status_code=403,
                detail="GitHub access denied or API rate limit reached."
            )

        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {error}"
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# -----------------------------
# RAG / Ask Repository
# -----------------------------

@app.post("/repositories/ask")
def ask_repository(
    request: RepositoryAskRequest
):
    # Validate question
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Validate file path
    if not request.file_path.strip():
        raise HTTPException(
            status_code=400,
            detail="File path cannot be empty."
        )

    # Validate GitHub URL
    if not request.repo_url.startswith(
        "https://github.com/"
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Please provide a valid GitHub repository URL. "
                "Example: https://github.com/owner/repository"
            )
        )

    try:
        # Convert URL to owner/repository
        repo_name = request.repo_url.rstrip("/").replace(
            "https://github.com/",
            ""
        )

        if not repo_name or "/" not in repo_name:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid GitHub repository URL. "
                    "Use: https://github.com/owner/repository"
                )
            )

        # Connect to GitHub
        github = get_github_client()

        repository = github.get_repo(repo_name)

        # Get source code
        content = get_file_content(
            repository,
            request.file_path
        )

        if not content.strip():
            raise HTTPException(
                status_code=400,
                detail="The selected file is empty."
            )

        # Split code into chunks
        chunks = chunk_code(content)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Could not create code chunks."
            )

        # Semantic search using FAISS
        results = search_code(
            chunks,
            request.question,
            top_k=3
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No relevant code was found."
            )

        # Prepare context for the LLM
        context = "\n\n".join(
            result["text"]
            for result in results
        )

        # Generate answer using local Ollama LLM
        answer = generate_answer(
            request.question,
            context
        )

        # Return final RAG response
        return {
            "repository": repository.full_name,
            "file": request.file_path,
            "question": request.question,
            "answer": answer,
            "sources": [
                {
                    "file": request.file_path,
                    "chunk_id": result["chunk_id"],
                    "distance": result["distance"],
                    "content": result["text"]
                }
                for result in results
            ]
        }

    # -----------------------------
    # GitHub Errors
    # -----------------------------

    except GithubException as error:

        if error.status == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository or file not found on GitHub."
            )

        if error.status == 403:
            raise HTTPException(
                status_code=403,
                detail=(
                    "GitHub access denied or API rate limit reached."
                )
            )

        if error.status == 401:
            raise HTTPException(
                status_code=401,
                detail=(
                    "GitHub authentication failed. "
                    "Check your GitHub token."
                )
            )

        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {error}"
        )

    # -----------------------------
    # Preserve HTTP errors
    # -----------------------------

    except HTTPException:
        raise

    # -----------------------------
    # General Errors
    # -----------------------------

    except Exception as error:

        error_message = str(error)

        if (
            "Connection refused" in error_message
            or "Failed to establish a new connection"
            in error_message
        ):
            raise HTTPException(
                status_code=503,
                detail=(
                    "Ollama is not running. "
                    "Start Ollama and try again."
                )
            )

        raise HTTPException(
            status_code=500,
            detail=f"GenCodeX processing error: {error_message}"
        )