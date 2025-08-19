"""
Resource Scheduler Agent - Changes capacity limits and elastic scaling.
UTCS-MI: AQUART-AGT-CODE-scheduler_agent-v1.0
"""
from .base_agent import AMEDEOAgent
from .intents import Intent, Result

class ResourceSchedulerAgent(AMEDEOAgent):
    """
    Agent that transforms resource allocation and capacity planning.
    Optimizes elastic scaling and operational envelope expansion.
    """

    def _execute_core(self, intent: Intent) -> Result:
        """Execute resource scheduling optimization."""

        if intent.kind == "ELASTIC_CAPACITY_TRANSFORM":
            return self._handle_elastic_transform(intent)
        elif intent.kind == "RESOURCE_ENVELOPE_EXPANSION":
            return self._handle_envelope_expansion(intent)
        else:
            # Default resource optimization
            gain = intent.payload.get("expected_gain", 3.4)
            return Result(
                status="SUCCESS",
                productivity_delta=max(gain, 3.0),
                metadata={
                    "transformation": "resource_optimization",
                    "optimization_type": "general"
                }
            )

    def _handle_elastic_transform(self, intent: Intent) -> Result:
        """Handle elastic capacity transformation."""
        base_multiplier = 3.4

        # Elastic scaling factors
        expands_envelope = intent.payload.get("expands_envelope", False)
        scaling_factor = intent.payload.get("scaling_factor", 1.0)
        utilization_efficiency = intent.payload.get("utilization_efficiency", 0.8)

        productivity_delta = base_multiplier

        if expands_envelope:
            # Envelope expansion is highly valuable
            productivity_delta *= 1.3

        # Scaling efficiency impacts
        productivity_delta *= scaling_factor

        # Utilization efficiency bonus
        if utilization_efficiency > 0.9:
            productivity_delta *= 1.1
        elif utilization_efficiency < 0.6:
            productivity_delta *= 0.95

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "elastic_transform",
                "expands_envelope": expands_envelope,
                "scaling_factor": scaling_factor,
                "utilization_efficiency": utilization_efficiency
            }
        )

    def _handle_envelope_expansion(self, intent: Intent) -> Result:
        """Handle operational envelope expansion."""
        base_gain = 3.6

        expansion_factor = intent.payload.get("expansion_factor", 1.0)
        capacity_increase = intent.payload.get("capacity_increase", 0.0)

        # Envelope expansion provides compound benefits
        productivity_delta = base_gain * expansion_factor

        if capacity_increase > 0:
            # Additional capacity provides multiplicative benefits
            productivity_delta *= (1 + capacity_increase)

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "envelope_expansion",
                "expansion_factor": expansion_factor,
                "capacity_increase": capacity_increase
            }
        )
