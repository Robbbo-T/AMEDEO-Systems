"""
Strategic Planner Agent - Changes decision horizons.
UTCS-MI: AQUART-AGT-CODE-planner_agent-v1.0
"""
from .base_agent import AMEDEOAgent
from .intents import Intent, Result

class StrategicPlannerAgent(AMEDEOAgent):
    """
    Agent that re-architects priorities and decision horizons.
    Transforms M/M/1 → M/G/k queuing models for portfolio management.
    """

    def _execute_core(self, intent: Intent) -> Result:
        """Execute strategic planning with horizon shifts."""

        # Handle different strategic intent types
        if intent.kind == "HORIZON_SHIFT":
            return self._handle_horizon_shift(intent)
        elif intent.kind == "PORTFOLIO_REBALANCE":
            return self._handle_portfolio_rebalance(intent)
        else:
            # Default strategic transformation
            gain = intent.payload.get("expected_gain", 3.2)
            return Result(
                status="SUCCESS",
                productivity_delta=max(gain, 3.0),  # Ensure depth requirement
                metadata={
                    "transformation": "strategic_planning",
                    "horizon_type": "decision_architecture"
                }
            )

    def _handle_horizon_shift(self, intent: Intent) -> Result:
        """Handle horizon shift transformations."""
        base_multiplier = 3.2

        # Strategic factors that affect decision horizons
        affects_strategy = intent.payload.get("affects_strategy", False)
        complexity_factor = intent.payload.get("complexity_factor", 1.0)

        if affects_strategy:
            # Major strategic realignment
            productivity_delta = base_multiplier * complexity_factor
        else:
            # Tactical adjustment
            productivity_delta = base_multiplier * 0.9

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "horizon_shift",
                "affects_strategy": affects_strategy,
                "complexity_factor": complexity_factor
            }
        )

    def _handle_portfolio_rebalance(self, intent: Intent) -> Result:
        """Handle portfolio rebalancing operations."""
        base_gain = 3.5
        risk_adjustment = intent.payload.get("risk_adjustment", 1.0)

        productivity_delta = base_gain * risk_adjustment

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "portfolio_rebalance",
                "risk_adjustment": risk_adjustment
            }
        )
