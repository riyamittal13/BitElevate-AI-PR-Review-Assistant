import subprocess

import requests
import streamlit as st
from google.genai.errors import APIError

from analyzer import analyze_code
from github_client import GitHubError, fetch_pr
from reviewer import review_pull_request

st.set_page_config(
    page_title="BitElevate AI PR Review Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 BitElevate AI PR Review Assistant")
st.caption("Smarter Code Reviews. Better Learning.")

st.write(
    "Analyze GitHub Pull Requests using AI, "
    "static code analysis, and actionable recommendations."
)

st.info(
    "This tool provides preliminary AI-assisted reviews. "
    "Final code approval must always be performed by a human reviewer."
)

pr_url = st.text_input(
    "GitHub Pull Request URL",
    placeholder="https://github.com/owner/repository/pull/123"
)

if st.button("Review Pull Request", type="primary"):

    if not pr_url.strip():
        st.warning("Please enter a GitHub Pull Request URL.")

    else:
        try:
            with st.spinner("Fetching Pull Request..."):
                pr = fetch_pr(pr_url)

            st.success("Pull Request fetched successfully!")

            st.subheader(pr["title"])

            col1, col2, col3 = st.columns(3)

            col1.metric("Author", pr["author"])
            col2.metric("Files Changed", pr["changed_files_count"])
            col3.metric("Lines Added", pr["additions"])

            st.metric("Lines Deleted", pr["deletions"])

            st.divider()

            static_results = {
                "ruff_findings": [],
                "bandit_findings": [],
                "error": None
            }

            with st.spinner("Running Ruff and Bandit..."):

                for file in pr["files"]:

                    if not file["filename"].endswith(".py"):
                        continue

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
                        st.warning(
                            f"Could not analyze {file['filename']}: {error}"
                        )

            with st.spinner("Gemini is reviewing your code..."):
                report = review_pull_request(pr, static_results)

            st.success("AI Code Review Completed!")

            st.subheader("Review Summary")
            st.write(report.summary)

            st.subheader("Overall Assessment")
            st.write(report.overall_status)

            st.divider()

            st.subheader("Code Review Findings")

            if report.findings:

                for finding in report.findings:

                    with st.expander(
                        f"{finding.severity} — {finding.issue}"
                    ):

                        st.write("**File:**", finding.file_name)
                        st.write("**Line:**", finding.line_number)
                        st.write("**Explanation:**", finding.explanation)
                        st.write("**Suggested Fix:**", finding.suggested_fix)

            else:
                st.success("No significant issues identified.")

            st.divider()

            st.subheader("Learning Recommendations")

            for recommendation in report.learning_recommendations:
                st.write("•", recommendation)

            st.caption(
                "BitElevate AI PR Review Assistant | "
                "AI-assisted review, human-led decisions."
            )

        except (GitHubError, ValueError) as error:
            st.error(str(error))

        except (APIError, requests.RequestException, subprocess.SubprocessError, OSError) as error:
            st.error(f"Review failed: {error}")
