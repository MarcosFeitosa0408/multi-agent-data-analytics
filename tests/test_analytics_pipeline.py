from src.pipeline.analytics_pipeline import AnalyticsPipeline


def test_analytics_pipeline_executes_complete_flow():
    pipeline = AnalyticsPipeline(task_id="task_integration_001")

    request = {
        "task": "Analyze sales performance",
        "dataset_path": "data/sales.csv",
    }

    result = pipeline.run(request)

    assert result["pipeline"] == "analytics_pipeline"
    assert result["task_id"] == "task_integration_001"

    assert "coordinator" in result
    assert "quality" in result
    assert "analytics" in result
    assert "review" in result

    assert result["coordinator"]["status"] == "COMPLETED"
    assert result["quality"]["status"] == "COMPLETED"
    assert result["analytics"]["status"] == "COMPLETED"
    assert result["review"]["status"] == "APPROVED"

    assert result["status"] == "COMPLETED"


def test_analytics_pipeline_rejects_invalid_request():
    pipeline = AnalyticsPipeline(task_id="task_integration_002")

    result = pipeline.run({})

    assert result["pipeline"] == "analytics_pipeline"
    assert result["status"] == "ERROR"
    assert result["task_id"] == "task_integration_002"
    assert result["failed_agent"] == "coordinator_agent"
