import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc.notna() & (fc != 0)
            # choppy calm profile = regime detector did not veto to "chop" (regime "unknown");
            # the situation = a 5-day fall (raw scaled return < 0); expected side = short
            situ = (regime == "unknown") & raw.notna() & (raw < 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": None},
            "main_measure": {"name": "slope t of next 5-bar excess return on forecast (forecast < 0, 5-bar grid)",
                             "value": None, "statistic": None,
                             "threshold": "confirm if t >= 2 with supporting check; reject if t <= -2"},
            "supporting_check": None,
            "counts": {"grid bars with forecast below 0": 0, "distinct days": 0},
            "decided_by": "No active bar in the record: fewer than 30 grid bars with forecast below 0.",
            "reading": "The choppy calm profile is read from the recorded regime ('unknown' = not vetoed to chop), since the detector's components are not recorded.",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope t of next 5-bar excess return on forecast (forecast < 0, 5-bar grid)",
                             "value": None, "statistic": None,
                             "threshold": "confirm if t >= 2 with supporting check; reject if t <= -2"},
            "supporting_check": None,
            "counts": {},
            "decided_by": "Fewer than 90% of active bars are short bars in the choppy calm profile after a 5-day fall (regime 'unknown' and raw scaled return < 0), as the Fidelity requires.",
            "reading": "The choppy calm profile is read from the recorded regime ('unknown' = not vetoed to chop), since the detector's components are not recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        cand = []
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
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    cand.append((coin, fc[i], r, ts.iloc[i].floor("D")))
        if all_rets:
            coin_means[coin] = float(np.mean(all_rets))
        for c, f, r, day in cand:
            rows.append({"coin": c, "f": f, "r": r, "day": day})

    reading = ("Profile read from the recorded regime ('unknown' = choppy calm); grid = positions 0,5,10,... of each window "
               "with a full 5-bar forward return inside the window; normal drift = coin's mean 5-bar return on that grid over all its windows; "
               "'cases of one day pooled' = OLS slope with standard errors clustered by UTC day (CR1); supporting mean = plain mean over cases; "
               "the plan's minimum counts are applied as 'not observable'.")

    n_cases = len(rows)
    n_days = len(set(r["day"] for r in rows)) if rows else 0
    counts = {"grid bars with forecast below 0": int(n_cases), "distinct days": int(n_days)}
    mm_name = "slope t of next 5-bar excess return on forecast (forecast < 0, 5-bar grid, days pooled)"
    thr = "confirm if t >= 2 and mean short unusual move > 0; reject if t <= -2; minimum 30 cases on 20 distinct days"

    if n_cases < 30 or n_days < 20:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "mean unusual move in the short direction", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Minimum count not reached: fewer than 30 grid bars with forecast below 0 or fewer than 20 distinct days.",
            "reading": reading,
        }

    dfc = pd.DataFrame(rows)
    dfc["ex"] = dfc["r"] - dfc["coin"].map(coin_means)
    x = dfc["f"].values.astype(float)
    y = dfc["ex"].values.astype(float)
    N = len(x)
    X = np.column_stack([np.ones(N), x])
    slope = None
    t = None
    try:
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        days = dfc["day"].values
        meat = np.zeros((2, 2))
        G = 0
        for dday in pd.unique(days):
            m = days == dday
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
            G += 1
        K = 2
        adj = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if G > 1 and N > K else 1.0
        V = adj * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None
    except np.linalg.LinAlgError:
        pass

    short_unusual = -dfc["ex"].values
    sup_val = float(np.mean(short_unusual))
    sup_pass = bool(sup_val > 0)

    if t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean unusual move in the short direction is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger scaled falls are followed by larger rebounds."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean unusual move in the short direction is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": slope,
                         "statistic": ({"name": "OLS slope t, day-clustered", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move in the short direction", "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
