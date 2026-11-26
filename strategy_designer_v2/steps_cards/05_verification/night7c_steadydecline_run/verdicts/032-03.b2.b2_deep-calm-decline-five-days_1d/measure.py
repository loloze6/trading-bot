import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FALL_COL = "debug_info.components.fall28.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            vol = pd.to_numeric(df["volume"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")

            # Low-volume regime: 28-bar mean volume below the mean of the 90 bars before it.
            short_m = vol.rolling(28, min_periods=28).mean()
            long_m = vol.shift(28).rolling(90, min_periods=90).mean()
            ratio = short_m / long_m
            regime_trending = df["regime"].astype(str).eq("trending")
            # Recompute where the window holds enough bars; otherwise use the detector's own decision.
            low_vol = pd.Series(np.where(ratio.notna(), ratio < 1.0, regime_trending), index=df.index).astype(bool)

            # 28-bar fall: the component's raw value, or recomputed from closes where it is not recorded.
            if FALL_COL in df.columns:
                raw = pd.to_numeric(df[FALL_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = close / close.shift(28) - 1.0
            fall_val = raw.where(raw.notna(), recomputed)
            fallen = (fall_val < 0).fillna(False)

            active = f != 0
            situation_short = low_vol & fallen & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_short).sum())

    if n_active > 0:
        agreement = n_agree / n_active
    else:
        agreement = None
    passed = (agreement is None) or (agreement >= 0.9)

    main_name = "t of the mean across days of the |forecast|/10-weighted short-direction unusual 5-bar move"
    threshold = "confirm t >= 2 with slope > 0; reject t <= -2; at least 30 distinct case days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"distinct case days": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars inside the "
                          "low-volume regime (28-bar mean volume below the prior 90-bar mean) after a 28-bar fall.",
            "reading": "The volume regime is recomputed from volume where the window holds 118 bars, else read "
                       "from the recorded regime; the fall from fall28's raw value, else from closes.",
        }

    # ---------- 2. Criterion ----------
    # Coin's mean 5-bar return over all windows (non-overlapping grid of every window).
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(close)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    rets.append(c1 / c0 - 1.0)
        coin_mu[coin] = float(np.mean(rets)) if rets else np.nan

    case_days, case_w, case_um, case_absf = [], [], [], []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                um = -(c1 / c0 - 1.0 - mu)
                case_days.append(ts.iloc[i].floor("D"))
                case_um.append(um)
                case_absf.append(abs(fi))
                case_w.append(um * abs(fi) / 10.0)

    n_cases = len(case_um)
    if n_cases > 0:
        daily = pd.Series(case_w).groupby(pd.Series(case_days)).sum()
        n_days = int(len(daily))
    else:
        daily = pd.Series(dtype=float)
        n_days = 0

    mean_val, t_val = None, None
    if n_days >= 2:
        sd = float(daily.std(ddof=1))
        mean_val = float(daily.mean())
        t_val = float(mean_val / (sd / np.sqrt(n_days))) if sd > 0 else None
    elif n_days == 1:
        mean_val = float(daily.mean())

    slope = None
    if n_cases >= 3 and np.std(case_absf) > 0:
        slope = float(stats.linregress(np.array(case_absf), np.array(case_um)).slope)

    slope_passed = None if slope is None else bool(slope > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days ({n_days}), the plan's minimum count, so the data cannot show the idea."
    elif t_val is None:
        status = "inconclusive"
        decided = "The main-measure t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and slope is not None and slope > 0:
        status = "confirmed"
        decided = "Main-measure t >= 2 with a positive slope and at least 30 distinct case days (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "Main-measure t <= -2 with at least 30 distinct case days (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Main-measure t >= 2 but the slope is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Main-measure t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean across days", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of short-direction unusual 5-bar move on |forecast|",
            "value": slope,
            "passed": slope_passed,
        },
        "counts": {"distinct case days": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": "The coin's mean 5-bar return is taken on the non-overlapping 5-bar grid of all its windows, "
                   "the slope is unweighted over all cases, a case day is the UTC date of the case bar, and the "
                   "volume regime is recomputed from volume where a window holds 118 bars, else read from the "
                   "recorded regime.",
    }
