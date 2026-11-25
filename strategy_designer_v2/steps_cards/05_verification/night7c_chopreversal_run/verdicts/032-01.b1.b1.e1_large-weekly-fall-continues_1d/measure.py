import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    PERIOD, VOL_PERIOD = 7, 30
    RAW = "debug_info.components.fall.last_history_value"

    def recompute_vsr(close):
        r = close.pct_change()
        ret7 = close / close.shift(PERIOD) - 1.0
        sd = r.rolling(VOL_PERIOD, min_periods=VOL_PERIOD).std(ddof=1)
        return ret7 / (sd * np.sqrt(PERIOD))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            vsr_re = recompute_vsr(close)
            if RAW in df.columns:
                vsr = pd.to_numeric(df[RAW], errors="coerce").combine_first(vsr_re)
            else:
                vsr = vsr_re
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & (vsr <= -2.0) & (fc < 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-side unusual 7-bar move per case (return minus coin's normal 7-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and deeper half beats shallower half; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Raw vsr taken from the recorded fall.last_history_value (recomputed from closes with ddof=1 where missing); "
               "a case is the first short bet (rise of |forecast| on the short side of at least 2 points from its lowest level since the last bet, reset at 0 after flat or side change) in each 7-bar grid cell from each window's first row, "
               "cases without 7 bars ahead in the window are dropped, drift is the coin's mean non-overlapping 7-bar return over all its windows, "
               "the day-clustered t uses per-day summed deviations with a G/(G-1) correction, "
               "the median split puts |forecast| above the median in the deeper half and at or below it in the shallower half, "
               "and fewer than 30 cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars (forecast != 0) are bars where the 7-day volatility-scaled return "
                           "is at or below -2 with a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, absf)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            prev_short = False
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f < 0:
                    mag = -f
                    if not prev_short:
                        ref = 0.0
                    if mag - ref >= BAND:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                    prev_short = True
                else:
                    ref = 0.0
                    prev_short = False
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not np.isfinite(drift[coin]):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                unusual = -(r - drift[coin])
                cases.append((ts.iloc[i].normalize(), unusual, abs(fc[i])))

    N = len(cases)
    vals = np.array([x[1] for x in cases], dtype=float)
    absf = np.array([x[2] for x in cases], dtype=float)
    days = [x[0] for x in cases]

    mean = float(np.mean(vals)) if N else None
    t = None
    G = len(set(days))
    if N >= 2 and G >= 2:
        dev = vals - vals.mean()
        s = pd.Series(dev).groupby(pd.Series(days)).sum().to_numpy()
        var = (G / (G - 1)) * np.sum(s ** 2) / N ** 2
        if var > 0:
            t = float(vals.mean() / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if N:
        med = np.median(absf)
        deep = vals[absf > med]
        shal = vals[absf <= med]
        if len(deep) and len(shal):
            sup_val = float(deep.mean() - shal.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": N, "days": G}

    if N < 30:
        status = "not observable"
        decided = f"Only {N} cases, fewer than the plan's minimum of 30."
    elif t is not None and mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-side unusual move above 0 with t >= 2 over at least 30 cases, and the deeper half outperforms the shallower half."
        else:
            status = "inconclusive"
            decided = "A confirming t, but the deeper half does not outperform the shallower half."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or could not be computed) over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "deeper-half minus shallower-half mean unusual move (split at median |forecast|)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
