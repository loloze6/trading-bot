import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    PUSH = "debug_info.components.push.last_history_value"
    PROFILE = "unknown"  # the only regime with a strategy: falling calm (vetoes send other bars to chop)

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            if PUSH in df.columns:
                p = pd.to_numeric(df[PUSH], errors="coerce").values
            else:
                p = np.full(len(df), np.nan)
            active = f != 0
            situ = (reg == PROFILE) & np.isfinite(p) & (p > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())
    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    main_name = "slope of 5-day forward return minus coin mean 5-day return on raw push"
    threshold = "t of slope >= 2 (with check and >= 100 samples) confirms; <= -2 (>= 100 samples) rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of active bars are falling-calm-profile bars with a positive push and a long forecast.",
            "reading": "The falling calm profile is read from the recorded regime 'unknown' (the detector's decision), the push's sign from its raw value.",
        }

    # ---------- 2. Coin drift: mean non-overlapping 5-day return over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Samples for the slope, and cases ----------
    xs, ys, days = [], [], []
    case_vals, case_days = [], []
    for coin, wins in bars.items():
        d = drift[coin]
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            n = len(df)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            if PUSH in df.columns:
                p = pd.to_numeric(df[PUSH], errors="coerce").values
            else:
                p = np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.strftime("%Y-%m-%d").values

            # slope samples on the grid
            for i in range(0, n - H, H):
                if reg[i] != PROFILE or not np.isfinite(p[i]):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                xs.append(p[i])
                ys.append(c[i + H] / c[i] - 1.0 - d)
                days.append(day[i])

            # bets (long side): rise of forecast >= band from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            trough = 0.0
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    trough = 0.0
                    continue
                if fi - trough >= BAND:
                    bet[i] = True
                    trough = fi
                else:
                    trough = min(trough, fi)
            # one case per grid cell (first bet in the cell)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                case_vals.append(c[i + H] / c[i] - 1.0 - d)
                case_days.append(day[i])

    n_samples = len(xs)
    n_cases = len(case_vals)

    # ---------- slope with day-clustered t ----------
    slope, t_slope = None, None
    if n_samples >= 3:
        x = np.asarray(xs, float)
        y = np.asarray(ys, float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            b = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            g = pd.Series(xc * e).groupby(np.asarray(days)).sum().values
            G = len(g)
            if G > 1:
                var = (G / (G - 1)) * float(np.sum(g ** 2)) / sxx ** 2
                if var > 0:
                    slope = b
                    t_slope = b / np.sqrt(var)
            if slope is None:
                slope = b

    # ---------- supporting check ----------
    check_val = float(np.mean(case_vals)) if n_cases > 0 else None
    check_pass = (check_val > 0) if check_val is not None else None

    counts = {"non-overlapping in-profile samples": int(n_samples), "cases": int(n_cases),
              "days of samples": int(len(set(days)))}

    if n_samples < 100 or n_cases < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_samples} samples (need 100) and {n_cases} cases (need 30).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more, the mean unusual move of the cases is above 0, with at least 100 samples."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 100 samples."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if slope is None else float(slope),
            "statistic": None if t_slope is None else {"name": "t of OLS slope, day-clustered SE", "value": float(t_slope)},
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean unusual 5-day move of cases (forecast rises >= 2) above 0",
                             "value": check_val, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The falling calm profile is the recorded regime 'unknown' (detector inputs are not recorded and need "
                    "365-day history), the drift is the coin's mean non-overlapping 5-day return over all its windows, "
                    "'cases on the same day taken together' is a pooled OLS slope with day-clustered standard errors, and "
                    "cases are the first long bet per 5-bar grid cell of each window."),
    }
