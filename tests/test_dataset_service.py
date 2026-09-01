from config import Config
from services.dataset_service import DatasetService


def test_missing_dataset_is_graceful(tmp_path):
    class TestConfig(Config):
        CODESEARCHNET_PATH = str(tmp_path / "missing")
        HUMANEVAL_PATH = str(tmp_path / "missing.jsonl.gz")

    summaries = DatasetService(TestConfig).summaries()
    assert summaries[0]["available"] is False
    assert summaries[2]["available"] is False
