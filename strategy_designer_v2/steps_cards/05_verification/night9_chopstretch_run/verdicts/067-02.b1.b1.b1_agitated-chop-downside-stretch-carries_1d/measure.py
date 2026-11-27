import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(v.values) if len(v) else 0
        unit = "ms" if med > 1e11 else "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.strftime("%Y-%m-%d").values


def measure(bars):
    H = 5
    RAW = "debug_info.components.stretch.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # below the 20-day average: from the recorded raw stretch, else from prices
            sma = close.rolling(20, min_periods=20).mean()
            below_px = close < sma
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                below = pd.Series(np.where(raw.notna(), raw < 0, below_px), index=df.index).astype(bool)
            else:
                below = below_px.astype(bool)
            profile = df["regime"].astype(str) == "unknown"  # the choppy-agitated regime (not vetoed to chop)
            active = fc.notna() & (fc != 0)
            agree = active & profile & below & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "abs(forecast)-weighted mean short-direction 5-day excess return over the coin's mean"
    thr = "confirm: > 0 with day-clustered t >= 2; reject: < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The forecast is active on bars that are not the plan's situation (choppy agitated "
                           "profile, close below its 20-day average) with a short: agreement %.3f < 0.90." % agreement),
            "reading": "The profile is read as the detector's regime 'unknown' (not vetoed to chop); below the average as a negative raw stretch.",
        }

    # ---------- 2. criterion ----------
    grid_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_day(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                grid_rows.append((coin, w, days[i], fc[i], c1 / c0 - 1.0))
    g = pd.DataFrame(grid_rows, columns=["coin", "window", "day", "forecast", "ret"])
    coin_mean = g.groupby("coin")["ret"].mean() if len(g) else pd.Series(dtype=float)
    cases = g[g["forecast"].notna() & (g["forecast"] < 0)].copy()
    cases["x"] = -(cases["ret"] - cases["coin"].map(coin_mean))
    cases["w"] = cases["forecast"].abs()
    cases = cases[np.isfinite(cases["x"]) & (cases["w"] > 0)]

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    m = None
    t = None
    if n_cases > 0:
        W = cases["w"].sum()
        m = float((cases["w"] * cases["x"]).sum() / W)
        e = cases["w"] * (cases["x"] - m) / W
        S = e.groupby(cases["day"]).sum()
        G = len(S)
        if G > 1:
            var = (G / (G - 1)) * float((S ** 2).sum())
            t = float(m / np.sqrt(var)) if var > 0 else None

    sup_val = None
    if n_cases >= 2:
        med = cases["w"].median()
        big = cases.loc[cases["w"] > med, "x"]
        small = cases.loc[cases["w"] <= med, "x"]
        if len(big) and len(small):
            sup_val = float(big.mean() - small.mean())
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "Minimum not reached: %d cases and %d distinct days, the plan needs at least 30 of each." % (n_cases, n_days)
    elif t is None or m is None:
        status = "inconclusive"
        decided = "The clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Weighted mean short-direction excess return above 0 with t >= 2, and the size-order check above 0."
        else:
            status = "inconclusive"
            decided = "Weighted mean above 0 with t >= 2, but the size-order check is not above 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "Weighted mean short-direction excess return below 0 with t <= -2: stretched-below closes return toward the average."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": None if t is None else {"name": "t of the weighted mean, clustered by day", "value": t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "size order: mean excess of larger half minus smaller half of abs(forecast)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The profile is the regime 'unknown' and below-average a negative raw stretch; the coin's mean 5-day "
                    "return is over its pooled non-overlapping grid of all windows; the larger half is abs(forecast) "
                    "above the median (ties go to the smaller half), compared by unweighted means; the clustered t uses "
                    "summed weighted deviations per UTC day with a G/(G-1) correction."),
    }
