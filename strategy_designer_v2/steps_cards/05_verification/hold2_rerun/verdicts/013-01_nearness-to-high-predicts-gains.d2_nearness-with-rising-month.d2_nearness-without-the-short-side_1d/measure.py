import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RET_COL = "debug_info.components.ret30.last_history_value"

    # ---------- 1. Situation check ----------
    # The plan's situation: 30-bar return > 0. The expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RET_COL in df.columns:
                rec = pd.to_numeric(df[RET_COL], errors="coerce")
            else:
                rec = pd.Series(np.nan, index=df.index)
            # Where the component is not recorded, recompute it from the prices
            # inside the window.
            recomputed = close / close.shift(30) - 1.0
            r30 = rec.where(rec.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & (r30 > 0) & (fc > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars "
                          "with a positive 30-bar return, which is the plan's situation and side.",
            "reading": "The situation is a 30-bar return above 0 (recorded ret30, recomputed from "
                       "closes where missing), on the long side.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, fc[i], c1 / c0 - 1.0))
    grid = pd.DataFrame(rows, columns=["coin", "window", "forecast", "fwd"])

    if len(grid) == 0:
        sel = grid.copy()
        sel["excess"] = []
    else:
        coin_mean = grid.groupby("coin")["fwd"].mean()
        grid["excess"] = grid["fwd"] - grid["coin"].map(coin_mean)
        sel = grid[grid["forecast"].notna() & (grid["forecast"] > 0)].copy()

    n_cases = int(len(sel))
    main_name = "mean 7-bar forward return minus coin's grid mean, forecast > 0 grid bars, pooled"
    threshold = "confirm if t >= 2 and supporting check passes; reject if t <= -2"

    mean_ex = float(sel["excess"].mean()) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(sel["excess"].std(ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_cases)))

    # Supporting check
    sup_val = None
    sup_pass = None
    n_upper = n_lower = 0
    if n_cases > 0:
        med = float(sel["forecast"].median())
        upper = sel[sel["forecast"] > med]["excess"]
        lower = sel[sel["forecast"] <= med]["excess"]
        n_upper, n_lower = int(len(upper)), int(len(lower))
        if n_upper > 0 and n_lower > 0:
            sup_val = float(upper.mean() - lower.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {
        "independent forecast > 0 cases": n_cases,
        "upper half cases": n_upper,
        "lower half cases": n_lower,
    }
    reading = ("Grid bars are positions 0, 7, 14, ... of each window with a 7-bar forward return "
               "inside the window; the coin mean is over all such grid bars of all windows; the "
               "median split puts forecast > median in the upper half and forecast <= median in the "
               "lower half; the 100-case minimum is applied as 'not observable'.")

    main = {
        "name": main_name,
        "value": mean_ex,
        "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
        "threshold": threshold,
    }
    supporting = {
        "name": "upper-half minus lower-half mean excess return (median forecast split)",
        "value": sup_val,
        "passed": sup_pass,
    }
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} independent forecast > 0 cases, fewer than the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the supporting check passes."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
