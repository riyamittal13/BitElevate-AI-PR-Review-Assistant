import subprocess

import requests
from google.genai.errors import APIError

from analyzer import analyze_code
from github_client import GitHubError, fetch_pr
from reviewer import review_pull_request

url = "https://github.com/psf/requests/pull/7388"

try:
    print("Fetching Pull Request...")
    pr = fetch_pr(url)

    print("Running static analysis...")

    static_results = {
        "ruff_findings": [],
        "bandit_findings": [],
        "error": None
    }

    for file in pr["files"]:
        if not file["filename"].endswith(".py"):
            continue

        print("Analyzing:", file["filename"])

        try:
            response = requests.get(
                file["raw_url"],
                timeout=20
            )
            response.raise_for_status()

            results = analyze_code(
                response.text,
                file["filename"]
            )

            static_results["ruff_findings"].extend(
                results["ruff_findings"]
            )

            static_results["bandit_findings"].extend(
                results["bandit_findings"]
            )

        except (requests.RequestException, subprocess.SubprocessError, OSError) as error:
            print("Could not analyze:", file["filename"], error)

    print("Sending changes to Gemini for review...")
    report = review_pull_request(pr, static_results)

    print("\n--- AI CODE REVIEW ---")
    print("Summary:", report.summary)
    print("Overall Status:", report.overall_status)

    print("\nFindings:")
    for finding in report.findings:
        print(f"\nSeverity: {finding.severity}")
        print(f"File: {finding.file_name}")
        print(f"Line: {finding.line_number}")
        print(f"Issue: {finding.issue}")
        print(f"Explanation: {finding.explanation}")
        print(f"Suggested Fix: {finding.suggested_fix}")

    print("\nLearning Recommendations:")
    for item in report.learning_recommendations:
        print("-", item)

except (GitHubError, ValueError) as error:
    print("\nProblem:", error)

except (APIError, requests.RequestException, subprocess.SubprocessError, OSError) as error:
    print("\nUnexpected error:", error)
