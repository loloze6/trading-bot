import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    BAND = 2.0
    MIN_CASES = 100
    MIN_DAYS = 60
    W_COL = "debug_info.components.width.last_history_value"

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + cases ----------
    n_active = 0
    n_agree = 0
    n_fallback = 0
    cases = []  # (day, excess_short, abs_forecast)

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0).values
            regime = d["regime"].astype(str).values if "regime" in d else np.array([""] * len(d))

            up = (close / close.shift(1) - 1.0).values
            trend = ((close / close.shift(60) - 1.0) * 100.0).values
            rng = high - low
            width_re = (rng / rng.rolling(20, min_periods=20).mean()).values
            if W_COL in d.columns:
                wraw = d[W_COL].astype(float).values
                width = np.where(np.isfinite(wraw), wraw, width_re)
            else:
                width = width_re

            # situation check on active bars
            for i in range(len(d)):
                f = fc[i]
                if f == 0 or not np.isfinite(f):
                    continue
                n_active += 1
                if np.isfinite(up[i]) and np.isfinite(trend[i]) and np.isfinite(width[i]):
                    sit = (up[i] > 0) and (width[i] > 1.0) and (trend[i] < -10.0)
                else:
                    # history before the window's first bars is not recorded: use the detector's decision
                    n_fallback += 1
                    sit = regime[i] == "mean_reversion"
                if sit and f < 0:
                    n_agree += 1

            # cases: short bets (rise of the short forecast of at least the band)
            ref = 0.0
            c = close.values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(len(d)):
                f = fc[i]
                if not (f < 0):
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND:
                    ref = m
                    if i + 1 < len(d) and np.isfinite(c[i]) and np.isfinite(c[i + 1]) and np.isfinite(mu):
                        r = c[i + 1] / c[i] - 1.0
                        x = -(r - mu)
                        cases.append((ts.iloc[i].normalize(), float(x), abs(float(f))))
                else:
                    ref = min(ref, m)

    agreement = float(n_agree / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean next-day excess return in the short direction over short bets"
    main_thr = "confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases"
    reading = ("Profile trend recomputed as the 60-bar % price change (veto at >= -10) and up day as close > previous close, "
               "falling back to the recorded regime where a window's own bars cannot give them; cases are short-side forecast "
               "rises of >= 2 points from the lowest short level since the last bet; day-clustered t without small-sample "
               "correction; halves split at n//2 after sorting by |forecast|; both 100 cases and 60 distinct days taken as minimum counts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short forecasts on falling-market "
                           "(60-bar change < -10%) up days with a range above its 20-day mean."),
            "reading": reading,
        }

    n = len(cases)
    days = sorted(set(cs[0] for cs in cases))
    n_days = len(days)
    counts = {"cases": int(n), "distinct days": int(n_days)}

    mean = None
    t = None
    if n > 0:
        x = np.array([cs[1] for cs in cases])
        mean = float(np.mean(x))
        dev = pd.Series(x - mean, index=[cs[0] for cs in cases])
        per_day = dev.groupby(level=0).sum().values
        se = np.sqrt(np.sum(per_day ** 2)) / n
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 4:
        arr = sorted(cases, key=lambda z: z[2])
        h = n // 2
        small = np.array([z[1] for z in arr[:h]])
        large = np.array([z[1] for z in arr[h:]])
        if len(small) > 1 and len(large) > 1:
            tt = stats.ttest_ind(large, small, equal_var=False)
            if np.isfinite(tt.statistic):
                sup_val = float(tt.statistic)
                sup_pass = bool(sup_val >= 1.0)

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None,
            "threshold": main_thr}
    sup = {"name": "Welch t, larger-half minus smaller-half |forecast| excess return (>= 1)",
           "value": sup_val, "passed": sup_pass}

    if n < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Minimum counts not reached: {n} cases (need 100) over {n_days} distinct days (need 60)."
    elif mean is None or t is None:
        status = "inconclusive"
        decided = "The main t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-direction excess return > 0 with t >= 2 over at least 100 cases, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The main t is >= 2 but the supporting check fails."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return < 0 with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
