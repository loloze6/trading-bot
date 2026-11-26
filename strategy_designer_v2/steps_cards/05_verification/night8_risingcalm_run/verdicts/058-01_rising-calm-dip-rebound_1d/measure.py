import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.pullback.last_history_value"
    IN_PROFILE_REGIME = "unknown"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            close = pd.to_numeric(d["close"], errors="coerce")
            # sign of the 3-day return: from the raw component value (3-day return / 30-day vol);
            # where it is missing, from the prices inside the window
            ret3_price = close / close.shift(3) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                fall = raw.where(raw.notna(), ret3_price) < 0
            else:
                fall = ret3_price < 0
            in_profile = d["regime"].astype(str) == IN_PROFILE_REGIME
            ok = in_profile & fall & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((ok & active).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the slope of 5-bar excess forward return on forecast, grid cells with forecast > 0, same-day cells pooled"
    threshold = "confirm: slope t >= 2 with mean excess > 0; reject: slope t <= -2; otherwise inconclusive; at least 30 grid cases"
    reading = ("The rising calm profile is read from the recorded regime (the bars the vetoes left as 'unknown', since the "
               "detector's components are not recorded and its 365-day lookback cannot be rebuilt inside a window), the fall "
               "from the sign of the raw pullback value; the coin's mean 5-bar return is the mean over all its windows' "
               "non-overlapping grid cells; 'same-day cells pooled' is a day-clustered (CR1) standard error of the OLS slope; "
               "the plan's 30-case minimum not reached is reported as not observable.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases with forecast > 0": None},
            "decided_by": ("Fewer than 90% of active bars are long bars inside the rising calm profile with a negative "
                           "3-day return, so the forecast does not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "fwd": c1 / c0 - 1.0,
                    "fc": fc[i],
                })
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows)
        mu = cdf["fwd"].mean()
        cdf["excess"] = cdf["fwd"] - mu
        rows.append(cdf)

    if rows:
        allc = pd.concat(rows, ignore_index=True)
        sel = allc[allc["fc"].notna() & (allc["fc"] > 0) & allc["excess"].notna()].copy()
    else:
        sel = pd.DataFrame(columns=["coin", "day", "fwd", "fc", "excess"])

    n_cases = int(len(sel))
    n_days = int(sel["day"].nunique()) if n_cases else 0
    counts = {"grid cases with forecast > 0": n_cases, "days": n_days}
    sc = {"agreement": float(agreement) if agreement is not None else None, "passed": bool(passed)}

    mean_ex = float(sel["excess"].mean()) if n_cases else None

    if n_cases < 30:
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess 5-bar return > 0", "value": mean_ex, "passed": None},
            "counts": counts,
            "decided_by": f"The plan needs at least 30 grid cases with forecast > 0; only {n_cases} exist.",
            "reading": reading,
        }

    x = sel["fc"].to_numpy(dtype=float)
    y = sel["excess"].to_numpy(dtype=float)
    X = np.column_stack([np.ones_like(x), x])
    XtX = X.T @ X
    slope = None
    t_slope = None
    try:
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ (X.T @ y)
        resid = y - X @ beta
        slope = float(beta[1])
        meat = np.zeros((2, 2))
        days = sel["day"].to_numpy()
        for dday in np.unique(days):
            m = days == dday
            s = X[m].T @ resid[m]
            meat += np.outer(s, s)
        G = len(np.unique(days))
        N, K = X.shape
        corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if G > 1 and N > K else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None
    except np.linalg.LinAlgError:
        pass

    sup_pass = bool(mean_ex is not None and mean_ex > 0)

    if t_slope is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope's t is 2 or more and the mean excess return is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject: the slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is 2 or more but the mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "day-clustered OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean excess 5-bar return > 0", "value": mean_ex, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
