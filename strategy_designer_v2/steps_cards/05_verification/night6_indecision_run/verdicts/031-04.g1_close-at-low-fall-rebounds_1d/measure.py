import numpy as np
import pandas as pd


def measure(bars):
    COMP = "debug_info.components.near_low.post_pipeline_value"
    MIN_CASES = 50

    # ---------- coin normal drift: mean 1-bar return over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        drift[coin] = float(np.nanmean(np.concatenate(rets))) if rets else np.nan

    # ---------- situation check + case collection ----------
    active_total = 0
    active_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r = close / close.shift(1) - 1.0
            # two conventions for the 20-day std: including bar t, or past 20 bars only
            sd_inc = r.rolling(20, min_periods=20).std(ddof=1)
            sd_exc = r.shift(1).rolling(20, min_periods=20).std(ddof=1)
            z_inc = r / sd_inc
            z_exc = r / sd_exc
            computable = z_inc.notna() | z_exc.notna()
            sharp = (z_inc <= -2.0).fillna(False) | (z_exc <= -2.0).fillna(False)

            fc = d["forecast"].astype(float)
            active = (fc != 0) & fc.notna() & computable
            active_total += int(active.sum())
            active_agree += int((active & sharp & (fc > 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True)
            comp = d[COMP].astype(float) if COMP in d.columns else pd.Series(np.nan, index=d.index)
            mask = d["regime"].astype(str) == "mean_reversion"
            for i in np.where(mask.values)[0]:
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].normalize(),
                    "x": comp.iloc[i],
                    "fc": fc.iloc[i],
                    "y": nxt.iloc[i] - drift[coin] if pd.notna(nxt.iloc[i]) else np.nan,
                })

    agreement = float(active_agree / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.9
    sit = {"agreement": agreement, "passed": bool(passed)}

    reading = ("The situation is a 1-day return at or below -2 times the std (ddof 1) of the last 20 daily returns "
               "of the window, taking either the std including or excluding the bar, and active bars of a window's "
               "first 20 bars where it cannot be computed are left out of the agreement; cases are bars with regime "
               "mean_reversion and a next-day return inside the window, the slope t is OLS with standard errors "
               "clustered by UTC day (small-sample corrected), and the supporting check uses the forecast column >= 2.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(active_total)},
            "decided_by": ("Fewer than 90% of the active bars are sharp down days (return <= -2 twenty-day std) "
                           "with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    cases = pd.DataFrame(rows, columns=["coin", "day", "x", "fc", "y"])
    reg = cases.dropna(subset=["x", "y"]).reset_index(drop=True)
    n = int(len(reg))
    n_days = int(reg["day"].nunique()) if n else 0

    slope = None
    t_slope = None
    if n >= 3 and reg["x"].std() > 0 and n_days >= 2:
        X = np.column_stack([np.ones(n), reg["x"].values])
        y = reg["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in reg.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = n_days
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup = cases.dropna(subset=["fc", "y"])
    sup = sup[sup["fc"] >= 2.0]
    sup_val = float(sup["y"].mean()) if len(sup) else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"sharp-down-day cases": n, "days": n_days, "cases with forecast >= 2": int(len(sup))}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} sharp-down-day cases across all coins and windows ({n})."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2.0 and sup_pass is True:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean unusual move of the cases with forecast >= 2 is above 0."
    elif t_slope >= 2.0:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean unusual move of the cases with forecast >= 2 is not above 0."
    elif t_slope <= -2.0:
        status = "rejected"
        decided = "The slope's t is -2 or less: closes nearer the low are followed by smaller next-day rises."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {
            "name": "slope of next-day excess return on near_low post-pipeline value",
            "value": slope,
            "statistic": {"name": "t of the slope, clustered by day", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm if t >= 2 (with supporting check), reject if t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual next-day move (long) of cases with forecast >= 2",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
