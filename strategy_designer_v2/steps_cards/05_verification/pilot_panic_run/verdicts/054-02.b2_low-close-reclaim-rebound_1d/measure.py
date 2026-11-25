import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PERIOD = 30
    BAND = 2.0
    MIN_CASES = 30

    def fnum(x):
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unchecked = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            for c in ["high", "low", "close", "forecast"]:
                d[c] = pd.to_numeric(d[c], errors="coerce")
            prior_low = d["low"].shift(1).rolling(PERIOD, min_periods=PERIOD).min()
            situation = (d["low"] < prior_low) & (prior_low < d["close"])
            fc = d["forecast"].fillna(0.0)
            active = fc != 0
            checkable = prior_low.notna() & d["low"].notna() & d["close"].notna()
            n_active_unchecked += int((active & ~checkable).sum())
            act_chk = active & checkable
            n_active += int(act_chk.sum())
            n_agree += int((act_chk & situation & (fc > 0)).sum())
            prepared[(coin, w)] = d

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation computed as low[t] < min(low[t-30..t-1]) < close[t] inside each window, active bars lacking "
               "30 prior bars in their window left out of the check; a case is the first bet (forecast rise of >= 2 "
               "points from its lowest level on its side since the last bet, from 0 after flat) in each 5-bar grid cell "
               "of a window, its return taken from that bet's close over 5 bars within the window; the coin's normal "
               "drift is the mean of its non-overlapping 5-bar grid returns over all windows; the supporting split uses "
               "forecast strictly above vs strictly below the cases' median forecast; the main t clusters cases by UTC day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": fnum(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars on situation and long": n_agree,
                       "active bars without 30-day history": n_active_unchecked},
            "decided_by": ("Fewer than 90% of active bars are bars where the day's low went under the prior 30-day low "
                           "and closed back above it with a long forecast, as the Fidelity requires."
                           if n_active > 0 else "No checkable active bars: the config never takes the plan's position."),
            "reading": reading,
        }

    # ---------- 2. Normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w in wins:
            c = prepared[(coin, w)]["close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases ----------
    cases = []
    for (coin, w), d in prepared.items():
        fc = d["forecast"].fillna(0.0).values
        c = d["close"].values
        n = len(d)
        side = 0
        low_level = 0.0
        bet_bars = []
        for t in range(n):
            f = fc[t]
            s = int(np.sign(f))
            if s == 0:
                side = 0
                low_level = 0.0
                continue
            if s != side:
                side = s
                low_level = 0.0
            mag = abs(f)
            if mag - low_level >= BAND:
                bet_bars.append((t, s, f))
                low_level = mag
            else:
                low_level = min(low_level, mag)
        seen_cells = set()
        for t, s, f in bet_bars:
            cell = t // H
            if cell in seen_cells:
                continue
            seen_cells.add(cell)
            if t + H >= n:
                continue
            if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                continue
            if not np.isfinite(drift[coin]):
                continue
            r = c[t + H] / c[t] - 1.0
            cases.append({
                "day": d["timestamp"].iloc[t].floor("D"),
                "unusual": s * (r - drift[coin]),
                "forecast": f,
            })

    cdf = pd.DataFrame(cases, columns=["day", "unusual", "forecast"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["unusual"].mean()) if n_cases else np.nan
    t_main = np.nan
    if n_cases > 1 and n_days > 1:
        e = (cdf["unusual"] - mean_u).groupby(cdf["day"]).sum().values
        se = np.sqrt(n_days / (n_days - 1) * np.sum(e ** 2)) / n_cases
        t_main = mean_u / se if se > 0 else np.nan

    diff = np.nan
    t_sup = np.nan
    n_above = n_below = 0
    if n_cases:
        med = cdf["forecast"].median()
        above = cdf.loc[cdf["forecast"] > med, "unusual"].values
        below = cdf.loc[cdf["forecast"] < med, "unusual"].values
        n_above, n_below = len(above), len(below)
        if n_above >= 1 and n_below >= 1:
            diff = float(above.mean() - below.mean())
        if n_above >= 2 and n_below >= 2:
            t_sup = float(stats.ttest_ind(above, below, equal_var=False).statistic)
    sup_passed = bool(np.isfinite(diff) and diff > 0)

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, fewer than the plan's minimum of 30."
    elif np.isfinite(t_main) and t_main <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2 (reject rule)."
    elif np.isfinite(t_main) and mean_u > 0 and t_main >= 2:
        if np.isfinite(t_sup) and t_sup <= -2:
            status = "rejected"
            decided = ("The main measure confirms but the above-median minus below-median difference has "
                       "Welch t <= -2 (reject rule).")
        elif sup_passed:
            status = "confirmed"
            decided = ("The mean unusual move is above 0 with t >= 2 and the above-median minus below-median "
                       "difference is above 0 (confirm rule).")
        else:
            status = "inconclusive"
            decided = ("The mean unusual move is above 0 with t >= 2 but the supporting difference is 0 or below "
                       "(or not measurable) with Welch t above -2 (inconclusive rule).")
    else:
        status = "inconclusive"
        decided = "The mean unusual move's t lies between -2 and 2 (or is not measurable): inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": fnum(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 5-day move (return minus coin's normal 5-day drift)",
            "value": fnum(mean_u),
            "statistic": {"name": "t of the mean, same-day cases pooled", "value": fnum(t_main)},
            "threshold": "confirm: mean > 0 with t >= 2; reject: t <= -2",
        },
        "supporting_check": {
            "name": "above-median minus below-median forecast mean unusual move (Welch t)",
            "value": fnum(diff),
            "passed": sup_passed,
            "welch_t": fnum(t_sup),
        },
        "counts": {
            "cases": n_cases,
            "days": n_days,
            "cases above median": int(n_above),
            "cases below median": int(n_below),
        },
        "decided_by": decided,
        "reading": reading,
    }
