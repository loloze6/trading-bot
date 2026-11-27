import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret7 = close / close.shift(7) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # The raw value is the 7-day return over a positive range base: its sign is the return's sign.
            rose = raw.where(raw.notna(), ret7) > 0
            # Falling calm profile: the detector's decision, regime "unknown" (neither veto fired).
            in_profile = df["regime"].astype(str) == "unknown"
            situation = rose & in_profile
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "forecast-weighted mean 3-day excess return (forward return minus coin's mean 3-day return)"
    threshold = "confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2"
    reading = ("The falling-calm profile is read from the recorded regime ('unknown' = no veto fired) and the 7-day rise "
               "from the sign of the raw component (7-day close return where missing); all coins in the record are used; "
               "the t of the weighted mean uses per-day sums of weighted deviations (clustered standard error with G/(G-1) "
               "correction); the median split drops cases exactly at the median and compares unweighted mean excess returns.")

    if agreement is None or not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a coin that rose over 7 days "
                           "inside the falling-calm profile" if n_active > 0 else "No bar has a non-zero forecast"),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    # Coin's mean 3-day return over all windows (non-overlapping grid)
    coin_mean = {}
    grid_rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                grid_rows.append((coin, r, fc[i], ts.iloc[i]))
        coin_mean[coin] = float(np.mean(allr)) if allr else np.nan

    cases = []
    for coin, r, f, t in grid_rows:
        if np.isfinite(f) and f > 0 and np.isfinite(coin_mean[coin]) and pd.notna(t):
            cases.append((coin, r - coin_mean[coin], float(f), t.floor("D")))

    n_cases = len(cases)
    if n_cases > 0:
        ex = np.array([c[1] for c in cases])
        wf = np.array([c[2] for c in cases])
        days = pd.Series([c[3] for c in cases])
        n_days = int(days.nunique())
    else:
        n_days = 0

    counts = {"cases": int(n_cases), "days": int(n_days)}

    value = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        sw = wf.sum()
        value = float((wf * ex).sum() / sw)
        dev = pd.Series(wf * (ex - value)).groupby(days.values).sum().values
        G = len(dev)
        if G > 1:
            var = (dev ** 2).sum() / sw ** 2 * G / (G - 1)
            se = np.sqrt(var)
            tval = float(value / se) if se > 0 else None
        med = float(np.median(wf))
        hi = ex[wf > med]
        lo = ex[wf < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": value,
            "statistic": {"name": "t of weighted mean, cases of one day summed", "value": tval} if tval is not None else None,
            "threshold": threshold}
    supporting = {"name": "mean excess above median forecast minus below median", "value": sup_val, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}): the plan's minimum count is not reached."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure is positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The main measure has t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
