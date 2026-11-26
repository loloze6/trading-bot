import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_shrink.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            in_prof = df["regime"].astype(str) == "unknown"
            ok = active & in_prof & raw.notna() & (raw < 0) & (f < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "slope of excess 5-bar forward return on forecast (in-profile grid bars)"
    thr = "confirm: slope > 0 with day-clustered t >= 2 and check < 0; reject: slope < 0 with t <= -2"
    sup_name = "mean excess 5-bar return, forecast <= -2 minus in-profile forecast == 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("No active bars: the config never takes the plan's short position in a falling market with shrunk volume."
                           if n_active == 0 else
                           f"Only {agreement:.1%} of active bars are short, in the falling profile (regime 'unknown'), with a negative "
                           "volume log ratio, below the 90% required by the plan's situation."),
            "reading": "The falling profile is the recorded regime 'unknown' (the veto sends non-falling bars to 'chop'); shrinkage is a raw log ratio below 0.",
        }

    # ---------- 2. grid samples ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                rows.append({"coin": coin, "r": r, "f": f[i], "inprof": reg[i] == "unknown",
                             "day": ts.iloc[i].strftime("%Y-%m-%d")})
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    d = pd.DataFrame(rows, columns=["coin", "r", "f", "inprof", "day"])
    if len(d):
        d["ex"] = d["r"] - d["coin"].map(coin_rets)
    else:
        d["ex"] = []
    s = d[d["inprof"] & d["f"].notna() & d["ex"].notna()].copy()
    shr = s[s["f"] <= -2]
    grow = s[s["f"] == 0]

    n_grid = int(len(s))
    n_shr = int(len(shr))
    n_days = int(shr["day"].nunique())
    counts = {"in-profile grid bars": n_grid,
              "grid bars with forecast <= -2": n_shr,
              "distinct days of forecast <= -2 cases": n_days,
              "in-profile grid bars with forecast 0": int(len(grow)),
              "distinct days of in-profile grid bars": int(s["day"].nunique())}

    # supporting check
    if n_shr > 0 and len(grow) > 0:
        diff = float(shr["ex"].mean() - grow["ex"].mean())
        sup_pass = bool(diff < 0)
    else:
        diff, sup_pass = None, None

    # slope with day-clustered (CR1) standard error
    slope, tval = None, None
    if n_grid >= 3 and s["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_grid), s["f"].values.astype(float)])
        y = s["ex"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        b = XtX_inv @ X.T @ y
        u = y - X @ b
        meat = np.zeros((2, 2))
        groups = s["day"].values
        for g in np.unique(groups):
            m = groups == g
            sg = X[m].T @ u[m]
            meat += np.outer(sg, sg)
        G = len(np.unique(groups))
        k = 2
        corr = (G / (G - 1)) * ((n_grid - 1) / (n_grid - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(b[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    reading = ("The falling profile is the recorded regime 'unknown'; the grid is positions 0,5,10,... of each window keeping bars with a "
               "5-bar return inside the window; the coin's mean 5-bar return is over all its grid bars in all windows; the slope is OLS "
               "with intercept and a CR1 day-clustered t; the 20-distinct-days minimum is read on the forecast <= -2 cases.")

    base = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "day-clustered t of slope", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }

    if n_grid < 60:
        return {**base, "status": "not observable",
                "decided_by": f"Only {n_grid} in-profile grid bars, below the plan's minimum of 60."}
    if n_shr < 30:
        return {**base, "status": "not observable",
                "decided_by": f"Only {n_shr} grid bars with forecast <= -2, below the plan's minimum of 30."}
    if n_days < 20:
        return {**base, "status": "not observable",
                "decided_by": f"The forecast <= -2 cases fall on only {n_days} distinct days, below the plan's minimum of 20."}
    if slope is None or tval is None:
        return {**base, "status": "inconclusive",
                "decided_by": "The slope or its t could not be computed (no variation in the forecast), so neither rule is met."}

    if slope > 0 and tval >= 2:
        if sup_pass:
            return {**base, "status": "confirmed",
                    "decided_by": "Confirm: the slope is positive with t >= 2 and the supporting difference is below 0."}
        return {**base, "status": "inconclusive",
                "decided_by": "Inconclusive: the slope confirms (positive, t >= 2) but the supporting check is not below 0."}
    if slope < 0 and tval <= -2:
        return {**base, "status": "rejected",
                "decided_by": "Reject: the slope is negative with t <= -2, larger shorts are followed by higher excess returns."}
    return {**base, "status": "inconclusive",
            "decided_by": "Inconclusive: the slope's t is between -2 and 2."}
