import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.rise_in_swings.last_history_value"
    BAND = 2.0
    H = 1
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            prev_close = np.r_[np.nan, close[:-1]]
            ret1 = close / prev_close - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            # one-day rise: the raw value's sign, or the price return where the raw value is missing
            rise = np.where(np.isfinite(raw), raw > 0, np.where(np.isfinite(ret1), ret1 > 0, False))
            # falling agitated profile = the detector's "unknown" regime (both chop vetoes not triggered)
            profile = d["regime"].astype(str).values == "unknown"
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & profile & rise & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-day unusual move of short cases (return minus coin drift, short direction)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move, larger half of |forecast| minus smaller half"

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are one-day rises in the falling agitated "
                          "profile (regime 'unknown') with a short forecast, as the plan's Fidelity requires.",
            "reading": "The falling agitated profile is read from the recorded regime ('unknown' = neither chop veto), "
                       "a one-day rise from the raw component value (or the close-to-close return where it is missing).",
        }

    # ---------- 2. criterion ----------
    vals, absf, days = [], [], []
    for coin, wins in bars.items():
        # coin's normal drift: mean 1-bar return over all its windows (grid positions 0,1,2,... per window)
        rets_all = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fwd = np.r_[close[H:] / close[:-H] - 1.0, [np.nan] * H] if len(close) > H else np.full(len(close), np.nan)
            grid = fwd[::H]
            rets_all.append(grid[np.isfinite(grid)])
            prepared.append((d, fwd))
        if not prepared:
            continue
        allr = np.concatenate(rets_all) if rets_all else np.array([])
        drift = float(np.mean(allr)) if len(allr) else np.nan
        for d, fwd in prepared:
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            ref = 0.0
            for i in range(len(d)):
                m = -fc[i] if fc[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, m)
                if m - ref >= BAND - 1e-12:
                    ref = m
                    if i % H == 0 and np.isfinite(fwd[i]) and np.isfinite(drift):
                        vals.append(-(fwd[i] - drift))
                        absf.append(abs(fc[i]))
                        days.append(ts.iloc[i].floor("D"))

    vals = np.asarray(vals, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days))) if n_cases else 0

    mean = float(np.mean(vals)) if n_cases else None
    tval = None
    if n_cases >= 2:
        dev = pd.Series(vals - mean).groupby(pd.Index(days)).sum().values
        se = np.sqrt(np.sum(dev ** 2)) / n_cases
        tval = float(mean / se) if se > 0 else None

    sup_val = None
    if n_cases >= 2:
        order = np.argsort(absf, kind="mergesort")
        k = n_cases // 2
        small = vals[order[:k]]
        large = vals[order[n_cases - k:]]
        sup_val = float(np.mean(large) - np.mean(small))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    counts = {"distinct days with cases": n_days, "cases": n_cases}

    if n_days < MIN_DAYS or tval is None:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, below the plan's minimum of {MIN_DAYS}." \
            if n_days < MIN_DAYS else "The t of the main measure could not be computed."
    elif mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: mean unusual move above 0 with t >= 2 and the supporting check above 0."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule met: mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        if mean > 0 and tval >= 2:
            decided = "Main measure meets the confirm rule but the supporting check is not above 0, so inconclusive."
        else:
            decided = "t between -2 and 2 (neither confirm nor reject rule met), so inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement),
                            "passed": bool(passed) if agreement is not None else None},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if tval is None else {"name": "t of the mean, cases of one day pooled", "value": tval},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are short-side bets (forecast deepening by >= 2 points from its least-short level since the last bet, "
                   "reset at flat), the drift is the coin's mean daily return over all its windows, the t sums deviations per UTC day, "
                   "the halves are the top and bottom floor(n/2) cases by |forecast| (middle case dropped if odd), the 30-day minimum "
                   "gives 'not observable', and the profile is the recorded regime 'unknown'.",
    }
