from src.pipeline.analytics_pipeline import AnalyticsPipeline


def test_analytics_pipeline_executes_complete_flow():
    pipeline = AnalyticsPipeline(task_id="task_pipeline_001")

    request = {
        "task": "Analyze sales performance",
        "dataset_path": "data/sales.csv",
    }

    result = pipeline.run(request)

    assert result["pipeline"] == "analytics_pipeline"
    assert result["status"] == "COMPLETED"
    assert result["task_id"] == "task_pipeline_001"

    assert result["coordinator"]["status"] == "COMPLETED"
    assert result["quality"]["status"] == "COMPLETED"
    assert result["analytics"]["status"] == "COMPLETED"
    assert result["review"]["status"] == "APPROVED"


def test_analytics_pipeline_preserves_task_id():
    pipeline = AnalyticsPipeline(task_id="task_pipeline_002")

    request = {
        "task": "Analyze sales performance",
        "dataset_path": "data/sales.csv",
    }

    result = pipeline.run(request)

    assert result["task_id"] == "task_pipeline_002"
    assert result["coordinator"]["task_id"] == "task_pipeline_002"
    assert result["quality"]["task_id"] == "task_pipeline_002"
    assert result["analytics"]["task_id"] == "task_pipeline_002"
    assert result["review"]["task_id"] == "task_pipeline_002"


def test_analytics_pipeline_rejects_invalid_request():
    pipeline = AnalyticsPipeline(task_id="task_pipeline_003")

    result = pipeline.run({})

    assert result["pipeline"] == "analytics_pipeline"
    assert result["status"] == "ERROR"
    assert result["task_id"] == "task_pipeline_003"
    assert result["failed_agent"] == "coordinator_agent"
