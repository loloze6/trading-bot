import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    MIN_CASES = 200

    # ---------- 1. Situation check: 72-bar return > 0, expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            ret72 = np.full(n, np.nan)
            if n > H:
                ret72[H:] = close[H:] / close[:-H] - 1.0
            active = np.isfinite(fc) & (fc != 0) & np.isfinite(ret72)
            n_active += int(active.sum())
            n_agree += int((active & (ret72 > 0) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("The plan's situation (72-bar return above zero, long) and the record's non-zero "
                           "forecasts disagree: fewer than 90 % of active bars are rising bars with a positive forecast"
                           if n_active > 0 else
                           "No active bars with a computable 72-bar return were found to compare with the plan's situation"),
            "reading": ("Active bars whose 72-bar return cannot be computed inside their window (the first 72 rows) "
                        "are left out of the agreement share."),
        }

    # ---------- 2. Criterion ----------
    case_fc = []
    case_fwd = []
    case_coin = []
    coin_means = {}
    for coin, wins in bars.items():
        all_fwd = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[j]) and close[i] > 0):
                    continue
                r = close[j] / close[i] - 1.0
                all_fwd.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    case_fc.append(fc[i])
                    case_fwd.append(r)
                    case_coin.append(coin)
        coin_means[coin] = float(np.mean(all_fwd)) if len(all_fwd) else np.nan

    case_fc = np.asarray(case_fc, dtype=float)
    case_fwd = np.asarray(case_fwd, dtype=float)
    means = np.asarray([coin_means[c] for c in case_coin], dtype=float)
    excess = case_fwd - means
    ok = np.isfinite(excess) & np.isfinite(case_fc)
    case_fc = case_fc[ok]
    excess = excess[ok]
    n_cases = int(len(excess))

    vals = (case_fc / 10.0) * excess
    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))

    slope = None
    if n_cases > 2 and np.std(case_fc) > 0:
        slope = float(stats.linregress(case_fc, excess).slope)
    slope_passed = None if slope is None else bool(slope > 0)

    main = {
        "name": "mean of (forecast/10) x 72-bar excess forward return on positive-forecast grid bars",
        "value": mean_val,
        "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
        "threshold": "confirm if t >= 2 with OLS slope > 0; reject if t <= -2; otherwise inconclusive",
    }
    supporting = {
        "name": "OLS slope of excess 72-bar forward return on forecast",
        "value": slope,
        "passed": slope_passed,
    }
    counts = {"positive-forecast grid cases across all coins and windows": n_cases}
    reading = ("The coin's mean 72-bar return is the mean over all non-overlapping grid returns of all its windows "
               "(not only positive-forecast bars), and the situation check leaves out bars whose 72-bar return "
               "cannot be computed inside their window.")

    if n_cases < MIN_CASES or t_val is None:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} positive-forecast grid cases ({n_cases}) across all coins and windows."
    elif t_val >= 2 and slope_passed:
        status = "confirmed"
        decided = "The main measure has t >= 2 and the OLS slope is above 0 (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2 (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the OLS slope is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
