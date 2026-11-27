import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    cases = []  # dicts: coin, day, ret, absf
    drift_samples = {}

    for coin, windows in bars.items():
        drift_samples.setdefault(coin, [])
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)

            # Situation, from prices: close location >= 0.5, 5-day return < 0,
            # and the choppy-agitated profile (the detector's vetoes give "chop").
            rng = high - low
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (close - low) / rng, np.nan)
            ret5 = np.full(n, np.nan)
            if n > 5:
                ret5[5:] = close[5:] / close[:-5] - 1.0
            profile_ok = regime != "chop"
            computable = ~np.isnan(loc) & ~np.isnan(ret5)
            situ = computable & (loc >= 0.5) & (ret5 < 0) & profile_ok

            active = (fc != 0) & computable
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            # Drift samples: non-overlapping H-bar returns on the grid 0, H, 2H, ...
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    drift_samples[coin].append(close[p + H] / close[p] - 1.0)

            # Short bets: rise of the short forecast's size of at least BAND,
            # from its lowest size since the last bet (from 0 after flat/side change).
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                f = fc[i]
                if f < 0:
                    m = -f
                    if not prev_short:
                        ref = 0.0
                    if m - ref >= BAND:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0

            # One case per non-overlapping H-bar grid cell: the cell's first bet.
            seen_cells = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                day = ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else str(i)
                cases.append({"coin": coin, "day": day,
                              "ret": close[i + H] / close[i] - 1.0,
                              "absf": abs(fc[i])})

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move of the short bets", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct days carrying cases": 0, "cases": 0},
            "decided_by": "No active bars: the record holds no bet to measure.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    reading = ("Situation = close location >= 0.5 and 5-day close return < 0 from the window's prices with the profile "
               "read as the detector's regime not 'chop' (bars whose location or 5-day return cannot be computed are left out); "
               "one case per 5-bar grid cell (its first bet, dropped if its 5-bar return leaves the window); "
               "the t clusters cases by UTC day (summed deviations, G/(G-1) correction); the larger half is |forecast| above "
               "the median and the smaller half at or below it; fewer than 30 days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move of the short bets", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {},
            "decided_by": (f"Only {agreement:.1%} of active bars are short bars with close location >= 0.5, a negative "
                           "5-day return and the choppy-agitated profile, below the 90 % the plan's situation needs."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}
    cdf = pd.DataFrame(cases, columns=["coin", "day", "ret", "absf"])
    if len(cdf):
        cdf["drift"] = cdf["coin"].map(drift)
        cdf["unusual"] = -(cdf["ret"] - cdf["drift"])
        cdf = cdf.dropna(subset=["unusual"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["unusual"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["unusual"] - mean_u
        D = dev.groupby(cdf["day"]).sum().to_numpy()
        G = len(D)
        var_mean = (G / (G - 1.0)) * np.sum(D ** 2) / (n_cases ** 2)
        se = np.sqrt(var_mean)
        if se > 0:
            t_val = float(mean_u / se)

    diff = None
    if n_cases >= 2:
        med = cdf["absf"].median()
        hi = cdf.loc[cdf["absf"] > med, "unusual"]
        lo = cdf.loc[cdf["absf"] <= med, "unusual"]
        if len(hi) and len(lo):
            diff = float(hi.mean() - lo.mean())
    sup_passed = (diff > 0) if diff is not None else None

    counts = {"distinct days carrying cases": n_days, "cases": n_cases}
    main = {"name": "mean unusual 5-bar move of the short bets (drift removed, short direction)",
            "value": mean_u,
            "statistic": ({"name": "t of the mean, same-day cases together", "value": t_val}
                          if t_val is not None else None),
            "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"}
    sup = {"name": "mean unusual move, larger-|forecast| half minus smaller half",
           "value": diff, "passed": sup_passed}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct days carry cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the larger half beats the smaller half (confirm rule)."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 (reject rule)."
    elif mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The mean unusual move is positive with t >= 2 but the size check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
