from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .github_service import get_repository, get_repository_files
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