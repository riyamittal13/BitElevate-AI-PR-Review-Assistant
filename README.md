# BitElevate AI PR Review Assistant

### Smarter Code Reviews. Better Learning.

An AI-powered GitHub Pull Request review tool that combines static code analysis and Large Language Models to identify potential issues, explain findings, and provide actionable recommendations.

---

## Overview

The BitElevate AI PR Review Assistant performs preliminary analysis of GitHub Pull Requests to help developers identify potential code-quality issues, logical errors, and security concerns.

The application combines:

- GitHub REST API for Pull Request data retrieval.
- Ruff for Python code-quality analysis.
- Bandit for Python security analysis.
- Google Gemini for contextual AI-powered code review.
- Pydantic for structured review output.
- Streamlit for an interactive dashboard.

The tool is designed to support human reviewers, not replace them.

## Features

- **GitHub Pull Request Analysis:** Analyze public GitHub Pull Requests using their URLs.
- **Automated Static Analysis:** Run Ruff and Bandit on supported Python files.
- **AI-Powered Code Review:** Use Gemini to identify potential logical, runtime, quality, and security issues.
- **Structured Findings:** Display severity, file name, approximate line number, explanations, and suggested fixes.
- **Learning Recommendations:** Provide concepts developers may need to understand or revise.
- **Interactive Dashboard:** View Pull Request information and review results through Streamlit.

## Architecture

```text
User
 |
 v
Streamlit Dashboard
 |
 v
GitHub Client
 |
 v
GitHub REST API
 |
 v
Pull Request Data
 |
 v
Static Code Analysis
 |             |
Ruff         Bandit
 |             |
 +------+------+
        |
        v
   Gemini AI
        |
        v
 Pydantic Validation
        |
        v
 Structured Review
        |
        v
 Streamlit Dashboard
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Core development |
| Streamlit | User interface |
| GitHub REST API | Pull Request retrieval |
| Gemini 3.1 Flash-Lite | AI code review |
| Ruff | Code-quality analysis |
| Bandit | Security analysis |
| Pydantic | Structured output validation |
| Requests | API communication |
| python-dotenv | Environment configuration |
| Pytest | Testing framework |

## Project Structure

```text
bitelevate-ai-pr-review/
│
├── app.py
├── github_client.py
├── reviewer.py
├── analyzer.py
├── schemas.py
├── config.py
│
├── docs/
│   ├── AI_Opportunity_Report.md
│   └── Technical_Approach_Report.md
│
├── examples/
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/riyamittal13/BitElevate-AI-PR-Review-Assistant.git
cd BitElevate-AI-PR-Review-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add the following credentials:

```env
GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key
```

A GitHub token is optional for public repository access but can help with API rate limits.

A valid Gemini API key is required for AI-powered reviews.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Open the Streamlit application.
2. Enter a public GitHub Pull Request URL.
3. Start the review.
4. Wait for GitHub data retrieval and code analysis.
5. View the AI-generated review report.
6. Examine findings, explanations, suggested fixes, and learning recommendations.

Example Pull Request URL:

```text
https://github.com/psf/requests/pull/7388
```

## Review Output

Each identified issue contains:

| Field | Description |
|---|---|
| Severity | Critical, High, Medium, or Low |
| File Name | File containing the potential issue |
| Line Number | Approximate issue location |
| Issue | Short issue description |
| Explanation | Why the issue matters |
| Suggested Fix | Recommended improvement |

The complete review also includes an overall summary, status, and learning recommendations.

## Limitations

- Currently supports public GitHub Pull Requests.
- Static analysis focuses on Python files.
- Static-analysis findings may include pre-existing issues.
- AI-generated findings may contain false positives.
- Large Pull Requests are subject to processing limits.
- The application does not automatically approve, reject, or merge Pull Requests.

## Future Improvements

- Changed-line-level issue filtering.
- Pull Request risk scoring and prioritization.
- GitHub webhook and CI/CD integration.
- Multi-language static analysis.
- Review history and analytics.
- Mentor feedback integration.

## Documentation

Additional project documentation is available in the `docs/` directory:

- [AI Opportunity Report](docs/AI_Opportunity_Report.md)
- [Technical Approach Report](docs/Technical_Approach_Report.md)

## Security

API credentials should be stored in environment variables and never committed to the repository.

Private source code should only be shared with external AI services with appropriate authorization.

## Disclaimer

This application provides preliminary AI-assisted code review. All findings should be verified by a human developer before making changes or merging a Pull Request.

---

**Developed as part of the Cynbit Technologies AI/ML Engineer Intern Assessment.**