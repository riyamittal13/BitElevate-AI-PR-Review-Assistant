import re

import requests

from config import GITHUB_API_URL, GITHUB_TOKEN, MAX_FILES, REQUEST_TIMEOUT


class GitHubError(Exception):
    """Raised when GitHub data cannot be retrieved."""


def parse_pr_url(url: str):
    """Extract owner, repository and PR number from a GitHub URL."""

    pattern = r"^https?://github\.com/([\w.-]+)/([\w.-]+)/pull/(\d+)/?$"

    match = re.match(pattern, url.strip())

    if not match:
        raise GitHubError(
            "Invalid URL. Use a link like "
            "https://github.com/owner/repository/pull/123"
        )

    owner, repo, number = match.groups()

    return owner, repo, int(number)


def _headers():
    """Prepare headers for GitHub API requests."""

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


def _get(url, params=None):
    """Send a request to GitHub and handle API errors."""

    try:
        response = requests.get(
            url,
            headers=_headers(),
            params=params,
            timeout=REQUEST_TIMEOUT
        )

    except requests.RequestException as exc:
        raise GitHubError(
            f"Could not connect to GitHub: {exc}"
        ) from exc

    if response.status_code == 404:
        raise GitHubError(
            "Pull request not found. Check the URL "
            "and ensure the repository is public."
        )

    if response.status_code in (403, 429):
        raise GitHubError(
            "GitHub rate limit reached or access denied. "
            "Try adding a GitHub token to your .env file."
        )

    if response.status_code != 200:
        raise GitHubError(
            f"GitHub API error: {response.status_code}"
        )

    return response.json()


def fetch_pr(url: str) -> dict:
    """Fetch pull request details and changed files."""

    owner, repo, number = parse_pr_url(url)

    base_url = (
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{number}"
    )

    pr = _get(base_url)

    files = _get(
        f"{base_url}/files",
        params={"per_page": MAX_FILES}
    )

    return {
        "title": pr["title"],
        "description": pr.get("body") or "",
        "author": pr["user"]["login"],
        "state": pr["state"],
        "head_sha": pr["head"]["sha"],
        "changed_files_count": pr["changed_files"],
        "additions": pr["additions"],
        "deletions": pr["deletions"],

        "files": [
            {
                "filename": file["filename"],
                "status": file["status"],
                "additions": file["additions"],
                "deletions": file["deletions"],
                "patch": file.get("patch"),
                "raw_url": file.get("raw_url")
            }
            for file in files
        ]
    }
