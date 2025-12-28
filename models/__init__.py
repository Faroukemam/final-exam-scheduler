"""
Models Layer - Data Models Package
Exports all data models for exam scheduling and invigilation
"""
from models.exam_models import (
    Student,
    Course,
    ExamSlot,
    ExamAssignment,
    Schedule,
    DiagnosticsResult
)

from models.invigilation_models import (
    StaffMember,
    InvigilationSession,
    Engagement,
    InvigilationAssignment,
    InvigilationSchedule
)

__all__ = [
    # Exam models
    'Student',
    'Course',
    'ExamSlot',
    'ExamAssignment',
    'Schedule',
    'DiagnosticsResult',
    # Invigilation models
    'StaffMember',
    'InvigilationSession',
    'Engagement',
    'InvigilationAssignment',
    'InvigilationSchedule',
]
