"""
Supply Buyer Agent - Changes procurement rhythms and supply chain resilience.
UTCS-MI: AQUART-AGT-CODE-buyer_agent-v1.0
"""
from .base_agent import AMEDEOAgent
from .intents import Intent, Result

class SupplyBuyerAgent(AMEDEOAgent):
    """
    Agent that redesigns supply chains for lead time reduction,
    CO2 optimization, and resilience enhancement.
    """

    def _execute_core(self, intent: Intent) -> Result:
        """Execute supply chain optimization."""

        if intent.kind == "SUPPLY_CHAIN_METAMORPHOSIS":
            return self._handle_supply_metamorphosis(intent)
        elif intent.kind == "PROCUREMENT_RHYTHM_CHANGE":
            return self._handle_procurement_rhythm(intent)
        else:
            # Default supply chain optimization
            gain = intent.payload.get("expected_gain", 3.5)
            return Result(
                status="SUCCESS",
                productivity_delta=max(gain, 3.0),
                metadata={
                    "transformation": "supply_optimization",
                    "optimization_type": "general"
                }
            )

    def _handle_supply_metamorphosis(self, intent: Intent) -> Result:
        """Handle major supply chain transformation."""
        base_multiplier = 3.5

        # Supply chain factors
        affects_tempo = intent.payload.get("affects_tempo", False)
        lead_time_reduction = intent.payload.get("lead_time_reduction", 0.0)
        resilience_factor = intent.payload.get("resilience_factor", 1.0)

        productivity_delta = base_multiplier

        if affects_tempo:
            # Tempo changes are multiplicative
            productivity_delta *= 1.2

        if lead_time_reduction > 0:
            # Lead time reduction provides exponential benefits
            productivity_delta *= (1 + lead_time_reduction)

        productivity_delta *= resilience_factor

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "supply_metamorphosis",
                "affects_tempo": affects_tempo,
                "lead_time_reduction": lead_time_reduction,
                "resilience_factor": resilience_factor
            }
        )

    def _handle_procurement_rhythm(self, intent: Intent) -> Result:
        """Handle procurement rhythm optimization."""
        base_gain = 3.3

        rhythm_change = intent.payload.get("rhythm_multiplier", 1.0)
        make_vs_buy_ratio = intent.payload.get("make_vs_buy_ratio", 0.5)

        # Optimize make vs buy decisions
        if make_vs_buy_ratio < 0.3:  # More buying
            productivity_delta = base_gain * rhythm_change * 1.1
        elif make_vs_buy_ratio > 0.7:  # More making
            productivity_delta = base_gain * rhythm_change * 1.05
        else:  # Balanced
            productivity_delta = base_gain * rhythm_change

        return Result(
            status="SUCCESS",
            productivity_delta=max(productivity_delta, 3.0),
            metadata={
                "transformation": "procurement_rhythm",
                "rhythm_multiplier": rhythm_change,
                "make_vs_buy_ratio": make_vs_buy_ratio
            }
        )
