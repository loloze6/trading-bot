import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: SMA50 below SMA200 (raw spread < 0). Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            fc = d["forecast"].astype(float).values
            raw = d[RAW].astype(float).values
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "Excess forward 20-bar return of short bars over all bars (non-overlapping 20-bar blocks)"
    threshold = ("confirm if excess < 0 with t <= -2 and the supporting slope is not positive; "
                 "reject if excess > 0 with t >= +2; otherwise inconclusive; "
                 "at least 6 short blocks (120 short bars)")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars on which the raw "
                           "SMA50-SMA200 spread is negative, so the config does not trade the plan's situation "
                           "(SMA50 below SMA200, short)."),
            "reading": "Situation taken as the raw component spread (last_history_value) below zero with forecast below zero.",
        }

    # ---------- 2. Criterion ----------
    all_rets = []
    short_rets = []
    short_sizes = []
    short_bars = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            # short bars count (all rows with negative forecast)
            short_bars += int(np.sum(np.where(np.isnan(fc), False, fc < 0)))
            for p in range(0, n, H):
                if p + H > n - 1:
                    continue
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[p]) and fc[p] < 0:
                    short_rets.append(r)
                    short_sizes.append(abs(fc[p]))

    all_rets = np.array(all_rets, dtype=float)
    short_rets = np.array(short_rets, dtype=float)
    short_sizes = np.array(short_sizes, dtype=float)
    n_short_blocks = int(len(short_rets))

    counts = {
        "non-overlapping 20-bar blocks of short exposure": n_short_blocks,
        "short bars across all windows": int(short_bars),
        "all non-overlapping 20-bar blocks": int(len(all_rets)),
    }

    diff = None
    tval = None
    if len(short_rets) >= 2 and len(all_rets) >= 2:
        diff = float(short_rets.mean() - all_rets.mean())
        t = stats.ttest_ind(short_rets, all_rets, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None
    elif len(short_rets) >= 1 and len(all_rets) >= 1:
        diff = float(short_rets.mean() - all_rets.mean())

    slope = None
    share_neg = None
    if len(short_rets) >= 1 and len(all_rets) >= 1:
        share_neg = float(np.mean((short_rets - all_rets.mean()) < 0))
    if len(short_rets) >= 2 and np.ptp(short_sizes) > 0:
        slope = float(stats.linregress(short_sizes, short_rets).slope)
    slope_ok = None if slope is None else bool(slope <= 0)

    supporting = {
        "name": "Slope of forward 20-bar return on |forecast| within short blocks (should be <= 0)",
        "value": slope,
        "passed": slope_ok,
        "share_short_blocks_negative_excess": share_neg,
    }

    reading = ("Blocks are the bars at positions 0, 20, 40, ... of each window with a full 20-bar forward return "
               "inside the window; a short block is one whose start bar has a negative forecast; the main measure is "
               "the Welch t of short-block returns minus all-block returns; the slope uses |forecast| on short blocks; "
               "the minimum is not reached if either fewer than 6 short blocks or fewer than 120 short bars.")

    if n_short_blocks < 6 or short_bars < 120:
        status = "not observable"
        decided_by = (f"Minimum count not reached: {n_short_blocks} short 20-bar blocks and {short_bars} short bars "
                      "(plan requires at least 6 blocks / 120 short bars).")
    elif tval is None or diff is None:
        status = "inconclusive"
        decided_by = "The t-statistic could not be computed, so the result meets neither the confirm nor the reject rule."
    elif diff < 0 and tval <= -2 and slope_ok is not False:
        status = "confirmed"
        decided_by = "Excess forward return while short is negative with t <= -2 and the supporting slope is not positive."
    elif diff > 0 and tval >= 2:
        status = "rejected"
        decided_by = "Excess forward return while short is positive with t >= +2 (price reverses after downward crosses)."
    else:
        status = "inconclusive"
        if diff < 0 and tval <= -2:
            decided_by = "t <= -2 but the supporting slope has the opposite (positive) sign, so the confirm rule is not met."
        else:
            decided_by = "t lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": None if tval is None else {"name": "Welch t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
