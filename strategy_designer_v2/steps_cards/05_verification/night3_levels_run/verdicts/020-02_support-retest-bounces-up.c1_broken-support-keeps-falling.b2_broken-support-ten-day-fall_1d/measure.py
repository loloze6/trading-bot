import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.support_above.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: a confirmed past swing low sits at or above the close
    # (raw proximity value > 0). Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            situ = raw.notna() & (raw > 0)
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where a past "
                           "swing low sits at or above the close (raw component value > 0), so the config does "
                           "not trade the plan's situation on its short side."),
            "reading": "The situation is read as the recorded raw component value being > 0; missing raw values count as outside the situation.",
        }

    # ---------- 2. Criterion ----------
    # Grid: positions 0, 10, 20, ... of each window; return inside the window.
    rows = []
    drift_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n - H, H):
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                allr.append(r)
                rows.append((coin, f[i], r))
        drift_rets[coin] = float(np.mean(allr)) if allr else np.nan

    vals, falls, absf = [], [], []
    for coin, f, r in rows:
        if not np.isfinite(f) or f >= 0:
            continue
        d = drift_rets.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        adj = r - d
        vals.append(-(f / 10.0) * adj)
        falls.append(-adj)
        absf.append(abs(f))
    vals = np.asarray(vals, float)
    falls = np.asarray(falls, float)
    absf = np.asarray(absf, float)
    n_cases = int(len(vals))

    mean = float(np.mean(vals)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t = None

    diff = None
    welch_t = None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(absf))
        hi = falls[absf > med]
        lo = falls[absf <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            diff = float(np.mean(hi) - np.mean(lo))
            if n_hi > 1 and n_lo > 1:
                tt = stats.ttest_ind(hi, lo, equal_var=False)
                welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = (diff > 0) if diff is not None else None

    counts = {
        "non-overlapping grid cases with forecast below 0": n_cases,
        "larger-forecast half": n_hi,
        "smaller-forecast half": n_lo,
    }

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping grid cases with forecast below 0, fewer than the plan's minimum of 100."
    elif mean is None or t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The main mean is > 0 with t >= 2 and the larger-minus-smaller forecast half difference is > 0."
        else:
            status = "inconclusive"
            decided = "The main mean is > 0 with t >= 2 but the supporting difference is <= 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main mean is < 0 with t <= -2: the coin rises beyond its drift after these closes."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of -(forecast/10) x drift-adjusted 10-bar return on short grid bars",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "drift-adjusted 10-bar fall, larger minus smaller |forecast| half (Welch t "
                    + (f"{welch_t:.3f}" if welch_t is not None else "n/a") + ")",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The grid is positions 0,10,20,... of each window with the 10-bar return kept inside it, the "
                    "drift is each coin's mean 10-bar return on that grid over all its windows, the larger half is "
                    "|forecast| strictly above the median (ties go to the smaller half), and the plan's 100-case "
                    "minimum is applied as 'not observable'."),
    }
