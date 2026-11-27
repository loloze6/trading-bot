import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    FC = "forecast"
    RAW = "debug_info.components.month_fall.last_history_value"
    CHOPPY_REGIME = "unknown"  # the only regime with a strategy; "chop" (|60-bar move| > 10) is null

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            return pd.to_datetime(s, unit="ms", utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # recompute the 30-bar percent change from prices where the raw value is not recorded
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            active = fc.notna() & (fc != 0)
            situation = (regime == CHOPPY_REGIME) & (raw < 0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)
    else:
        agreement = None
        passed = True

    main_name = "slope of drift-adjusted 7-bar forward return on forecast (grid bars with forecast < 0)"
    threshold = "confirm: slope > 0 with t >= 2 (and mean short gain > 0); reject: slope < 0 with t <= -2"
    reading = ("The choppy market is read as the detector's regime 'unknown' (the 60-bar move within +-10, "
               "the only regime with a strategy) and the fall as a negative 30-bar raw value; the normal 7-bar "
               "drift is the coin's mean 7-bar return on the non-overlapping grid of all its windows; pooling "
               "cases of the same day is done with a day-clustered standard error of the OLS slope; and the "
               "plan's 'fewer than 100 cases or 60 days' is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the choppy "
                           "regime with the close below its close of 30 bars earlier."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            ts = to_time(d["timestamp"])
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid.append({"coin": coin, "ret": r, "fc": fc[i],
                                  "day": ts.iloc[i].strftime("%Y-%m-%d")})
        if not coin_grid:
            continue
        g = pd.DataFrame(coin_grid)
        drift = g["ret"].mean()
        g["y"] = g["ret"] - drift
        rows.append(g)

    if rows:
        allg = pd.concat(rows, ignore_index=True)
        cases = allg[allg["fc"].notna() & (allg["fc"] < 0) & allg["y"].notna()].copy()
    else:
        cases = pd.DataFrame(columns=["coin", "ret", "fc", "day", "y"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t = None
    if n_cases >= 3:
        x = cases["fc"].astype(float).values
        y = cases["y"].astype(float).values
        xm = x.mean()
        sxx = np.sum((x - xm) ** 2)
        if sxx > 0:
            slope = float(np.sum((x - xm) * (y - y.mean())) / sxx)
            intercept = y.mean() - slope * xm
            resid = y - intercept - slope * x
            score = pd.Series((x - xm) * resid).groupby(cases["day"].values).sum().values
            G = len(score)
            if G > 1:
                var = (G / (G - 1)) * np.sum(score ** 2) / sxx ** 2
                se = np.sqrt(var)
                t = float(slope / se) if se > 0 else None

    mean_gain = float((-cases["y"]).mean()) if n_cases else None
    check_passed = (mean_gain > 0) if mean_gain is not None else None

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided_by = (f"The minimum count was not reached: {n_cases} cases (need 100) on {n_days} distinct days "
                      f"(need 60).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided_by = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if check_passed:
            status = "confirmed"
            decided_by = "The slope is positive with t >= 2 and the mean short gain is above 0, with at least 100 cases on 60 days."
        else:
            status = "inconclusive"
            decided_by = "The slope is positive with t >= 2 but the mean short gain is not above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2: deeper falls are followed by larger excess rises."
    else:
        status = "inconclusive"
        decided_by = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t, day-clustered", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean short gain (minus drift-adjusted 7-bar return)",
                             "value": mean_gain,
                             "passed": (bool(check_passed) if check_passed is not None else None)},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
