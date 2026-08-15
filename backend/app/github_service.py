from github import Github


def get_repository(repo_url):
    repo_name = repo_url.rstrip("/").replace(
        "https://github.com/", ""
    )

    github = Github()
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

    github = Github()
    repository = github.get_repo(repo_name)

    contents = repository.get_contents("")

    files = []

    for item in contents:
        if item.type == "file":
            files.append({
                "name": item.name,
                "path": item.path,
                "size": item.size
            })

    return {
        "repository": repository.full_name,
        "files": files
    }