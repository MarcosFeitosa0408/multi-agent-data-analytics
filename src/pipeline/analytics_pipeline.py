"""
Analytics Pipeline
------------------
Orchestrates the execution flow between the system agents.

Flow:
User Request
    ↓
Coordinator Agent
    ↓
Quality Agent
    ↓
Analytics Agent
    ↓
Reviewer Agent
"""

from agents.coordinator_agent.agent import CoordinatorAgent
from agents.quality_agent.agent import QualityAgent
from agents.analytics_agent.agent import AnalyticsAgent
from agents.reviewer_agent.agent import ReviewerAgent


class AnalyticsPipeline:
    """Orchestrates the multi-agent analytics workflow."""

    def __init__(self, task_id: str | None = None):
        self.coordinator = CoordinatorAgent(task_id=task_id)

    def run(self, request: dict) -> dict:
        """Execute the complete analytics pipeline."""

        # ---------------------------------------------------------
        # 1. Coordinator
        # ---------------------------------------------------------
        coordinator_result = self.coordinator.run(request)

        if coordinator_result["status"] != "COMPLETED":
            return {
                "pipeline": "analytics_pipeline",
                "status": "ERROR",
                "task_id": coordinator_result["task_id"],
                "failed_agent": "coordinator_agent",
                "coordinator": coordinator_result,
            }

        task_id = coordinator_result["task_id"]
        dataset_path = coordinator_result["dataset_path"]
        task = coordinator_result["task"]
        context = coordinator_result["context"]

        # ---------------------------------------------------------
        # 2. Quality Agent
        # ---------------------------------------------------------
        quality_agent = QualityAgent(
            dataset_path=dataset_path,
            task_id=task_id,
        )

        quality_result = quality_agent.run()

        if quality_result["status"] != "COMPLETED":
            return {
                "pipeline": "analytics_pipeline",
                "status": "ERROR",
                "task_id": task_id,
                "failed_agent": "quality_agent",
                "coordinator": coordinator_result,
                "quality": quality_result,
            }

        # ---------------------------------------------------------
        # 3. Analytics Agent
        # ---------------------------------------------------------
        analytics_agent = AnalyticsAgent(
            dataset_path=dataset_path,
            task_id=task_id,
        )

        analytics_result = analytics_agent.run()

        if analytics_result["status"] != "COMPLETED":
            return {
                "pipeline": "analytics_pipeline",
                "status": "ERROR",
                "task_id": task_id,
                "failed_agent": "analytics_agent",
                "coordinator": coordinator_result,
                "quality": quality_result,
                "analytics": analytics_result,
            }

        # ---------------------------------------------------------
        # 4. Reviewer Agent
        # ---------------------------------------------------------
        reviewer_agent = ReviewerAgent(task_id=task_id)

        review_result = reviewer_agent.run(
            quality_report=quality_result,
            analytics_result=analytics_result,
            context=context,
        )

        if review_result["status"] != "APPROVED":
            return {
                "pipeline": "analytics_pipeline",
                "status": "REJECTED",
                "task_id": task_id,
                "failed_agent": "reviewer_agent",
                "coordinator": coordinator_result,
                "quality": quality_result,
                "analytics": analytics_result,
                "review": review_result,
            }

        # ---------------------------------------------------------
        # 5. Final Pipeline Result
        # ---------------------------------------------------------
        return {
            "pipeline": "analytics_pipeline",
            "status": "COMPLETED",
            "task_id": task_id,
            "task": task,
            "context": context,
            "coordinator": coordinator_result,
            "quality": quality_result,
            "analytics": analytics_result,
            "review": review_result,
        }
