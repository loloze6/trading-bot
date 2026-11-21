import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    RAW = "debug_info.components.grind_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret24 = close / close.shift(24) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # net 24-hour fall: the raw component is signed by the 24h net return;
            # where it is not recorded, use the prices' 24h return
            fall = pd.Series(np.where(raw.notna(), raw < 0, ret24 < 0), index=df.index)
            fall = fall & (raw.notna() | ret24.notna())
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fall.astype(bool) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of 48-bar excess forward return on forecast (non-overlapping grid, pooled)"
    main_thr = "confirm if slope t >= 2 (with >= 300 positive-forecast grid cases and supporting difference > 0); reject if slope t <= -2"
    sup_name = "grind (upper-median) minus jump (lower-median) mean excess 48-bar return among forecast > 0 grid bars"
    reading = ("Net 24-hour fall is read from the sign of the raw component (prices' 24h return where it is missing); "
               "the grid is positions 0, 48, 96, ... of each window; the coin's normal drift is the mean of its non-overlapping "
               "48-bar grid returns over all windows; the upper half is forecast > median and the lower half forecast <= median; "
               "the supporting check passes when the difference is > 0; fewer than 300 positive-forecast grid cases is 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a net 24-hour fall, "
                           "as the plan's Fidelity (long only after net 24-hour falls) requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0 if close[i] and np.isfinite(close[i]) else np.nan
                else:
                    r = np.nan
                rows.append((coin, w, fc[i], r))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "fwd"])
    g = g[np.isfinite(g["fwd"])]
    drift = g.groupby("coin")["fwd"].mean()
    g["excess"] = g["fwd"] - g["coin"].map(drift)
    g = g[np.isfinite(g["forecast"]) & np.isfinite(g["excess"])]

    n_grid = int(len(g))
    pos = g[g["forecast"] > 0]
    n_pos = int(len(pos))

    slope = None
    t_slope = None
    if n_grid >= 3 and g["forecast"].nunique() > 1:
        lr = stats.linregress(g["forecast"].values, g["excess"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = None
    t_w = None
    n_up = n_lo = 0
    if n_pos >= 2:
        med = pos["forecast"].median()
        up = pos[pos["forecast"] > med]["excess"]
        lo = pos[pos["forecast"] <= med]["excess"]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up >= 1 and n_lo >= 1:
            diff = float(up.mean() - lo.mean())
        if n_up >= 2 and n_lo >= 2:
            t_w = float(stats.ttest_ind(up.values, lo.values, equal_var=False).statistic)
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {
        "positive-forecast grid cases": n_pos,
        "grid cases": n_grid,
        "upper (grind) half cases": n_up,
        "lower (jump) half cases": n_lo,
    }

    if n_pos < 300:
        status = "not observable"
        decided = f"Only {n_pos} positive-forecast grid cases, below the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 with at least 300 positive-forecast grid cases and the grind-minus-jump difference above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the supporting check (grind minus jump difference > 0) fails."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2 with at least 300 positive-forecast grid cases."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": diff,
            "passed": sup_pass,
            "welch_t": t_w,
            "slope": slope,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
