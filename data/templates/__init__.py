"""
Data Layer - Template Generator Package
Exports template generation functions
"""
from data.templates.template_generator import (
    generate_exam_scheduler_templates,
    generate_invigilation_templates,
    generate_courses_report_templates
)

__all__ = [
    'generate_exam_scheduler_templates',
    'generate_invigilation_templates',
    'generate_courses_report_templates',
]
