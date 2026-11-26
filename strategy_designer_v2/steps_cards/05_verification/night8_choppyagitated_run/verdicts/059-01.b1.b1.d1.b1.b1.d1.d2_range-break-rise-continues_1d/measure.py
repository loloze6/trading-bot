import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.scaled_rise_near_high.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(d["close"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            ret7 = close / close.shift(7) - 1.0
            # the 7-day rise: the raw component's sign, else the 7-day return from prices
            rise = np.where(raw.notna(), raw > 0, ret7 > 0)
            # the choppy-calm profile is the default regime ('unknown') where the strategy runs
            profile = d["regime"].astype(str).values == "unknown"
            active = (f != 0).values
            ok = active & profile & rise & (f > 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90 % of the active bars are long bars inside the choppy-calm profile "
                           "after a 7-day rise (or no active bars at all)"),
            "reading": "profile read from the recorded regime 'unknown' (the strategy's regime, flat when vetoed to chop); "
                       "the rise from the raw component's sign, else the 7-day return from prices",
        }

    # ---------- 2. criterion ----------
    rows = []
    drift_parts = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    rows.append((coin, ts.iloc[i].floor("D"), float(f[i]), r))
        drift_parts[coin] = float(np.mean(all_r)) if all_r else np.nan

    df = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
    if len(df):
        df["drift"] = df["coin"].map(drift_parts)
        df["x"] = df["r"] - df["drift"]
        df = df.dropna(subset=["x", "f"])
    n_cases = int(len(df))
    n_days = int(df["day"].nunique()) if n_cases else 0
    counts = {"grid bars with forecast > 0": n_cases, "distinct days": n_days}

    wmean = None
    t = None
    slope = None
    if n_cases > 0 and df["f"].sum() > 0:
        F = df["f"].sum()
        wmean = float((df["f"] * df["x"]).sum() / F)
        dev = (df["f"] * (df["x"] - wmean)).groupby(df["day"]).sum().values
        G = len(dev)
        if G > 1:
            var = (dev ** 2).sum() * G / (G - 1) / F ** 2
            if var > 0:
                t = float(wmean / np.sqrt(var))
        if n_cases > 1 and df["f"].nunique() > 1:
            slope = float(np.polyfit(df["f"].values, df["x"].values, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)

    main = {
        "name": "forecast-weighted mean excess 14-bar return",
        "value": wmean,
        "statistic": None if t is None else {"name": "t of the weighted mean, cases of one day pooled", "value": t},
        "threshold": "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2",
    }
    supp = {"name": "OLS slope of excess 14-bar return on forecast", "value": slope, "passed": slope_pass}
    reading = ("grid at positions 0,14,28,... of each window with the 14-bar return inside the window; drift = coin's mean "
               "14-bar return on that grid over all its windows; t = weighted mean over a standard error from the "
               "forecast-weighted deviations summed per UTC day (with G/(G-1) correction); the plan's 'fewer than 30 grid "
               "bars or 20 days' is treated as a minimum count, giving 'not observable'; profile read from the regime "
               "column 'unknown'.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = "fewer than 30 grid bars with forecast > 0 or fewer than 20 distinct days"
    elif wmean is None or t is None:
        status = "inconclusive"
        decided = "the weighted mean or its t could not be computed"
    elif wmean > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "weighted mean excess return above 0 with t >= 2 and a positive slope"
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = "weighted mean excess return below 0 with t <= -2"
    elif wmean > 0 and t >= 2:
        status = "inconclusive"
        decided = "confirming mean with t >= 2 but the slope is 0 or negative"
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: neither the confirm nor the reject rule is met"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
