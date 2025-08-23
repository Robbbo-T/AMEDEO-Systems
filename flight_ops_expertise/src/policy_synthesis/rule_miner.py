from typing import Dict, Any, List


def mine_best_practices(models: Dict[str, Dict], feature_store: Any, params: Dict) -> List[Dict[str, Any]]:
    # Return a small set of dummy practices
    return [
        {
            "id": "W-EDR-001",
            "title": "Avoid climb profiles with EDR > 0.6 in convective SIGMET areas",
            "evidence": {"support": 0.78, "confidence": 0.88},
            "action": "Delay climb or select alternate route",
        },
        {
            "id": "S-SHEAR-002",
            "title": "Stabilize approach if shear index > 0.7",
            "evidence": {"support": 0.65, "confidence": 0.9},
            "action": "Execute go-around criteria per SOP",
        },
        {
            "id": "E-FUEL-003",
            "title": "Refine fuel plan when deviation > 2.5% predicted",
            "evidence": {"support": 0.52, "confidence": 0.81},
            "action": "Adjust reserve and taxi fuel estimates",
        },
    ]
