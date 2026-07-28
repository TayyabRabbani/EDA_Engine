"""eda_engine — schema-driven, on-demand exploratory data analysis.

Quick start:
    from eda_engine import EDA
    eda = EDA(df)
    eda.overview()
    eda.plot_distribution("Age")
"""
from .core import EDA
from .schema import SchemaDetector
from .quality import QualityAnalyzer
from .profiler import StatisticalProfiler
from .visualizer import Visualizer

__all__ = [
    "EDA",
    "SchemaDetector",
    "QualityAnalyzer",
    "StatisticalProfiler",
    "Visualizer",
]
