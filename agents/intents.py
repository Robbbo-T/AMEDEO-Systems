"""
AMEDEO Intent and Result classes for agent communication.
UTCS-MI: AQUART-AGT-CODE-intents-v1.0
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Intent:
    """Represents an intent sent to an AMEDEO agent."""
    kind: str
    payload: Dict[str, Any]

    def __post_init__(self):
        if not isinstance(self.payload, dict):
            self.payload = {}

@dataclass
class Result:
    """Represents the result of an agent's execution."""
    status: str
    productivity_delta: float
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
