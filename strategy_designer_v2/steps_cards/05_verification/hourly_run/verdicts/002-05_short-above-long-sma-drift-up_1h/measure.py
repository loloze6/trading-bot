import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. situation check: SMA50 above SMA200 (raw spread > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (d[RAW] > 0) & (d["forecast"] > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled excess 24-bar forward return in zone (forecast > 0) over the window's all-block mean"
    threshold = ("confirm: excess > 0 with t >= 2 and >= 4 of 6 windows positive; "
                 "reject: excess < 0 with t <= -2; at least 150 in-zone blocks")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is SMA50 above SMA200 (raw spread > 0) on the long side, "
                           "but fewer than 90% of bars with a non-zero forecast are such bars with a positive forecast."),
            "reading": ("The raw sma_cross last_history_value is read as the SMA50-SMA200 spread, "
                        "so the situation is that value > 0 with forecast > 0."),
        }

    # ---------- 2. criterion ----------
    excess_all = []
    in_pos = []
    all_pos = []
    window_excess = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            n = len(d)
            grid = np.arange(0, n, H)
            rets, fcs = [], []
            for i in grid:
                if i + H >= n:
                    continue
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                rets.append(c1 / c0 - 1.0)
                fcs.append(f)
            if len(rets) == 0:
                continue
            rets = np.array(rets)
            fcs = np.array(fcs)
            base = rets.mean()
            all_pos.extend((rets > 0).tolist())
            mask = np.isfinite(fcs) & (fcs > 0)
            if mask.sum() == 0:
                continue
            ex = rets[mask] - base
            excess_all.extend(ex.tolist())
            in_pos.extend((rets[mask] > 0).tolist())
            window_excess[f"{coin}:{w}"] = float(ex.mean())

    n_blocks = len(excess_all)
    ex = np.array(excess_all, dtype=float)
    if n_blocks >= 2 and np.std(ex, ddof=1) > 0:
        mean_ex = float(ex.mean())
        t = float(mean_ex / (np.std(ex, ddof=1) / np.sqrt(n_blocks)))
    elif n_blocks >= 1:
        mean_ex, t = float(ex.mean()), None
    else:
        mean_ex, t = None, None

    n_win_pos = int(sum(1 for v in window_excess.values() if v > 0))

    if len(in_pos) > 0 and len(all_pos) > 0:
        sup_val = float(np.mean(in_pos) - np.mean(all_pos))
        sup_pass = bool(sup_val >= 0)
    else:
        sup_val, sup_pass = None, None

    if n_blocks < 150 or t is None or mean_ex is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 150 non-overlapping in-zone 24-bar blocks pooled (or no usable t)."
    elif mean_ex > 0 and t >= 2:
        if n_win_pos >= 4:
            status = "confirmed"
            decided = "Confirm: pooled excess is positive with t >= 2 and at least 4 of the 6 windows have a positive excess."
        else:
            status = "inconclusive"
            decided = "Inconclusive: confirming t but fewer than 4 of the 6 windows have a positive excess."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: pooled excess is negative with t <= -2, the drift reverses."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies strictly between -2 and +2 (or sign and t disagree)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean of pooled per-block excess", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of positive in-zone blocks minus share over all blocks (>= 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping in-zone 24-bar blocks pooled": int(n_blocks),
            "windows with positive excess": n_win_pos,
            "windows with in-zone blocks": int(len(window_excess)),
        },
        "decided_by": decided,
        "reading": ("Blocks start at positions 0, 24, 48, ... of each window and are in-zone when forecast > 0 at "
                    "the block start; each in-zone return is reduced by the mean of all blocks of its window, and the "
                    "pooled excesses are tested with the ordinary t of the mean; a window counts as positive if its "
                    "mean excess is > 0; the supporting check passes at a difference >= 0 and does not decide the status."),
    }
