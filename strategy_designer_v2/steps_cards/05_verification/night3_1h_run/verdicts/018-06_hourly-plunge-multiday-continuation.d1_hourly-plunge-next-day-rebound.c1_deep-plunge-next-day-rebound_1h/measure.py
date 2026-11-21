import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.drop_multiple.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # recompute the 24-bar return (percent) from prices where the raw value is missing
            recomputed = (close / close.shift(H) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            # situation: the coin fell over the last 24 bars (standardise keeps the sign), side long
            situ_long = (raw < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ_long).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_situ = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is read as a negative 24-bar return (a drop, which standardise expresses as a "
               "multiple of the usual daily move and the graded dead zone weights), on the long side. "
               "A bet is a rise of the forecast of at least 2 points from its lowest level since the last bet "
               "(from 0 after a flat), and the first bet in each 24-bar grid cell is the case. "
               "The coin's normal drift is the mean of its non-overlapping 24-bar returns on the grid of all its windows. "
               "The supporting check passes when the difference of means (forecast >= 10 minus < 10) is above 0, "
               "and the Welch t is reported. The plan's 30-case minimum, when not reached, gives 'not observable'.")

    if not passed_situ:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the coin fell over "
                           "the last 24 bars with a long forecast, so the config does not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret = []   # (coin, return, forecast)
    drift_samples = {}
    for coin, wins in bars.items():
        drift_samples.setdefault(coin, [])
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # normal drift samples: grid positions 0, H, 2H, ...
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    drift_samples[coin].append(c1 / c0 - 1.0)
            # bets
            trough = 0.0
            bet_bars = []
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    trough = 0.0
                    continue
                if f < trough:
                    trough = f
                if f - trough >= BAND:
                    bet_bars.append(i)
                    trough = f
            seen_cells = set()
            for i in bet_bars:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    case_ret.append((coin, c1 / c0 - 1.0, fc[i]))

    drift = {c: (float(np.mean(v)) if len(v) > 0 else np.nan) for c, v in drift_samples.items()}
    excess = []
    fcs = []
    for coin, r, f in case_ret:
        d = drift.get(coin, np.nan)
        if np.isfinite(d):
            excess.append(r - d)
            fcs.append(f)
    excess = np.array(excess, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_ex = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_ex = float(mean_ex / (sd / np.sqrt(n_cases)))

    hi = excess[fcs >= 10] if n_cases > 0 else np.array([])
    lo = excess[fcs < 10] if n_cases > 0 else np.array([])
    diff = None
    welch_t = None
    if len(hi) > 0 and len(lo) > 0:
        diff = float(np.mean(hi) - np.mean(lo))
        if len(hi) > 1 and len(lo) > 1:
            tt = stats.ttest_ind(hi, lo, equal_var=False)
            if np.isfinite(tt.statistic):
                welch_t = float(tt.statistic)
    supp_passed = None if diff is None else bool(diff > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_ex is not None and mean_ex > 0 and t_ex >= 2:
        if supp_passed:
            status = "confirmed"
            decided_by = ("The mean excess 24-bar return is positive with t >= 2 over at least 30 cases, "
                          "and the forecast>=10 minus forecast<10 difference is above 0.")
        else:
            status = "inconclusive"
            decided_by = "A confirming t with a non-positive (or undefined) supporting difference is inconclusive."
    elif t_ex is not None and mean_ex < 0 and t_ex <= -2:
        status = "rejected"
        decided_by = "The mean excess 24-bar return is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean excess 24-bar return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed_situ},
        "main_measure": {
            "name": "mean excess 24-bar return after a bet, before costs",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_ex} if t_ex is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "mean excess, forecast >= 10 minus forecast < 10 (Welch t "
                    + ("%.3f" % welch_t if welch_t is not None else "n/a") + ")",
            "value": diff,
            "passed": supp_passed,
        },
        "counts": {
            "cases": n_cases,
            "cases forecast >= 10": int(len(hi)),
            "cases forecast < 10": int(len(lo)),
        },
        "decided_by": decided_by,
        "reading": reading,
    }
