"""Data ingestion and split management.

Loads:
- FlightOperation data (FDR/FOQA aggregates)
- IncidentRecord data (NTSB/FAA/EASA harmonized)
- WeatherSnapshot data (METAR/TAF, reanalysis, winds/temps aloft)
- AirlinePolicy snippets

Creates time-based TTS splits and OOD holdouts.
"""
from typing import Dict, Tuple


def load_all_sources(data_paths: Dict) -> Tuple[Dict, Dict]:
    """Load all data and return (raw_data, holdout_sets).
    This is a placeholder returning empty dicts.
    """
    raw = {}
    holdouts = {}
    return raw, holdouts
