import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    COMP = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            spread = pd.to_numeric(df[COMP], errors="coerce") if COMP in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & (spread < 0) & (f < 0)
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "excess forward 20-bar return while short vs all bars",
                "value": None, "statistic": None,
                "threshold": "t <= -2 with negative excess confirms; t >= +2 with positive excess rejects",
            },
            "supporting_check": None,
            "counts": {"short blocks": None, "short bars": None},
            "decided_by": ("Fewer than 90% of active bars are bars where SMA50 is below SMA200 (raw spread < 0) "
                           "with a short forecast; the standardised, clipped forecast is active outside the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    excess_blocks = []
    short_bars = 0
    slope_x = []
    slope_y = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            short_bars += int(np.sum(f < 0))

            # all-bar slope data within short bars
            m = (f < 0) & np.isfinite(fwd)
            slope_x.extend(np.abs(f[m]).tolist())
            slope_y.extend(fwd[m].tolist())

            # non-overlapping grid
            grid = np.arange(0, n, H)
            g_fwd = fwd[grid]
            g_f = f[grid]
            valid = np.isfinite(g_fwd)
            if valid.sum() == 0:
                continue
            baseline = float(np.mean(g_fwd[valid]))
            sm = valid & np.isfinite(g_f) & (g_f < 0)
            excess_blocks.extend((g_fwd[sm] - baseline).tolist())

    excess_blocks = np.array(excess_blocks, dtype=float)
    n_blocks = int(len(excess_blocks))

    mean_ex = float(np.mean(excess_blocks)) if n_blocks > 0 else None
    t_val = None
    if n_blocks >= 2:
        sd = float(np.std(excess_blocks, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_blocks)))

    slope = None
    if len(slope_x) >= 3 and np.ptp(slope_x) > 0:
        slope = float(stats.linregress(slope_x, slope_y).slope)
    share_neg = float(np.mean(excess_blocks < 0)) if n_blocks > 0 else None
    slope_ok = None if slope is None else bool(slope <= 0)

    threshold = "t <= -2 with negative excess (and slope not positive) confirms; t >= +2 with positive excess rejects; else inconclusive"

    if n_blocks < 6 or short_bars < 120:
        status = "not observable"
        decided_by = (f"Minimum not reached: {n_blocks} non-overlapping 20-bar short blocks (need 6) "
                      f"and {short_bars} short bars (need 120).")
    elif t_val is not None and mean_ex < 0 and t_val <= -2 and slope_ok is not False:
        status = "confirmed"
        decided_by = "Excess forward return while short is negative with t <= -2 and the supporting slope is not positive."
    elif t_val is not None and mean_ex > 0 and t_val >= 2:
        status = "rejected"
        decided_by = "Excess forward return while short is positive with t >= +2: price reverses after downward crosses."
    else:
        status = "inconclusive"
        if t_val is not None and t_val <= -2 and slope_ok is False:
            decided_by = "t <= -2 but the supporting slope has the opposite (positive) sign, so the confirm rule is not met."
        else:
            decided_by = "t lies between -2 and +2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "excess forward 20-bar return while short vs all bars",
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of mean excess across non-overlapping short blocks", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of fwd 20-bar return on |forecast| within short bars (share of short blocks with negative excess reported in name)",
            "value": slope,
            "passed": slope_ok,
            "share_negative_short_blocks": share_neg,
        },
        "counts": {"short blocks": n_blocks, "short bars": int(short_bars)},
        "decided_by": decided_by,
        "reading": ("Blocks are the bars at positions 0, 20, 40, ... of each window with a full 20-bar forward return, the baseline is "
                    "the mean forward return over all such grid bars of the same window, the t is the ordinary t of the mean excess "
                    "of short blocks, and the slope uses all short bars with forecast size taken as |forecast|."),
    }
