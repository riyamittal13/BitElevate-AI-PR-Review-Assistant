
import json

from google import genai

from config import GEMINI_API_KEY
from schemas import ReviewReport

# MODEL_NAME = "gemini-3.6-flash"
# MODEL_NAME = "gemini-3.8-flash"
# MODEL_NAME = "gemini-3.5-flash-lite"
MODEL_NAME = "gemini-3.1-flash-lite"


def review_pull_request(pr_data: dict, static_analysis: dict) -> ReviewReport:
    """Use Gemini to review GitHub PR changes."""

    if not GEMINI_API_KEY:
        raise ValueError(
            "Gemini API key is missing. Add it to your .env file."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Prepare the changed code for Gemini.
    changed_files = []

    for file in pr_data.get("files", []):
        patch = file.get("patch")

        if not patch:
            continue

        changed_files.append({
            "filename": file["filename"],
            "patch": patch[:12000]
        })

    if not changed_files:
        raise ValueError(
            "No readable code changes found in this Pull Request."
        )

    prompt = f"""
You are an experienced software engineer conducting a
careful GitHub Pull Request code review.

Review the following Pull Request.

PR TITLE:
{pr_data.get("title", "")}

PR DESCRIPTION:
{pr_data.get("description", "")}

CHANGED CODE:
{json.dumps(changed_files, indent=2)}

STATIC ANALYSIS RESULTS:
{json.dumps(static_analysis, indent=2)}

YOUR TASK:
1. Identify genuine logical bugs and potential runtime errors.
2. Identify code quality and maintainability problems.
3. Identify possible security risks.
4. Consider the Ruff and Bandit findings provided above.
5. Avoid repeating the same issue unnecessarily.
6. Do not invent issues. Report only problems supported by the code.
7. Give clear explanations and practical suggested fixes.
8. Use the exact filename from the supplied changes.
9. Use the closest relevant line number when possible.
10. If no significant issues are found, return an empty findings list.

Severity must be one of:
Critical, High, Medium, Low.

Overall status must be one of:
Good, Needs Improvement, Critical.

Return a structured review report.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ReviewReport.model_json_schema()
        }
    )

    return ReviewReport.model_validate_json(response.text)
