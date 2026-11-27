import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    FC = "forecast"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            o = d["open"].astype(float)
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            c = d["close"].astype(float)
            f = d[FC].astype(float)
            rng = h - l
            body = (c - o).abs()
            flat = 1.0 - body / rng.replace(0.0, np.nan)
            rise5 = c / c.shift(5) - 1.0
            mean_rng = rng.rolling(20, min_periods=20).mean()
            width = rng / mean_rng.replace(0.0, np.nan)
            known = flat.notna() & rise5.notna() & width.notna()
            sit = (flat >= 0.9 - 1e-9) & (rise5 > 0) & (width > 1.0)
            active = f.notna() & (f != 0) & known
            n_active += int(active.sum())
            n_agree += int((active & sit & (f > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "mean unusual 3-bar move per case",
                "value": None,
                "statistic": None,
                "threshold": "mean > 0 with day-grouped t >= 2 to confirm; mean < 0 with t <= -2 to reject",
            },
            "supporting_check": None,
            "counts": {"cases": 0, "days": 0},
            "decided_by": (
                "Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's situation "
                "(5-day return > 0, flatness >= 0.9, range above its 20-bar mean range incl. bar t)."
            ),
            "reading": "Bars whose situation cannot be computed inside their window (first 19 bars) are left out of the agreement share.",
        }

    # ---------- 2. Normal drift per coin (non-overlapping 3-bar grid, all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: bets (forecast rises of >= band on its side), one per 3-bar grid cell ----------
    cases = []  # (unusual, forecast, day)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = d[FC].astype(float).fillna(0.0).to_numpy()
            c = d["close"].astype(float).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            side = 0
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            bet_dir = np.zeros(n)
            for i in range(n):
                fi = f[i]
                s = 1 if fi > 0 else (-1 if fi < 0 else 0)
                if s == 0:
                    side = 0
                    low = 0.0
                    continue
                mag = abs(fi)
                if s != side:
                    side = s
                    low = 0.0
                if mag - low >= BAND:
                    bet[i] = True
                    bet_dir[i] = s
                    low = mag
                else:
                    low = min(low, mag)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                un = bet_dir[i] * (r - drift[coin])
                cases.append((un, f[i], ts.iloc[i].date()))

    n_cases = len(cases)
    n_days = len(set(x[2] for x in cases))
    counts = {"cases": int(n_cases), "days": int(n_days)}

    main_name = "mean unusual 3-bar move per case (return from signal close minus coin's normal 3-bar drift)"
    thr = "confirm: mean > 0 with day-grouped t >= 2 and check passing; reject: mean < 0 with t <= -2"
    reading = (
        "Cases are the first bet in each 3-bar grid cell of a window (grid from the window's first row) with 3 bars ahead; "
        "the t uses deviations summed per UTC day; the halves are the n//2 largest and n//2 smallest forecasts at the signal bar "
        "(the middle case dropped when n is odd); situation bars not computable in-window are left out of the agreement share; "
        "the plan's 'fewer than 30 cases or 30 days' rule is reported as not observable."
    )

    mean_u = None
    t_val = None
    diff = None
    check_passed = None
    if n_cases > 0:
        x = np.array([cs[0] for cs in cases], dtype=float)
        mean_u = float(x.mean())
        dev = pd.Series(x - x.mean()).groupby([cs[2] for cs in cases]).sum().to_numpy()
        se = np.sqrt(np.sum(dev ** 2)) / n_cases
        t_val = float(mean_u / se) if se > 0 else None
        if n_cases >= 2:
            fc = np.array([cs[1] for cs in cases], dtype=float)
            order = np.argsort(fc, kind="mergesort")
            k = n_cases // 2
            low_half = x[order[:k]]
            high_half = x[order[n_cases - k:]]
            diff = float(high_half.mean() - low_half.mean())
            check_passed = bool(diff > 0)

    result = {
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases grouped by day", "value": t_val},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move, larger-forecast half minus smaller half, above 0",
            "value": diff,
            "passed": check_passed,
        },
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 30 or n_days < 30:
        result["status"] = "not observable"
        result["decided_by"] = (
            f"The plan's minimum of 30 cases on at least 30 days is not reached ({n_cases} cases on {n_days} days)."
        )
        return result

    if t_val is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t of the mean could not be computed (zero standard error), so neither rule is met."
        return result

    if mean_u > 0 and t_val >= 2:
        if check_passed:
            result["status"] = "confirmed"
            result["decided_by"] = "The mean unusual move is above 0 with t >= 2 and the larger-forecast half beats the smaller half."
        else:
            result["status"] = "inconclusive"
            result["decided_by"] = "The mean unusual move is above 0 with t >= 2 but the supporting check fails."
    elif mean_u < 0 and t_val <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "The mean unusual move is below 0 with t <= -2."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t of the mean unusual move lies between -2 and 2."
    return result
