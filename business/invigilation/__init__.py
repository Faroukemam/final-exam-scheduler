"""
Business Layer - Invigilation Scheduling Package
Exports the main invigilation scheduling function
"""
from business.invigilation.scheduler import run_optimization

__all__ = [
    'run_optimization',
]
