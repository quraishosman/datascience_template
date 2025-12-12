"""
Visualization module – beautiful, auto-saved, publication-ready plots.
"""
from .visualize import (
    plot_correlation_matrix,
    plot_feature_importance,
    plot_prediction_vs_actual,
    plot_training_history,
    plot_distribution_interactive,
    plot_time_series_interactive,
    save_fig,
)

__all__ = [
    "plot_correlation_matrix",
    "plot_feature_importance",
    "plot_prediction_vs_actual",
    "plot_training_history",
    "plot_distribution_interactive",
    "plot_time_series_interactive",
    "save_fig",
]
