import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RR = "debug_info.components.range_ratio.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            ret20 = np.full(n, np.nan)
            if n > 20:
                ret20[20:] = close[20:] / close[:-20] - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            rr = (pd.to_numeric(df[RR], errors="coerce").values
                  if RR in df.columns else np.full(n, np.nan))
            for i in range(n):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(ret20[i]):
                    rising = ret20[i] > 0
                else:
                    rising = reg[i] == "trending"
                ratio_ok = np.isfinite(rr[i]) and rr[i] > 0
                if rising and ratio_ok and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of pooled 10-day excess return on forecast"
    threshold = "confirm if slope t >= 2 and the check passes; reject if slope t <= -2"
    reading = ("The 20-day return is recomputed from closes inside each window, with the recorded regime "
               "used on the first 20 bars of a window where it cannot be computed; the in-regime median is "
               "the median forecast over the in-regime cases, 'above' is strictly above it and the other "
               "side is at or below it; a case needs its 10-day return inside its window; the plan's "
               "minimum counts, when not reached, give 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside a positive "
                           "20-day return with a recorded positive range ratio, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        all_r = []
        cand = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                all_r.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]) and fc[i] > 0:
                    cand.append((fc[i], r))
        if not all_r:
            continue
        mu = float(np.mean(all_r))
        for f, r in cand:
            xs.append(float(f))
            ys.append(r - mu)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))
    if n_cases > 0:
        med = float(np.median(x))
        above = x > med
        n_above = int(above.sum())
        n_below = int((~above).sum())
    else:
        med = None
        above = np.zeros(0, dtype=bool)
        n_above = n_below = 0

    counts = {"in-regime cases": n_cases,
              "cases above the median": n_above,
              "cases at or below the median": n_below}

    slope = None
    t = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(np.mean(y[above])) if n_above > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    main = {"name": main_name,
            "value": t,
            "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "mean excess 10-day return of cases above the in-regime median forecast",
               "value": sup_val, "passed": sup_pass}

    if n_cases < 100 or n_above < 30 or n_below < 30 or t is None:
        status = "not observable"
        decided = ("A minimum count is not reached: the plan needs at least 100 in-regime cases and 30 on "
                   "either side of the median (in-regime cases %d, above %d, at or below %d)."
                   % (n_cases, n_above, n_below))
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope t is 2 or more and the above-median cases' mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: the slope t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the slope t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
