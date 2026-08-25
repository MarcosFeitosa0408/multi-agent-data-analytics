from agents.quality_agent.agent import QualityAgent 


def test_quality_agent_detects_missing_values():
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    missing_issues = [
        issue
        for issue in report["issues"]
        if issue["type"] == "missing_values"
    ]

    assert missing_issues


def test_quality_agent_detects_duplicate_order_id():
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    duplicate_issues = [
        issue
        for issue in report["issues"]
        if issue["type"] == "duplicate_order_id"
    ]

    assert duplicate_issues


def test_quality_agent_detects_invalid_total_sales():
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    invalid_total_issues = [
        issue
        for issue in report["issues"]
        if issue["type"] == "invalid_total_sales"
    ]

    assert invalid_total_issues


def test_quality_agent_returns_quality_score():
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    assert "quality_score" in report
    assert 0 <= report["quality_score"] <= 100


def test_quality_agent_returns_expected_status():
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    assert report["status"] == "COMPLETED"


def test_quality_agent_returns_task_id():
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    assert "task_id" in report
    assert report["task_id"]


def test_quality_agent_error_returns_structured_error():
    agent = QualityAgent("data/dataset_inexistente.csv")

    report = agent.run()

    assert report["status"] == "ERROR"
    assert "task_id" in report
    assert "error" in report
    assert "type" in report["error"]
    assert "message" in report["error"]
