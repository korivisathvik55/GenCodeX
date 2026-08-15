import os

from dotenv import load_dotenv
from github import Github


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".html",
    ".css",
    ".json",
    ".md",
    ".txt"
}


def get_github_client():
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is not configured.")

    return Github(GITHUB_TOKEN)


def get_repository(repo_url):
    repo_name = repo_url.rstrip("/").replace(
        "https://github.com/", ""
    )

    github = get_github_client()
    repository = github.get_repo(repo_name)

    return {
        "name": repository.name,
        "full_name": repository.full_name,
        "description": repository.description,
        "language": repository.language,
        "stars": repository.stargazers_count,
        "forks": repository.forks_count
    }


def get_repository_files(repo_url):
    repo_name = repo_url.rstrip("/").replace(
        "https://github.com/", ""
    )

    github = get_github_client()
    repository = github.get_repo(repo_name)

    branch = repository.default_branch

    tree = repository.get_git_tree(
        branch,
        recursive=True
    )

    files = []

    for item in tree.tree:
        if item.type != "blob":
            continue

        file_name = item.path.split("/")[-1]
        file_extension = ""

        if "." in file_name:
            file_extension = "." + file_name.split(".")[-1].lower()

        if file_extension in ALLOWED_EXTENSIONS:
            files.append({
                "name": file_name,
                "path": item.path,
                "size": item.size
            })

    return {
        "repository": repository.full_name,
        "branch": branch,
        "total_files": len(files),
        "files": files
    }
def get_file_content(repository, file_path):
    file = repository.get_contents(file_path)

    if isinstance(file, list):
        raise ValueError("The provided path is a directory, not a file.")

    content = file.decoded_content.decode("utf-8")

    return content