"""
Utils Layer - Time Utilities
Time parsing and formatting functions
"""
from typing import Any
import re

def time_to_min(x: Any) -> int:
    """
    Accept '09:30' or 930 / 1130 style. Return minutes from 00:00.
    """
    if isinstance(x, (int, float)):
        hhmm = int(x)
        h = hhmm // 100
        m = hhmm % 100
        return h * 60 + m
    if isinstance(x, str):
        x = x.strip()
        if ':' in x:
            parts = x.split(':')
            if len(parts) == 2:
                try:
                    h = int(parts[0])
                    m = int(parts[1])
                    return h * 60 + m
                except ValueError:
                    pass
        else:
            try:
                hhmm = int(x)
                h = hhmm // 100
                m = hhmm % 100
                return h * 60 + m
            except ValueError:
                pass
    return 0

def fmt_hhmm(minutes: int) -> str:
    """Format minutes to HH:MM string."""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

def parse_time_to_min(val) -> int:
    """
    Convert 930 or '09:30' or 930.0 to minutes from start of day.
    """
    if pd.isna(val):
        return 0
    if isinstance(val, (int, float)):
        hhmm = int(val)
        h = hhmm // 100
        m = hhmm % 100
        return h * 60 + m
    if isinstance(val, str):
        val = val.strip()
        if ':' in val:
            h, m = val.split(':')
            return int(h) * 60 + int(m)
        else:
            hhmm = int(val)
            h = hhmm // 100
            m = hhmm % 100
            return h * 60 + m
return 0

import pandas as pd
