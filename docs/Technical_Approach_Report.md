# Technical Approach Report
## BitElevate AI PR Review Assistant

**Prepared for:** Cynbit Technologies  
**Role:** AI/ML Engineer Intern Assessment  
**Project:** BitElevate AI PR Review Assistant  
**Date:** November 2026

---

## 1. Introduction

The BitElevate AI PR Review Assistant is a Python-based application designed to perform preliminary analysis of GitHub Pull Requests.

The system combines GitHub API integration, static code analysis, and Large Language Model (LLM)-based reasoning to identify potential code issues and generate structured review feedback.

The primary objective is to assist developers and mentors by providing an additional layer of analysis before a human reviewer examines the Pull Request.

The application focuses on:

- Identifying potential logical and runtime issues.
- Detecting code-quality and maintainability concerns.
- Highlighting possible security vulnerabilities.
- Explaining identified issues in understandable language.
- Suggesting practical improvements.
- Providing learning recommendations for developers.

The system is designed as a supporting tool. It does not automatically approve, reject, or merge Pull Requests.

## 2. Technology Stack

The following technologies were selected based on their suitability for building a functional and modular prototype.

| Technology | Purpose |
|---|---|
| Python 3.10 | Core application development |
| Streamlit | Interactive user interface |
| GitHub REST API | Pull Request data retrieval |
| Gemini 3.1 Flash-Lite | AI-powered code review |
| Ruff | Python code-quality analysis |
| Bandit | Python security analysis |
| Pydantic | Structured output validation |
| Requests | HTTP communication |
| python-dotenv | Environment variable management |
| Pytest | Automated testing framework |
| Git and GitHub | Version control and source-code hosting |

### 2.1 Python

Python was selected because of its extensive ecosystem for AI/ML development, API integration, automation, and code analysis.

It also provides straightforward integration with the selected libraries.

### 2.2 Streamlit

Streamlit provides the application's interactive interface.

It allows users to submit GitHub Pull Request URLs and view generated review reports without requiring a separate frontend application.

### 2.3 GitHub REST API

The GitHub REST API is used to retrieve:

- Pull Request title and description.
- Author and current state.
- Changed-file information.
- Additions and deletions.
- Available code patches.
- File download references.

The prototype currently works with public GitHub Pull Requests.

An optional GitHub personal access token can be configured to improve API access and rate-limit handling.

### 2.4 Gemini 3.1 Flash-Lite

Gemini is used as the primary LLM for understanding code changes and generating contextual review feedback.

The model was selected for its ability to process code-related prompts and return structured JSON responses.

The application uses the `google-genai` Python SDK.

### 2.5 Ruff and Bandit

The system uses two static-analysis tools:

**Ruff:** Identifies Python code-quality issues, including style violations, unused imports, and other potential problems.

**Bandit:** Identifies common security-related patterns and potential vulnerabilities in Python code.

These tools provide deterministic analysis signals that complement the LLM's contextual reasoning.

### 2.6 Pydantic

Pydantic validates the structure of AI-generated review reports.

It ensures that the generated response follows a predefined schema instead of relying entirely on unstructured text.

## 3. System Architecture

The application follows a modular architecture in which each component has a specific responsibility.

### 3.1 High-Level Architecture

```text
              USER
                |
                v
        Streamlit Interface
              app.py
                |
                v
       GitHub Client Module
          github_client.py
                |
                v
         GitHub REST API
                |
                v
       Pull Request Data
       Metadata and Diffs
                |
                v
       Static Code Analysis
            analyzer.py
                |
          +-----+-----+
          |           |
          v           v
         Ruff       Bandit
          |           |
          +-----+-----+
                |
                v
       AI Review Engine
           reviewer.py
                |
                v
        Gemini 3.1 Flash-Lite
                |
                v
      Structured Output Validation
             schemas.py
                |
                v
         Streamlit Dashboard
                |
                v
        Human Review Support
```

### 3.2 Module Responsibilities

| Module | Responsibility |
|---|---|
| `app.py` | Handles the user interface and coordinates the review workflow |
| `github_client.py` | Validates GitHub PR URLs and retrieves Pull Request information |
| `analyzer.py` | Executes Ruff and Bandit on supported Python files |
| `reviewer.py` | Prepares the review prompt and communicates with Gemini |
| `schemas.py` | Defines and validates the structured review output |
| `config.py` | Loads API credentials and application configuration |

This separation makes the application easier to maintain, test, and extend.

## 4. Data Pipeline and Processing Workflow

The application processes a Pull Request through the following stages.

### Stage 1: Pull Request Input

The user enters a public GitHub Pull Request URL through the Streamlit interface.

The application validates the URL to extract:

- Repository owner.
- Repository name.
- Pull Request number.

Invalid URLs are rejected with an appropriate error message.

### Stage 2: GitHub Data Retrieval

The GitHub client sends requests to the GitHub REST API.

It retrieves Pull Request metadata and the list of changed files.

The application extracts relevant information, including:

- Pull Request title.
- Description.
- Author.
- State.
- Commit SHA.
- Changed-file count.
- Number of additions and deletions.
- Available code patches.

The prototype limits the number of retrieved changed files to 30 to control processing size.

### Stage 3: Static Code Analysis

For supported Python files, the application retrieves the available source content and performs static analysis.

Two tools are executed:

1. Ruff for code-quality checks.
2. Bandit for security-related checks.

The analyzer first checks Python syntax using Python's AST parser.

If the source contains a syntax error, the analyzer returns an error instead of proceeding with normal static analysis.

The results are collected and passed to the AI review component.

**Important implementation detail:** Static analysis currently examines the retrieved Python file contents, not exclusively the newly added or modified lines. Therefore, some findings may refer to pre-existing issues.

### Stage 4: AI-Powered Code Review

The reviewer module prepares a structured prompt containing:

- Pull Request title.
- Pull Request description.
- Available code patches.
- Static-analysis results.

The prompt instructs Gemini to:

- Identify genuine logical bugs and runtime issues.
- Examine code quality and maintainability.
- Identify possible security concerns.
- Consider static-analysis findings.
- Avoid unnecessary duplicate findings.
- Avoid inventing unsupported issues.
- Provide practical explanations and suggested fixes.

The model is instructed to use the supplied filenames and provide approximate line numbers wherever possible.

### Stage 5: Structured Output Generation

Gemini generates a JSON response following the Pydantic-defined schema.

The response contains:

**Review summary:** An overall explanation of the Pull Request.

**Findings:** Each finding includes:

- Severity.
- File name.
- Approximate line number.
- Issue description.
- Explanation.
- Suggested fix.

**Overall status:** Good, Needs Improvement, or Critical.

**Learning recommendations:** Concepts that the developer may need to understand or revise.

Pydantic validates the generated response before it is displayed.

### Stage 6: Review Dashboard

The Streamlit interface displays:

- Pull Request information.
- Overall review status.
- AI-generated summary.
- Individual findings.
- Severity information.
- Explanations and suggested fixes.
- Learning recommendations.

The dashboard makes the generated analysis easier to understand and review.

## 5. Prompt Engineering Approach

Prompt engineering plays an important role because code review requires more than simply describing code.

The model must identify potential issues while avoiding unsupported assumptions.

The prompt is designed around the following principles:

### 5.1 Role Definition

Gemini is instructed to behave as an experienced software engineer conducting a careful Pull Request review.

This establishes the expected context and review perspective.

### 5.2 Context Provision

The model receives the Pull Request title, description, changed code patches, and static-analysis results.

Providing this information helps the model understand the purpose of the changes and evaluate potential issues in context.

### 5.3 Explicit Review Instructions

The prompt defines specific review responsibilities:

- Logical correctness.
- Runtime safety.
- Code quality.
- Maintainability.
- Security considerations.

### 5.4 False-Positive Reduction

The model is instructed not to invent issues and to report only problems supported by the supplied code.

It is also instructed to avoid unnecessarily repeating findings already identified through static analysis.

### 5.5 Structured Responses

The application uses Gemini's JSON response configuration and the Pydantic schema to obtain predictable output.

This makes it easier to validate, process, and display findings consistently.

## 6. Review Output Schema

The system uses two main Pydantic models.

### ReviewFinding

Represents an individual issue identified during the review.

| Field | Description |
|---|---|
| `severity` | Critical, High, Medium, or Low |
| `file_name` | File containing the potential issue |
| `line_number` | Approximate line number |
| `issue` | Short description of the issue |
| `explanation` | Why the issue matters |
| `suggested_fix` | Recommended improvement |

### ReviewReport

Represents the complete Pull Request review.

| Field | Description |
|---|---|
| `summary` | Overall review summary |
| `findings` | List of ReviewFinding objects |
| `overall_status` | Good, Needs Improvement, or Critical |
| `learning_recommendations` | Concepts the developer should revise |

This structure separates individual findings from the overall assessment.

## 7. Security and Configuration

The application uses environment variables to manage API credentials.

The `.env` file contains the required credentials:

- `GITHUB_TOKEN`
- `GEMINI_API_KEY`

The `python-dotenv` package loads these values through the configuration module.

The `.env` file is excluded from Git through `.gitignore`.

An `.env.example` file is included to document the required configuration without exposing actual credentials.

Additional considerations include:

- Only publicly accessible repositories are supported by the current prototype.
- GitHub API errors and rate limits are handled through exception handling.
- API requests use configured timeouts.
- Private repository integration would require appropriate authorization.
- Source code should only be transmitted to an external AI service with explicit authorization.
- AI-generated findings must be reviewed by a human before acting on them.

## 8. Error Handling

The application includes handling for common operational errors.

Examples include:

| Error condition | Handling approach |
|---|---|
| Invalid GitHub URL | Return a validation error |
| Pull Request not found | Display an appropriate error |
| GitHub rate limit or access denial | Inform the user about authentication and rate limits |
| Network failure | Return a connection error |
| Missing Gemini API key | Display a configuration error |
| Unsupported file type | Skip static analysis for unsupported files |
| Python syntax error | Return the syntax error |
| No readable code patches | Inform the user that review cannot proceed |

These checks help prevent common failures from interrupting the entire workflow without explanation.

## 9. Implementation and Validation

The application was developed incrementally using Visual Studio Code and Python 3.10.11.

The implementation was divided into the following activities:

1. Environment setup and dependency installation.
2. GitHub URL parsing and API integration.
3. Pull Request metadata and file retrieval.
4. Static-analysis integration.
5. Gemini API integration.
6. Structured response validation using Pydantic.
7. Streamlit dashboard development.
8. End-to-end testing using a public GitHub Pull Request.

### Validation Performed

The following checks were performed during development:

- Verified the Python environment and installed dependencies.
- Tested the Gemini API connection successfully.
- Tested GitHub Pull Request retrieval using a public repository.
- Verified the retrieval of Pull Request metadata and code changes.
- Executed static analysis on retrieved Python files.
- Tested Gemini-generated structured review output.
- Ran the complete workflow through the Streamlit interface.

The application successfully generated a review report for a test Pull Request.

These checks establish that the core prototype works. They do not represent a formal benchmark of detection accuracy or production readiness.

## 10. Current Scope and Limitations

The current implementation is a proof of concept and has certain limitations.

### Current Scope

- Public GitHub Pull Request analysis.
- Python-focused static analysis.
- Ruff and Bandit integration.
- Gemini-based contextual code review.
- Structured JSON output.
- Streamlit-based review dashboard.
- Learning recommendations.

### Current Limitations

- Static analysis may identify issues outside the changed lines.
- AI-generated findings may contain false positives.
- Approximate line numbers may not always match the exact location.
- Large Pull Requests may exceed processing limits.
- Unsupported file types do not receive the same static-analysis coverage.
- The application is not yet integrated into GitHub webhook or CI/CD workflows.
- The current prototype does not implement persistent review history.
- No formal accuracy benchmark has been completed.

## 11. Future Enhancements

The following improvements could be considered for a more complete implementation.

### 11.1 Changed-Line-Level Analysis

Map static-analysis findings to the actual changed lines in a Pull Request to reduce unrelated findings.

### 11.2 PR Risk Scoring

Introduce a risk-prioritization mechanism based on factors such as:

- Number of changed files.
- Nature of the modifications.
- Security-sensitive changes.
- Static-analysis findings.
- Potential impact on critical modules.

### 11.3 GitHub Integration

Introduce GitHub webhooks or CI/CD integration to trigger preliminary analysis when a Pull Request is created or updated.

### 11.4 Multi-Language Support

Extend static analysis to additional programming languages using suitable language-specific tools.

### 11.5 Review History and Analytics

Store review results to support trend analysis, recurring issue identification, and review-efficiency measurements.

### 11.6 Mentor Feedback Integration

Allow mentors to mark findings as useful, incorrect, or resolved. This feedback could help evaluate and improve the quality of future reviews.

## 12. Conclusion

The BitElevate AI PR Review Assistant demonstrates how GitHub integration, static code analysis, and LLM-based reasoning can be combined into a practical AI-powered engineering application.

The modular architecture separates data retrieval, code analysis, AI reasoning, structured validation, and user interaction.

The combination of Ruff and Bandit with Gemini provides two complementary approaches: deterministic static checks and contextual AI-based analysis.

The resulting application produces structured review findings and learning recommendations that can support developers and mentors during preliminary Pull Request examination.

The current implementation establishes a functional foundation that can be extended with changed-line analysis, risk prioritization, GitHub automation, and mentor feedback.

The solution is intended to complement human engineering judgment rather than replace it.

**Project:** BitElevate AI PR Review Assistant

*Smarter Code Reviews. Better Learning.*