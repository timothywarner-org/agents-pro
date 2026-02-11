"""GitHub issue fetcher using the GitHub REST API.

This is a simple stand-in for MCP-driven fetching in a local run.
It requires a GITHUB_TOKEN in your environment.
"""

from typing import Any, Dict


def fetch_github_issue(owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
    """Fetch a GitHub issue and map it to the pipeline Issue schema."""
    try:
        import os
        import requests

        github_token = os.getenv("GITHUB_TOKEN")

        if not github_token:
            raise RuntimeError(
                "GITHUB_TOKEN not found in environment. "
                "Please set it in your .env file."
            )

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        gh_issue = response.json()

        if "pull_request" in gh_issue:
            raise RuntimeError(
                f"Issue #{issue_number} is a pull request. "
                "Please use an issue number, not a PR number."
            )

        return {
            "issue_id": f"{owner}/{repo}#{issue_number}",
            "repo": f"{owner}/{repo}",
            "issue_number": issue_number,
            "title": gh_issue["title"],
            "body": gh_issue.get("body") or "",
            "labels": [label["name"] for label in gh_issue.get("labels", [])],
            "url": gh_issue["html_url"],
            "source": "github-mcp",
        }

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise RuntimeError(
                f"Issue #{issue_number} not found in {owner}/{repo}. "
                "Check that the issue exists and you have access."
            ) from e
        if e.response.status_code == 401:
            raise RuntimeError(
                "GitHub authentication failed. "
                "Check that your GITHUB_TOKEN is valid."
            ) from e
        raise RuntimeError(f"GitHub API error: {e}") from e

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch GitHub issue: {e}") from e

    except Exception as e:
        raise RuntimeError(f"Unexpected error fetching issue: {e}") from e
