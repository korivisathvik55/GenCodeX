from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .github_service import (
    get_repository,
    get_repository_files,
    get_file_content
)

app = FastAPI(title="GenCodeX API")


class RepositoryRequest(BaseModel):
    repo_url: str


@app.get("/")
def home():
    return {
        "message": "Welcome to GenCodeX!",
        "status": "running"
    }
@app.post("/repositories/files")
def repository_files(request: RepositoryRequest):
    try:
        return get_repository_files(request.repo_url)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.post("/repositories")
def repository_info(request: RepositoryRequest):
    try:
        return get_repository(request.repo_url)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.post("/repositories/content")
def repository_file_content(request: RepositoryRequest):
    try:
        repo_name = request.repo_url.rstrip("/").replace(
            "https://github.com/", ""
        )

        from github import Github
        from .github_service import get_github_client

        github = get_github_client()
        repository = github.get_repo(repo_name)

        file_path = "README.md"

        content = get_file_content(
            repository,
            file_path
        )

        return {
            "repository": repository.full_name,
            "file": file_path,
            "content": content
        }

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )