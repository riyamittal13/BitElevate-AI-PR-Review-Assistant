
from pydantic import BaseModel, Field


class ReviewFinding(BaseModel):
    severity: str = Field(
        description="Severity: Critical, High, Medium, or Low"
    )

    file_name: str = Field(
        description="Name of the file containing the issue"
    )

    line_number: int | None = Field(
        default=None,
        description="Approximate line number of the issue"
    )

    issue: str = Field(
        description="Short description of the identified issue"
    )

    explanation: str = Field(
        description="Why this issue matters"
    )

    suggested_fix: str = Field(
        description="Recommended way to fix the issue"
    )


class ReviewReport(BaseModel):
    summary: str = Field(
        description="Overall summary of the code review"
    )

    findings: list[ReviewFinding] = Field(
        description="List of identified code issues"
    )

    overall_status: str = Field(
        description="Overall assessment: Good, Needs Improvement, or Critical"
    )

    learning_recommendations: list[str] = Field(
        description="Concepts the developer should learn or revise"
    )