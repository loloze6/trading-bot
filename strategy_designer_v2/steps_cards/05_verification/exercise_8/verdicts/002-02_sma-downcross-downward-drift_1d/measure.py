import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    # The situation holds while SMA50 is below SMA200 (raw spread < 0).
    # The expected side is short, so the forecast should be negative.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "excess forward 20-bar return on short blocks vs all-bar mean"
    thr = "confirm if excess < 0 with t <= -2 (slope not positive); reject if excess > 0 with t >= +2; else inconclusive; at least 6 short blocks (120 short bars)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Active bars do not match the plan's situation: fewer than 90% of non-zero-forecast bars "
                           "have SMA50 below SMA200 with a short forecast, because the standardised spread can be "
                           "negative while SMA50 is still above SMA200." if n_active > 0 else
                           "The strategy never took a position, so no active bar matches the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    all_fwd = []
    short_fwd = []
    short_size = []
    n_short_bars = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n_short_bars += int(np.sum(fc < 0))
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_fwd.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    short_fwd.append(r)
                    short_size.append(abs(fc[i]))

    all_fwd = np.array(all_fwd, dtype=float)
    short_fwd = np.array(short_fwd, dtype=float)
    short_size = np.array(short_size, dtype=float)
    n_blocks = int(len(short_fwd))

    baseline = float(np.mean(all_fwd)) if len(all_fwd) else np.nan
    excess = short_fwd - baseline if n_blocks else np.array([])
    mean_ex = float(np.mean(excess)) if n_blocks else None
    t = None
    if n_blocks >= 2:
        sd = np.std(excess, ddof=1)
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n_blocks)))

    slope = None
    if n_blocks >= 3 and np.ptp(short_size) > 0:
        slope = float(stats.linregress(short_size, short_fwd).slope)
    share_neg = float(np.mean(excess < 0)) if n_blocks else None
    slope_ok = None if slope is None else bool(slope <= 0)

    if n_blocks < 6 or n_short_bars < 120:
        status = "inconclusive"
        decided = "Fewer than 6 non-overlapping 20-bar blocks of short exposure (120 short bars), so the run is inconclusive whatever the t."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so no confirm or reject rule is met."
    elif mean_ex < 0 and t <= -2:
        if slope_ok is False:
            status = "inconclusive"
            decided = "Excess return is negative with t <= -2, but the supporting slope has the opposite (positive) sign, so the confirm rule is not met."
        else:
            status = "confirmed"
            decided = "Excess forward return while short is negative with t <= -2 and the supporting slope is not positive."
    elif mean_ex > 0 and t >= 2:
        status = "rejected"
        decided = "Excess forward return while short is positive with t >= +2: price reverses after downward crosses."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t is None else {"name": "one-sample t of mean excess across short blocks", "value": t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "slope of forward 20-bar return on |forecast| within short blocks (should be <= 0)",
            "value": slope,
            "passed": slope_ok,
            "share_short_blocks_negative_excess": share_neg,
        },
        "counts": {
            "non-overlapping 20-bar blocks of short exposure": n_blocks,
            "short bars across all windows": int(n_short_bars),
        },
        "decided_by": decided,
        "reading": ("Blocks start at positions 0, 20, 40, ... of each window; a short block starts on a bar with a negative forecast; "
                    "the baseline is the pooled mean forward 20-bar return over all block starts of all windows; the t is the one-sample t of "
                    "the excess across short blocks; the slope uses |forecast| on short blocks; the minimum requires both 6 blocks and 120 short bars."),
    }
