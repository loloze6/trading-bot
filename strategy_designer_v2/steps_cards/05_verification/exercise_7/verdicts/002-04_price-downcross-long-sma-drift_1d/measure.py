import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.below_sma200.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the close is below its 200-day SMA, i.e. the raw percent distance is negative.
    # Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int((act & (d[RAW] < 0) & (d["forecast"] < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = ("Confirm if the difference is <= -2 percentage points with Welch t <= -2; "
                     "reject if the difference is >= 0")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean 20-bar forward return on short bars minus on all bars",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The bars where the forecast is active are not, for at least 90%, bars where the "
                           "close is below its 200-day SMA with a short forecast, as the plan's situation requires."),
            "reading": "Situation taken as the raw percent distance to the 200-day SMA being negative, with the side being short.",
        }

    # ---------- 2. Criterion ----------
    short_rets, short_fc, all_rets = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_rets.append(r)
                    short_fc.append(fc[t])

    short_rets = np.array(short_rets, dtype=float)
    short_fc = np.array(short_fc, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff_pp = None
    t_val = None
    hit_diff_pp = None
    tert_mean = None
    if n_short > 0 and n_all > 0:
        diff_pp = float((short_rets.mean() - all_rets.mean()) * 100.0)
        hit_short = float(np.mean(short_rets < 0))
        hit_all = float(np.mean(all_rets < 0))
        hit_diff_pp = float((hit_short - hit_all) * 100.0)
        if n_short >= 2 and n_all >= 2:
            tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
            t_val = float(tt.statistic) if np.isfinite(tt.statistic) else None
        k = int(np.ceil(n_short / 3.0))
        order = np.argsort(short_fc, kind="mergesort")  # most negative forecast first
        tert_mean = float(short_rets[order[:k]].mean())

    hit_pass = None if hit_diff_pp is None else bool(hit_diff_pp >= 10.0)

    counts = {"non-overlapping short cases": n_short,
              "non-overlapping bars (all)": n_all}

    if n_short < 15:
        status = "inconclusive"
        decided = "Fewer than 15 non-overlapping short cases pooled across windows, so the run is inconclusive whatever the numbers show."
    elif diff_pp is not None and diff_pp >= 0:
        status = "rejected"
        decided = "The difference is 0 or positive: price falls no further after short bars than after all bars."
    elif hit_diff_pp is not None and hit_diff_pp <= 0:
        status = "rejected"
        decided = "The hit rate on short bars is not above the unconditional share of negative 20-bar returns."
    elif tert_mean is not None and tert_mean > 0:
        status = "rejected"
        decided = "The mean forward return after the largest-tertile shorts is positive, indicating reversal."
    elif (diff_pp is not None and diff_pp <= -2.0 and t_val is not None and t_val <= -2.0
          and hit_diff_pp is not None and hit_diff_pp >= 10.0):
        status = "confirmed"
        decided = ("The difference is at most -2 percentage points with t at or below -2, and the short-bar hit rate "
                   "exceeds the unconditional share by at least 10 points.")
    else:
        status = "inconclusive"
        decided = "The result lies between the confirm and reject lines."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 20-bar forward return on short bars minus on all bars (pp)",
            "value": diff_pp,
            "statistic": None if t_val is None else {"name": "Welch t", "value": t_val},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "short-bar share of negative 20-bar returns minus all-bar share (pp), needs >= 10",
            "value": hit_diff_pp,
            "passed": hit_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Short bars are the 20-bar grid bars (positions 0, 20, 40, ... of each window) with forecast < 0, "
                    "compared against all grid bars; the largest-tertile shorts are the ceil(n/3) short cases with the most "
                    "negative forecast; the threshold for 'not above' in the hit rate is a difference of 0 or less; and the "
                    "minimum count is checked first, then the reject rules, then the confirm rule."),
    }
