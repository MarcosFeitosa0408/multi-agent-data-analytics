from agents.analytics_agent.agent import AnalyticsAgent


def test_analytics_agent_requires_quality_report():
    agent = AnalyticsAgent("data/sales.csv")

    report = agent.run({})

    assert report["status"] == "ERROR"
    assert "task_id" in report
    assert "error" in report


def test_analytics_agent_rejects_quality_error():
    agent = AnalyticsAgent("data/sales.csv")

    quality_report = {
        "agent": "quality_agent",
        "status": "ERROR",
        "task_id": "task_001",
        "issues": [],
    }

    report = agent.run(quality_report)

    assert report["status"] == "ERROR"
    assert "task_id" in report
    assert "error" in report


def test_analytics_agent_returns_completed_status():
    agent = AnalyticsAgent("data/sales.csv")

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 90.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert report["status"] == "COMPLETED"


def test_analytics_agent_returns_metrics():
    agent = AnalyticsAgent("data/sales.csv")

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 90.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert "metrics" in report
    assert isinstance(report["metrics"], list)
    assert report["metrics"]


def test_analytics_agent_returns_insights():
    agent = AnalyticsAgent("data/sales.csv")

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 90.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert "insights" in report
    assert isinstance(report["insights"], list)
