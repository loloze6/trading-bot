import importlib
from typing import Any, Dict, List, Optional, Type

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere


def _load_class(class_path: str) -> Type:
    """
    Load a class from a dotted import path.
    Raises ValueError with a clear message on any import or attribute error.

    Example: 'strategies.strategy_components.EfficiencyRatioRegimeComponent'
    """
    try:
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Cannot load component class '{class_path}': {e}") from e


def _safe_zscore(s: pd.Series) -> float:
    std = s.std()
    return float((s.iloc[-1] - s.mean()) / std) if std > 1e-10 else 0.0


def _ratio_to_mean(s: pd.Series) -> float:
    mean = s.abs().mean()
    return float(s.iloc[-1] / mean) if mean > 1e-10 else 0.0


# ---------------------------------------------------------------------------
# Pipeline-based transform ops
# Signature: (v: float, h: pd.Series, p: dict, data: pd.DataFrame | None) -> float
#
# History-based ops  — recompute from the full series `h`, ignoring `v`.
# Scalar ops         — operate on the accumulated pipeline value `v`.
# Data-aware ops     — read the current OHLCV bar from `data`.
#
# WARNING: history-based ops (identity, percentile, zscore, ratio_to_mean, ema)
# discard the accumulated pipeline value and recompute from the raw history.
# They must appear BEFORE any scalar ops (scale, threshold_filter, clip, negate, sigmoid).
# Writing [scale, percentile] silently throws away the scale output.
#
# Use apply_transform_pipeline() to run an ordered list of these ops.
# ---------------------------------------------------------------------------
TRANSFORM_OPS_REGISTRY: Dict[str, Any] = {
    # History-based — recompute from `h`, ignore `v`
    "identity":          lambda v, h, p, d: float(h.iloc[-1]),
    "percentile":        lambda v, h, p, d: float(h.rank(pct=True).iloc[-1]),
    "negate_percentile": lambda v, h, p, d: float(1.0 - h.rank(pct=True).iloc[-1]),
    "zscore":            lambda v, h, p, d: _safe_zscore(h),
    "ratio_to_mean":     lambda v, h, p, d: _ratio_to_mean(h),
    "ema":               lambda v, h, p, d: float(
        h.ewm(span=min(len(h), p.get("span", 10)), adjust=False).mean().iloc[-1]
    ),
    # Scalar — operate on accumulated `v`, ignore `h`
    "scale":             lambda v, h, p, d: v * p.get("factor", 1.0),
    "threshold_filter":  lambda v, h, p, d: v if abs(v) >= p.get("min_abs", 0.0) else 0.0,
    "clip":              lambda v, h, p, d: float(np.clip(v, p.get("min", -np.inf), p.get("max", np.inf))),
    "sigmoid":           lambda v, h, p, d: float(1.0 / (1.0 + np.exp(-v))),
    "negate":            lambda v, h, p, d: -v,
    # Data-aware — read current OHLCV bar from `d`
    # Intentionally NO guard: NaN stddev_24 must propagate as NaN (not 0.0) so that
    # pandas mean() in ratio_to_mean skips those entries rather than being poisoned.
    "vol_normalize":     lambda v, h, p, d: v / (d["stddev_24"].iloc[-1] * d["close"].iloc[-1]),
    "vol_adjusted":      lambda v, h, p, d: (
        v / (d["stddev_24"].iloc[-1] * d["close"].iloc[-1])
        if d is not None and "stddev_24" in d.columns
        and (d["stddev_24"].iloc[-1] * d["close"].iloc[-1]) > 1e-10
        else v
    ),
    "price_normalized":  lambda v, h, p, d: (
        v / d["close"].iloc[-1]
        if d is not None and d["close"].iloc[-1] > 1e-10
        else v
    ),
    "volume_filter":     lambda v, h, p, d: (
        v if d is None or
        d["volume"].iloc[-1] >= d["volume"].rolling(p.get("period", 20)).mean().iloc[-1]
        else 0.0
    ),
}


def apply_transform_pipeline(
    history:    pd.Series,
    transforms: List[Dict[str, Any]],
    data:       Optional[pd.DataFrame] = None,
) -> float:
    """
    Execute an ordered list of transform ops against a component's rolling history.

    The pipeline seeds with the latest raw value. History-based ops recompute
    from `history`; scalar ops operate on the accumulated value from previous ops.
    Data-aware ops may read the current OHLCV bar from `data` (optional).
    """
    # logger.debug(f"DEBUG // apply_transform_pipeline is called and len(history) is {len(history)}")
    if not len(history):
        return 0.0
    value = float(history.iloc[-1])
    for step in transforms:
        # logger.debug(f"DEBUG // apply_transform_pipeline is now calling step {step["op"]}")
        op     = TRANSFORM_OPS_REGISTRY[step["op"]]
        params = step.get("params", {})
        value  = op(value, history, params, data)
        # logger.debug(f"DEBUG // apply_transform_pipeline is for step {step["op"]} got a value of {value}")
    return value


# Minimum number of history samples each op needs to produce a reliable output.
# Scalar ops need only 1 (they operate on the current value, not the history).
# History-based ops need enough samples for their statistic to stabilize.
TRANSFORM_MIN_PERIODS: Dict[str, int] = {
    "identity":          1,
    "percentile":        50,   # rank over <20 samples is too coarse
    "negate_percentile": 50,
    "zscore":            30,   # mean and std unstable below ~30 samples
    "ratio_to_mean":     30,
    "ema":               1,    # dynamic: resolved in transform_min_periods() using span
    "scale":             1,
    "threshold_filter":  1,
    "clip":              1,
    "sigmoid":           1,
    "negate":            1,
    "vol_normalize":     1,
    "vol_adjusted":      1,
    "price_normalized":  1,
    "volume_filter":     1,
}


def transform_min_periods(op: str, params: Dict[str, Any]) -> int:
    """Return the minimum history samples needed for `op` with these params to be reliable."""
    if op == "ema":
        # EWM with span s is ~95% warmed up after 3×s bars
        return params.get("span", 10) * 3
    if op not in TRANSFORM_MIN_PERIODS:
        raise KeyError(
            f"Op '{op}' is in TRANSFORM_OPS_REGISTRY but has no entry in "
            f"TRANSFORM_MIN_PERIODS. Add one before using it in a transforms list."
        )
    return TRANSFORM_MIN_PERIODS[op]


def component_effective_lookback(c_spec: Dict[str, Any], comp_required: int) -> int:
    """
    Return the history buffer size needed for one component spec.

    Takes the max of the component's own required periods and the minimum
    history any of its transform steps needs to produce a reliable output.
    """
    all_steps = c_spec.get("transforms", []) + c_spec.get("history_transforms", [])
    transform_min = max(
        (transform_min_periods(step["op"], step.get("params", {})) for step in all_steps),
        default=1,
    )
    return max(comp_required, transform_min)
