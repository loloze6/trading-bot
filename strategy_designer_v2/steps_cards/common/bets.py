"""A bet of an idea, read on a backtest record: where the forecast makes one, and the band it trades with.
The same rule as the engine's holding period (trading-bot/core/holding_period.py; common/forecast.md 7).
Used by idea_size.py (step 5) and by the book's diagnosis (topics/34_review/).

Why this can't leak: it reads a finished record's forecast after the fact; it changes no decision.
"""
import json, math
import numpy as np


def bets(fc, band=0.2):
    """The bars where a bet is made: the forecast rises on its own side by at least the band (on the signal scale,
    forecast / 10) from its lowest level on that side since its last bet (from 0 after a flat or a change of side).
    The same rule as the engine's holding period (trading-bot/core/holding_period.py; common/forecast.md 7)."""
    out, prev, low = [], 0.0, 0.0
    for t, f in enumerate((np.asarray(fc, float) / 10.0).tolist()):
        if not math.isfinite(f):
            continue
        side = (f > 0) - (f < 0)
        if side == 0 or (prev > 0) != (f > 0) or (prev < 0) != (f < 0):
            low = 0.0
        prev = f
        if side == 0:
            continue
        size = side * f
        if size > 0 and size - low >= band - 1e-9:
            out.append(t); low = size
        elif low > 0:
            low = min(low, size)
    return np.array(out, dtype=int)


def band_of(record):
    """The band the record's config traded with: strategies.min_allocation_change, else the risk layer's 0.2."""
    try:
        v = json.loads((record / "config.json").read_text())["strategies"].get("min_allocation_change")
        return float(v) if v is not None else 0.2
    except (OSError, KeyError, ValueError):
        return 0.2
