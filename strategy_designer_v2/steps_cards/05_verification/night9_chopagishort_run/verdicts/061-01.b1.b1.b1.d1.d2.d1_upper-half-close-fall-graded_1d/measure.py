import json
import numpy as np
import pandas as pd


def _comp_series(df, cid, field):
    """Return a float Series of a recorded component value, NaN where not recorded."""
    flat = f"debug_info.components.{cid}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(cid)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        val = float(x) if x is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 5
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: (len(s), s)):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            prepared[(coin, w)] = df
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rng = high - low
            loc = (close - low) / rng.where(rng > 0)
            ret5 = (close / close.shift(5) - 1.0) * 100.0
            rec = _comp_series(df, "fall5", "last_history_value")
            ret5 = ret5.where(ret5.notna(), rec)
            active = fc != 0
            known = loc.notna() & ret5.notna()
            use = active & known
            sit = (loc > 0.5) & (ret5 < 0)
            n_active += int(use.sum())
            n_agree += int((use & sit & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed_sit = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 5-bar move of short cases, short-signed (signal-bar return minus coin's normal 5-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; minimum 30 distinct case days"
    sup_name = "mean unusual move of larger-|forecast| half minus smaller half, > 0"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "distinct case days": None},
            "decided_by": ("fewer than 90% of the active bars are bars with close location above 0.5 and a negative "
                           "5-day return held short" if n_active > 0 else "no active bars in the record"),
            "reading": "situation recomputed from prices (5-day return from the recorded fall5 value where the window start leaves no prior closes); active bars where it cannot be computed are left out",
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin in sorted(bars):
        rets = []
        for (c, w), df in prepared.items():
            if c != coin:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    cases = []  # (day, unusual, absf)
    for (coin, w), df in prepared.items():
        close = pd.to_numeric(df["close"], errors="coerce").values
        fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
        ts = pd.to_datetime(df["timestamp"], utc=True)
        n = len(df)
        bet = np.zeros(n, dtype=bool)
        ref = 0.0
        for i in range(n):
            s = -fc[i] if fc[i] < 0 else 0.0
            if fc[i] >= 0:
                ref = 0.0
                continue
            if s - ref >= BAND:
                bet[i] = True
                ref = s
            else:
                ref = min(ref, s)
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if not idx:
                continue
            t = idx[0]
            if t + H >= n:
                continue
            a, b = close[t], close[t + H]
            if not (np.isfinite(a) and np.isfinite(b) and a > 0) or not np.isfinite(drift.get(coin, np.nan)):
                continue
            r = b / a - 1.0
            unusual = -(r - drift[coin])
            cases.append((ts.iloc[t].normalize(), unusual, abs(fc[t])))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"distinct case days": n_days, "cases": n_cases}

    mean_u = None
    tval = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases])
        mean_u = float(x.mean())
        if n_days > 1:
            dev = pd.Series(x - mean_u).groupby(pd.Series([c[0] for c in cases])).sum().values
            se = np.sqrt(n_days / (n_days - 1) * np.sum(dev ** 2)) / n_cases
            tval = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        absf = np.array([c[2] for c in cases])
        x = np.array([c[1] for c in cases])
        med = np.median(absf)
        big = x[absf > med]
        small = x[absf <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    reading = ("situation recomputed from prices (fall5's recorded value fills the 5-day return at window starts); "
               "a case is the first short bet (rise of |forecast| on the short side of >= 2 from its lowest level since the last bet, reset on flat/long) "
               "in each 5-bar grid cell from each window's first row; t clusters cases by UTC day of the signal bar; "
               "the larger half is |forecast| strictly above the median, the smaller half at or below it; "
               "the 30-day minimum, per the workflow, gives 'not observable'.")

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases summed per day", "value": tval} if tval is not None else None,
            "threshold": threshold}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sitc = {"agreement": agreement, "passed": True}

    if n_days < 30:
        return {"status": "not observable", "situation_check": sitc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"only {n_days} distinct case days, below the plan's minimum of 30.",
                "reading": reading}

    if mean_u is not None and tval is not None and mean_u > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        dec = "mean unusual move positive with t >= 2 and the larger-|forecast| half beating the smaller half: the confirm rule."
    elif mean_u is not None and tval is not None and mean_u < 0 and tval <= -2:
        status = "rejected"
        dec = "mean unusual move negative with t <= -2: the reject rule."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        dec = "t >= 2 but the supporting check failed: the inconclusive rule."
    else:
        status = "inconclusive"
        dec = "t between -2 and 2: the inconclusive rule."

    return {"status": status, "situation_check": sitc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": dec, "reading": reading}
