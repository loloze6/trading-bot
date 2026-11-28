import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _clustered_t(values, days):
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        return float("nan"), 0
    m = values.mean()
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum()
    g = len(dev)
    if g < 2:
        return float("nan"), g
    var = float((dev.values ** 2).sum()) / (n ** 2) * g / (g - 1)
    if var <= 0:
        return float("nan"), g
    return float(m / np.sqrt(var)), g


def measure(bars):
    H = 5
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            for t in range(n):
                if f[t] == 0:
                    continue
                if t < 3:
                    # run of 2 down closes cannot be read from this window's prices
                    continue
                n_active += 1
                up = c[t] > c[t - 1]
                d1 = c[t - 1] < c[t - 2]
                d2 = c[t - 2] < c[t - 3]
                if up and d1 and d2 and f[t] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else float("nan")
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if np.isnan(agreement) else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": "Fewer than 90 % of the active bars are long bars on an up close breaking a run of at least 2 down closes, as the plan's situation requires (or no active bar).",
            "reading": "Active bars in the first 3 bars of a window, where the run cannot be read from the window's prices, are left out of the agreement share.",
        }

    # ---------- 2. criterion ----------
    case_ret, case_fc, case_day = [], [], []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 5-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            days = _ts(df["timestamp"]).dt.floor("D").astype(str).values
            n = len(df)
            # bets: rise of the long forecast of at least BAND from its low since last bet
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                if f[t] <= 0:
                    low = 0.0
                    continue
                if f[t] - low >= BAND:
                    bet[t] = True
                    low = f[t]
                else:
                    low = min(low, f[t])
            # one case per 5-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                case_ret.append(r - drift)
                case_fc.append(f[t])
                case_day.append(days[t])

    n_cases = len(case_ret)
    n_days = len(set(case_day))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_um = float(np.mean(case_ret)) if n_cases else None
    t_main, _ = _clustered_t(case_ret, case_day) if n_cases else (float("nan"), 0)

    diff = None
    t_diff = float("nan")
    if n_cases:
        x = np.asarray(case_ret)
        fc = np.asarray(case_fc)
        med = float(np.median(fc))
        hi = x[fc > med]
        lo = x[fc <= med]
        counts["cases above median"] = int(len(hi))
        counts["cases at or below median"] = int(len(lo))
        if len(hi) > 0 and len(lo) > 0:
            diff = float(hi.mean() - lo.mean())
        if len(hi) >= 2 and len(lo) >= 2:
            t_diff = float(stats.ttest_ind(hi, lo, equal_var=False).statistic)
    sup_passed = None if diff is None else bool(diff > 0)

    def _num(v):
        return None if v is None or (isinstance(v, float) and not np.isfinite(v)) else float(v)

    main = {
        "name": "mean unusual 5-day move of the bets",
        "value": mean_um,
        "statistic": {"name": "t clustered by day", "value": _num(t_main)},
        "threshold": "positive with t >= 2 to confirm; t <= -2 to reject",
    }
    sup = {
        "name": "unusual move above-median forecast minus at-or-below (Welch t %s)" % (
            "n/a" if not np.isfinite(t_diff) else "%.3f" % t_diff),
        "value": _num(diff),
        "passed": sup_passed,
    }
    reading = ("A case is the first bet (forecast rise of at least 2 from its low since the last bet) in each "
               "5-bar grid cell from each window's first row, the day t uses the day-clustered standard error with a "
               "G/(G-1) correction, the plan's minimum of 30 cases on 30 days gives 'not observable' when not met, "
               "and active bars in a window's first 3 bars are left out of the situation check.")

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "The plan's minimum of at least 30 cases on at least 30 distinct days is not reached."
    else:
        tm = t_main if np.isfinite(t_main) else 0.0
        td = t_diff if np.isfinite(t_diff) else 0.0
        if tm <= -2 or td <= -2:
            status = "rejected"
            decided = ("Reject: the main measure's t is -2 or less." if tm <= -2 else
                       "Reject: the larger minus smaller turning days difference has a Welch t of -2 or less.")
        elif mean_um is not None and mean_um > 0 and tm >= 2 and diff is not None and diff > 0:
            status = "confirmed"
            decided = "Confirm: the main measure is positive with a t of 2 or more and the supporting difference is positive."
        else:
            status = "inconclusive"
            decided = "Inconclusive: the numbers meet neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
