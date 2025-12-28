"""
Utils Layer - Date Utilities
Date normalization and manipulation functions
"""
from datetime import datetime
import pandas as pd
from typing import Any

def normalize_date_ignore_year(x: Any):
    """
    Parse date then force year=2000 so comparisons depend on month/day only.
    Returns pandas Timestamp or NaT.
    """
    if pd.isna(x):
        return pd.NaT
    try:
        ts = pd.to_datetime(x, errors='coerce')
        if pd.notna(ts):
            return ts.replace(year=2000)
        return pd.NaT
    except:
        return pd.NaT

def normalize_date(val):
    """
    Normalize date to MM-DD key format.
    Examples:
        5/1           -> 05-01
        05/01/2025    -> 05-01
        2025-01-05    -> 01-05
    """
    if pd.isna(val):
        return None
    try:
        dt = pd.to_datetime(val, errors='coerce')
        if pd.notna(dt):
            return f"{dt.month:02d}-{dt.day:02d}"
    except:
        pass
    return None

def mmdd_str(ts):
    """Convert timestamp to MM-DD string."""
    if pd.notna(ts):
        return f"{ts.month:02d}-{ts.day:02d}"
    return ""
