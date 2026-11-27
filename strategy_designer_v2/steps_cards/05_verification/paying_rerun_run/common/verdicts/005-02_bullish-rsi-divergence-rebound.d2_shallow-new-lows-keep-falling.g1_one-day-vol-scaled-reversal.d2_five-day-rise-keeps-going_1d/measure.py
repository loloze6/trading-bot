import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.vsr5.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # Fallback sign from prices, inside the window only.
            ret5 = close / close.shift(5) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret5)
            else:
                raw = ret5
            active = fc.notna() & (fc != 0)
            # Situation: a 5-day rise (scaled return > 0). Side: long (forecast > 0).
            situ = raw.notna() & (raw > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of the demeaned 3-bar forward return on the forecast (non-overlapping grid, pooled)"
    threshold = "confirm if slope t >= 2 with a positive supporting check; reject if slope t <= -2"
    supp_name = "mean unusual 3-bar move of grid bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a "
                           "positive vol-scaled 5-day return, as the plan's situation requires."),
            "reading": "The situation is a positive raw vol-scaled 5-bar return (recomputed from prices where the raw value is missing), on the long side.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    rows.append((coin, w, fc[i], r))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    g = g.replace([np.inf, -np.inf], np.nan)
    # Coin's normal drift: mean 3-bar return on the non-overlapping grid of all its windows.
    g = g.dropna(subset=["ret"])
    drift = g.groupby("coin")["ret"].mean()
    g["unusual"] = g["ret"] - g["coin"].map(drift)
    g = g.dropna(subset=["forecast", "unusual"])

    n_total = int(len(g))
    pos = g[g["forecast"] > 0]
    n_pos = int(len(pos))

    slope = None
    t_slope = None
    if n_total >= 3 and g["forecast"].nunique() > 1:
        lr = stats.linregress(g["forecast"].values, g["unusual"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    supp_val = float(pos["unusual"].mean()) if n_pos > 0 else None
    supp_pass = (supp_val > 0) if supp_val is not None else None

    counts = {"grid bars with forecast > 0": n_pos, "grid bars in total": n_total}

    if n_pos < 300 or n_total < 1000:
        status = "not observable"
        missing = []
        if n_pos < 300:
            missing.append(f"{n_pos} grid bars with forecast > 0 (minimum 300)")
        if n_total < 1000:
            missing.append(f"{n_total} grid bars in total (minimum 1000)")
        decided_by = "Minimum count not reached: " + " and ".join(missing) + "."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and supp_pass:
        status = "confirmed"
        decided_by = "Confirm rule met: slope t >= 2 and the mean unusual move of forecast > 0 grid bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Reject rule met: slope t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive rule met: slope t >= 2 but the supporting check is not positive."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule met: slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": supp_name, "value": supp_val,
                             "passed": (bool(supp_pass) if supp_pass is not None else None)},
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The coin's mean 3-bar return is taken on the same non-overlapping grid pooled over all its windows, "
                    "grid bars without a full 3-bar forward return in their window are dropped, the slope t is the "
                    "ordinary OLS t on the pooled grid, and the plan's 'inconclusive with too few bars' is reported "
                    "as 'not observable' as the workflow requires."),
    }
