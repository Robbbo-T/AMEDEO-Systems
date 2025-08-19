"""
Base AMEDEO Agent implementation with depth validation and metrics.
UTCS-MI: AQUART-AGT-CODE-base_agent-v1.0
"""
import logging
import time
from abc import ABC, abstractmethod
from .intents import Intent, Result

def to_factor(metric: float, mode: str) -> float:
    """Convert metrics to productivity factors."""
    if mode == "gain":
        return max(metric, 1.0)  # Floor at 1.0
    elif mode == "reduce":
        if metric <= 0.0:
            return 1e6  # Avoid division by zero
        if metric >= 1.0:
            return 1e6  # Perfect reduction = massive gain
        return 1.0 / metric
    return 1.0

class AMEDEOAgent(ABC):
    """Base class for all AMEDEO agents with depth validation."""

    def __init__(self, agent_id: str, policy_path: str):
        self.id = agent_id
        self.policy_path = policy_path
        self.logger = logging.getLogger(f"amedeo.{agent_id}")

    def execute(self, intent: Intent) -> Result:
        """Execute an intent with depth validation."""
        start_time = time.time()

        # Validate intent
        if not isinstance(intent, Intent):
            return Result(status="ERROR", productivity_delta=1.0,
                         metadata={"error": "Invalid intent type"})

        try:
            # Execute core logic
            result = self._execute_core(intent)

            # Validate productivity delta meets depth requirements
            if result.productivity_delta < 3.0:
                self.logger.warning(f"Low productivity delta: {result.productivity_delta:.2f}x")

            # Add execution metadata
            execution_time = time.time() - start_time
            if result.metadata is None:
                result.metadata = {}
            result.metadata.update({
                "agent_id": self.id,
                "execution_time": execution_time,
                "intent_kind": intent.kind
            })

            return result

        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
            return Result(status="ERROR", productivity_delta=1.0,
                         metadata={"error": str(e), "agent_id": self.id})

    @abstractmethod
    def _execute_core(self, intent: Intent) -> Result:
        """Core execution logic to be implemented by subclasses."""
        pass
