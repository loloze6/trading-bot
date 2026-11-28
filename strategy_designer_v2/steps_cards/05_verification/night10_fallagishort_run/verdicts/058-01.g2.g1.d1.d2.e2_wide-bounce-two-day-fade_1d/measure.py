import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret1 = close / close.shift(1) - 1.0
            ret3 = close / close.shift(3) - 1.0
            active = fc != 0
            computable = ret1.notna() & ret3.notna()
            mask = active & computable
            n_active += int(mask.sum())
            situ = (ret1 > 0) & (ret3 < 0) & (fc < 0)
            n_agree += int((mask & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in the situation on the short side": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are up days (1-day return > 0) with a negative "
                           "3-day return held short, as the plan's Fidelity requires."),
            "reading": ("Situation recomputed from closes inside each window; bars whose 1- or 3-day return "
                        "cannot be computed inside the window are left out of the agreement."),
        }

    # ---------- 2. criterion ----------
    case_vals = []   # unusual move (short side)
    case_abs_fc = []
    case_days = []

    for coin, wins in bars.items():
        # normal 2-day drift of the coin over all its windows (non-overlapping grid)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for d in prepared:
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(close)
            # bets on the short side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            # one case per 2-bar grid cell
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                case_vals.append(-(r - drift))
                case_abs_fc.append(abs(fc[t]))
                case_days.append(ts.iloc[t].floor("D"))

    x = np.asarray(case_vals, dtype=float)
    n_cases = int(len(x))
    days = pd.Series(case_days) if n_cases else pd.Series([], dtype="datetime64[ns, UTC]")
    n_days = int(days.nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(np.mean(x)) if n_cases else None
    tstat = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - mean)
        sums = dev.groupby(days.values).sum().to_numpy()
        D = len(sums)
        var = (D / (D - 1)) * np.sum(sums ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        tstat = float(mean / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        a = np.asarray(case_abs_fc)
        med = np.median(a)
        up = x[a > med]
        lo = x[a <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean unusual 2-day move on the short side",
        "value": mean,
        "statistic": {"name": "t of the mean, cases of one day taken together", "value": tstat} if tstat is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2",
    }
    supporting = {"name": "mean unusual move, upper half minus lower half of |forecast|",
                  "value": sup_val, "passed": sup_pass}
    reading = ("A case is the first short bet (forecast rising in size by at least 2 points from its lowest short "
               "level since the last bet) in each 2-bar grid cell from each window's first row, its 2-bar return "
               "taken from that bar's close inside the window; the drift is the coin's mean non-overlapping 2-bar "
               "return over all its windows; the t clusters cases by UTC day of the signal bar (with D/(D-1) "
               "correction); the upper half is |forecast| strictly above the median, the lower half at or below it.")

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_cases} cases and {n_days} distinct days, "
                   f"the plan needs at least 30 of each.")
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2, and the upper half of |forecast| exceeds the lower half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the upper half of |forecast| does not exceed the lower half (inconclusive rule)."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the coin rises more than its drift after these up days."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: neither the confirm nor the reject rule is met (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
