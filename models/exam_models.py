"""
Models Layer - Exam Scheduling Data Models
Contains all data structures for exam scheduling
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd


@dataclass
class Student:
    """Student registration information."""
    id: str
    name: str
    program: str
    courses: List[str]


@dataclass
class Course:
    """Course information."""
    code: str
    name: str
    program: str
    exam_group: str
    duration_min: int


@dataclass
class ExamSlot:
    """Exam time slot."""
    date: datetime
    slot_id: str
    start_time: str
    end_time: str
    capacity: int


@dataclass
class ExamAssignment:
    """Exam group assignment to a slot."""
    exam_group: str
    date: datetime
    slot_id: str
    num_students: int


@dataclass
class Schedule:
    """Complete exam schedule."""
    assignments: List[ExamAssignment]
    violations: Dict[str, Any]
    metrics: Dict[str, Any]
    
    
@dataclass
class DiagnosticsResult:
    """Results from diagnostics check."""
    student_count: int
    course_count: int
    conflicts: pd.DataFrame
    capacity_issues: pd.DataFrame
    rest_violations: pd.DataFrame
    summary: Dict[str, Any]
