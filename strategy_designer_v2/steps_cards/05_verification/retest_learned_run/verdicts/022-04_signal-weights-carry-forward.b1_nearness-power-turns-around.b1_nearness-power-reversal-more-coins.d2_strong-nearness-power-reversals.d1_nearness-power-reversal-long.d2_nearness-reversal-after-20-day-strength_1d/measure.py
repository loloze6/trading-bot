import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.npower_rev.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            r20 = close / close.shift(20) - 1.0
            # where the 20-day return can't be rebuilt inside the window, use the detector's own decision
            regime_on = df["regime"].astype(str).eq("trending") if "regime" in df.columns else pd.Series(False, index=df.index)
            r20_pos = np.where(r20.notna(), r20 > 0, regime_on)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # standardise keeps the raw sign, negate flips it, clip keeps the positive side: long when raw < 0
            reading_long = (raw < 0).fillna(False).to_numpy()
            situation = np.asarray(r20_pos, dtype=bool) & reading_long
            active = (fc != 0).to_numpy()
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0).to_numpy()).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean of forecast x (5-bar return minus coin's mean 5-bar return), grid bars with forecast > 0"
    main_thr = "confirm if t >= 2 (with supporting check > 0); reject if t <= -2"
    sup_name = "mean excess 5-bar return, 20-day return above median minus below median"
    reading = ("The plan's situation is taken as raw component value < 0 (negated, standardised, clipped at 0 -> long) "
               "while the 20-day return recomputed from closes is > 0 (the regime column used only on the first 20 bars "
               "of a window, where it cannot be recomputed); the coin's mean 5-bar return is over all non-overlapping "
               "grid bars of all its windows; the supporting check splits the forecast > 0 cases at the pooled median of "
               "their recomputed 20-day return (cases without it left out, cases equal to the median in neither group); "
               "the 100-case minimum not reached gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "grid cases with forecast > 0": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with a negative raw "
                           "excess-power reading and a positive 20-day return, as the plan's situation requires."
                           if n_active > 0 else "No bar has a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            r20 = pd.Series(close) / pd.Series(close).shift(20) - 1.0
            for t in range(0, n, H):
                if t + H >= n:
                    break
                ret = close[t + H] / close[t] - 1.0
                rows.append((coin, w, t, fc[t], ret, r20.iloc[t]))
    g = pd.DataFrame(rows, columns=["coin", "window", "t", "forecast", "ret", "r20"])
    g = g[np.isfinite(g["ret"])]
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["excess"] = []
    cases = g[(g["forecast"] > 0) & g["forecast"].notna()].copy()
    n_cases = int(len(cases))
    counts = {"grid cases with forecast > 0": n_cases}

    val = cases["forecast"] * cases["excess"]
    mean_v = float(val.mean()) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(val.std(ddof=1))
        if sd > 0:
            tstat = mean_v / (sd / np.sqrt(n_cases))

    sub = cases[cases["r20"].notna()]
    diff = None
    n_above = n_below = 0
    if len(sub):
        med = float(sub["r20"].median())
        above = sub[sub["r20"] > med]["excess"]
        below = sub[sub["r20"] < med]["excess"]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            diff = float(above.mean() - below.mean())
    sup_pass = (diff > 0) if diff is not None else None

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 100."
    elif tstat is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed (no spread), so neither confirm nor reject is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is >= 2 and the supporting check's difference is > 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The main measure's t is <= -2."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The main measure's t is >= 2 but the supporting check's difference is not > 0."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": ({"name": "ordinary t of the mean", "value": float(tstat)} if tstat is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
