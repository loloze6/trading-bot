import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    SLOW = "debug_info.components.slow.last_history_value"
    MED = "debug_info.components.medium.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            # Price-based returns inside the window, used only where the recorded value is missing
            r60_px = close / close.shift(60) - 1
            r20_px = close / close.shift(20) - 1
            if SLOW in df.columns:
                r60 = pd.to_numeric(df[SLOW], errors="coerce").reset_index(drop=True)
                r60 = r60.where(r60.notna(), r60_px)
            else:
                r60 = r60_px
            if MED in df.columns:
                r20 = pd.to_numeric(df[MED], errors="coerce").reset_index(drop=True)
                r20 = r20.where(r20.notna(), r20_px)
            else:
                r20 = r20_px
            situation = (r60 > 0) & (r20 > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 20-bar forward excess return (vs coin mean 20-bar return) on active bars, non-overlapping, pooled"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; inconclusive otherwise or if fewer than 30 non-overlapping active blocks"
    reading = ("The coin's mean 20-bar return is the mean of every bar's 20-bar forward return across all of that coin's windows "
               "(all bars, overlapping), and active blocks are bars with forecast > 0 on the grid 0, 20, 40, ... of each window "
               "with a complete 20-bar forward return inside the window; the t-statistic is mean / (sd / sqrt(n)) and the "
               "supporting slope is the OLS slope of excess return on forecast over those same blocks.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where both the 60-bar and the 20-bar "
                           "return are above 0, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess_list = []
    fc_list = []
    for coin, wins in bars.items():
        # coin mean 20-bar return over all windows pooled
        all_fwd = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            fwd = close.shift(-H) / close - 1
            all_fwd.append(fwd.dropna().values)
            frames.append((fwd, fc))
        if not all_fwd:
            continue
        pooled = np.concatenate(all_fwd) if len(all_fwd) else np.array([])
        if pooled.size == 0:
            continue
        coin_mean = float(np.mean(pooled))
        for fwd, fc in frames:
            idx = np.arange(0, len(fwd), H)
            f = fwd.iloc[idx]
            c = fc.iloc[idx]
            m = f.notna() & c.notna() & (c > 0)
            excess_list.extend((f[m] - coin_mean).tolist())
            fc_list.extend(c[m].tolist())

    ex = np.asarray(excess_list, dtype=float)
    fcs = np.asarray(fc_list, dtype=float)
    n_blocks = int(ex.size)
    counts = {"non-overlapping 20-bar active blocks": n_blocks}

    mean_ex = float(np.mean(ex)) if n_blocks > 0 else None
    t_val = None
    if n_blocks >= 2:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_blocks)))

    slope = None
    if n_blocks >= 3 and np.ptp(fcs) > 0:
        slope = float(stats.linregress(fcs, ex).slope)
    supporting = {
        "name": "OLS slope of 20-bar excess return on forecast level (active, non-overlapping)",
        "value": slope,
        "passed": (bool(slope > 0) if slope is not None else None),
    }

    main = {
        "name": main_name,
        "value": mean_ex,
        "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
        "threshold": threshold,
    }

    if n_blocks < 30:
        status = "not observable"
        decided = f"Only {n_blocks} non-overlapping 20-bar active blocks pooled across coins and windows, fewer than the plan's minimum of 30."
    elif t_val is not None and mean_ex > 0 and t_val >= 2:
        status = "confirmed"
        decided = "The mean 20-bar excess return on active bars is above 0 with t >= 2 (confirm rule)."
    elif t_val is not None and mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean 20-bar excess return on active bars is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the mean 20-bar excess return lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
