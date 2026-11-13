import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MOM_COL = "debug_info.components.mom.last_history_value"
    DIST_COL = "debug_info.components.dist.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan: close above its 200-day SMA (dist >= 0) and above its close of
    # 20 bars earlier (mom >= 0). Expected side: long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            mom = pd.to_numeric(df[MOM_COL], errors="coerce") if MOM_COL in df.columns \
                else pd.Series(np.nan, index=df.index)
            dist = pd.to_numeric(df[DIST_COL], errors="coerce") if DIST_COL in df.columns \
                else pd.Series(np.nan, index=df.index)
            have = mom.notna() & dist.notna()
            sit_comp = (mom >= 0) & (dist >= 0)
            # Fallback when a raw component value is missing: the detector's
            # label, whose rule is exactly the plan's two conditions.
            if "regime" in df.columns:
                sit_reg = df["regime"].astype(str).str.lower().eq("trending")
            else:
                sit_reg = pd.Series(False, index=df.index)
            sit = sit_comp.where(have, sit_reg)
            agree = active & sit.astype(bool) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean forward 20-bar return after forecast > 0 minus coin's mean 20-bar return"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 30 non-overlapping active cases"
    reading = ("Situation checked on the recorded raw mom/dist component values (dist >= 0 and mom >= 0, long side), "
               "falling back to regime == 'trending' where a value is missing; cases and the coin's baseline mean both use "
               "the non-overlapping grid (positions 0, 20, 40, ... of each window), the coin mean pools all its windows, "
               "the t is the ordinary t of the pooled mean excess return, the slope is OLS of excess return on forecast "
               "over active grid bars, and fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the close is at or above "
                           "its 200-day SMA and its close of 20 bars earlier, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess_list = []
    fc_list = []
    for coin, wins in bars.items():
        grid_rets = []
        grid_fc = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rets.append(c1 / c0 - 1.0)
                grid_fc.append(fc[i])
        if len(grid_rets) == 0:
            continue
        grid_rets = np.array(grid_rets)
        grid_fc = np.array(grid_fc)
        coin_mean = float(np.mean(grid_rets))
        act = np.isfinite(grid_fc) & (grid_fc > 0)
        excess_list.extend((grid_rets[act] - coin_mean).tolist())
        fc_list.extend(grid_fc[act].tolist())

    ex = np.array(excess_list, dtype=float)
    fcs = np.array(fc_list, dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    slope = None
    slope_passed = None
    if n_cases >= 3 and np.ptp(fcs) > 0:
        slope = float(stats.linregress(fcs, ex).slope)
        slope_passed = bool(slope > 0)

    counts = {"non-overlapping active 20-bar cases pooled": n_cases, "active bars": int(n_active)}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping active 20-bar cases pooled, fewer than the plan's minimum of 30."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "confirmed"
        decided = "Mean excess forward 20-bar return is above 0 with t >= 2."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess forward 20-bar return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-stat lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of forward 20-bar excess return on forecast (active, non-overlapping)",
                             "value": slope, "passed": slope_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
