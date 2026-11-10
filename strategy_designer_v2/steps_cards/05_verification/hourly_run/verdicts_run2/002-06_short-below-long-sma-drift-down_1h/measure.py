import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    raw_col = "debug_info.components.sma_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: short SMA below long SMA, so the raw SMA50-SMA200 spread is < 0.
    # Expected side: short, because the outcome is a fall.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", raw_col]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (d[raw_col] < 0) & (d["forecast"] < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-stat of slope of next-24-bar excess return on forecast at block start"
    thr = "Confirm if slope t >= 2 with in-zone falling share > 50%; reject if slope t <= -2; at least 60 in-zone blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars where the "
                          "raw SMA50-SMA200 spread is below 0, so the config does not trade the plan's "
                          "situation (short SMA below long SMA) on the short side.",
            "reading": "Situation taken as raw sma_spread last_history_value < 0, with an expected forecast < 0.",
        }

    # ---------- 2. Criterion ----------
    h = 24
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            rets, fcs = [], []
            for t in range(0, n - h, h):
                c0, c1, f = close[t], close[t + h], fc[t]
                if np.isnan(c0) or np.isnan(c1) or np.isnan(f) or c0 == 0:
                    continue
                rets.append(c1 / c0 - 1.0)
                fcs.append(f)
            if len(rets) == 0:
                continue
            rets = np.array(rets)
            drift = rets.mean()
            ys.extend(list(rets - drift))
            xs.extend(fcs)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_blocks = int(len(x))

    slope = None
    t_stat = None
    if n_blocks >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_stat = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    inz = x < 0
    n_inzone = int(inz.sum())
    share = None
    pval = None
    if n_inzone > 0:
        k = int((y[inz] < 0).sum())
        share = float(k / n_inzone)
        pval = float(stats.binomtest(k, n_inzone, 0.5).pvalue)
    sup_passed = None if share is None else bool(share > 0.5)

    if n_inzone < 60 or t_stat is None:
        status = "inconclusive"
        decided = (f"Fewer than 60 in-zone non-overlapping blocks ({n_inzone}), or the slope t is undefined, "
                   "so the result is inconclusive.")
    elif t_stat >= 2 and share is not None and share > 0.5:
        status = "confirmed"
        decided = "Slope t >= 2 with an in-zone share of falling blocks above 50%, and at least 60 in-zone blocks."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Slope t <= -2: in-zone blocks are followed by excess rises (reversal), with at least 60 in-zone blocks."
    else:
        status = "inconclusive"
        if t_stat >= 2:
            decided = ("Slope t >= 2 but the in-zone share of falling blocks is not above 50%, so the confirm "
                       "rule is not met and the reject rule does not apply.")
        else:
            decided = "Slope t is between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_stat,
            "statistic": None if t_stat is None else {"name": "OLS slope t", "value": t_stat},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "in-zone share of blocks with excess 24-bar return < 0 (binomial vs 50%, two-sided p="
                    + ("nan" if pval is None else f"{pval:.4g}") + ")",
            "value": share,
            "passed": sup_passed,
        },
        "counts": {"in-zone non-overlapping blocks": n_inzone, "non-overlapping blocks": n_blocks},
        "decided_by": decided,
        "reading": ("Blocks start at positions 0, 24, 48, ... of each window. Each window's drift is the mean of "
                    "its own non-overlapping block returns. The slope t is from OLS with an intercept on all pooled "
                    "blocks. In-zone means forecast < 0. The supporting check passes on a share above 50%, and the "
                    "binomial test is two-sided and reported only."),
    }
