"""
UTCS-MI: AQUART-TMR-MODULE-tmr_backend-v1.0
Triple Modular Redundancy (TMR) Backend with 2oo3 Consensus
"""

from .core import TMRBackend, PromptSpec, ResponseSpec, ValidationReport, ConsensusResult
from .engines import EngineAdapter, OpenAIAdapter, AnthropicAdapter, GoogleAdapter
from .validators import TMRValidator, UTCSValidator, S1000DValidator
from .consensus import ConsensusEngine

__all__ = [
    'TMRBackend',
    'PromptSpec', 
    'ResponseSpec',
    'ValidationReport',
    'ConsensusResult',
    'EngineAdapter',
    'OpenAIAdapter',
    'AnthropicAdapter', 
    'GoogleAdapter',
    'TMRValidator',
    'UTCSValidator',
    'S1000DValidator',
    'ConsensusEngine'
]