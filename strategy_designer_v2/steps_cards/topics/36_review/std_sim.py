"""Recompute a one-component forecast from the recorded raw value (last_history_value) for a standardise window W:
clip(10 x raw / mean(|raw| over the W stored values before it), +-20); 0 when fewer than min_periods past values or the
past mean is about 0. Compared with a record's own forecast, from bar W on (the warm-up before a window is not
recorded)."""
import numpy as np, pandas as pd
def std_forecast(raw, W, mp, target=10.0, cap=20.0, start_hist=None):
    out = np.zeros(len(raw)); hist = list(start_hist or [])
    for t, x in enumerate(raw):
        past = [v for v in hist[-W:] if np.isfinite(v)]
        if np.isfinite(x) and len(past) >= mp:
            m = np.mean(np.abs(past))
            out[t] = 0.0 if m <= 1e-10 else max(-cap, min(cap, target * x / m))
        hist.append(x)
    return out
