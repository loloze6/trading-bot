import numpy as np
import pandas as pd

RAW = "debug_info.components.res_break.last_history_value"
H = 20
BAND = 2.0
MIN_CASES = 30


def _ordered_windows(d):
    def key(w):
        s = str(w)
        digits = "".join(ch for ch in s if ch.isdigit())
        return (int(digits) if digits else 0, s)
    return sorted(d.keys(), key=key)


def _prep(df):
    df = df.copy()
    if "timestamp" in df.columns:
        df = df.sort_values("timestamp", kind="mergesort")
    return df.reset_index(drop=True)


def _bets_long(fc):
    """Long bets: rise of the forecast on the long side of at least BAND, from the lowest
    long-side level since the last bet (from 0 after a flat or a side change)."""
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            continue
        if f - ref >= BAND:
            bets[i] = True
            ref = f
        else:
            ref = min(ref, f)
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in _ordered_windows(bars[coin]):
            df = _prep(bars[coin][w])
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            situation = raw.notna() & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of mean 20-bar excess return of long cases over coin drift"
    threshold = "confirm t >= 2 over >= 30 cases with upper-minus-lower > 0; reject t <= -2 over >= 30 cases"
    reading = ("Situation bars are bars with raw res_break value > 0 (a 90-day swing-high level crossed upward) on the "
               "long side; a case is the first long bet (forecast rise >= 2 from its lowest long level since the last "
               "bet, reset at 0 at each window start and after flat) in each 20-bar grid cell of a window with a full "
               "20-bar return in that window; the median split puts forecasts strictly above the median in the upper "
               "half and the rest in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on which the close crossed "
                           "a repeatedly-touched 90-day swing-high level (raw res_break > 0), as the plan's situation requires."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    case_fc = []
    for coin in sorted(bars.keys()):
        # drift: non-overlapping 20-bar returns on grid 0,20,... of all windows
        drift_rets = []
        cases = []
        for w in _ordered_windows(bars[coin]):
            df = _prep(bars[coin][w])
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    drift_rets.append(b / a - 1.0)
            bets = _bets_long(fc)
            for start in range(0, n, H):
                end = min(start + H, n)
                idx = np.where(bets[start:end])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    cases.append((b / a - 1.0, fc[t]))
        if not cases or not drift_rets:
            continue
        drift = float(np.mean(drift_rets))
        for r, f in cases:
            excess.append(r - drift)
            case_fc.append(f)

    excess = np.asarray(excess, dtype=float)
    case_fc = np.asarray(case_fc, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    diff = None
    n_up = n_low = 0
    if n_cases > 0:
        med = float(np.median(case_fc))
        up = excess[case_fc > med]
        low = excess[case_fc <= med]
        n_up, n_low = int(len(up)), int(len(low))
        if n_up > 0 and n_low > 0:
            diff = float(np.mean(up) - np.mean(low))
    sup_pass = (diff > 0) if diff is not None else False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}): the plan's minimum count of cases is not reached."
    elif t_stat is not None and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean excess return has t >= 2 over at least 30 cases and the upper-minus-lower difference is above 0."
    elif t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided = "The mean excess return has t <= -2 over at least 30 cases."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 while the upper-minus-lower difference is not above 0."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 (or undefined) over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean excess return (median forecast split)",
            "value": diff,
            "passed": bool(sup_pass) if diff is not None else None,
        },
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_low},
        "decided_by": decided,
        "reading": reading,
    }
