from agents.analytics_agent.agent import AnalyticsAgent


def test_analytics_agent_returns_completed_status():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    result = agent.run()

    assert result["status"] == "COMPLETED"


def test_analytics_agent_returns_task_id():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    result = agent.run()

    assert "task_id" in result
    assert result["task_id"] == "task_001"


def test_analytics_agent_returns_metrics():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    result = agent.run()

    assert "metrics" in result
    assert isinstance(result["metrics"], list)


def test_analytics_agent_returns_insights():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    result = agent.run()

    assert "insights" in result
    assert isinstance(result["insights"], list)


def test_analytics_agent_metric_structure():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    result = agent.run()

    for metric in result["metrics"]:
        assert "name" in metric
        assert "value" in metric
        assert "description" in metric


def test_analytics_agent_insight_structure():
    agent = AnalyticsAgent(
        dataset_path="data/sales.csv",
        task_id="task_001",
    )

    result = agent.run()

    for insight in result["insights"]:
        assert "type" in insight
        assert "description" in insight
        assert "severity" in insight


def test_analytics_agent_handles_missing_dataset():
    agent = AnalyticsAgent(
        dataset_path="data/dataset_inexistente.csv",
        task_id="task_001",
    )

    result = agent.run()

    assert result["status"] == "ERROR"
    assert result["task_id"] == "task_001"
    assert "error" in result
    assert "type" in result["error"]
    assert "message" in result["error"]
