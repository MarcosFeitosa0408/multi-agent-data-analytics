from agents.final_result_agent.agent import FinalResultAgent


def test_final_result_agent_returns_completed_status():
    agent = FinalResultAgent(task_id="task_001")

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 95.0,
        "issues": [],
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": [
            {
                "name": "total_sales",
                "value": 10000.0,
            }
        ],
        "insights": [
            "Sales performance is positive."
        ],
    }

    review_result = {
        "agent": "reviewer_agent",
        "status": "APPROVED",
        "task_id": "task_001",
        "approved": True,
        "issues": [],
    }

    result = agent.run(
        quality_report=quality_report,
        analytics_result=analytics_result,
        review_result=review_result,
    )

    assert result["agent"] == "final_result_agent"
    assert result["status"] == "COMPLETED"
    assert result["task_id"] == "task_001"
    assert result["approved"] is True


def test_final_result_agent_preserves_metrics_and_insights():
    agent = FinalResultAgent(task_id="task_002")

    quality_report = {
        "status": "COMPLETED",
        "task_id": "task_002",
        "quality_score": 98.0,
        "issues": [],
    }

    analytics_result = {
        "status": "COMPLETED",
        "task_id": "task_002",
        "metrics": [
            {
                "name": "total_sales",
                "value": 15000.0,
            }
        ],
        "insights": [
            "Sales increased."
        ],
    }

    review_result = {
        "status": "APPROVED",
        "task_id": "task_002",
        "approved": True,
        "issues": [],
    }

    result = agent.run(
        quality_report=quality_report,
        analytics_result=analytics_result,
        review_result=review_result,
    )

    assert result["quality_score"] == 98.0
    assert result["metrics"] == analytics_result["metrics"]
    assert result["insights"] == analytics_result["insights"]


def test_final_result_agent_rejects_unapproved_review():
    agent = FinalResultAgent(task_id="task_003")

    quality_report = {
        "status": "COMPLETED",
        "task_id": "task_003",
        "quality_score": 95.0,
        "issues": [],
    }

    analytics_result = {
        "status": "COMPLETED",
        "task_id": "task_003",
        "metrics": [],
        "insights": [],
    }

    review_result = {
        "status": "REJECTED",
        "task_id": "task_003",
        "approved": False,
        "issues": [
            {
                "type": "invalid_metric",
                "severity": "HIGH",
            }
        ],
    }

    result = agent.run(
        quality_report=quality_report,
        analytics_result=analytics_result,
        review_result=review_result,
    )

    assert result["status"] == "REJECTED"
    assert result["approved"] is False
    assert result["task_id"] == "task_003"


def test_final_result_agent_rejects_missing_input():
    agent = FinalResultAgent(task_id="task_004")

    result = agent.run(
        quality_report={},
        analytics_result={},
        review_result={},
    )

    assert result["status"] == "ERROR"
    assert result["approved"] is False
    assert result["task_id"] == "task_004"
    assert result["issues"]
