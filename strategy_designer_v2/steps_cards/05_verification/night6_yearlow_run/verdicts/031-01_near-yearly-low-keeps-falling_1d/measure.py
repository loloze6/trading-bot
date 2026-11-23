import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.low_prox.last_history_value"
    MIN_CASES = 100

    # ---------- 1. Situation check ----------
    # Situation: graded proximity to the 365-bar closing low, raw value in (0, 1].
    # Expected side: short (the outcome is a fall).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0) & raw.notna()
            n_active += int(active.sum())
            situ = (raw > 0) & (raw <= 1.0 + 1e-12)
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of drift-adjusted 20-bar short gain on |forecast|"
    threshold = "slope > 0 with t >= 2 confirms (with top-fifth check); slope < 0 with t <= -2 rejects"
    sup_name = "mean drift-adjusted short gain of the top fifth of |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a recorded proximity to the "
                           "365-bar closing low in (0, 1], so the forecast does not do what the Fidelity says."),
            "reading": "Active bars without a recorded raw proximity value were left out of the agreement share.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = c[p], c[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_cases.append((c1 / c0 - 1.0, f[p]))
        if not coin_cases:
            continue
        r = np.array([x[0] for x in coin_cases])
        drift = float(np.mean(r))  # coin's mean 20-bar return over all its windows
        for ret, fc in coin_cases:
            if np.isfinite(fc):
                rows.append((-(ret - drift), abs(fc)))

    n_cases = len(rows)
    counts = {"non-overlapping cases": n_cases}
    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 100.",
            "reading": ("Cases are grid positions 0, 20, 40, ... of each window with a 20-bar forward close in the "
                        "same window, all grid cases kept (|forecast| 0 included); drift is each coin's mean over its grid."),
        }

    y = np.array([r[0] for r in rows], dtype=float)
    x = np.array([r[1] for r in rows], dtype=float)

    slope = None
    t = None
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    k = n_cases // 5
    order = np.argsort(-x, kind="mergesort")
    top = y[order[:k]] if k > 0 else np.array([])
    top_mean = float(np.mean(top)) if len(top) > 0 else None
    top_pass = bool(top_mean is not None and top_mean > 0)
    counts["top-fifth cases"] = int(k)

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in |forecast|), so it is not outside -2..2."
    elif slope > 0 and t >= 2:
        if top_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-fifth mean short gain is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top-fifth mean short gain is not above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: gains fall as proximity to the yearly low rises."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": top_mean, "passed": top_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are grid positions 0, 20, 40, ... of each window with a 20-bar forward close in the same "
                    "window, all kept including |forecast| 0, drift is each coin's mean 20-bar grid return over all "
                    "its windows, and the top fifth is the floor(n/5) pooled cases with the largest |forecast|."),
    }
