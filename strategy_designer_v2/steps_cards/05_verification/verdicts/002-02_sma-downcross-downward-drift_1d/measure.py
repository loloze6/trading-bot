import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross_down.last_history_value"
    MIN_BLOCKS = 6
    MIN_BARS = 120

    # ---------- 1. Situation check ----------
    # Situation: SMA50 below SMA200 (raw spread < 0); expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            n_agree += int((active & (d[RAW] < 0) & (d["forecast"] < 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    threshold_txt = ("confirm if excess < 0 with t <= -2 and slope not positive; "
                     "reject if excess > 0 with t >= +2; otherwise inconclusive; "
                     "inconclusive if fewer than 6 short blocks (120 short bars)")
    main_name = "excess forward 20-bar return while short (vs all-bar window mean), non-overlapping blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "active_bars_in_situation_on_side": int(n_agree)},
            "decided_by": ("The plan's situation is SMA50 below SMA200 with a short position, but fewer than 90% "
                           "of the active bars have a negative raw SMA spread and a negative forecast "
                           "(the standardised, clipped spread goes short while SMA50 is still above SMA200)."),
            "reading": "Situation taken as raw spread last_history_value < 0 with forecast < 0, over active bars with that value present.",
        }

    # ---------- 2. Criterion ----------
    excess_blocks = []
    slope_x = []
    slope_y = []
    short_bars = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float)
            fwd = close.shift(-H) / close - 1.0

            short_bars += int((fc < 0).sum())

            valid_all = fwd.notna()
            if valid_all.sum() == 0:
                continue
            base = float(fwd[valid_all].mean())

            # non-overlapping grid: positions 0, H, 2H, ...
            grid = np.arange(0, len(d), H)
            for i in grid:
                if pd.notna(fwd.iloc[i]) and pd.notna(fc.iloc[i]) and fc.iloc[i] < 0:
                    excess_blocks.append(float(fwd.iloc[i]) - base)

            # supporting slope: all short bars with a valid forward return
            m = (fc < 0) & fwd.notna()
            slope_x.extend(np.abs(fc[m]).tolist())
            slope_y.extend(fwd[m].tolist())

    n_blocks = len(excess_blocks)
    ex = np.array(excess_blocks, dtype=float)
    mean_ex = float(ex.mean()) if n_blocks > 0 else None
    if n_blocks >= 2 and ex.std(ddof=1) > 0:
        t_val = float(mean_ex / (ex.std(ddof=1) / np.sqrt(n_blocks)))
    else:
        t_val = None

    share_neg = float((ex < 0).mean()) if n_blocks > 0 else None

    slope = None
    if len(slope_x) >= 3 and np.ptp(np.array(slope_x)) > 0:
        slope = float(stats.linregress(np.array(slope_x), np.array(slope_y)).slope)
    slope_ok = None if slope is None else bool(slope <= 0)

    # decision
    if n_blocks < MIN_BLOCKS or short_bars < MIN_BARS:
        status = "inconclusive"
        decided = ("Inconclusive: fewer than 6 non-overlapping 20-bar blocks of short exposure "
                   "(or fewer than 120 short bars), whatever the t.")
    elif t_val is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic cannot be computed, so it does not reach either threshold."
    elif mean_ex < 0 and t_val <= -2:
        if slope_ok is False:
            status = "inconclusive"
            decided = ("Excess return while short is negative with t <= -2, but the supporting slope has the "
                       "opposite (positive) sign, so the confirm rule is not met.")
        else:
            status = "confirmed"
            decided = ("Confirmed: excess forward return while short is negative with t <= -2 and the "
                       "supporting slope is not of the opposite sign.")
    elif mean_ex > 0 and t_val >= 2:
        status = "rejected"
        decided = "Rejected: excess forward return while short is positive with t >= +2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean excess across short blocks", "value": t_val},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "slope of forward 20-bar return on |forecast| within short bars (should be <= 0); share of short blocks with negative excess",
            "value": slope,
            "passed": slope_ok,
            "share_negative_excess_blocks": share_neg,
        },
        "counts": {
            "short_blocks": int(n_blocks),
            "short_bars": int(short_bars),
        },
        "decided_by": decided,
        "reading": ("Each short block's excess is its forward 20-bar return (grid bars 0, 20, 40, ... of each window "
                    "with forecast < 0) minus the mean forward 20-bar return over all bars of its own window, tested "
                    "by the ordinary t of the mean. The minimum counts require both 6 short blocks and 120 short bars. "
                    "The slope regresses forward 20-bar return on |forecast| over all short bars."),
    }
