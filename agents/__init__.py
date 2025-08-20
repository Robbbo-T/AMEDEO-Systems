"""
AMEDEO Agent Framework
UTCS-MI: AQUART-AGT-CODE-init-v1.0
"""

from .base_agent import AMEDEOAgent, Intent, Result, DET, AMOReS, SEAL, to_factor
from .planner_agent import StrategicPlannerAgent
from .buyer_agent import SupplyBuyerAgent
from .scheduler_agent import ResourceSchedulerAgent
from .ops_pilot_agent import OpsPilotAgent

__all__ = [
    'AMEDEOAgent',
    'Intent',
    'Result', 
    'DET',
    'AMOReS',
    'SEAL',
    'to_factor',
    'StrategicPlannerAgent',
    'SupplyBuyerAgent',
    'ResourceSchedulerAgent',
    'OpsPilotAgent'
]

__version__ = "1.0.0"
__motto__ = "no hacen recados: bordean el futuro en profundidad, no lo pintan en superficie"