"""
FOLD - Fractal Optimized Layered Data

A production-grade library for converting arbitrary data to video files and back.
"""

__version__ = "1.0.0"
__author__ = "FOLD Team"

from .core.encoder import store
from .core.decoder import retrieve

__all__ = ["store", "retrieve"]