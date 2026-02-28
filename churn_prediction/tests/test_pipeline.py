from src.pipeline.pipeline import run_pipeline


def test_pipeline_runs():
    df = run_pipeline()
    assert df is not None
    assert not df.empty