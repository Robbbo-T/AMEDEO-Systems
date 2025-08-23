from typing import Any, Dict, List
import random


class DummyRepresentation:
    def __init__(self, dim: int = 16):
        self.dim = dim

    def encode(self, flights: List[dict]) -> List[List[float]]:
        random.seed(42)
        return [[random.random() for _ in range(self.dim)] for _ in flights]


def pretrain_representation(flights: Any, params: Dict) -> DummyRepresentation:
    # Ignore params in this stub, return a small encoder
    return DummyRepresentation(dim=16)


class DummyHead:
    def __init__(self, task: str):
        self.task = task

    def predict(self, features: List[List[float]]):
        random.seed(hash(self.task) % (2**32))
        if self.task in ("weather", "safety"):
            return [random.random() for _ in features]
        if self.task == "efficiency":
            return [0.02 + (random.random() * 0.01) for _ in features]  # ~2-3% MAPE
        return [0.5 for _ in features]


def finetune_multi_task(representation: DummyRepresentation, labels: Dict[str, Any], params: Dict) -> Dict[str, Any]:
    # Create per-task heads
    heads = {task: DummyHead(task) for task in labels.keys()}

    class MultiTaskModel:
        def __init__(self, rep: DummyRepresentation, heads: Dict[str, DummyHead]):
            self.rep = rep
            self.heads = heads

        def predict(self, flights: List[dict]) -> Dict[str, List[float]]:
            feats = self.rep.encode(flights)
            return {task: head.predict(feats) for task, head in self.heads.items()}

    return {"model": MultiTaskModel(representation, heads)}
