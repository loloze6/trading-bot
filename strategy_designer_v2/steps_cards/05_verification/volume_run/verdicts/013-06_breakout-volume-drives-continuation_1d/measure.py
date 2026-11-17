import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    TOL = 1e-12

    def _sorted(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp")
        return df.reset_index(drop=True)

    # ---------- 1. Situation check ----------
    # Situation: close above every prior close in the 364-bar lookback; expected side: long.
    # Warm-up bars are not in the record and windows must not be joined, so only the
    # in-window prior closes can be checked: an active bar whose close is not above every
    # earlier close of its window cannot be a new 364-bar closing high.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df0 in wins.items():
            df = _sorted(df0)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            prior_max = pd.Series(close).shift(1).expanding(min_periods=1).max().to_numpy()
            for i in range(len(df)):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if not np.isfinite(close[i]):
                    continue
                new_high = (not np.isfinite(prior_max[i])) or (close[i] > prior_max[i] + TOL * abs(prior_max[i]))
                if new_high and regime[i] == "trending" and fc[i] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_check = ("the situation is checked as regime 'trending', forecast > 0 and a close above every "
                     "earlier close of the same window, since the 364 prior closes are not all in the record "
                     "and windows are never joined")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "high-minus-low relative-volume mean 30-bar excess return",
                "value": None,
                "statistic": None,
                "threshold": "confirm if positive with Welch t >= 2; reject if negative with Welch t <= -2",
            },
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of the active bars are long bars on a new closing high in the trending "
                           "regime, so the config does not trade the plan's breakout situation on the long side"
                           if n_active > 0 else "no active bars in the record, so the plan's situation is never traded"),
            "reading": reading_check,
        }

    # ---------- 2. Coin mean 30-bar return (non-overlapping grid, all windows together) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df0 in wins.items():
            df = _sorted(df0)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n, H):
                if p + H < n and np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    rets.append(close[p + H] / close[p] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if len(rets) > 0 else np.nan

    # ---------- 3. Cases ----------
    case_fc = []
    case_out = []
    for coin, wins in bars.items():
        cm = coin_mean.get(coin, np.nan)
        for w, df0 in wins.items():
            df = _sorted(df0)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            n = len(df)
            last_kept = None
            for i in range(n):
                if regime[i] != "trending" or not np.isfinite(fc[i]) or fc[i] <= 0:
                    continue
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0):
                    continue
                if not np.isfinite(cm):
                    continue
                if last_kept is not None and i - last_kept < H:
                    continue
                last_kept = i
                case_fc.append(fc[i])
                case_out.append(close[i + H] / close[i] - 1.0 - cm)

    case_fc = np.asarray(case_fc, dtype=float)
    case_out = np.asarray(case_out, dtype=float)
    n_total = int(len(case_fc))

    if n_total > 0:
        med = float(np.median(case_fc))
        hi = case_out[case_fc > med]
        lo = case_out[case_fc <= med]
    else:
        med = None
        hi = np.array([])
        lo = np.array([])
    n_hi, n_lo = int(len(hi)), int(len(lo))

    counts = {"kept cases in total": n_total, "high-volume group": n_hi, "low-volume group": n_lo}

    diff = float(np.mean(hi) - np.mean(lo)) if (n_hi > 0 and n_lo > 0) else None
    t = None
    if n_hi >= 2 and n_lo >= 2:
        res = stats.ttest_ind(hi, lo, equal_var=False)
        t = float(res.statistic) if np.isfinite(res.statistic) else None

    threshold = "confirm if positive with Welch t >= 2; reject if negative with Welch t <= -2; otherwise inconclusive"
    reading = (reading_check + "; the median is taken over all kept cases pooled across coins and windows, kept bars "
               "are chosen greedily in time order within each window, and the coin mean is the mean of the "
               "non-overlapping 30-bar returns at window positions 0, 30, 60, ... over all its windows.")

    if n_total < 40 or n_hi < 15 or n_lo < 15:
        status = "not observable"
        decided_by = (f"the plan's minimum counts are not reached (need at least 40 kept cases and 15 per group; "
                      f"got {n_total} total, {n_hi} high, {n_lo} low)")
    elif t is None or diff is None:
        status = "inconclusive"
        decided_by = "the Welch t could not be computed, so neither the confirm nor the reject rule is met"
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided_by = "the high-volume group minus the low-volume group is positive with Welch t >= 2"
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided_by = "the high-volume group minus the low-volume group is negative with Welch t <= -2"
    else:
        status = "inconclusive"
        decided_by = "the Welch t lies between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "high-minus-low relative-volume mean 30-bar excess return",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
