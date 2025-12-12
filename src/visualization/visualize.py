"""
Professional visualization utilities.
Auto-saves all figures to reports/figures/ with timestamp.
Uses seaborn + plotly with consistent, beautiful style.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
from src.utils import logger

# ----------------------------------------------------------------------
# Global config – consistent look across all plots
# ----------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("deep")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 12
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 14

# Auto-save directory
FIGURES_DIR = Path("reports/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def _auto_save(fig, filename: str, formats: List[str] = ["png", "pdf"]) -> Path:
    """Internal helper to save figure in multiple formats with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = FIGURES_DIR / f"{timestamp}_{filename}"
    for fmt in formats:
        path = base_name.with_suffix(f".{fmt}")
        fig.savefig(path, bbox_inches="tight", dpi=300)
    logger.info(f"Figure saved → {base_name}.png (and {', '.join(formats[1:])})")
    return base_name.with_suffix(".png")


# ----------------------------------------------------------------------
# Matplotlib / Seaborn plots
# ----------------------------------------------------------------------
def plot_correlation_matrix(
    df: pd.DataFrame,
    title: str = "Correlation Matrix",
    figsize: Tuple[int, int] = (14, 12),
    annot: bool = True,
) -> plt.Figure:
    plt.figure(figsize=figsize)
    corr = df.corr(numeric_only=True)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr,
        mask=mask,
        annot=annot,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    plt.title(title, pad=20)
    return _auto_save(plt.gcf(), "correlation_matrix")


def plot_feature_importance(
    importance: np.ndarray,
    feature_names: List[str],
    top_n: int = 20,
    title: str = "Top Feature Importance",
) -> plt.Figure:
    indices = np.argsort(importance)[-top_n:]
    plt.figure(figsize=(10, max(6, top_n * 0.4)))
    plt.barh(range(len(indices)), importance[indices], align="center")
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel("Importance")
    plt.title(title)
    plt.tight_layout()
    return _auto_save(plt.gcf(), "feature_importance")


def plot_prediction_vs_actual(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Predictions vs Actual",
) -> plt.Figure:
    plt.figure(figsize=(10, 10))
    plt.scatter(y_true, y_pred, alpha=0.6, edgecolors="k", s=60)
    min_val, max_val = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], "r--", lw=2)
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    return _auto_save(plt.gcf(), "pred_vs_actual")


def plot_training_history(history, title: str = "Model Training History") -> plt.Figure:
    """For Keras / PyTorch Lightning style history dict or DataFrame"""
    if isinstance(history, dict):
        hist_df = pd.DataFrame(history)
    else:
        hist_df = history

    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    plt.plot(hist_df["loss"], label="train_loss", marker="o")
    if "val_loss" in hist_df.columns:
        plt.plot(hist_df["val_loss"], label="val_loss", marker="o")
    plt.title("Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if "accuracy" in hist_df.columns or "acc" in hist_df.columns:
        plt.subplot(1, 2, 2)
        acc_key = "accuracy" if "accuracy" in hist_df.columns else "acc"
        plt.plot(hist_df[acc_key], label=f"train_{acc_key}", marker="o")
        if f"val_{acc_key}" in hist_df.columns:
            plt.plot(hist_df[f"val_{acc_key}"], label=f"val_{acc_key}", marker="o")
        plt.title("Accuracy")
        plt.legend()
        plt.grid(True, alpha=0.3)

    plt.suptitle(title)
    return _auto_save(plt.gcf(), "training_history")


# ----------------------------------------------------------------------
# Plotly interactive plots
# ----------------------------------------------------------------------
def plot_distribution_interactive(
    df: pd.DataFrame,
    column: str,
    title: Optional[str] = None,
) -> go.Figure:
    fig = px.histogram(
        df,
        x=column,
        marginal="box",
        hover_data=df.columns,
        title=title or f"Distribution of {column}",
        template="simple_white",
    )
    fig.update_layout(showlegend=False)
    path = FIGURES_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_dist_{column}.html"
    fig.write_html(path)
    logger.info(f"Interactive plot saved → {path.name}")
    fig.show()
    return fig


def plot_time_series_interactive(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Time Series",
    color: Optional[str] = None,
) -> go.Figure:
    fig = px.line(df, x=x, y=y, color=color, title=title, template="simple_white")
    path = FIGURES_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_ts_{y}.html"
    fig.write_html(path)
    logger.info(f"Interactive time series saved → {path.name}")
    fig.show()
    return fig


# ----------------------------------------------------------------------
# Generic save helper
# ----------------------------------------------------------------------
def save_fig(
    fig: plt.Figure = None,
    name: str = "figure",
    formats: List[str] = ["png", "pdf"],
) -> None:
    """Manually save current or passed figure."""
    if fig is None:
        fig = plt.gcf()
    _auto_save(fig, name, formats)
    plt.close(fig)
