#!/usr/bin/env python3
"""
Digital Evidence Twin (DET) - Minimal runtime stub for demos/tests.

Provides async initialize() and log_event() APIs used by AMEDEO demos.
This lightweight implementation stores events in memory and optionally
writes a compact line to a local logfile for traceability.
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any, Dict, List, Optional


class DigitalEvidenceTwin:
    """Simple in-memory DET used for local demonstration runs."""

    def __init__(self, logfile: str = "det_events.log"):
        self._events: List[Dict[str, Any]] = []
        self._initialized: bool = False
        self._logfile = logfile

    async def initialize(self) -> bool:
        # Simulate async init latency
        await asyncio.sleep(0)
        self._initialized = True
        return True

    async def log_event(self, event: Dict[str, Any]) -> None:
        # Ensure event is timestamped
        if "timestamp" not in event:
            event["timestamp"] = time.time()
        self._events.append(event)
        # Write compact NDJSON line for quick inspection (best-effort)
        try:
            with open(self._logfile, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception:
            # Non-fatal in demo context
            pass

    def get_events(self) -> List[Dict[str, Any]]:
        return list(self._events)
