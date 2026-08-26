from agents.reviewer_agent.agent import ReviewerAgent


def test_reviewer_agent_approves_valid_result(): 
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": [
            {
                "name": "total_sales",
                "value": 10000,
                "description": "Total sales",
            }
        ],
        "insights": [
            {
                "type": "sales_growth",
                "description": "Sales increased.",
                "severity": "LOW",
            }
        ],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "APPROVED"
    assert report["approved"] is True
    assert report["task_id"] == "task_001"


def test_reviewer_agent_rejects_task_id_mismatch():
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_002",
        "metrics": [],
        "insights": [],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False
    assert report["issues"]


def test_reviewer_agent_rejects_failed_quality_agent():
    quality_report = {
        "agent": "quality_agent",
        "status": "ERROR",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": [],
        "insights": [],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False


def test_reviewer_agent_returns_structured_error_for_missing_input():
    agent = ReviewerAgent("task_001")

    report = agent.run(
        {},
        {},
    )

    assert report["status"] == "REJECTED"
    assert report["task_id"] == "task_001"
    assert report["approved"] is False
    assert report["issues"]

def test_reviewer_agent_rejects_missing_metrics():
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "insights": [],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False
    assert any(
        issue["type"] == "missing_metrics"
        for issue in report["issues"]
    )


def test_reviewer_agent_rejects_invalid_metrics_structure():
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": "invalid",
        "insights": [],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False
    assert any(
        issue["type"] == "invalid_metrics_structure"
        for issue in report["issues"]
    )


def test_reviewer_agent_rejects_missing_insights():
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": [],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False
    assert any(
        issue["type"] == "missing_insights"
        for issue in report["issues"]
    )


def test_reviewer_agent_rejects_invalid_insights_structure():
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": [],
        "insights": "invalid",
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False
    assert any(
        issue["type"] == "invalid_insights_structure"
        for issue in report["issues"]
    )


def test_reviewer_agent_rejects_invalid_insight_severity():
    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
    }

    analytics_result = {
        "agent": "analytics_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "metrics": [],
        "insights": [
            {
                "type": "sales_growth",
                "description": "Sales increased.",
                "severity": "INVALID",
            }
        ],
    }

    agent = ReviewerAgent("task_001")

    report = agent.run(
        quality_report,
        analytics_result,
    )

    assert report["status"] == "REJECTED"
    assert report["approved"] is False
    assert any(
        issue["type"] == "invalid_insight_severity"
        for issue in report["issues"]
    )
