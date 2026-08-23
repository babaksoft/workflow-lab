"""
Application-wide utilities.
"""

from workflow_lab.utils.instrumentation import instrument
from workflow_lab.utils.timer import Timer

__all__ = [
    "Timer",
    "instrument",
]
