"""
Models Layer - Invigilation Data Models
Contains all data structures for invigilation scheduling
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class StaffMember:
    """Staff member information."""
    staff_id: str
    name: str
    load_type: str  # 'full' or 'half'
    max_hours: float


@dataclass
class InvigilationSession:
    """Exam session requiring invigilators."""
    session_id: str
    room: str
    date: datetime
    start_time: str
    end_time: str
    duration_min: int
    invigilators_needed: int


@dataclass
class Engagement:
    """Staff engagement/unavailability."""
    staff_id: str
    date: datetime
    start_time: str
    end_time: str
    is_busy: bool  # True if engaged/unavailable


@dataclass
class InvigilationAssignment:
    """Assignment of staff to session."""
    session_id: str
    staff_id: str
    staff_name: str


@dataclass
class InvigilationSchedule:
    """Complete invigilation schedule."""
    assignments: List[InvigilationAssignment]
    staff_loads: dict  # staff_id -> hours assigned
    fairness_metrics: dict
    unassigned_sessions: List[str]
