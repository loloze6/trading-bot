import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    RAW = "debug_info.components.weekend_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret1)
            else:
                raw = ret1
            d["raw"] = raw
            d["is_sunday"] = d["ts"].dt.dayofweek == 6
            d["fc"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            prepared[coin][w] = d
            active = d["fc"] != 0
            situ = d["is_sunday"] & (d["raw"] < 0) & (d["fc"] > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "forecast-weighted mean excess 2-bar return of Sunday cases with forecast > 0"
    threshold = "confirm: > 0 with t >= 2 and slope > 0; reject: < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are Sunday bars with a negative 1-bar return and a positive (long) forecast, as the plan's Fidelity states.",
            "reading": "Sunday bar = bar whose UTC start timestamp is a Sunday; weekend fall = the component's raw 1-bar return (recomputed from closes where missing) below 0.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in prepared.items():
        # coin's mean 2-bar return over all windows, non-overlapping grid 0,2,4...
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                grid_rets.append(c[i + H] / c[i] - 1.0)
        grid_rets = np.array(grid_rets, dtype=float)
        grid_rets = grid_rets[np.isfinite(grid_rets)]
        if len(grid_rets) == 0:
            continue
        mu = float(grid_rets.mean())
        for w, d in wins.items():
            c = d["close"].astype(float).values
            n = len(d)
            idx = np.where(d["is_sunday"].values & (d["fc"].values > 0))[0]
            for i in idx:
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append({
                    "coin": coin,
                    "sunday": d["ts"].iloc[i].strftime("%Y-%m-%d"),
                    "fc": float(d["fc"].iloc[i]),
                    "ex": float(r - mu),
                })

    cases = pd.DataFrame(rows, columns=["coin", "sunday", "fc", "ex"])
    n_cases = int(len(cases))
    n_sundays = int(cases["sunday"].nunique()) if n_cases else 0
    counts = {"Sundays carrying a case": n_sundays, "cases": n_cases}

    wmean = float((cases["ex"] * cases["fc"]).sum() / cases["fc"].sum()) if n_cases and cases["fc"].sum() > 0 else None

    tval = None
    if n_sundays >= 2:
        per = cases.groupby("sunday")["ex"].mean().values
        sd = per.std(ddof=1)
        if sd > 0:
            tval = float(per.mean() / (sd / np.sqrt(len(per))))

    slope = None
    if n_cases >= 3 and cases["fc"].nunique() > 1:
        slope = float(stats.linregress(cases["fc"].values, cases["ex"].values).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    reading = ("Sunday bar = bar whose UTC start timestamp is a Sunday; the coin's mean 2-bar return is taken on the "
               "non-overlapping grid (positions 0, 2, 4, ...) of all its windows pooled; cases without 2 later bars in "
               "the window are dropped; the t uses the unweighted cross-coin mean of excess returns per Sunday; the "
               "slope is an ordinary least-squares fit of excess return on forecast over all cases.")

    main = {"name": main_name, "value": wmean,
            "statistic": None if tval is None else {"name": "t of the mean of per-Sunday cross-coin means", "value": tval},
            "threshold": threshold}
    supp = {"name": "OLS slope of excess 2-bar return on forecast", "value": slope, "passed": slope_pass}

    if n_sundays < 100 or n_cases < 300:
        status = "not observable"
        decided = f"minimum counts not reached: {n_sundays} Sundays carrying a case (need 100) and {n_cases} cases (need 300)."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "the main measure or its t could not be computed."
    elif wmean > 0 and tval >= 2 and slope_pass:
        status = "confirmed"
        decided = "the forecast-weighted mean excess 2-bar return is above 0 with t >= 2 and the slope is above 0."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "the forecast-weighted mean excess 2-bar return is below 0 with t <= -2."
    elif wmean > 0 and tval >= 2:
        status = "inconclusive"
        decided = "a confirming mean and t with a slope at or below 0 is inconclusive."
    else:
        status = "inconclusive"
        decided = "the numbers meet neither the confirm nor the reject rule (t between -2 and 2, or sign and t disagree)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
