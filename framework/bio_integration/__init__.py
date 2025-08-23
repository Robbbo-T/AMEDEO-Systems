"""
UTCS-MI: AQUART-BIO-CODE-init-v1.0
Bio-Integration Framework for Living Aircraft Systems
"""

from .bio_aircraft import LivingAircraftSystem, BioConsciousnessSystem
from .bio_consciousness import ConsciousnessFramework, ConsciousnessMeter

__all__ = [
    'LivingAircraftSystem',
    'BioConsciousnessSystem', 
    'ConsciousnessFramework',
    'ConsciousnessMeter'
]

__version__ = "1.0.0"
__motto__ = "Bridging the gap between digital systems and biological consciousness"