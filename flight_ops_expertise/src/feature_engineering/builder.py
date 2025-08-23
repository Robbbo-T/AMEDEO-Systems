from dataclasses import dataclass
from typing import Any, Dict
import random


@dataclass
class FeatureStore:
    flights: Any
    labels: Dict[str, Any]


def build_features(raw_data: Dict, feature_params: Dict) -> FeatureStore:
    """Build features and return a minimal feature store.

    This stub generates small synthetic data structures sufficient for the
    downstream stubs to run. It does not read real data.
    """
    # Minimal synthetic dataset
    num_samples = 50
    flights = [{
        "id": i,
        "phase": random.choice(["climb", "cruise", "descent", "approach"]),
        "edr": random.random(),
        "shear": random.random(),
        "ri": random.random(),
        "fuel_plan": 1000 + random.randint(-50, 50),
        "fuel_actual": 1000 + random.randint(-50, 50),
    } for i in range(num_samples)]

    # Task labels
    labels = {
        "weather": [1 if f["edr"] > 0.6 else 0 for f in flights],
        "safety": [1 if f["shear"] > 0.7 else 0 for f in flights],
        "efficiency": [
            abs(f["fuel_actual"] - f["fuel_plan"]) / max(1, f["fuel_plan"]) for f in flights
        ],
    }

    return FeatureStore(flights=flights, labels=labels)
