import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    comp_col = "debug_info.components.sma_spread.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if comp_col not in df.columns or "forecast" not in df.columns:
                continue
            sub = df[["forecast", comp_col]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (sub[comp_col] < 0) & (sub["forecast"] < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-stat of slope of excess next-24-bar return on forecast (non-overlapping blocks, pooled)"
    threshold = "confirm if slope t >= 2 with in-zone falling share > 50%; reject if slope t <= -2; at least 60 in-zone blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is short SMA below long SMA (raw spread < 0) with a short position, "
                           "but fewer than 90% of the bars with a non-zero forecast are short bars with a negative spread."),
            "reading": "The situation is read as the raw component value (SMA50 - SMA200 spread) below 0, with the expected side short (forecast < 0).",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].to_numpy(dtype=float)
            fc = d["forecast"].to_numpy(dtype=float)
            n = len(d)
            starts = np.arange(0, n, H)
            starts = starts[starts + H < n]
            rets, fcs = [], []
            for t in starts:
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                rets.append(c1 / c0 - 1.0)
                fcs.append(f)
            if len(rets) == 0:
                continue
            rets = np.array(rets)
            fcs = np.array(fcs)
            drift = rets.mean()
            ok = ~np.isnan(fcs)
            xs.extend(fcs[ok].tolist())
            ys.extend((rets[ok] - drift).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)

    slope = None
    t_slope = None
    if len(x) >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    zone = x < 0
    n_zone = int(zone.sum())
    share = None
    pval = None
    sup_passed = None
    if n_zone > 0:
        k = int((y[zone] < 0).sum())
        share = float(k / n_zone)
        pval = float(stats.binomtest(k, n_zone, 0.5, alternative="greater").pvalue)
        sup_passed = bool(share > 0.5)

    if n_zone < 60:
        status = "inconclusive"
        decided = "Fewer than 60 in-zone non-overlapping blocks across the windows, so the 60-block minimum makes the result inconclusive."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t-stat cannot be computed, so the result is inconclusive."
    elif t_slope >= 2 and share is not None and share > 0.5:
        status = "confirmed"
        decided = "Slope t >= 2 with an in-zone share of falling blocks above 50% and at least 60 in-zone blocks: confirm."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2 with at least 60 in-zone blocks: reject (in-zone blocks followed by excess rises)."
    else:
        status = "inconclusive"
        if t_slope >= 2:
            decided = "Slope t >= 2 but the in-zone share of falling blocks is not above 50%, so neither confirm nor reject holds: inconclusive."
        else:
            decided = "Slope t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "in-zone share of blocks with excess 24-bar return < 0 (binomial vs 50%, one-sided p = "
                    + ("nan" if pval is None else f"{pval:.4g}") + ")",
            "value": share,
            "passed": sup_passed,
        },
        "counts": {"in-zone non-overlapping blocks": n_zone, "non-overlapping blocks": int(len(x))},
        "decided_by": decided,
        "reading": ("The window's mean 24-bar return is taken as the mean of that window's non-overlapping grid-block returns "
                    "(blocks at positions 0, 24, 48, ... with a full 24 bars ahead in the window), the slope t is the OLS slope "
                    "over its standard error, and the supporting check passes when the share is above 50%."),
    }
