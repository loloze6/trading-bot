import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    LOOKBACK = 6
    MIN_CASES = 300

    # ---------- 1. Situation check: 6-day return > 0, long side ----------
    n_active = 0
    n_agree = 0
    n_active_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            ret6 = np.full(n, np.nan)
            if n > LOOKBACK:
                ret6[LOOKBACK:] = close[LOOKBACK:] / close[:-LOOKBACK] - 1.0
            active = np.isfinite(fc) & (fc != 0)
            verifiable = active & np.isfinite(ret6)
            n_active_unverifiable += int((active & ~np.isfinite(ret6)).sum())
            n_active += int(verifiable.sum())
            n_agree += int((verifiable & (ret6 > 0) & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = (
        "Situation check uses close[t]/close[t-6]-1 > 0 inside each window, leaving out active bars of a window's first "
        "6 rows where it cannot be computed; regime bars are rows with regime == 'trending'; the coin's normal 3-bar "
        "drift is its mean 3-bar return over the non-overlapping grid (positions 0,3,6,...) of all its windows; the "
        "slope is OLS of drift-adjusted return on forecast with a day-clustered standard error (CR1 G/(G-1) scaling, "
        "days by UTC date); top and bottom thirds are the n//3 highest and lowest forecasts by rank (ties broken by "
        "coin, window, time); the plan's 'fewer than 300 cases' rule is reported as 'not observable'."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars without 6-bar history": n_active_unverifiable},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are bars with a positive 6-day return "
                          "and a long (positive) forecast, so the config does not follow the plan's situation and side.",
            "reading": reading,
        }

    # ---------- 2. Build grid cases ----------
    rows = []
    for coin, wins in bars.items():
        all_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = d["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_grid_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    coin_cases.append((coin, str(w), ts.iloc[i], ts.iloc[i].strftime("%Y-%m-%d"), fc[i], r))
        if len(all_grid_rets) == 0:
            continue
        drift = float(np.mean(all_grid_rets))
        for c in coin_cases:
            rows.append({"coin": c[0], "window": c[1], "ts": c[2], "day": c[3],
                         "x": float(c[4]), "y": float(c[5] - drift)})

    cases = pd.DataFrame(rows, columns=["coin", "window", "ts", "day", "x", "y"])
    N = len(cases)
    n_days = int(cases["day"].nunique()) if N else 0
    counts = {"regime grid cases": N, "days": n_days}

    main_name = "slope of drift-adjusted 3-bar forward return on forecast (regime bars, 3-bar grid)"
    threshold = "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2"

    if N < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {N} regime grid cases, fewer than the plan's minimum of 300.",
            "reading": reading,
        }

    x = cases["x"].to_numpy()
    y = cases["y"].to_numpy()
    xm, ym = x.mean(), y.mean()
    dx = x - xm
    sxx = float((dx ** 2).sum())
    if sxx <= 0:
        slope, t = None, None
    else:
        slope = float((dx * (y - ym)).sum() / sxx)
        a = ym - slope * xm
        e = y - a - slope * x
        s = pd.Series(dx * e).groupby(cases["day"].to_numpy()).sum().to_numpy()
        G = len(s)
        var = (s ** 2).sum() / sxx ** 2
        if G > 1:
            var *= G / (G - 1)
        se = np.sqrt(var)
        t = float(slope / se) if se > 0 else None

    # supporting check
    srt = cases.sort_values(["x", "coin", "window", "ts"], kind="mergesort").reset_index(drop=True)
    k = N // 3
    if k > 0:
        diff = float(srt["y"].iloc[-k:].mean() - srt["y"].iloc[:k].mean())
        check_passed = bool(diff > 0)
    else:
        diff, check_passed = None, None

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no spread of forecasts), so the result is inconclusive."
    elif slope > 0 and t >= 2:
        if check_passed:
            status = "confirmed"
            decided = "The slope is above 0 with t >= 2 and the top-minus-bottom-third check is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is above 0 with t >= 2 but the top-minus-bottom-third check is not above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "t of slope, day-clustered", "value": t} if t is not None else None,
                         "threshold": threshold},
        "supporting_check": {"name": "mean drift-adjusted 3-bar return, top third minus bottom third of forecasts",
                             "value": diff, "passed": check_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
