import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.dip.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: rising market (regime "unknown", i.e. not vetoed to "chop")
    # and close below its 5-day closing high (raw dip < 0). Expected side: short.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rising = df["regime"].astype(str) == "unknown"
            in_dip = raw.notna() & (raw < 0)
            agree = active & rising & in_dip & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess 5-bar return on |forecast|"
    threshold = "confirm if slope < 0 with t <= -2; reject if slope > 0 with t >= 2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active),
                       "grid cases with a nonzero forecast": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are rising-market bars "
                           "below the 5-day closing high with a short forecast, as the Fidelity states."),
            "reading": ("Situation taken as regime 'unknown' (the rising profile, not vetoed to chop) "
                        "with the recorded raw dip value below 0, on the short side."),
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        grid_cases = []  # (ret, |forecast|)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] != 0:
                    grid_cases.append((r, abs(f[i])))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, a in grid_cases:
            ys.append(r - drift)
            xs.append(a)

    n_cases = len(xs)
    counts = {"grid cases with a nonzero forecast": int(n_cases)}

    slope = None
    tval = None
    if n_cases >= 3:
        x = np.asarray(xs, dtype=float)
        y = np.asarray(ys, dtype=float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
                tval = float(lr.slope / lr.stderr)

    stat = {"name": "OLS slope t", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}
    reading = ("Situation taken as regime 'unknown' with raw dip < 0 on the short side; the coin's drift is "
               "the mean of its 5-bar returns on the non-overlapping grids of all its windows; the plan's "
               "minimum of 100 grid cases is applied as a minimum count, so below it the status is 'not observable'.")

    if n_cases < 100:
        status = "not observable"
        decided = (f"Only {n_cases} grid cases with a nonzero forecast, below the plan's minimum of 100.")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and tval <= -2:
        status = "confirmed"
        decided = "The slope of excess 5-bar return on |forecast| is negative with t <= -2 (confirm rule)."
    elif slope > 0 and tval >= 2:
        status = "rejected"
        decided = "The slope of excess 5-bar return on |forecast| is positive with t >= 2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
