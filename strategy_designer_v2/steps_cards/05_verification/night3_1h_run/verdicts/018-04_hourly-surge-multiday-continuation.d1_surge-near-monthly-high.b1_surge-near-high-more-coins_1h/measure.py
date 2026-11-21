import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 120
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.surge_near_high.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret24 = close / close.shift(24) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Situation: an upside surge, i.e. raw value (24h return in usual moves x proximity weight) > 0;
            # where the raw value is missing, the positive 24h return from prices.
            sit = np.where(raw.notna(), raw > 0, ret24 > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (fc > 0) & pd.Series(sit, index=df.index).astype(bool)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
    else:
        agreement = None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 120-bar move of long cases (return minus coin's normal 120-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "Fewer than 90% of the active bars are long bars where the 24h surge is upside (raw value > 0), as the plan's situation requires.",
            "reading": "none",
        }

    # ---------- 2. Cases ----------
    cases = []  # (unusual move, forecast at signal bar)
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 120-bar returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc in prepared:
            n = len(close)
            side = 0
            low = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    side = 0
                    low = 0.0
                    continue
                s = 1 if f > 0 else -1
                mag = abs(f)
                if s != side:
                    side = s
                    low = 0.0
                bet = False
                if mag - low >= BAND:
                    bet = True
                    low = mag
                else:
                    low = min(low, mag)
                if bet and s == 1:
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            cases.append((r - drift, float(f)))

    n_cases = len(cases)
    counts = {"cases": n_cases}
    reading = ("A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet) "
               "in each 120-bar grid cell counted from each window's first row, kept only if its 120-bar return "
               "lies inside the window; the halves are the forecast-sorted lower and upper n//2 cases (middle case "
               "dropped when n is odd); the situation is a positive raw component value (upside surge).")

    if n_cases < MIN_CASES:
        mean_u = float(np.mean([c[0] for c in cases])) if n_cases > 0 else None
        tval = None
        if n_cases >= 2:
            u = np.array([c[0] for c in cases])
            sd = u.std(ddof=1)
            tval = float(u.mean() / (sd / np.sqrt(n_cases))) if sd > 0 else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": mean_u,
                             "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Fewer than 30 cases ({n_cases}) were observed, below the plan's minimum.",
            "reading": reading,
        }

    u = np.array([c[0] for c in cases], dtype=float)
    f = np.array([c[1] for c in cases], dtype=float)
    mean_u = float(u.mean())
    sd = float(u.std(ddof=1))
    tval = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    order = np.argsort(f, kind="mergesort")
    half = n_cases // 2
    lower = u[order[:half]]
    upper = u[order[n_cases - half:]]
    sup_val = float(upper.mean() - lower.mean())
    sup_pass = bool(sup_val > 0)
    counts["upper_half_cases"] = int(len(upper))
    counts["lower_half_cases"] = int(len(lower))

    if mean_u > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 over at least 30 cases and the upper-minus-lower-half check is above 0."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the upper-minus-lower-half supporting check fails."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean", "value": tval},
                         "threshold": threshold},
        "supporting_check": {"name": "upper-half minus lower-half mean unusual move (by signal forecast)",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
