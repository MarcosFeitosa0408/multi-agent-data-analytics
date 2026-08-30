"""
Coordinator Agent
-----------------
Responsible for orchestrating the execution flow between agents.
"""

from typing import Any


class CoordinatorAgent:
    """Agent responsible for coordinating the analytics workflow."""

    def __init__(self, task_id: str = "task_001"):
        self.task_id = task_id

    def validate_input(self, request: dict) -> list:
        """Validate the initial user request."""

        issues = []

        if not request:
            issues.append(
                {
                    "type": "missing_request",
                    "severity": "CRITICAL",
                    "message": "User request is missing.",
                }
            )
            return issues

        if "dataset_path" not in request:
            issues.append(
                {
                    "type": "missing_dataset_path",
                    "severity": "CRITICAL",
                    "message": "Dataset path is required.",
                }
            )

        if "task" not in request:
            issues.append(
                {
                    "type": "missing_task",
                    "severity": "HIGH",
                    "message": "Task description is required.",
                }
            )

        return issues

    def create_context(self, request: dict) -> dict:
        """Create execution context."""

        return {
            "source": "user",
            "environment": request.get(
                "environment",
                "development",
            ),
        }

    def prepare_execution(self, request: dict) -> dict:
        """Prepare the structured execution request."""

        return {
            "task_id": self.task_id,
            "dataset_path": request["dataset_path"],
            "task": request["task"],
            "context": self.create_context(request),
        }

    def run(self, request: dict) -> dict:
        """Execute the coordinator validation and preparation."""

        try:
            issues = self.validate_input(request)

            if issues:
                return {
                    "agent": "coordinator_agent",
                    "status": "ERROR",
                    "task_id": self.task_id,
                    "error": {
                        "type": "INVALID_INPUT",
                        "message": issues[0]["message"],
                    },
                    "issues": issues,
                }

            execution = self.prepare_execution(request)

            return {
                "agent": "coordinator_agent",
                "status": "COMPLETED",
                "task_id": self.task_id,
                "dataset_path": execution["dataset_path"],
                "task": execution["task"],
                "context": execution["context"],
            }

        except Exception as exc:
            return {
                "agent": "coordinator_agent",
                "status": "ERROR",
                "task_id": self.task_id,
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            }
