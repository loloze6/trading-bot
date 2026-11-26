import numpy as np
import pandas as pd
from scipy import stats

def measure(bars):
    H = 7
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            # recompute the scaled 7-bar rise from prices, inside the window, for bars where raw is missing
            r1 = close.pct_change()
            rec = (close / close.shift(H) - 1.0) / r1.rolling(30, min_periods=30).std()
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), rec)
            f = df["forecast"].astype(float).fillna(0.0)
            active = f != 0
            n_active += int(active.sum())
            agree = active & (raw > 0) & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    sit = {"agreement": agreement, "passed": passed}

    main_name = "forecast-weighted mean excess 7-day return (coin mean 7-day return removed)"
    threshold = "confirm: > 0 with t >= 2 and slope > 0; reject: < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are bars with a positive scaled 7-day rise and a long forecast, as the Fidelity's situation (rises only, long) requires",
            "reading": "the situation is a raw scaled_week_rise above 0 (recomputed from prices where not recorded) with a positive forecast; the profile filter is code's and only restricts the bars",
        }

    # ---------- 2. criterion ----------
    # coin mean 7-day return over all windows, non-overlapping grid
    coin_mean = {}
    cases = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H < len(df) and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    r = close[i + H] / close[i] - 1.0
                    allr.append(r)
                    if np.isfinite(f[i]) and f[i] > 0:
                        cases.append((coin, ts.iloc[i].floor("D"), float(f[i]), r))
        coin_mean[coin] = float(np.mean(allr)) if allr else np.nan

    rows = [(c, d, f, r - coin_mean[c]) for (c, d, f, r) in cases if np.isfinite(coin_mean[c])]
    cdf = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"distinct days with cases": n_days, "cases": n_cases}
    reading = ("cases are grid bars (positions 0, 7, 14, ... of each window) with forecast > 0 and a 7-bar forward return inside the window; "
               "the t is the weighted mean over its day-clustered standard error (per day the sum of weight x deviation, with D/(D-1) correction); "
               "the plan's minimum of 30 distinct days is applied as 'not observable' as the workflow requires.")

    value = None
    tval = None
    slope = None
    if n_cases > 0:
        wsum = cdf["f"].sum()
        value = float((cdf["f"] * cdf["ex"]).sum() / wsum)
        if n_days >= 2:
            dev = cdf["f"] * (cdf["ex"] - value)
            per_day = dev.groupby(cdf["day"]).sum().values
            var = (per_day ** 2).sum() / wsum ** 2 * n_days / (n_days - 1)
            se = np.sqrt(var)
            tval = float(value / se) if se > 0 else None
        if n_cases >= 3 and cdf["f"].nunique() > 1:
            slope = float(stats.linregress(cdf["f"].values, cdf["ex"].values).slope)

    slope_pass = None if slope is None else bool(slope > 0)
    mm = {"name": main_name, "value": value,
          "statistic": None if tval is None else {"name": "t of the weighted mean, cases of one day summed", "value": tval},
          "threshold": threshold}
    sc = {"name": "OLS slope of excess 7-day return on forecast", "value": slope, "passed": slope_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"the plan needs at least 30 distinct days with cases; only {n_days} were found"
    elif tval is None:
        status = "inconclusive"
        decided = "the t of the main measure could not be computed, so neither the confirm nor the reject rule is met"
    elif value > 0 and tval >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "the main measure is above 0 with t >= 2 and the slope is above 0 (confirm rule)"
        else:
            status = "inconclusive"
            decided = "a main t >= 2 with a slope at or below 0 is inconclusive"
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = "the main measure is below 0 with t <= -2 (reject rule)"
    else:
        status = "inconclusive"
        decided = "the t of the main measure is between -2 and 2 (inconclusive rule)"

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": sc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
