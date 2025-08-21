#!/usr/bin/env python3
"""Test metric normalization edge cases"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from base_agent import to_factor


def test_to_factor_gain():
    assert to_factor(4.2, "gain") == 4.2
    assert to_factor(0.5, "gain") == 1.0
    assert to_factor(-1.0, "gain") == 1.0


def test_to_factor_reduce_primary():
    # reduce expects remaining fraction; 0.72 -> 1/(1-0.72) ~ 3.571
    assert to_factor(0.72, "reduce") == pytest.approx(3.571, rel=0.01)


def test_to_factor_reduce_edges():
    assert to_factor(0.0, "reduce") >= 1e6
    assert to_factor(1.0, "reduce") >= 1e6
