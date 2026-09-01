import gzip
import json
import os
from pathlib import Path


class DatasetService:
    def __init__(self, config):
        self.config = config
        self._mbpp_dataset = None

    def _get(self, name):
        return self.config.get(name) if hasattr(self.config, "get") else getattr(self.config, name)

    def _codesearchnet(self):
        root = Path(self._get("CODESEARCHNET_PATH"))
        files = list(root.rglob("*.arrow")) if root.exists() else []
        if not files:
            return {"name": "CodeSearchNet", "available": False, "message": "CodeSearchNet dataset not found. Please place the dataset under datasets/codesearchnet.", "sample_count": None}
        return {"name": "CodeSearchNet", "available": True, "message": "Local Arrow shards detected; samples load only during evaluation.", "sample_count": None, "files": len(files)}

    def _humaneval(self):
        path = Path(self._get("HUMANEVAL_PATH"))
        if not path.exists():
            return {"name": "HumanEval", "available": False, "message": "HumanEval dataset not found under datasets/humaneval.", "sample_count": None}
        count = 0
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line in stream:
                if line.strip():
                    count += 1
        return {"name": "HumanEval", "available": True, "message": "Local HumanEval problems detected.", "sample_count": count}

    def _mbpp(self):
        try:
            import datasets
        except ImportError:
            return {"name": "MBPP", "available": False, "message": "Install the datasets package to load MBPP.", "sample_count": None}
        return {"name": "MBPP", "available": True, "message": "MBPP loader is ready. Samples load when evaluation starts.", "sample_count": None}

    def load_mbpp(self):
        if self._mbpp_dataset is None:
            from datasets import load_dataset
            self._mbpp_dataset = load_dataset("mbpp", split="train")
        return self._mbpp_dataset

    def load_samples(self, dataset_name: str, limit: int):
        limit = max(1, min(limit, 100))
        if dataset_name.lower() == "mbpp":
            return list(self.load_mbpp().select(range(min(limit, len(self.load_mbpp())))))
        if dataset_name.lower() == "humaneval":
            path = Path(self._get("HUMANEVAL_PATH"))
            if not path.exists():
                return []
            opener = gzip.open if path.suffix == ".gz" else open
            samples = []
            with opener(path, "rt", encoding="utf-8") as stream:
                for line in stream:
                    if line.strip():
                        samples.append(json.loads(line))
                        if len(samples) >= limit:
                            break
            return samples
        return []

    def summaries(self):
        return [self._codesearchnet(), self._mbpp(), self._humaneval()]

    def sample(self, dataset_name: str, limit: int):
        for item in self.summaries():
            if item["name"].lower() == dataset_name.lower():
                return item
        return None
