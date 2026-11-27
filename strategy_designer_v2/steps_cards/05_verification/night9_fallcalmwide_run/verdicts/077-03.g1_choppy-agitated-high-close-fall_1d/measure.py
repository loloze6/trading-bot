import numpy as np
import pandas as pd


def measure(bars):
    BAND = 2.0
    CL_MAX = 0.25

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            hi = pd.to_numeric(df["high"], errors="coerce").values
            lo = pd.to_numeric(df["low"], errors="coerce").values
            cl = pd.to_numeric(df["close"], errors="coerce").values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (hi - cl) / rng, np.nan)  # 0 at high, 1 at low
            reg = df["regime"].astype(str).str.lower().values
            profile = reg != "chop"  # vetoes (outside choppy-agitated profile) give "chop"
            situation = profile & (np.nan_to_num(loc, nan=np.inf) <= CL_MAX)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    sit = {"agreement": agreement, "passed": bool(passed)}

    main_name = "mean next-day return minus coin drift, short direction, per short bet"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting diff > 0; reject: mean < 0 with t <= -2"
    reading = ("The profile is read from the regime column (not 'chop' = inside the choppy agitated profile) and the "
               "close location recomputed from prices; a case is a bet per the workflow's holding rule (short forecast "
               "rising by >= 2 points from its lowest level since the last bet, from 0 after flat or a side change) on the "
               "1-bar grid; the day-clustered t uses a D/(D-1) correction; the median split puts |forecast| above the "
               "median in the larger half and at or below it in the smaller half; the plan's '<100 cases or <60 days' "
               "rule is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the choppy agitated "
                           "profile with a close in the top quarter of the day's range."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- 3. cases ----------
    vals, absf, days = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            dkey = ts.dt.strftime("%Y-%m-%d").values
            ref = 0.0
            n = len(df)
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi):
                    continue
                s = -fi if fi < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                bet = (s - ref) >= BAND
                if bet:
                    ref = s
                else:
                    ref = min(ref, s)
                if not bet or i + 1 >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + 1]) and c[i] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                r = c[i + 1] / c[i] - 1.0
                vals.append(-(r - d))
                absf.append(abs(fi))
                days.append(dkey[i])

    vals = np.asarray(vals, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(vals.mean()) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(vals - vals.mean()).groupby(pd.Series(days)).sum().values
        var = (dev ** 2).sum() / n_cases ** 2 * n_days / (n_days - 1)
        se = np.sqrt(var)
        tval = float(mean / se) if se > 0 else None

    diff = None
    sup_pass = None
    if n_cases >= 2:
        med = np.median(absf)
        big = vals[absf > med]
        small = vals[absf <= med]
        if len(big) and len(small):
            diff = float(big.mean() - small.mean())
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False
    supporting = {"name": "mean unusual short move, larger |forecast| half minus smaller half",
                  "value": diff, "passed": sup_pass}
    mm = {"name": main_name, "value": mean,
          "statistic": ({"name": "t of the mean, cases of one day taken together", "value": tval}
                        if tval is not None else None),
          "threshold": thr}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (minimum 100) and {n_days} distinct days (minimum 60).")
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure is positive with t >= 2 and the larger-|forecast| half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "The main measure is positive with t >= 2 but the supporting difference is not above 0."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2: the next day rises against the short beyond the drift."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
