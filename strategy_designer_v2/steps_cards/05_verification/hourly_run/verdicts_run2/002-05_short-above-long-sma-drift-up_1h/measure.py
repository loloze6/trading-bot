import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check: SMA50 above SMA200 (raw spread > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            f = d["forecast"].astype(float).values
            raw = d[RAW].astype(float).values
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "pooled excess 24-bar forward return in zone over all-bar mean",
                "value": None,
                "statistic": None,
                "threshold": "positive with t >= 2 and >= 4 of 6 windows positive to confirm; negative with t <= -2 to reject",
            },
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars where SMA50 is above SMA200 "
                          "(raw spread > 0), so the config does not trade the plan's situation on its side.",
            "reading": "Situation taken as raw SMA50-SMA200 spread > 0 with forecast > 0 on bars where forecast is non-zero.",
        }

    # ---------- 2. Criterion ----------
    in_ex = []      # in-zone block returns minus window all-block mean
    all_ex = []     # all block returns minus window all-block mean
    in_pos = []     # in-zone block positive flags
    all_pos = []    # all block positive flags
    win_excess = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            idx = np.arange(0, n, H)
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            r = close[idx + H] / close[idx] - 1.0
            f = fc[idx]
            ok = np.isfinite(r)
            r_all = r[ok]
            if len(r_all) == 0:
                continue
            base = r_all.mean()
            okz = ok & np.isfinite(f) & (f > 0)
            r_in = r[okz]
            all_ex.extend((r_all - base).tolist())
            all_pos.extend((r_all > 0).tolist())
            in_ex.extend((r_in - base).tolist())
            in_pos.extend((r_in > 0).tolist())
            key = f"{coin}:{w}"
            win_excess[key] = float(r_in.mean() - base) if len(r_in) > 0 else None

    n_in = len(in_ex)
    n_all = len(all_ex)
    value = float(np.mean(in_ex)) if n_in > 0 else None
    t = None
    if n_in >= 2 and n_all >= 2:
        tt = stats.ttest_ind(np.array(in_ex), np.array(all_ex), equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    pos_windows = int(sum(1 for v in win_excess.values() if v is not None and v > 0))

    sup_val = None
    sup_pass = None
    if n_in > 0 and n_all > 0:
        sup_val = float(np.mean(in_pos) - np.mean(all_pos))
        sup_pass = bool(sup_val >= 0)

    if n_in < 150:
        status = "inconclusive"
        decided = "Fewer than 150 non-overlapping in-zone 24-bar blocks pooled, so the result is inconclusive."
    elif t is None or value is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so no confirm or reject rule is met."
    elif t >= 2 and value > 0 and pos_windows >= 4:
        status = "confirmed"
        decided = "Pooled excess forward return in the zone is positive with t >= 2 and at least 4 of the 6 windows have a positive excess."
    elif t <= -2 and value < 0:
        status = "rejected"
        decided = "Pooled excess forward return in the zone is negative with t <= -2: the drift reverses."
    elif t >= 2 and value > 0:
        status = "inconclusive"
        decided = "The t confirms but fewer than 4 of the 6 windows have a positive excess, so the result is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies strictly between -2 and +2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled excess 24-bar forward return in zone over all-bar mean",
            "value": value,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "positive with t >= 2 and >= 4 of 6 windows positive to confirm; negative with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "in-zone minus all-block share of positive 24-bar blocks",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping in-zone 24-bar blocks pooled": int(n_in),
            "all non-overlapping 24-bar blocks pooled": int(n_all),
            "windows with positive excess": pos_windows,
            "windows": int(len(win_excess)),
        },
        "decided_by": decided,
        "reading": "Blocks start at positions 0, 24, 48... of each window and are in-zone when forecast > 0 at the block start; "
                   "each block return is demeaned by its window's all-block mean, the pooled excess is the mean of in-zone "
                   "demeaned returns tested by Welch t against all demeaned blocks; a window with no in-zone blocks counts as not "
                   "positive; the supporting check passes at a difference >= 0 and does not enter the decision.",
    }
