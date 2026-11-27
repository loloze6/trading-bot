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
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback where the raw value is not recorded: sign of close - SMA20 inside the window
            sma = close.rolling(20, min_periods=20).mean()
            stretch_sign = np.sign(raw)
            fb = raw.isna()
            stretch_sign[fb] = np.sign(close[fb] - sma[fb])
            choppy = df["regime"].astype(str) == "unknown"
            active = fc.notna() & (fc != 0)
            agree = active & choppy & stretch_sign.notna() & (np.sign(fc) == stretch_sign) & (stretch_sign != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The choppy profile is read as the detector's regime 'unknown' (the regime that carries the stretch "
               "strategy; trend beyond ±10 is vetoed to the flat regime), the expected side as the sign of the raw "
               "stretch (close above SMA20 = long); the coin's mean 5-bar return is the mean over all its "
               "non-overlapping grid bars of all windows; the day-clustered t sums deviations per UTC day with a "
               "D/(D-1) correction; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' as the "
               "workflow requires.")

    main_name = "mean of (forecast/10) x (5-bar forward return - coin mean 5-bar return), grid cases"
    main_thr = "confirm: > 0 with t >= 2 and both sides > 0; reject: < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("Fewer than 90% of active bars are choppy-profile (regime 'unknown') bars with the forecast "
                           "on the side of the close's stretch from its 20-day average."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    coin_cases.append((f, r, ts.iloc[i].floor("D")))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for f, r, d in coin_cases:
            rows.append({"coin": coin, "f": f, "v": (f / 10.0) * (r - mu), "day": d})

    cases = pd.DataFrame(rows, columns=["coin", "f", "v", "day"])
    n_cases = int(len(cases))
    n_long = int((cases["f"] > 0).sum()) if n_cases else 0
    n_short = int((cases["f"] < 0).sum()) if n_cases else 0
    n_days = int(cases["day"].nunique()) if n_cases else 0

    def clustered(sub):
        if len(sub) == 0:
            return None, None
        m = float(sub["v"].mean())
        dev = (sub["v"] - m).groupby(sub["day"]).sum()
        D = len(dev)
        if D < 2:
            return m, None
        var = float((dev ** 2).sum()) * D / (D - 1)
        se = np.sqrt(var) / len(sub)
        return m, (float(m / se) if se > 0 else None)

    mean_all, t_all = clustered(cases)
    mean_long = float(cases.loc[cases["f"] > 0, "v"].mean()) if n_long else None
    mean_short = float(cases.loc[cases["f"] < 0, "v"].mean()) if n_short else None
    sup_pass = None
    if mean_long is not None and mean_short is not None:
        sup_pass = bool(mean_long > 0 and mean_short > 0)

    counts = {"cases": n_cases, "long cases": n_long, "short cases": n_short, "distinct days": n_days}

    if n_cases < 200 or n_long < 50 or n_short < 50 or n_days < 100:
        status = "not observable"
        decided = ("A minimum count is not reached (needs at least 200 cases, 50 on each side, on at least 100 "
                   "distinct days).")
    elif mean_all is not None and t_all is not None and mean_all > 0 and t_all >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure is above 0 with t >= 2 and the mean is above 0 on both the long and short sides."
    elif mean_all is not None and t_all is not None and mean_all < 0 and t_all <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2: stretches revert."
    elif mean_all is not None and t_all is not None and mean_all > 0 and t_all >= 2:
        status = "inconclusive"
        decided = "The main measure is above 0 with t >= 2 but the two-side check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_all,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_all}
                          if t_all is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "same mean on long and on short cases, each above 0",
            "value": (min(mean_long, mean_short) if (mean_long is not None and mean_short is not None) else None),
            "passed": sup_pass,
            "long_mean": mean_long,
            "short_mean": mean_short,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
