import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 50
    MIN_POS_BLOCKS = 20

    def find_raw_col(df):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        pref = "debug_info.components.ma_dist.last_history_value"
        if pref in cols:
            return pref
        return cols[0] if cols else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    raw_col_used = None
    for coin, wins in bars.items():
        for w, df in wins.items():
            col = find_raw_col(df)
            if col is None:
                continue
            raw_col_used = col
            sub = df[["forecast", col]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            ok = active & (sub[col] > 0) & (sub["forecast"] > 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation 'close above its 200-day SMA' is taken as the component's raw value "
               f"({raw_col_used}) > 0, since warm-up bars are absent and the SMA cannot be rebuilt from prices; "
               "blocks start at positions 0, 10, 20, ... of each window, a block needs close[t+10] inside the same window; "
               "the supporting check passes when the share of positive returns in forecast > 0 blocks exceeds the share over all blocks; "
               "a t-stat >= 2 without the supporting share is not a confirm and is treated as inconclusive.")

    main_name = "OLS slope (with intercept) of next-10-bar log return on forecast at block start"
    threshold = "slope t-stat >= 2 confirms (with supporting share higher), <= -2 rejects, between is inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the close sits above "
                           "its 200-day SMA, so the config does not trade the plan's situation on its long side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 <= 0 or c1 <= 0:
                    continue
                xs.append(f)
                ys.append(np.log(c1 / c0))

    x = np.array(xs)
    y = np.array(ys)
    n_blocks = int(len(x))
    n_pos = int((x > 0).sum())

    slope = None
    tstat = None
    if n_blocks >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr > 0 else None

    share_all = float((y > 0).mean()) if n_blocks > 0 else None
    share_pos = float((y[x > 0] > 0).mean()) if n_pos > 0 else None
    if share_all is not None and share_pos is not None:
        sup_value = share_pos - share_all
        sup_passed = bool(share_pos > share_all)
    else:
        sup_value = None
        sup_passed = None

    if n_blocks < MIN_BLOCKS or n_pos < MIN_POS_BLOCKS:
        status = "inconclusive"
        decided = (f"Inconclusive: the plan needs at least {MIN_BLOCKS} non-overlapping blocks and {MIN_POS_BLOCKS} "
                   f"starting with forecast > 0; the record has {n_blocks} and {n_pos}.")
    elif tstat is None:
        status = "inconclusive"
        decided = "Inconclusive: the slope t-stat cannot be computed (no variation in the forecast at block starts)."
    elif tstat >= 2 and sup_passed:
        status = "confirmed"
        decided = ("Confirm: slope t-stat >= 2 and the share of positive 10-bar returns is higher in forecast > 0 "
                   "blocks than in all blocks.")
    elif tstat <= -2:
        status = "rejected"
        decided = "Reject: slope t-stat <= -2, moves above the average reverse."
    elif tstat >= 2:
        status = "inconclusive"
        decided = ("Inconclusive: slope t-stat >= 2 but the supporting share is not higher in forecast > 0 blocks, "
                   "so the confirm rule is not met.")
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope t-stat lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t-stat", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of positive 10-bar returns in forecast > 0 blocks minus share over all blocks",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping blocks": n_blocks,
            "blocks starting with forecast > 0": n_pos,
        },
        "decided_by": decided,
        "reading": reading,
    }
