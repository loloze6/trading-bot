import numpy as np
import pandas as pd


def measure(bars):
    COMP = "run_break_fade"
    BAND_RUN = 2          # a down run of two or more closes
    RET20_LIM = -10.0     # ret20 in percent, regime holds at or below
    MIN_CASES = 30
    MIN_DAYS = 30

    def to_ts(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def comp_raw(df):
        col = "debug_info.components.%s.last_history_value" % COMP
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").values
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                if isinstance(v, dict):
                    c = v.get(COMP)
                    if isinstance(c, dict):
                        try:
                            val = float(c.get("last_history_value"))
                        except (TypeError, ValueError):
                            val = np.nan
                out.append(val)
            return np.array(out, dtype=float)
        return np.full(len(df), np.nan)

    # ---------- pass 1: coin drift over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- pass 2: situation check and cases ----------
    n_active = 0
    n_agree = 0
    case_x, case_f, case_day = [], [], []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            reg = df["regime"].astype(str).values
            raw = comp_raw(df)
            ts = to_ts(df["timestamp"])
            days = ts.dt.strftime("%Y-%m-%d").values

            for t in range(n):
                if f[t] != 0:
                    n_active += 1
                    # the run break: up close after >= 2 down closes
                    if t >= BAND_RUN + 1:
                        ev = c[t] > c[t - 1] and all(
                            c[t - k] < c[t - k - 1] for k in range(1, BAND_RUN + 1))
                    else:
                        ev = np.isfinite(raw[t]) and raw[t] != 0
                    # deep 20-day fall (recomputed where the window allows)
                    if t >= 20 and np.isfinite(c[t - 20]) and c[t - 20] > 0:
                        deep = (c[t] / c[t - 20] - 1.0) * 100.0 <= RET20_LIM + 1e-9
                    else:
                        deep = True
                    # falling calm profile + ret20 rule: the detector's decision
                    prof = reg[t] == "trending"
                    if ev and deep and prof and f[t] < 0:
                        n_agree += 1
                # cases: forecast below 0, next-day return inside the window
                if f[t] < 0 and t + 1 < n and np.isfinite(c[t]) and np.isfinite(c[t + 1]) \
                        and c[t] > 0 and np.isfinite(mu):
                    r = c[t + 1] / c[t] - 1.0
                    case_x.append(-(r - mu))
                    case_f.append(abs(f[t]))
                    case_day.append(days[t])

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    sit = {"agreement": float(agreement), "passed": bool(passed)}

    main_name = "mean short-direction next-day unusual move (return minus coin drift, negated)"
    thr = "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"
    reading = ("Case bars are every bar with forecast below 0 whose next close is in the same window, "
               "the drift is the coin's mean daily return over all its windows, the t clusters the cases "
               "by UTC day (deviations summed per day, G/(G-1) correction), the slope is ordinary least "
               "squares on abs(forecast), and both 30-case and 30-day minimums are treated as minimum "
               "counts for observability.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on an up close breaking a "
                           "down run of two or more days with the 20-day return at or below -10 % in the "
                           "falling calm regime."),
            "reading": reading,
        }

    x = np.array(case_x, dtype=float)
    a = np.array(case_f, dtype=float)
    d = np.array(case_day)
    n_cases = int(len(x))
    n_days = int(len(np.unique(d))) if n_cases else 0

    mean = float(np.mean(x)) if n_cases else None
    tstat = None
    if n_cases >= 2 and n_days >= 2:
        dev = x - mean
        s = pd.Series(dev).groupby(d).sum().values
        G = len(s)
        var = (G / (G - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            tstat = float(mean / np.sqrt(var))

    slope = None
    if n_cases >= 2 and np.var(a) > 0:
        slope = float(np.cov(a, x, ddof=1)[0, 1] / np.var(a, ddof=1))
    slope_ok = (slope is not None and slope > 0)

    counts = {"cases": n_cases, "distinct days": n_days}
    mm = {"name": main_name, "value": mean,
          "statistic": ({"name": "t of the mean, cases clustered by day", "value": tstat}
                        if tstat is not None else None),
          "threshold": thr}
    sc = {"name": "OLS slope of unusual move on abs(forecast)", "value": slope,
          "passed": bool(slope_ok) if slope is not None else None}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = ("Fewer than 30 cases or fewer than 30 distinct days (%d cases, %d days)."
                   % (n_cases, n_days))
    elif tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tstat >= 2:
        if slope_ok:
            status = "confirmed"
            decided = ("Confirm rule: mean short-direction unusual move above 0 with t >= 2 over at "
                       "least 30 cases on at least 30 days, and the supporting slope is positive.")
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: a confirm-strength mean with a slope not above 0."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = ("Reject rule: mean short-direction unusual move below 0 with t <= -2 over at "
                   "least 30 cases.")
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": sc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
