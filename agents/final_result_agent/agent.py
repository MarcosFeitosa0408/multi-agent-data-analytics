"""
Final Result Agent
------------------
Responsible for consolidating validated results and producing
the final structured response for the user.
"""


class FinalResultAgent:
    """Agent responsible for consolidating the final analytics result."""

    def __init__(self, task_id: str = "task_001"):
        self.task_id = task_id

    def validate_input(
        self,
        quality_report: dict,
        analytics_result: dict,
        review_result: dict,
    ) -> list:
        """Validate mandatory inputs."""

        issues = []

        if not quality_report:
            issues.append(
                {
                    "type": "missing_quality_report",
                    "severity": "CRITICAL",
                    "message": "Quality report is missing.",
                }
            )

        if not analytics_result:
            issues.append(
                {
                    "type": "missing_analytics_result",
                    "severity": "CRITICAL",
                    "message": "Analytics result is missing.",
                }
            )

        if not review_result:
            issues.append(
                {
                    "type": "missing_review_result",
                    "severity": "CRITICAL",
                    "message": "Review result is missing.",
                }
            )

        return issues

    def validate_approval(self, review_result: dict) -> list:
        """Ensure the Reviewer approved the results."""

        issues = []

        if review_result.get("task_id") != self.task_id:
            issues.append(
                {
                    "type": "task_id_mismatch",
                    "severity": "CRITICAL",
                    "message": "Reviewer task_id does not match.",
                }
            )

        if review_result.get("status") != "APPROVED":
            issues.append(
                {
                    "type": "review_not_approved",
                    "severity": "CRITICAL",
                    "message": "Results were not approved by Reviewer Agent.",
                }
            )

        return issues

    def build_result(
        self,
        quality_report: dict,
        analytics_result: dict,
        review_result: dict,
    ) -> dict:
        """Build the final structured result."""

        return {
            "agent": "final_result_agent",
            "status": "COMPLETED",
            "task_id": self.task_id,
            "approved": True,
            "quality_score": quality_report.get("quality_score"),
            "metrics": analytics_result.get("metrics", []),
            "insights": analytics_result.get("insights", []),
            "review": review_result,
        }

    def run(
        self,
        quality_report: dict,
        analytics_result: dict,
        review_result: dict,
    ) -> dict:
        """Generate the final result after validation."""

        try:
            issues = self.validate_input(
                quality_report,
                analytics_result,
                review_result,
            )

            if issues:
                return {
                    "agent": "final_result_agent",
                    "status": "ERROR",
                    "task_id": self.task_id,
                    "approved": False,
                    "issues": issues,
                }

            approval_issues = self.validate_approval(review_result)

            if approval_issues:
                return {
                    "agent": "final_result_agent",
                    "status": "REJECTED",
                    "task_id": self.task_id,
                    "approved": False,
                    "issues": approval_issues,
                }

            return self.build_result(
                quality_report,
                analytics_result,
                review_result,
            )

        except Exception as exc:
            return {
                "agent": "final_result_agent",
                "status": "ERROR",
                "task_id": self.task_id,
                "approved": False,
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            }
