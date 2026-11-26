import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.stretch.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # raw distance of the close from its 20-bar SMA; recomputed from prices where not recorded
            sma = close.rolling(20, min_periods=20).mean()
            dist_px = close - sma
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                dist = raw.where(raw.notna(), dist_px)
            else:
                dist = dist_px
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series(["unknown"] * len(df))
            active = fc != 0
            situ = (dist > 0) & (regime == "unknown") & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of drift-removed 5-bar forward return on the forecast (grid, forecast < 0)"
    thr = "slope t >= 2 confirms (with strength > 0 and >= 50 cases); t <= -2 rejects (>= 50 cases)"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "grid cases with forecast below 0": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close above "
                           "its 20-day average in the rising-agitated regime, as the plan's situation requires."),
            "reading": "The situation is the recorded raw distance above 0 (prices where missing), regime 'unknown' (the profile's active regime) and a negative forecast.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        coin_rets[coin] = np.array(allr, dtype=float)

    drift = {c: (float(np.mean(a)) if len(a) else np.nan) for c, a in coin_rets.items()}
    usual = {c: (float(np.std(a, ddof=1)) if len(a) > 1 else np.nan) for c, a in coin_rets.items()}

    cases = pd.DataFrame(rows, columns=["coin", "day", "x", "r"])
    if len(cases):
        cases["y"] = cases["r"] - cases["coin"].map(drift)
        cases["u"] = cases["coin"].map(usual)
        cases = cases.dropna(subset=["x", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t = None
    if n_cases >= 3:
        x = cases["x"].values
        y = cases["y"].values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            b = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            g = pd.Series(xc * e).groupby(cases["day"].values).sum().values
            G = len(g)
            if G > 1:
                var = float(np.sum(g ** 2)) / sxx ** 2 * G / (G - 1)
                if var > 0:
                    slope = b
                    t = float(b / np.sqrt(var))

    strength = None
    if n_cases:
        sc = cases.dropna(subset=["u"])
        sc = sc[sc["u"] > 0]
        if len(sc):
            strength = float(np.mean(-sc["y"].values / sc["u"].values))
    sup_pass = None if strength is None else bool(strength > 0)

    if n_cases < 50:
        status = "not observable"
        decided = f"Fewer than 50 grid cases with a forecast below 0 ({n_cases}): the plan's minimum count is not reached."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more, the strength is above 0, with at least 50 cases."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 50 cases: a larger stretch above the average is followed by a further rise."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check (strength above 0) fails."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if t is None else {"name": "slope t, day-clustered", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "strength: mean drift-removed 5-bar return in the short direction over the coin's usual 5-bar move",
                             "value": strength, "passed": sup_pass},
        "counts": {"grid cases with forecast below 0": n_cases, "days": n_days, "active bars": n_active},
        "decided_by": decided,
        "reading": ("Same-day cases are taken together through day-clustered standard errors of the OLS slope "
                    "(with G/(G-1) correction); drift and usual move are each coin's mean and standard deviation of "
                    "5-bar returns on the non-overlapping grid of all its windows; the profile is read from the "
                    "regime column ('unknown' = rising agitated), since its components are not recorded."),
    }
