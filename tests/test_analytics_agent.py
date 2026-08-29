from agents.analytics_agent.agent import AnalyticsAgent


def test_analytics_agent_returns_completed_status():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 95.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert report["status"] == "COMPLETED"


def test_analytics_agent_preserves_task_id():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 95.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert "task_id" in report
    assert report["task_id"] == "task_001"


def test_analytics_agent_returns_metrics():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 95.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert "metrics" in report
    assert isinstance(report["metrics"], list)


def test_analytics_agent_returns_insights():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    quality_report = {
        "agent": "quality_agent",
        "status": "COMPLETED",
        "task_id": "task_001",
        "quality_score": 95.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert "insights" in report
    assert isinstance(report["insights"], list)


def test_analytics_agent_rejects_invalid_quality_report():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    quality_report = {
        "agent": "quality_agent",
        "status": "ERROR",
        "task_id": "task_001",
        "quality_score": 0.0,
        "issues": [],
    }

    report = agent.run(quality_report)

    assert report["status"] == "ERROR"
    assert report["task_id"] == "task_001"
