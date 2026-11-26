import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.absorb.last_history_value"
    H = 1

    # ---------- collect per-bar data ----------
    frames = []
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = w
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["date"] = d["ts"].dt.floor("D")
            vol = d["volume"].astype(float)
            prior = vol.shift(1).rolling(20, min_periods=20).mean()
            d["vr_calc"] = vol / prior.replace(0, np.nan)
            rng = (d["high"] - d["low"]).astype(float)
            d["cl_low"] = (d["high"] - d["close"]) / rng.replace(0, np.nan)
            if LHV not in d.columns:
                d[LHV] = np.nan
            d["lhv"] = pd.to_numeric(d[LHV], errors="coerce")
            # next-bar return inside the window only
            d["ret1"] = d["close"].shift(-H) / d["close"] - 1.0
            frames.append(d)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "t of slope of excess next-day return on forecast, heavy-volume days, same-day cases pooled",
                             "value": None, "statistic": None, "threshold": "slope t >= 2 confirms (with top-minus-bottom > 0); slope t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"heavy-volume days": 0, "distinct dates": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)
    allb["forecast"] = pd.to_numeric(allb["forecast"], errors="coerce").fillna(0.0)

    # ---------- situation check ----------
    # heavy: volume >= 1.5 x mean of prior 20 days (recomputed from volume inside the window);
    # where the window has fewer than 20 prior bars, the detector's own decision (regime == trending) stands in.
    heavy = np.where(allb["vr_calc"].notna(), allb["vr_calc"] >= 1.5 - 1e-9,
                     allb["regime"].astype(str) == "trending")
    # close low in range (not at the high): raw component value > 0 where recorded, else from prices
    lowclose = np.where(allb["lhv"].notna(), allb["lhv"] > 0, allb["cl_low"] > 0)
    situation = pd.Series(heavy & lowclose, index=allb.index)
    active = allb["forecast"] != 0
    n_active = int(active.sum())
    if n_active == 0:
        agreement = None
        passed = False
    else:
        ok = situation & (allb["forecast"] > 0)
        agreement = float(ok[active].mean())
        passed = agreement >= 0.9

    main_name = "t of slope of excess next-day return on forecast, heavy-volume days, same-day cases pooled"
    threshold = "slope t >= 2 with top-minus-bottom > 0 confirms; slope t <= -2 rejects; else inconclusive; needs >= 100 heavy-volume days over >= 50 distinct dates"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("The forecast is never active, so it does not act on the plan's situation (heavy-volume day closing below its high, long)."
                           if n_active == 0 else
                           "Fewer than 90% of the bars with a non-zero forecast are long bars on heavy-volume days (volume >= 1.5x prior 20-day mean) closing below their high."),
            "reading": "Heavy volume recomputed from each window's volume (regime used where fewer than 20 prior bars exist); close below the high from the recorded raw component, else from prices.",
        }

    # ---------- criterion ----------
    coin_mean = allb.groupby("coin")["ret1"].mean()
    allb["excess"] = allb["ret1"] - allb["coin"].map(coin_mean)

    cases = allb[(allb["regime"].astype(str) == "trending")].dropna(subset=["excess", "forecast"]).copy()
    n_cases = int(len(cases))
    n_dates = int(cases["date"].nunique()) if n_cases else 0
    counts = {"heavy-volume days": n_cases, "distinct dates": n_dates}

    # slope t, cluster-robust by date (same-day cases across coins pooled as one piece of evidence)
    slope = None
    t_slope = None
    if n_cases >= 3 and cases["forecast"].var() > 0 and n_dates >= 2:
        X = np.column_stack([np.ones(n_cases), cases["forecast"].values.astype(float)])
        y = cases["excess"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        g = cases["date"].values
        meat = np.zeros((2, 2))
        tmp = pd.DataFrame({"g": g, "s0": X[:, 0] * e, "s1": X[:, 1] * e}).groupby("g")[["s0", "s1"]].sum().values
        for row in tmp:
            meat += np.outer(row, row)
        G = tmp.shape[0]
        N, K = n_cases, 2
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1.0)) * ((N - 1.0) / (N - K))
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    # supporting check: top third minus bottom third of forecasts (Welch)
    diff = None
    welch_t = None
    if n_cases >= 3:
        srt = cases.sort_values(["forecast", "ts", "coin"], kind="mergesort")
        k = n_cases // 3
        bottom = srt["excess"].values[:k]
        top = srt["excess"].values[-k:] if k > 0 else np.array([])
        if k >= 1:
            diff = float(np.mean(top) - np.mean(bottom))
            if k >= 2:
                tt = stats.ttest_ind(top, bottom, equal_var=False)
                welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = (diff is not None and diff > 0)

    if n_cases < 100 or n_dates < 50:
        status = "not observable"
        decided = (f"The plan's minimum is not reached: {n_cases} heavy-volume days over {n_dates} distinct dates "
                   "(needs at least 100 over at least 50 dates).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm: the slope t is 2 or more and the top-minus-bottom difference is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject: the slope t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the slope t is 2 or more but the top-minus-bottom difference is 0 or less."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": t_slope,
                         "statistic": ({"name": "slope t (date-clustered OLS)", "value": t_slope} if t_slope is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "top-third minus bottom-third forecast mean excess next-day return (Welch t " +
                                     ("%.3f" % welch_t if welch_t is not None else "n/a") + ")",
                             "value": diff,
                             "passed": sup_passed if diff is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Heavy-volume days are the bars with regime 'trending' and a next-day close in the same window, "
                    "including those with forecast 0; the slope's t pools same-day cases with standard errors clustered by date (CR1); "
                    "thirds are the lowest and highest n//3 cases by forecast with ties ordered by time then coin; "
                    "the coin mean is its mean 1-day return over all its windows."),
    }
