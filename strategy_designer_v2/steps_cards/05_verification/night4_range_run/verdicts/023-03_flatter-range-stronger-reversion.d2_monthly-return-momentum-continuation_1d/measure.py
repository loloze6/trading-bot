import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.ret30.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = 30-bar percent return (signed, graded); outcome = larger rise
    # for a larger return, so the expected side is long when the return is positive and
    # short when it is negative. Every active bar must have sign(forecast) == sign(raw return).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                close = pd.to_numeric(df["close"], errors="coerce")
                raw = close / close.shift(30) - 1.0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == np.sign(raw))
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the sign "
                           "of the 30-bar return, so the config does not take the long-after-rise / "
                           "short-after-fall side the plan's Fidelity states."),
            "reading": "Situation taken as the sign of the recorded raw 30-bar return; expected side = same sign.",
        }

    # ---------- 2. Criterion ----------
    # Grid cases per window: positions 0, 5, 10, ... with t+5 inside the window.
    coin_rets = {}   # all grid 5-bar returns per coin (for the drift)
    cases = []       # (coin, forecast, ret)
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = (pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
                  if "forecast" in df.columns else np.full(len(df), np.nan))
            for t in range(0, len(df) - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[t]):
                    cases.append((coin, float(fc[t]), r))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    x = np.array([c[1] for c in cases], dtype=float)
    y = np.array([c[2] - coin_rets[c[0]] for c in cases], dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = int(len(x))

    slope = None
    tval = None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    threshold = ("confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; "
                 "at least 200 non-overlapping grid cases")

    if n < 200:
        status = "not observable"
        decided_by = f"Only {n} non-overlapping grid cases with a recorded forecast, below the plan's minimum of 200."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 over at least 200 grid cases (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2 over at least 200 grid cases (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of excess 5-bar forward return on forecast, pooled",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {"non-overlapping grid cases with a recorded forecast": n},
        "decided_by": decided_by,
        "reading": ("Cases are grid bars 0,5,10,... of each window with t+5 in the window and a non-missing forecast "
                    "(zero forecasts included); each coin's drift is the mean of its grid 5-bar returns over all its "
                    "windows; the slope and its t come from a pooled OLS with an intercept."),
    }
