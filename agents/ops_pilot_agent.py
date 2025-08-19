"""
Ops Pilot Agent - Changes operational envelopes and mission parameters.
UTCS-MI: AQUART-AGT-CODE-ops_pilot_agent-v1.0
"""
from .base_agent import AMEDEOAgent
from .intents import Intent, Result

class OpsPilotAgent(AMEDEOAgent):
    """
    Agent that expands operational envelopes and optimizes mission execution.
    Handles real-time operational parameter adjustments.
    """

    def _execute_core(self, intent: Intent) -> Result:
        """Execute operational envelope optimization."""

        if intent.kind == "OPERATIONAL_ENVELOPE_EXPANSION":
            return self._handle_envelope_expansion(intent)
        elif intent.kind == "MISSION_PARAMETER_OPTIMIZATION":
            return self._handle_mission_optimization(intent)
        else:
            # Default operational optimization
            gain = intent.payload.get("expected_gain", 3.3)
            return Result(
                status="SUCCESS",
                productivity_delta=max(gain, 3.0),
                metadata={
                    "transformation": "operational_optimization",
                    "optimization_type": "general"
                }
            )

    def _handle_envelope_expansion(self, intent: Intent) -> Result:
        """Handle operational envelope expansion."""
        base_multiplier = 3.3

        # Operational factors
        expands_envelope = intent.payload.get("expands_envelope", False)
        safety_margin = intent.payload.get("safety_margin", 0.1)
        performance_gain = intent.payload.get("performance_gain", 0.0)

        productivity_delta = base_multiplier

        if expands_envelope:
            # Envelope expansion enables new operational modes
            productivity_delta *= 1.25

        # Safety margin considerations (higher margin = lower risk, slight productivity trade-off)
        if safety_margin > 0.2:
            productivity_delta *= 0.98  # Small penalty for conservative operation
        elif safety_margin < 0.05:
            productivity_delta *= 1.02  # Bonus for optimized operation

        # Performance gain multiplier
        if performance_gain > 0:
            productivity_delta *= (1 + performance_gain)

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "envelope_expansion",
                "expands_envelope": expands_envelope,
                "safety_margin": safety_margin,
                "performance_gain": performance_gain
            }
        )

    def _handle_mission_optimization(self, intent: Intent) -> Result:
        """Handle mission parameter optimization."""
        base_gain = 3.4

        mission_efficiency = intent.payload.get("mission_efficiency", 1.0)
        parameter_count = intent.payload.get("optimized_parameters", 1)

        # More parameters optimized = higher gains
        productivity_delta = base_gain * mission_efficiency
        productivity_delta *= (1 + (parameter_count - 1) * 0.1)

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "mission_optimization",
                "mission_efficiency": mission_efficiency,
                "optimized_parameters": parameter_count
            }
        )
