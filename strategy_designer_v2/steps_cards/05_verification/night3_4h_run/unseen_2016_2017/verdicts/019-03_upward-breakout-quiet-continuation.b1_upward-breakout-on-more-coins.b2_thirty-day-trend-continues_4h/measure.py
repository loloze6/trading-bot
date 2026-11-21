import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    RAW = "debug_info.components.ret30d.last_history_value"
    MIN_POS = 300

    # ---------- 1. Situation check ----------
    # Situation: the coin's 30-day (180-bar) return is positive. Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Recompute the raw value from prices where it is not recorded.
            # This uses the window's own bars only, so it is NaN near a window's start.
            recomputed = (close / close.shift(180) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        if agreement is None:
            why = ("No bar has a non-zero forecast, so the plan's situation "
                   "(a positive 30-day return, long) cannot be matched.")
        else:
            why = ("Fewer than 90% of the bars with a non-zero forecast have a positive "
                   "30-day return with a long forecast, so the config does not do what "
                   "the Fidelity says.")
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": why,
            "reading": ("Situation taken as ret30d raw value > 0 (recomputed from closes "
                        "where it is missing), side long."),
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            # Grid positions 0, 18, 36, ... counted from the window's first row,
            # keeping only those whose forward return stays inside the window.
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, float(c1 / c0 - 1.0), fc[t]))

    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(g):
        # Drift from holding: the coin's mean 18-bar grid return over all its windows.
        drift = g.groupby("coin")["ret"].transform("mean")
        g["y"] = g["ret"] - drift
        g = g[np.isfinite(g["fc"].astype(float))]
        g["fc"] = g["fc"].astype(float)

    n_cases = int(len(g))
    n_pos = int((g["fc"] > 0).sum()) if n_cases else 0

    slope = None
    tval = None
    if n_cases >= 3 and g["fc"].nunique() > 1:
        lr = stats.linregress(g["fc"].values, g["y"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {
        "grid cases with forecast > 0": n_pos,
        "grid cases": n_cases,
    }

    if n_pos < MIN_POS:
        status = "not observable"
        decided = (f"Only {n_pos} grid cases have forecast > 0, "
                   f"below the plan's minimum of {MIN_POS}.")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be estimated, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = (f"The slope is positive with t >= 2, over at least {MIN_POS} "
                   "grid cases with forecast > 0.")
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = (f"The slope is negative with t <= -2, over at least {MIN_POS} "
                   "grid cases with forecast > 0.")
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which meets the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": ("pooled OLS slope of the 18-bar forward return minus the coin's "
                     "mean 18-bar return, on the forecast"),
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval}
                          if tval is not None else None),
            "threshold": ("confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; "
                          "at least 300 grid cases with forecast > 0"),
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": ("The regression is pooled OLS with an intercept over all grid cases, "
                    "flat cases included, with the drift taken as each coin's mean 18-bar "
                    "grid return over all its windows; following the workflow, fewer than "
                    "300 grid cases with forecast > 0 is reported as 'not observable'."),
    }
