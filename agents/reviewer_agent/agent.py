"""
Reviewer Agent
--------------
Responsible for reviewing the results produced by previous agents
and verifying consistency, quality, and contract compliance.
"""

from typing import Any


class ReviewerAgent:
    """Agent responsible for reviewing analytical results."""

    def __init__(self, task_id: str = "task_001"):
        self.task_id = task_id

    def validate_input(
        self,
        quality_report: dict,
        analytics_result: dict,
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

        return issues

    def validate_task_id(
        self,
        quality_report: dict,
        analytics_result: dict,
    ) -> list:
        """Verify task_id consistency across agent results."""

        issues = []

        quality_task_id = quality_report.get("task_id")
        analytics_task_id = analytics_result.get("task_id")

        if quality_task_id != self.task_id:
            issues.append(
                {
                    "type": "task_id_mismatch",
                    "severity": "HIGH",
                    "message": (
                        "Quality report task_id does not match "
                        "the review task_id."
                    ),
                }
            )

        if analytics_task_id != self.task_id:
            issues.append(
                {
                    "type": "task_id_mismatch",
                    "severity": "HIGH",
                    "message": (
                        "Analytics result task_id does not match "
                        "the review task_id."
                    ),
                }
            )

        return issues

    def validate_status(
        self,
        quality_report: dict,
        analytics_result: dict,
    ) -> list:
        """Verify that previous agents completed successfully."""

        issues = []

        if quality_report.get("status") != "COMPLETED":
            issues.append(
                {
                    "type": "quality_agent_status",
                    "severity": "CRITICAL",
                    "message": (
                        "Quality Agent did not complete successfully."
                    ),
                }
            )

        if analytics_result.get("status") != "COMPLETED":
            issues.append(
                {
                    "type": "analytics_agent_status",
                    "severity": "CRITICAL",
                    "message": (
                        "Analytics Agent did not complete successfully."
                    ),
                }
            )

        return issues

    def validate_metrics(
        self,
        analytics_result: dict,
    ) -> list:
        """Validate analytical metrics."""

        issues = []

        if "metrics" not in analytics_result:
            issues.append(
                {
                    "type": "missing_metrics",
                    "severity": "HIGH",
                    "message": "Analytics result does not contain metrics.",
                }
            )
            return issues

        metrics = analytics_result["metrics"]

        if not isinstance(metrics, list):
            issues.append(
                {
                    "type": "invalid_metrics_structure",
                    "severity": "HIGH",
                    "message": "Metrics must be provided as a list.",
                }
            )
            return issues

        for index, metric in enumerate(metrics):
            if not isinstance(metric, dict):
                issues.append(
                    {
                        "type": "invalid_metric",
                        "severity": "HIGH",
                        "message": (
                            f"Metric at index {index} must be an object."
                        ),
                    }
                )
                continue

            required_fields = [
                "name",
                "value",
                "description",
            ]

            missing_fields = [
                field
                for field in required_fields
                if field not in metric
            ]

            if missing_fields:
                issues.append(
                    {
                        "type": "invalid_metric_structure",
                        "severity": "HIGH",
                        "message": (
                            f"Metric at index {index} is missing "
                            f"fields: {missing_fields}."
                        ),
                    }
                )

        return issues

    def validate_insights(
        self,
        analytics_result: dict,
    ) -> list:
        """Validate analytical insights."""

        issues = []

        if "insights" not in analytics_result:
            issues.append(
                {
                    "type": "missing_insights",
                    "severity": "HIGH",
                    "message": (
                        "Analytics result does not contain insights."
                    ),
                }
            )
            return issues

        insights = analytics_result["insights"]

        if not isinstance(insights, list):
            issues.append(
                {
                    "type": "invalid_insights_structure",
                    "severity": "HIGH",
                    "message": "Insights must be provided as a list.",
                }
            )
            return issues

        allowed_severities = {
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        }

        for index, insight in enumerate(insights):
            if not isinstance(insight, dict):
                issues.append(
                    {
                        "type": "invalid_insight",
                        "severity": "HIGH",
                        "message": (
                            f"Insight at index {index} must be an object."
                        ),
                    }
                )
                continue

            required_fields = [
                "type",
                "description",
                "severity",
            ]

            missing_fields = [
                field
                for field in required_fields
                if field not in insight
            ]

            if missing_fields:
                issues.append(
                    {
                        "type": "invalid_insight_structure",
                        "severity": "HIGH",
                        "message": (
                            f"Insight at index {index} is missing "
                            f"fields: {missing_fields}."
                        ),
                    }
                )

            severity = insight.get("severity")

            if severity is not None and severity not in allowed_severities:
                issues.append(
                    {
                        "type": "invalid_insight_severity",
                        "severity": "MEDIUM",
                        "message": (
                            f"Insight at index {index} has invalid "
                            f"severity: {severity}."
                        ),
                    }
                )

        return issues

    def review(
        self,
        quality_report: dict,
        analytics_result: dict,
        context: dict | None = None,
    ) -> dict:
        """Review results produced by previous agents."""

        issues = []

        issues.extend(
            self.validate_input(
                quality_report,
                analytics_result,
            )
        )

        if issues:
            return self._build_rejection(issues)

        issues.extend(
            self.validate_task_id(
                quality_report,
                analytics_result,
            )
        )

        issues.extend(
            self.validate_status(
                quality_report,
                analytics_result,
            )
        )

        issues.extend(
            self.validate_metrics(
                analytics_result,
            )
        )

        issues.extend(
            self.validate_insights(
                analytics_result,
            )
        )

        if issues:
            return self._build_rejection(issues)

        return {
            "agent": "reviewer_agent",
            "status": "APPROVED",
            "task_id": self.task_id,
            "approved": True,
            "issues": [],
        }

    def _build_rejection(
        self,
        issues: list,
    ) -> dict:
        """Build a structured rejection response."""

        return {
            "agent": "reviewer_agent",
            "status": "REJECTED",
            "task_id": self.task_id,
            "approved": False,
            "issues": issues,
        }

    def run(
        self,
        quality_report: dict,
        analytics_result: dict,
        context: dict | None = None,
    ) -> dict:
        """Execute the review process."""

        try:
            return self.review(
                quality_report=quality_report,
                analytics_result=analytics_result,
                context=context,
            )

        except Exception as exc:
            return {
                "agent": "reviewer_agent",
                "status": "ERROR",
                "task_id": self.task_id,
                "approved": False,
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            }
