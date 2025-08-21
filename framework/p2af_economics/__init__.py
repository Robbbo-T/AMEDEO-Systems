"""
UTCS-MI: AQUART-P2AF-CODE-init-v1.0
P²AF (Public-Private Autonomous Finance) Framework
Corruption-proof economic systems for aerospace applications
"""

from .corruption_proof_economics import (
    CorruptionProofEconomics,
    EconomicTransaction,
    TransactionType,
    EthicsViolation,
    AuditRecord
)

__all__ = [
    'CorruptionProofEconomics',
    'EconomicTransaction', 
    'TransactionType',
    'EthicsViolation',
    'AuditRecord'
]

__version__ = "1.0.0"
__motto__ = "Making corruption mathematically impossible through autonomous transparency"