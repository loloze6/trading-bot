import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    LHV = "debug_info.components.quieting.last_history_value"
    PROFILE_REGIME = "unknown"  # the rising profile: the regime with a strategy; "chop" is the veto (profile_trend <= 10)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if not active.any():
                continue
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            in_sit = (reg == PROFILE_REGIME) & raw.notna() & (raw < 0)
            agree = active & in_sit & (f > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean excess 3-bar return over positive-forecast grid bars"
    main_thr = "confirm: positive with t >= 2 (and supporting difference > 0); reject: negative with t <= -2"
    sup_name = "mean excess 3-bar return, forecast above median of positive forecasts minus forecast 0, inside rising profile"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars inside the rising profile "
                           "(regime not chop) with recent 14-day swings below the prior 90 days (raw centred ratio < 0)."
                           if n_active > 0 else "The record has no bar with a nonzero forecast."),
            "reading": "The rising profile is read from the recorded regime (the detector's decision, its component is not recorded) and the quieting from the raw centred ratio being below 0.",
        }

    # ---------- 2. grid of 3-bar forward returns ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({
                    "coin": coin, "window": w,
                    "ret": c1 / c0 - 1.0,
                    "forecast": f[i],
                    "regime": reg[i],
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                })
    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast", "regime", "day"])
    if len(g):
        g["coin_mean"] = g.groupby("coin")["ret"].transform("mean")
        g["ex"] = g["ret"] - g["coin_mean"]
    else:
        g["coin_mean"] = []
        g["ex"] = []

    g = g[g["forecast"].notna()]
    pos = g[g["forecast"] > 0]
    n_cases = int(len(pos))
    n_days = int(pos["day"].nunique()) if n_cases else 0

    # main measure: forecast-weighted mean, t with one day's cases pooled (cluster-by-day SE)
    m = None
    t = None
    if n_cases > 0:
        wts = pos["forecast"].values.astype(float)
        ex = pos["ex"].values.astype(float)
        W = wts.sum()
        m = float(np.sum(wts * ex) / W)
        dev = pd.Series(wts * (ex - m)).groupby(pos["day"].values).sum().values
        G = len(dev)
        if G > 1:
            var = np.sum(dev ** 2) / W ** 2 * G / (G - 1)
            se = np.sqrt(var)
            t = float(m / se) if se > 0 else None

    # supporting check
    prof = g[g["regime"] == PROFILE_REGIME]
    ppos = prof[prof["forecast"] > 0]
    diff = None
    sup_pass = None
    if len(ppos) > 0:
        med = ppos["forecast"].median()
        g1 = prof[prof["forecast"] > med]
        g2 = prof[prof["forecast"] == 0]
        if len(g1) > 0 and len(g2) > 0:
            diff = float(g1["ex"].mean() - g2["ex"].mean())
            sup_pass = bool(diff > 0)
        n_g1, n_g2 = int(len(g1)), int(len(g2))
    else:
        n_g1, n_g2 = 0, int((prof["forecast"] == 0).sum())

    counts = {
        "positive-forecast grid cases": n_cases,
        "distinct days": n_days,
        "supporting group above median": n_g1,
        "supporting group forecast 0": n_g2,
    }

    if n_cases < 60 or n_days < 30:
        status = "not observable"
        decided_by = (f"The minimum of 60 positive-forecast grid cases over 30 distinct days is not reached "
                      f"({n_cases} cases, {n_days} days).")
    elif m is None or t is None:
        status = "inconclusive"
        decided_by = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "The main measure is positive with t >= 2 and the supporting difference is > 0."
        else:
            status = "inconclusive"
            decided_by = "The main measure is positive with t >= 2 but the supporting difference is not > 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided_by = "The main measure is negative with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The t of the main measure lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": ({"name": "t of the weighted mean, cases of one day pooled", "value": t} if t is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The rising profile is the recorded regime 'unknown' (not the chop veto), the coin's mean is over its grid "
                    "3-bar returns of all windows, the t pools each day's weighted deviations into one cluster "
                    "(SE^2 = sum of squared day sums / (sum of weights)^2 x G/(G-1)), the median is over positive-forecast "
                    "grid bars inside the profile, and a missing supporting group counts as a failed check."),
    }
