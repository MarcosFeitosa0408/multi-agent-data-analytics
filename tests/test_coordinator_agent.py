from agents.coordinator_agent.agent import CoordinatorAgent


def test_coordinator_agent_creates_execution():
    agent = CoordinatorAgent("task_001")

    request = {
        "task": "Analyze sales performance",
        "dataset_path": "data/sales.csv",
    }

    report = agent.run(request)

    assert report["agent"] == "coordinator_agent"
    assert report["status"] == "COMPLETED"
    assert report["task_id"] == "task_001"
    assert report["dataset_path"] == "data/sales.csv"
    assert report["task"] == "Analyze sales performance"
    assert "context" in report


def test_coordinator_agent_rejects_missing_dataset():
    agent = CoordinatorAgent("task_001")

    request = {
        "task": "Analyze sales performance",
    }

    report = agent.run(request)

    assert report["status"] == "ERROR"
    assert report["task_id"] == "task_001"
    assert report["error"]
    assert report["issues"]


def test_coordinator_agent_rejects_missing_task():
    agent = CoordinatorAgent("task_001")

    request = {
        "dataset_path": "data/sales.csv",
    }

    report = agent.run(request)

    assert report["status"] == "ERROR"
    assert report["task_id"] == "task_001"
    assert report["error"]
    assert report["issues"]


def test_coordinator_agent_rejects_empty_request():
    agent = CoordinatorAgent("task_001")

    report = agent.run({})

    assert report["status"] == "ERROR"
    assert report["task_id"] == "task_001"
    assert report["error"]
    assert report["issues"]


def test_coordinator_agent_preserves_environment():
    agent = CoordinatorAgent("task_001")

    request = {
        "task": "Analyze sales performance",
        "dataset_path": "data/sales.csv",
        "environment": "production",
    }

    report = agent.run(request)

    assert report["status"] == "COMPLETED"
    assert report["context"]["source"] == "user"
    assert report["context"]["environment"] == "production"
