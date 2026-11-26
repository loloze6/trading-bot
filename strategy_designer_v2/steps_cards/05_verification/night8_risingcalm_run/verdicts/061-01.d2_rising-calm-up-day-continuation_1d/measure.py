import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(d["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Raw scaled rise if recorded, else its sign from the 1-day price return.
            rise_pos = np.where(raw.notna(), raw > 0, ret1 > 0)
            regime = d["regime"].astype(str)
            # Rising-calm profile: the detector did not veto to chop (regime "unknown").
            in_profile = (regime == "unknown").values
            situation = in_profile & rise_pos
            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0).values).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 5-bar forward return on forecast (forecast > 0, grid cases)"
    thr = "slope > 0 with day-clustered t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects"
    sup_name = "mean excess 5-bar return, upper half minus lower half of forecasts"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars in the rising-calm profile "
                          "(regime not vetoed to chop) with a positive 1-day scaled rise.",
            "reading": "The profile is read from the recorded regime ('unknown' = not vetoed), the rise from the "
                       "scaled_rise raw value (or the 1-day price return where not recorded).",
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, len(d), H):
                if i + H >= len(d):
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({
                    "coin": coin, "window": str(w),
                    "day": ts.iloc[i].floor("D").strftime("%Y-%m-%d"),
                    "ts": ts.iloc[i].value,
                    "fc": fc[i], "fwd": c1 / c0 - 1.0,
                })
    g = pd.DataFrame(rows)
    if len(g) == 0:
        cases = g
    else:
        coin_mean = g.groupby("coin")["fwd"].mean()
        g["excess"] = g["fwd"] - g["coin"].map(coin_mean)
        cases = g[np.isfinite(g["fc"]) & (g["fc"] > 0) & np.isfinite(g["excess"])].copy()

    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n > 0 else 0
    counts = {"grid cases with a positive forecast": n, "days": n_days}
    reading = ("Profile from the recorded regime ('unknown' = not vetoed); coin mean = mean of its non-overlapping "
               "5-bar grid returns over all windows; t is the OLS slope over a day-clustered (CR1, G/(G-1)) standard "
               "error; halves are the lower and upper n//2 cases sorted by forecast (middle case dropped if n is odd); "
               "the plan's 'fewer than 100 cases' minimum is reported as not observable.")

    if n < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 100 grid cases with a positive forecast (the plan's minimum count).",
            "reading": reading,
        }

    x = cases["fc"].values.astype(float)
    y = cases["excess"].values.astype(float)
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    days = cases["day"].values
    meat = np.zeros((2, 2))
    for dday in np.unique(days):
        m = days == dday
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(np.unique(days))
    corr = G / (G - 1) if G > 1 else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t = slope / se if (se is not None and np.isfinite(se) and se > 0) else 0.0

    srt = cases.sort_values(["fc", "coin", "ts"], kind="mergesort")
    half = n // 2
    lower = srt["excess"].values[:half]
    upper = srt["excess"].values[n - half:]
    sup_val = float(np.mean(upper) - np.mean(lower))
    sup_pass = bool(sup_val > 0)

    if slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        dec = "The slope is positive with t >= 2 and the supporting check passes."
    elif slope < 0 and t <= -2:
        status = "rejected"
        dec = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        dec = "The slope is positive with t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        dec = "The slope has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "t of slope, day-clustered", "value": float(t)},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": dec,
        "reading": reading,
    }
