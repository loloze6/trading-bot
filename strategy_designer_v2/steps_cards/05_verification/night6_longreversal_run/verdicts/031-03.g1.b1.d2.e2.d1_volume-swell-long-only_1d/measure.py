import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.vol_swell.last_history_value"
    MIN_CASES = 200
    MIN_DAYS = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            vol = pd.to_numeric(df["volume"], errors="coerce")
            rec = (vol.rolling(14, min_periods=14).mean()
                   / vol.rolling(30, min_periods=30).mean() - 1.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), rec)
            else:
                raw = rec
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the "
                           "14-day mean volume is above the 30-day mean with a long (positive) forecast."),
            "reading": "none",
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        all_grid = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_grid.append(r)
                f = fc[p]
                if np.isfinite(f) and f > 0:
                    coin_cases.append((r, float(f), ts.iloc[p].floor("D")))
        if not all_grid:
            continue
        drift = float(np.mean(all_grid))
        for r, f, d in coin_cases:
            rows.append({"x": r - drift, "f": f, "day": d})

    cases = pd.DataFrame(rows, columns=["x", "f", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"positive-forecast grid cases": n_cases, "distinct days": n_days}

    m = None
    t = None
    slope = None
    if n_cases > 0:
        x = cases["x"].values
        f = cases["f"].values
        sw = f.sum()
        m = float((f * x).sum() / sw)
        dev = pd.Series(f * (x - m)).groupby(cases["day"].values).sum().values
        D = len(dev)
        if D > 1:
            se = np.sqrt((D / (D - 1.0)) * np.sum(dev ** 2)) / sw
            t = float(m / se) if se > 0 else None
        if n_cases > 1 and np.var(f) > 0:
            fm = f.mean()
            slope = float(np.sum((f - fm) * (x - x.mean())) / np.sum((f - fm) ** 2))

    slope_pass = None if slope is None else bool(slope > 0)

    main = {
        "name": "forecast-weighted mean 14-bar excess return on positive-forecast grid bars",
        "value": m,
        "statistic": None if t is None else {"name": "t of the weighted mean, cases of one day summed", "value": t},
        "threshold": "confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2",
    }
    supp = {"name": "OLS slope of excess 14-bar return on forecast", "value": slope, "passed": slope_pass}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} positive-forecast grid cases (need 200) "
                   f"on {n_days} distinct days (need 100).")
    elif t is None or m is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the supporting slope is above 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    elif m > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": ("The normal drift is each coin's mean 14-bar return on the non-overlapping grid of all its "
                    "windows, and the day-clustered t sums the weighted deviations f*(x-mean) per UTC day with a "
                    "D/(D-1) correction, the standard error being divided by the sum of forecasts."),
    }
