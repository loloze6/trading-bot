import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 84
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            rng = (high - low) / close
            short_m = rng.rolling(6, min_periods=6).mean()
            long_m = rng.rolling(180, min_periods=180).mean()
            ratio = long_m / short_m  # MeanBarRangeRatio(long, short) < 1 <=> short range above long
            regime_px = (ratio < 1.0)
            regime_lbl = (df["regime"].astype(str) == "mean_reversion")
            regime_ok = np.where(ratio.notna().values, regime_px.values, regime_lbl.values)

            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret6 = close / close.shift(6) - 1.0
            fall_ok = np.where(raw.notna().values, raw.values < 0,
                               np.where(ret6.notna().values, ret6.values < 0, False))

            active = f != 0
            agree = active & regime_ok.astype(bool) & fall_ok.astype(bool) & (f > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90% of the active bars are long bars in a 6-bar fall while the 6-bar mean "
                           "bar range is above its 180-bar mean" if n_active > 0 else
                           "the forecast is never active, so it cannot match the plan's long-in-a-fall situation"),
            "reading": "situation = regime by price range ratio (regime label where 180 bars of range are not yet "
                       "recorded) and a negative raw 6-bar scaled return, on the long side.",
        }

    # ---------- 2. criterion ----------
    excess_all = []
    fc_all = []
    for coin, wins in bars.items():
        # normal drift: mean 84-bar return on the non-overlapping grid over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ref = 0.0
            seen_cells = set()
            for t in range(len(f)):
                ft = f[t]
                if ft <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, ft)
                if ft - ref >= BAND:
                    ref = ft
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < len(c) and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                        r = c[t + H] / c[t] - 1.0
                        excess_all.append(r - drift)
                        fc_all.append(ft)

    n = len(excess_all)
    ex = np.array(excess_all, dtype=float)
    fc = np.array(fc_all, dtype=float)
    mean_ex = float(ex.mean()) if n > 0 else None
    t_stat = None
    if n >= 2:
        sd = ex.std(ddof=1)
        t_stat = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n >= 2 and np.ptp(fc) > 0:
        slope = float(stats.linregress(fc, ex).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"fewer than {MIN_CASES} non-overlapping cases across all coins and windows ({n})."
    elif t_stat is None:
        status = "inconclusive"
        decided = "the t of the mean excess return cannot be computed, so no confirm or reject rule is met."
    elif mean_ex > 0 and t_stat >= 2 and slope_pass:
        status = "confirmed"
        decided = "mean excess return positive with t >= 2 over at least 30 cases, and the slope is positive."
    elif mean_ex > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "positive t of 2 or more but the slope is not positive."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 84-bar excess return over the coin's drift per bet",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": "positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "OLS slope of excess return on forecast at signal bar",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"non-overlapping cases": n},
        "decided_by": decided,
        "reading": "a bet is a rise of the forecast of at least 2 points from its lowest positive level since the "
                   "last bet (from 0 after a flat), the first bet in each 84-bar grid cell of a window counted from "
                   "its first row is the case, and the drift is each coin's mean 84-bar return on that grid over "
                   "all its windows.",
    }
