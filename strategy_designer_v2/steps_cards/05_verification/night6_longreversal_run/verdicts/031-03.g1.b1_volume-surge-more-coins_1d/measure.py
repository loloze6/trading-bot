import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.vol_swell.last_history_value"

    def _raw_from_volume(vol):
        # (mean of last 14 volumes / mean of last 30 volumes) - 1, current bar included, inside one window
        s = vol.rolling(14, min_periods=14).mean()
        l = vol.rolling(30, min_periods=30).mean()
        return s / l - 1.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rec = _raw_from_volume(pd.to_numeric(df["volume"], errors="coerce"))
            raw = raw.where(raw.notna(), rec)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & (((raw > 0) & (f > 0)) | ((raw < 0) & (f < 0)))
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean of forecast/10 x (14-bar forward return - coin's mean 14-bar return), grid cases"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("the forecast's sign does not follow the plan's situation (long when 14-day mean volume "
                           "is above the 30-day mean, short when below) on at least 90% of active bars"),
            "reading": "Situation sign taken from the recorded raw volume ratio - 1 (recomputed from volume where missing).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                j = i + H
                if j >= len(df):
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "fc": f[i],
                    "ret": c1 / c0 - 1.0,
                })
    cases = pd.DataFrame(rows, columns=["coin", "day", "fc", "ret"])
    if len(cases):
        cases["drift"] = cases.groupby("coin")["ret"].transform("mean")
        cases = cases[np.isfinite(cases["fc"])].copy()
        cases["excess"] = cases["ret"] - cases["drift"]
        cases["x"] = cases["fc"] / 10.0 * cases["excess"]
        cases["dir"] = np.sign(cases["fc"]) * cases["excess"]

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = None
    t = None
    if n_cases > 0:
        mean = float(cases["x"].mean())
        dev = cases["x"] - mean
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        a = cases["fc"].abs()
        med = float(a.median())
        hi = cases.loc[a > med, "dir"]
        lo = cases.loc[a < med, "dir"]
        if len(hi) and len(lo):
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    reading = ("Every grid bar (positions 0,14,28,... per coin and window) with a 14-bar forward return inside its "
               "window is a case, forecast 0 included; the coin's mean 14-bar return is the mean over its grid cases of "
               "all windows; the t clusters case deviations summed per UTC day (with D/(D-1) correction); the median "
               "split uses |forecast| strictly above vs strictly below the median, directional excess = "
               "sign(forecast) x excess return.")

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided_by = (f"minimum counts not reached: {n_cases} cases (need 200) on {n_days} distinct days (need 100)")
    elif mean is None or t is None:
        status = "inconclusive"
        decided_by = "the t could not be computed, so neither the confirm nor the reject rule is met"
    elif mean > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided_by = "the main mean is positive with t >= 2 and the supporting check passes"
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided_by = "the main mean is negative with t <= -2"
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided_by = "t >= 2 but the supporting check fails, which the plan calls inconclusive"
    else:
        status = "inconclusive"
        decided_by = "-2 < t < 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean, cases summed per day", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean directional excess 14-bar return, |forecast| above median minus below",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
