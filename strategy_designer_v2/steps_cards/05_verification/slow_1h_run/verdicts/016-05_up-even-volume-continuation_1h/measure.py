import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    FC = "forecast"

    # ---------- 1. Situation check: rise regime (close above its level 72 bars ago), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = df[FC].astype(float).values
            past = np.full(len(close), np.nan)
            if len(close) > H:
                past[H:] = close[:-H]
            rise = close / past - 1.0
            computable = ~np.isnan(rise) & ~np.isnan(fc)
            active = computable & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (rise > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation check uses only bars whose 72-bar-back close lies inside the same window "
               "(the first 72 bars of each window are left out of it). Thirds are the floor(n/3) "
               "lowest and highest forecasts of the pooled grid cases (stable sort by forecast). "
               "Each coin's mean 72-bar return is the mean over its non-overlapping 72-bar grid of all windows. "
               "Trending bars are those with regime 'trending'. Fewer than 30 cases in a third is "
               "reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the close is "
                           "above its level 72 bars ago with a long (positive) forecast, as the Fidelity's "
                           "rise situation and long side require."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            grid = np.arange(0, n, H)
            for i in grid:
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                f = df[FC].iloc[i]
                reg = df["regime"].iloc[i]
                if pd.isna(f):
                    continue
                f = float(f)
                if str(reg) == "trending" and f > 0:
                    rows.append((coin, f, r))
        coin_means[coin] = float(np.mean(all_rets)) if len(all_rets) > 0 else np.nan

    data = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    if len(data) > 0:
        data["excess"] = data["ret"] - data["coin"].map(coin_means)
        data = data.dropna(subset=["excess", "forecast"])
    else:
        data = pd.DataFrame(columns=["coin", "forecast", "ret", "excess"])

    n_total = len(data)
    k = n_total // 3
    data = data.sort_values("forecast", kind="mergesort").reset_index(drop=True)
    bottom = data["excess"].values[:k].astype(float)
    top = data["excess"].values[n_total - k:].astype(float) if k > 0 else np.array([])

    counts = {
        "grid cases (trending, forecast > 0)": int(n_total),
        "top third grid cases": int(len(top)),
        "bottom third grid cases": int(len(bottom)),
    }

    mm_name = "top-third minus bottom-third mean excess 72-bar forward return (by forecast)"
    thr = "Welch t >= 2 confirms (with top-third excess > 0); Welch t <= -2 rejects"

    if len(top) < 30 or len(bottom) < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "top-third mean excess 72-bar return > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 30 independent grid cases in each of the top and bottom thirds is not reached.",
            "reading": reading,
        }

    diff = float(np.mean(top) - np.mean(bottom))
    t = stats.ttest_ind(top, bottom, equal_var=False).statistic
    t = float(t) if np.isfinite(t) else None
    top_mean = float(np.mean(top))
    sup_pass = bool(top_mean > 0)

    if t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Welch t of the top-minus-bottom difference is 2 or more and the top third's mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "Welch t of the top-minus-bottom difference is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "Welch t is 2 or more but the top third's mean excess return is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "Welch t of the top-minus-bottom difference lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": diff,
                         "statistic": {"name": "Welch t", "value": t}, "threshold": thr},
        "supporting_check": {"name": "top-third mean excess 72-bar return > 0", "value": top_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
