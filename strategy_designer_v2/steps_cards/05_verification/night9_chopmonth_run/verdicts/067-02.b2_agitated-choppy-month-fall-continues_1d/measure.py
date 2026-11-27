import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.fall30.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: inside the choppy agitated profile (regime "unknown", the only regime with a strategy)
    # and close below its close 30 days earlier (raw 30-day return < 0); expected side: short.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Where the component is not recorded, recompute it from the prices inside the window.
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            in_profile = d["regime"].astype(str) == "unknown"
            active = fc.notna() & (fc != 0)
            situation = in_profile & (raw < 0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on the short side": int(n_agree)},
            "decided_by": (f"only {agreement:.1%} of active bars are short bars inside the choppy agitated profile "
                           "with the close under its close 30 days earlier, below the 90% required"),
            "reading": "the profile is read as regime 'unknown' (no veto fired), the fall as the raw 30-day return below 0",
        }

    # ---------- 2. Criterion ----------
    # Grid returns per coin (for drift) and cases.
    rows = []
    drift_parts = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0:
                    rows.append((coin, f, r, ts.iloc[i].normalize()))
        drift_parts[coin] = float(np.mean(allr)) if len(allr) > 0 else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "f", "r", "day"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift_parts)
        cases = cases.dropna(subset=["f", "r", "drift"])
        cases["ex"] = cases["r"] - cases["drift"]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    counts = {"grid cases with a forecast below 0": n_cases, "distinct days": n_days}
    reading = ("the drift is each coin's mean 7-bar return on the non-overlapping grid of all its windows, the slope "
               "is in 7-bar excess return (fraction) per forecast point with CR1 day-clustered errors, and the plan's "
               "minimum counts lead to 'not observable' as the workflow requires")
    mm_name = "OLS slope of 7-bar excess return on the forecast (forecast < 0 grid bars)"
    mm_thr = "confirm: slope > 0 with t >= 2 (and mean unusual short move > 0); reject: slope < 0 with t <= -2"
    sit = {"agreement": None if agreement is None else float(agreement), "passed": True}

    if n_cases < 30 or n_days < 20:
        slope = None
        tval = None
        mean_short = float((-cases["ex"]).mean()) if n_cases else None
    else:
        x = cases["f"].values.astype(float)
        y = cases["ex"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX = X.T @ X
        try:
            bread = np.linalg.inv(XtX)
        except np.linalg.LinAlgError:
            bread = None
        if bread is None:
            slope, tval = None, None
        else:
            beta = bread @ X.T @ y
            u = y - X @ beta
            meat = np.zeros((2, 2))
            groups = cases["day"].values
            for g in pd.unique(groups):
                m = groups == g
                s = X[m].T @ u[m]
                meat += np.outer(s, s)
            G = len(pd.unique(groups))
            N, K = X.shape
            c = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 and N > K else np.nan
            V = c * bread @ meat @ bread
            se = np.sqrt(V[1, 1]) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None
        mean_short = float((-cases["ex"]).mean())

    support_passed = None if mean_short is None else bool(mean_short > 0)
    supporting = {"name": "mean unusual move in the short direction (minus excess return)",
                  "value": mean_short, "passed": support_passed}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"minimum counts not reached: {n_cases} grid cases with a forecast below 0 (need 30) "
                   f"on {n_days} distinct days (need 20)")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "the slope's clustered t could not be computed, so neither the confirm nor the reject rule is met"
    elif slope > 0 and tval >= 2 and support_passed:
        status = "confirmed"
        decided = "the slope is positive with t >= 2 and the mean unusual move in the short direction is above 0"
    elif tval >= 2:
        status = "inconclusive"
        decided = "the slope t is >= 2 but the mean unusual move in the short direction is at or below 0"
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "the slope is negative with t <= -2"
    else:
        status = "inconclusive"
        decided = "the slope t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {
            "name": mm_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "t, errors clustered by day", "value": tval},
            "threshold": mm_thr,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
