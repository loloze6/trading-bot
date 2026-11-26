import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        unit = "ms" if v.abs().median() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    LOC_COL = "debug_info.components.close_loc.last_history_value"
    BAND = 2.0

    # ---------- per-coin drift (mean 1-bar return over all windows, inside windows only)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check and cases
    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, value, loc)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            o_close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            hi = pd.to_numeric(df["high"], errors="coerce").to_numpy(float)
            lo = pd.to_numeric(df["low"], errors="coerce").to_numpy(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc_px = np.where(rng > 0, (o_close - lo) / rng, np.nan)
            if LOC_COL in df.columns:
                rec = pd.to_numeric(df[LOC_COL], errors="coerce").to_numpy(float)
                loc = np.where(np.isfinite(rec), rec, loc_px)
            else:
                loc = loc_px
            prev = np.concatenate([[np.nan], o_close[:-1]])
            up = np.where(np.isfinite(prev), o_close > prev, np.nan)
            days = _to_utc(df["timestamp"]).dt.strftime("%Y-%m-%d").to_numpy()

            # situation check on active bars (bars with a computable situation)
            for i in range(len(df)):
                if f[i] == 0:
                    continue
                if not np.isfinite(up[i]) if isinstance(up[i], float) else False:
                    continue
                if not np.isfinite(loc[i]):
                    continue
                n_active += 1
                if up[i] == 1 and loc[i] > 0.5 and f[i] < 0:
                    n_agree += 1

            # cases: rise of the short-side forecast by >= band from its lowest level since last bet
            ref = 0.0
            for i in range(len(df)):
                m = -f[i] if f[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    ref = m
                    if i + 1 < len(df) and np.isfinite(o_close[i]) and np.isfinite(o_close[i + 1]) \
                            and np.isfinite(drift[coin]):
                        r = o_close[i + 1] / o_close[i] - 1.0
                        val = -(r - drift[coin])
                        cases.append((coin, days[i], float(val), float(loc[i]) if np.isfinite(loc[i]) else np.nan))
                else:
                    ref = min(ref, m)

    agreement = float(n_agree / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The falling-agitated profile (60-bar trend and 365-bar volatility percentile) cannot be rebuilt "
               "inside ~122-bar windows, so the situation check tests the up close (close above prior close in the same "
               "window, first bars left out) and close location > 0.5 with a short forecast; the day-clustered t uses "
               "per-day summed deviations with a G/(G-1) correction, and the median split puts locations above the "
               "median in the upper half and the rest in the lower half.")

    main_name = "mean short-side unusual next-bar move after short-forecast rises of >= 2 points"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of active bars are up-close bars with close location above 0.5 "
                           "and a short forecast, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["coin", "day", "val", "loc"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean = float(cdf["val"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["val"] - mean
        per_day = dev.groupby(cdf["day"]).sum()
        G = len(per_day)
        se = np.sqrt((per_day ** 2).sum() * G / (G - 1)) / n_cases
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    sub = cdf.dropna(subset=["loc"])
    if len(sub) >= 2:
        med = sub["loc"].median()
        upper = sub.loc[sub["loc"] > med, "val"]
        lower = sub.loc[sub["loc"] <= med, "val"]
        if len(upper) and len(lower):
            sup_val = float(upper.mean() - lower.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n_cases, "distinct days of cases": n_days}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 30) and {n_days} distinct days (need 20).")
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero spread), so neither confirm nor reject is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-side unusual move above 0 with t >= 2 and the upper-half-minus-lower-half difference above 0."
        else:
            status = "inconclusive"
            decided = "Positive main result with t >= 2 but the supporting check (upper minus lower half above 0) fails."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move below 0 with t <= -2: the coin rises more than its drift after these closes."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-side unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "upper-half minus lower-half mean unusual move, split at median close location",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
