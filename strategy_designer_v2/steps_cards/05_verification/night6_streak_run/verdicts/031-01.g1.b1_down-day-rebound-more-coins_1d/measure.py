import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            ret1 = close.pct_change(1)
            raw_px = ret1 / ret1.rolling(60, min_periods=60).std()
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").where(lambda s: s.notna(), raw_px)
            else:
                raw = raw_px
            f = pd.to_numeric(d["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are down days (raw scaled one-day return below 0) "
                           "with a long forecast, as the plan's situation and side require."),
            "reading": "none",
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- samples ----------
    xs, ys, days = [], [], []
    unusual = []
    for coin, wins in bars.items():
        dr = drift[coin]
        if not np.isfinite(dr):
            continue
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            # main sample: grid bars with forecast > 0
            for i in range(0, n - H, H):
                if np.isfinite(f[i]) and f[i] > 0:
                    r = c[i + H] / c[i] - 1.0
                    if np.isfinite(r):
                        xs.append(float(f[i]))
                        ys.append(r - dr)
                        days.append(ts.iloc[i].floor("D"))
            # bets (holding period) for supporting check
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_long = False
            for i in range(n):
                fi = f[i]
                if np.isfinite(fi) and fi > 0:
                    if not prev_long:
                        ref = 0.0
                    if fi - ref >= BAND:
                        bet[i] = True
                        ref = fi
                    else:
                        ref = min(ref, fi)
                    prev_long = True
                else:
                    ref = 0.0
                    prev_long = False
            for k in range(0, n, H):
                idx = np.where(bet[k:k + H])[0]
                if len(idx) == 0:
                    continue
                i = k + int(idx[0])
                if i + H < n:
                    r = c[i + H] / c[i] - 1.0
                    if np.isfinite(r):
                        unusual.append(r - dr)

    x = np.array(xs)
    y = np.array(ys)
    n_cases = int(len(x))
    n_days = int(len(set(days)))

    slope, t = None, None
    if n_cases >= 3 and np.var(x) > 0:
        xc = x - x.mean()
        sxx = float((xc ** 2).sum())
        slope = float((xc * (y - y.mean())).sum() / sxx)
        a = y.mean() - slope * x.mean()
        e = y - a - slope * x
        s = pd.Series(xc * e).groupby(pd.Series(days)).sum().values
        G = len(s)
        if G > 1:
            var = (G / (G - 1)) * float((s ** 2).sum()) / sxx ** 2
            t = float(slope / np.sqrt(var)) if var > 0 else None

    mean_unusual = float(np.mean(unusual)) if unusual else None
    sup_pass = None if mean_unusual is None else bool(mean_unusual > 0)

    counts = {"grid cases": n_cases, "distinct days": n_days, "bet cases": int(len(unusual))}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 grid cases on 50 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the mean unusual move is at or below 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 3-day return minus drift on forecast (grid bars, forecast > 0, pooled)",
            "value": slope,
            "statistic": None if t is None else {"name": "slope t clustered by day", "value": t},
            "threshold": "confirm: slope > 0 with t >= 2 (and mean unusual move > 0); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {"name": "mean unusual move of the bets, before costs", "value": mean_unusual,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The situation is a raw scaled return below 0 with a positive forecast; the drift is each coin's "
                    "mean non-overlapping 3-bar return over all its windows; the slope is OLS with intercept and its t "
                    "uses day-clustered errors with a G/(G-1) factor; the supporting check uses the first bet "
                    "(forecast rise >= 2 points) per 3-bar grid cell; the plan's 'fewer cases' rule is reported "
                    "as not observable."),
    }
