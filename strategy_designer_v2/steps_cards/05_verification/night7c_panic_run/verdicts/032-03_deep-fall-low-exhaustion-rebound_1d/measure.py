import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    LOW_PERIOD = 30

    def _ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            unit = "ms" if v.dropna().abs().median() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
            regime = df["regime"].astype(str).reset_index(drop=True)
            prior_min = close.shift(1).rolling(LOW_PERIOD, min_periods=LOW_PERIOD).min()
            low_ok = close < prior_min
            low_known = prior_min.notna()
            # range-ratio condition (365-bar mean range) cannot be rebuilt inside ~120-bar windows:
            # taken from the detector's regime; new 30-day low rebuilt from prices where 30 prior bars exist
            in_regime = regime == "mean_reversion"
            situation = in_regime & (low_ok | ~low_known)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active == 0:
        agreement = None
        sit_passed = False
    else:
        agreement = n_agree / n_active
        sit_passed = agreement >= 0.9

    if n_active > 0 and not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 30-day "
                           "ranges are wider than the year's (detector regime) and the close is a new 30-day low."),
            "reading": ("The 365-bar range ratio cannot be recomputed inside ~120-bar windows, so it is taken from "
                        "the recorded regime; the new 30-day low is rebuilt from closes where 30 prior bars exist."),
        }

    # ---------- 2. criterion ----------
    case_u, case_f, case_day = [], [], []
    for coin, wins in bars.items():
        # normal drift: non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = _ts(df["timestamp"].reset_index(drop=True))
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((close, fc, ts, n))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc, ts, n in prepared:
            # long bets: rise of the forecast of at least the band from its lowest level since the last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet[t] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # once per 5-bar grid cell: the first bet in each cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                d = ts.iloc[t]
                if pd.isna(d):
                    continue
                case_u.append(r - drift)
                case_f.append(fc[t])
                case_day.append(d.strftime("%Y-%m-%d"))

    u = np.asarray(case_u, dtype=float)
    f = np.asarray(case_f, dtype=float)
    n_cases = int(len(u))
    n_days = int(len(set(case_day)))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        dev = pd.Series(u - mean_u).groupby(pd.Series(case_day)).sum().to_numpy()
        G = len(dev)
        if G > 1:
            se = np.sqrt(G / (G - 1) * np.sum(dev ** 2)) / n_cases
            if se > 0:
                t_val = float(mean_u / se)
    rho = None
    if n_cases > 2 and np.std(f) > 0 and np.std(u) > 0:
        rho = float(stats.spearmanr(f, u).correlation)
    sup_passed = None if rho is None else bool(rho > 0)

    reading = ("The 365-bar range ratio is taken from the recorded regime (not rebuildable in ~120-bar windows); "
               "a case is the first long bet (forecast rise >= 2 from its low since the last bet, reset at flat) in "
               "each 5-bar grid cell counted from each window's first row, needing 5 bars ahead in the window; the "
               "drift is the mean of the coin's non-overlapping 5-bar grid returns over all windows; the t clusters "
               "deviations summed per day with a G/(G-1) correction; 'at least 30 cases on distinct days' is read as "
               "at least 30 distinct case days, and fewer is reported as not observable.")

    if n_days < 30 or t_val is None:
        status = "not observable"
        decided = f"The minimum of 30 cases on distinct days is not reached ({n_days} days)."
    elif mean_u > 0 and t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 and Spearman correlation above 0: confirm rule."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the Spearman correlation is at or below 0: inconclusive rule."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: reject rule."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2: inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement),
                            "passed": bool(sit_passed)},
        "main_measure": {
            "name": "mean unusual 5-bar move of long cases",
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases grouped by day", "value": t_val},
            "threshold": "confirm: mean > 0 with t >= 2 (and correlation > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {"name": "Spearman(forecast, unusual move) > 0", "value": rho, "passed": sup_passed},
        "counts": {"cases": n_cases, "cases on distinct days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
