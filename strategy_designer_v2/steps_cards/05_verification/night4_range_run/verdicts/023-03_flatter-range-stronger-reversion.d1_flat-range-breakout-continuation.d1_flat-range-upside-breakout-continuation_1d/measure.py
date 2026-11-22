import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.flat_range_pos.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: close above the middle of a flat 30-day closing range.
    # The raw component (2*pos-1)*(1-|net|/range) is > 0 exactly there.
    # Expected side: long, from the Fidelity outcome "a larger rise".
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if FC not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = ("pooled OLS slope of 5-day forward return minus coin mean 5-day return "
                 "on recorded forecast, non-overlapping 5-bar grid")
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("Situation taken as raw component > 0 (close above the range middle with a nonzero "
               "flatness factor, 'far above' having no stated cut-off) on the long side; the coin's mean "
               "5-day return is the mean of its non-overlapping grid returns over all windows; the slope "
               "is from OLS with an intercept; the plan's 'fewer than 200 grid cases with forecast > 0' "
               "is treated as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active),
                       "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are long bars where the close "
                           "sits above the middle of a flat 30-day range (raw component > 0)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "close" not in df.columns or FC not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i]))
    grid = pd.DataFrame(rows, columns=["coin", "ret", "fc"])

    if len(grid):
        coin_mean = grid.groupby("coin")["ret"].mean()
        grid["excess"] = grid["ret"] - grid["coin"].map(coin_mean)
        g = grid.dropna(subset=["excess", "fc"])
    else:
        g = grid.assign(excess=[])

    n_grid = int(len(g))
    n_pos = int((g["fc"] > 0).sum()) if n_grid else 0
    counts = {"grid cases with forecast > 0": n_pos, "grid cases": n_grid}

    slope = None
    tval = None
    if n_grid >= 3:
        x = g["fc"].to_numpy(dtype=float)
        y = g["excess"].to_numpy(dtype=float)
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            s2 = float(np.sum(resid ** 2) / (n_grid - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            tval = float(b / se) if se > 0 else None

    stat = {"name": "OLS slope t", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}
    sc = {"agreement": agreement, "passed": True}

    if n_pos < 200:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": None, "counts": counts,
                "decided_by": f"Only {n_pos} grid cases with forecast > 0, fewer than the plan's minimum of 200.",
                "reading": reading}

    if tval is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so no rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tval:.2f} >= 2 (confirm rule); no supporting check."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tval:.2f} <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = f"The slope's t = {tval:.2f} lies between -2 and 2 (inconclusive rule)."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": None, "counts": counts,
            "decided_by": decided, "reading": reading}
