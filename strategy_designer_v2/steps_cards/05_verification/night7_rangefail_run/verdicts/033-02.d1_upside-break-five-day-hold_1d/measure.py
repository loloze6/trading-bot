import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.break_dist.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            prior_max = high.shift(1).rolling(20, min_periods=20).max()
            recomputed = (close - prior_max) / prior_max * 100.0
            if LHV in df.columns:
                dist = df[LHV].astype(float).where(df[LHV].notna(), recomputed)
            else:
                dist = recomputed
            f = df["forecast"].astype(float).fillna(0.0)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & (dist > 0) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose close is above "
                           "the prior 20 bars' highest high, the plan's situation and side."),
            "reading": "none",
        }

    # ---------- 2. cases ----------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on the non-overlapping grid of all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in prepared:
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # bets: a rise of the long forecast of at least the band from its lowest level since the last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if f[i] > 0:
                    if f[i] - ref >= BAND:
                        bet[i] = True
                        ref = f[i]
                    else:
                        ref = min(ref, f[i])
                else:
                    ref = 0.0
            # one case per 5-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                rows.append({
                    "day": ts.iloc[i].floor("D"),
                    "ts": ts.iloc[i],
                    "coin": coin,
                    "forecast": float(f[i]),
                    "unusual": r - drift,
                })

    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    reading = ("A case is the first bar in each 5-bar grid cell (from each window's first row) where the long forecast "
               "rises by at least 2 points from its lowest level since the last bet, its 5-bar return needing the bar "
               "5 rows later in the same window; the day-clustered t uses per-day summed deviations with a G/(G-1) "
               "correction; the halves are the lower and upper floor(n/2) cases by forecast rank (ties by time, coin), "
               "the middle case left out when n is odd.")

    mean_u = None
    t_main = None
    if n_cases > 0:
        u = cases["unusual"].values
        mean_u = float(np.mean(u))
        dev = cases.assign(d=u - mean_u).groupby("day")["d"].sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_main = float(mean_u / se) if se > 0 else None

    diff = None
    welch = None
    if n_cases >= 2:
        s = cases.sort_values(["forecast", "ts", "coin"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        low = s["unusual"].values[:k]
        high = s["unusual"].values[n_cases - k:]
        diff = float(np.mean(high) - np.mean(low))
        if k >= 2:
            tt = stats.ttest_ind(high, low, equal_var=False)
            welch = float(tt.statistic) if np.isfinite(tt.statistic) else None

    sup_passed = None if diff is None else bool(diff > 0)

    main = {
        "name": "mean unusual 5-bar move of long cases",
        "value": mean_u,
        "statistic": {"name": "day-clustered t", "value": t_main} if t_main is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 on at least 30 case-days; reject: t <= -2 on at least 30 case-days",
    }
    sup = {"name": "larger-half minus smaller-half mean unusual move (by forecast)",
           "value": diff, "passed": sup_passed}
    counts = {"case-days": n_days, "cases": n_cases}

    def out(status, decided):
        return {
            "status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": sup,
            "counts": counts,
            "decided_by": decided,
            "reading": reading,
        }

    if n_days < 30 or t_main is None:
        return out("not observable", f"Fewer than 30 case-days ({n_days}), the plan's minimum count.")

    if t_main <= -2:
        return out("rejected", "The mean unusual move has a day-clustered t <= -2 on at least 30 case-days.")
    if welch is not None and welch <= -2:
        return out("rejected", "The larger-half minus smaller-half difference has a Welch t <= -2.")
    if mean_u > 0 and t_main >= 2 and diff is not None and diff > 0:
        return out("confirmed", "Mean unusual move above 0 with t >= 2 on at least 30 case-days, and the larger-half "
                                "minus smaller-half difference above 0.")
    if t_main >= 2:
        return out("inconclusive", "t >= 2 but the half difference is at or below 0 with its Welch t above -2.")
    return out("inconclusive", "The day-clustered t lies between -2 and 2.")
