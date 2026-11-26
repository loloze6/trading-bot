import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    LHV = "debug_info.components.fall_vol.last_history_value"
    PPV = "debug_info.components.fall_vol.post_pipeline_value"
    MIN_DAYS = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            prev = close.shift(1)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw_fall = raw > 0
            price_fall = (close < prev) | prev.isna()
            situation = raw_fall & price_fall
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope t of excess 2-day return on post_pipeline forecast, cases with positive forecast, day-clustered"
    threshold = "t >= 2 confirms (with supporting check); t <= -2 rejects; otherwise inconclusive; fewer than 100 independent case-days not observable"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars after a one-day fall (positive raw fall_vol value and a lower close), so the config does not do what the Fidelity's situation and long side say.",
            "reading": "Situation taken as a positive raw fall_vol value with a close below the previous close (first bar of a window judged on the raw value alone), expected side long.",
        }

    # ---------- 2. cases ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ppv = pd.to_numeric(df[PPV], errors="coerce").values if PPV in df.columns else np.full(len(df), np.nan)
            dret = pd.Series(close).pct_change()
            vol60 = dret.rolling(60, min_periods=60).std().values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append({
                        "coin": coin, "r": r, "x": ppv[i], "vol": vol60[i],
                        "day": ts.iloc[i].floor("D"),
                    })
        if coin_rets:
            m = float(np.mean(coin_rets))
            for c in coin_cases:
                c["ex"] = c["r"] - m
                rows.append(c)

    cases = pd.DataFrame(rows, columns=["coin", "r", "x", "vol", "day", "ex"])
    reg = cases.dropna(subset=["x", "ex"])
    n_cases = int(len(reg))
    n_days = int(reg["day"].nunique()) if n_cases else 0

    # ---------- main measure: OLS slope, SE clustered by day ----------
    slope = None
    t = None
    if n_cases >= 3 and n_days >= 2 and reg["x"].std() > 0:
        X = np.column_stack([np.ones(n_cases), reg["x"].values])
        y = reg["ex"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in reg.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - 2))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(beta[1] / se) if np.isfinite(se) and se > 0 else None

    # ---------- supporting check ----------
    sup = cases.dropna(subset=["vol", "ex"])
    sup_val = None
    sup_pass = None
    if len(sup) >= 2:
        med = sup["vol"].median()
        hi = sup[sup["vol"] > med]["ex"]
        lo = sup[sup["vol"] <= med]["ex"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
    sup_n = int(len(sup))

    # ---------- decision ----------
    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} independent case-days, under the plan's minimum of 100, so the data cannot show the idea whatever the t."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The slope's t is 2 or more and high-volatility falls have a higher mean excess 2-day return than low-volatility falls."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t, standard error clustered by day", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 2-day return, high minus low 60-day volatility (median split)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "independent case-days": n_days,
            "cases": n_cases,
            "cases with 60-day volatility": sup_n,
        },
        "decided_by": decided,
        "reading": "Cases are grid bars (positions 0, 2, 4, ... of each window) with forecast > 0; the coin's mean 2-day return is taken on that same grid over all its windows; 'the cases of one day pooled' is read as a standard error clustered by calendar day (UTC), with independent case-days the number of distinct days; the 60-day volatility is the ddof-1 standard deviation of the last 60 daily close returns inside the window (cases without 60 returns left out of the check), high meaning strictly above the median; the plan's fewer-than-100-case-days minimum is reported as not observable; the situation is a positive raw fall_vol value with a lower close, on the long side.",
    }
